from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import PricingData, AnalysisResult, UploadedFile
from app.services.analyzer import PricingAnalyzer
from app.services.report_generator import ReportGenerator
import pandas as pd
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/analyze/{file_id}")
async def analyze_data(file_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Run comprehensive analysis on uploaded pricing data"""
    
    # Check if file exists and is processed
    file_record = db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    if not file_record.processed:
        raise HTTPException(status_code=400, detail="File has not been processed yet")
    
    # Check if analysis already exists
    existing_analysis = db.query(AnalysisResult).filter(AnalysisResult.file_id == file_id).first()
    if existing_analysis:
        logger.info(f"Returning existing analysis for file {file_id}")
        return {
            "file_id": file_id,
            "analysis_id": existing_analysis.id,
            "analysis_date": existing_analysis.created_at.isoformat(),
            "summary": {
                "total_records": existing_analysis.total_records,
                "average_price": existing_analysis.average_price,
                "min_price": existing_analysis.min_price,
                "max_price": existing_analysis.max_price,
                "variance": existing_analysis.variance,
                "outliers_detected": existing_analysis.outliers_detected,
                "date_range": f"{existing_analysis.date_range_start.date()} to {existing_analysis.date_range_end.date()}",
                "analysis_summary": existing_analysis.analysis_summary
            }
        }
    
    try:
        # Get pricing data from database
        pricing_records = db.query(PricingData).filter(PricingData.file_id == file_id).all()
        
        if not pricing_records:
            raise HTTPException(status_code=404, detail="No pricing data found for this file")
        
        # Convert to DataFrame
        df = pd.DataFrame([{
            'product_name': record.product_name,
            'category': record.category,
            'price': record.price,
            'quantity': record.quantity,
            'date': record.date,
            'supplier': record.supplier,
            'region': record.region
        } for record in pricing_records])
        
        # Run analysis
        analyzer = PricingAnalyzer()
        analysis_result = analyzer.analyze_pricing_data(df)
        
        # Save analysis results to database
        basic_stats = analysis_result['basic_stats']
        analysis_record = AnalysisResult(
            file_id=file_id,
            total_records=basic_stats['total_records'],
            average_price=basic_stats['price_statistics']['mean'],
            min_price=basic_stats['price_statistics']['min'],
            max_price=basic_stats['price_statistics']['max'],
            variance=basic_stats['price_statistics']['variance'],
            outliers_detected=analysis_result['outlier_analysis']['iqr']['count'],
            date_range_start=pd.to_datetime(basic_stats['date_range']['start']),
            date_range_end=pd.to_datetime(basic_stats['date_range']['end']),
            analysis_summary=str(analysis_result)
        )
        
        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)
        
        logger.info(f"Analysis completed for file {file_id}")
        
        return {
            "file_id": file_id,
            "analysis_id": analysis_record.id,
            "analysis_date": analysis_record.created_at.isoformat(),
            "detailed_analysis": analysis_result,
            "summary": {
                "total_records": analysis_record.total_records,
                "average_price": analysis_record.average_price,
                "min_price": analysis_record.min_price,
                "max_price": analysis_record.max_price,
                "variance": analysis_record.variance,
                "outliers_detected": analysis_record.outliers_detected,
                "date_range": f"{analysis_record.date_range_start.date()} to {analysis_record.date_range_end.date()}",
                "analysis_summary": analysis_record.analysis_summary
            }
        }
        
    except Exception as e:
        logger.error(f"Error analyzing data for file {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing data: {str(e)}")

@router.get("/stats/{file_id}")
async def get_statistics(file_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get statistical summary as JSON"""
    
    # Check if file exists
    file_record = db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get pricing data
    pricing_records = db.query(PricingData).filter(PricingData.file_id == file_id).all()
    
    if not pricing_records:
        raise HTTPException(status_code=404, detail="No pricing data found for this file")
    
    # Calculate statistics
    prices = [record.price for record in pricing_records]
    dates = [record.date for record in pricing_records]
    
    stats = {
        "total_records": len(pricing_records),
        "average_price": sum(prices) / len(prices),
        "min_price": min(prices),
        "max_price": max(prices),
        "price_range": max(prices) - min(prices),
        "date_range": f"{min(dates).date()} to {max(dates).date()}",
        "unique_products": len(set(record.product_name for record in pricing_records)),
        "unique_categories": len(set(record.category for record in pricing_records if record.category)),
        "unique_suppliers": len(set(record.supplier for record in pricing_records if record.supplier)),
        "unique_regions": len(set(record.region for record in pricing_records if record.region))
    }
    
    return stats

@router.get("/reports/{file_id}/download")
async def download_report(file_id: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Generate and download Excel report"""
    
    # Check if file exists
    file_record = db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Get pricing data
        pricing_records = db.query(PricingData).filter(PricingData.file_id == file_id).all()
        
        if not pricing_records:
            raise HTTPException(status_code=404, detail="No pricing data found for this file")
        
        # Convert to DataFrame
        df = pd.DataFrame([{
            'product_name': record.product_name,
            'category': record.category,
            'price': record.price,
            'quantity': record.quantity,
            'date': record.date,
            'supplier': record.supplier,
            'region': record.region
        } for record in pricing_records])
        
        # Generate report
        report_generator = ReportGenerator()
        report_path = report_generator.generate_excel_report(df, file_id, file_record.original_filename)
        
        logger.info(f"Report generated for file {file_id}: {report_path}")
        
        return {
            "message": "Report generated successfully",
            "file_id": file_id,
            "report_path": report_path,
            "download_url": f"/api/reports/{file_id}/download-file"
        }
        
    except Exception as e:
        logger.error(f"Error generating report for file {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@router.get("/reports/{file_id}/download-file")
async def download_report_file(file_id: str, db: Session = Depends(get_db)):
    """Download the generated Excel report file"""
    
    from fastapi.responses import FileResponse
    import os
    
    report_path = f"reports/pricing_report_{file_id}.xlsx"
    
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report file not found")
    
    return FileResponse(
        path=report_path,
        filename=f"pricing_report_{file_id}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.get("/reports/{file_id}/visualizations")
async def get_visualizations(file_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Generate data visualizations"""
    
    # Check if file exists
    file_record = db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Get pricing data
        pricing_records = db.query(PricingData).filter(PricingData.file_id == file_id).all()
        
        if not pricing_records:
            raise HTTPException(status_code=404, detail="No pricing data found for this file")
        
        # Convert to DataFrame
        df = pd.DataFrame([{
            'product_name': record.product_name,
            'category': record.category,
            'price': record.price,
            'quantity': record.quantity,
            'date': record.date,
            'supplier': record.supplier,
            'region': record.region
        } for record in pricing_records])
        
        # Generate visualizations
        report_generator = ReportGenerator()
        visualization_paths = report_generator.generate_visualizations(df, file_id)
        
        return {
            "file_id": file_id,
            "visualizations": visualization_paths
        }
        
    except Exception as e:
        logger.error(f"Error generating visualizations for file {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating visualizations: {str(e)}")

@router.delete("/analysis/{file_id}")
async def delete_analysis(file_id: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Delete analysis results for a file"""
    
    # Check if file exists
    file_record = db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Delete analysis results
        deleted_count = db.query(AnalysisResult).filter(AnalysisResult.file_id == file_id).delete()
        db.commit()
        
        logger.info(f"Deleted {deleted_count} analysis records for file {file_id}")
        
        return {"message": f"Deleted {deleted_count} analysis records"}
        
    except Exception as e:
        logger.error(f"Error deleting analysis for file {file_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting analysis: {str(e)}")
