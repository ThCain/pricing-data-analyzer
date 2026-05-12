from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UploadedFile, PricingData
from app.utils.data_cleaner import DataCleaner
from app.services.analyzer import PricingAnalyzer
import pandas as pd
import uuid
import os
import aiofiles
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Upload and process a pricing data file"""
    
    # Validate file type
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(
            status_code=400, 
            detail="Only CSV and Excel files are supported"
        )
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Save file record to database
        db_file = UploadedFile(
            file_id=file_id,
            original_filename=file.filename,
            file_path=file_path,
            file_size=len(content),
            content_type=file.content_type
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        # Process the file
        df = await _read_file(file_path, file.filename)
        
        # Clean data
        cleaner = DataCleaner()
        cleaned_df = cleaner.clean_data(df)
        
        # Save cleaned data to database
        await _save_pricing_data(db, file_id, cleaned_df)
        
        # Mark file as processed
        db_file.processed = True
        db.commit()
        
        # Get data summary
        summary = cleaner.get_data_summary(cleaned_df)
        
        logger.info(f"Successfully processed file {file.filename} with {len(cleaned_df)} records")
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "status": "processed",
            "summary": summary
        }
        
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        
        # Clean up file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Remove database record
        db.rollback()
        
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/files")
async def list_uploaded_files(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """List all uploaded files"""
    files = db.query(UploadedFile).all()
    
    return {
        "files": [
            {
                "file_id": f.file_id,
                "filename": f.original_filename,
                "file_size": f.file_size,
                "content_type": f.content_type,
                "processed": f.processed,
                "uploaded_at": f.created_at.isoformat()
            }
            for f in files
        ]
    }

@router.get("/files/{file_id}")
async def get_file_info(file_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get information about a specific uploaded file"""
    file_record = db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get pricing data count
    data_count = db.query(PricingData).filter(PricingData.file_id == file_id).count()
    
    return {
        "file_id": file_record.file_id,
        "filename": file_record.original_filename,
        "file_size": file_record.file_size,
        "content_type": file_record.content_type,
        "processed": file_record.processed,
        "data_records": data_count,
        "uploaded_at": file_record.created_at.isoformat()
    }

@router.delete("/files/{file_id}")
async def delete_file(file_id: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Delete an uploaded file and its associated data"""
    file_record = db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Delete associated pricing data
        db.query(PricingData).filter(PricingData.file_id == file_id).delete()
        
        # Delete file record
        db.delete(file_record)
        db.commit()
        
        # Delete physical file
        if os.path.exists(file_record.file_path):
            os.remove(file_record.file_path)
        
        logger.info(f"Successfully deleted file {file_id}")
        
        return {"message": "File deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting file {file_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

async def _read_file(file_path: str, filename: str) -> pd.DataFrame:
    """Read uploaded file into pandas DataFrame"""
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")
        
        return df
        
    except Exception as e:
        logger.error(f"Error reading file {filename}: {str(e)}")
        raise

async def _save_pricing_data(db: Session, file_id: str, df: pd.DataFrame):
    """Save cleaned pricing data to database"""
    try:
        # Convert DataFrame to list of dictionaries
        records = df.to_dict('records')
        
        # Add file_id to each record
        for record in records:
            record['file_id'] = file_id
        
        # Bulk insert
        db.bulk_insert_mappings(PricingData, records)
        db.commit()
        
        logger.info(f"Saved {len(records)} pricing records for file {file_id}")
        
    except Exception as e:
        logger.error(f"Error saving pricing data: {str(e)}")
        db.rollback()
        raise
