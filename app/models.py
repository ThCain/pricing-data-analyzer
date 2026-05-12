from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.database import Base

class PricingData(Base):
    __tablename__ = "pricing_data"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, index=True)
    product_name = Column(String)
    category = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    date = Column(DateTime)
    supplier = Column(String)
    region = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, index=True)
    total_records = Column(Integer)
    average_price = Column(Float)
    min_price = Column(Float)
    max_price = Column(Float)
    variance = Column(Float)
    outliers_detected = Column(Integer)
    date_range_start = Column(DateTime)
    date_range_end = Column(DateTime)
    analysis_summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, unique=True, index=True)
    original_filename = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)
    content_type = Column(String)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
