import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self):
        self.required_columns = ['product_name', 'price', 'date']
        self.optional_columns = ['category', 'quantity', 'supplier', 'region']
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate pricing data"""
        try:
            logger.info(f"Starting data cleaning for {len(df)} records")
            
            # Make a copy to avoid modifying original
            cleaned_df = df.copy()
            
            # Standardize column names
            cleaned_df = self._standardize_columns(cleaned_df)
            
            # Validate required columns exist
            self._validate_columns(cleaned_df)
            
            # Clean price column
            cleaned_df = self._clean_price_column(cleaned_df)
            
            # Clean date column
            cleaned_df = self._clean_date_column(cleaned_df)
            
            # Clean text columns
            cleaned_df = self._clean_text_columns(cleaned_df)
            
            # Handle missing values
            cleaned_df = self._handle_missing_values(cleaned_df)
            
            # Remove duplicates
            cleaned_df = self._remove_duplicates(cleaned_df)
            
            # Validate data types
            cleaned_df = self._validate_data_types(cleaned_df)
            
            logger.info(f"Data cleaning completed. {len(cleaned_df)} records remaining")
            return cleaned_df
            
        except Exception as e:
            logger.error(f"Error in data cleaning: {str(e)}")
            raise
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names to lowercase with underscores"""
        column_mapping = {
            'Product Name': 'product_name',
            'ProductName': 'product_name',
            'product': 'product_name',
            'Price': 'price',
            'Unit Price': 'price',
            'UnitPrice': 'price',
            'Date': 'date',
            'Transaction Date': 'date',
            'TransactionDate': 'date',
            'Category': 'category',
            'Quantity': 'quantity',
            'Qty': 'quantity',
            'Supplier': 'supplier',
            'Region': 'region',
            'Location': 'region'
        }
        
        df = df.rename(columns=column_mapping)
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        return df
    
    def _validate_columns(self, df: pd.DataFrame):
        """Validate that required columns are present"""
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    def _clean_price_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate price column"""
        # Remove currency symbols and convert to float
        df['price'] = df['price'].astype(str).str.replace('$', '').str.replace(',', '')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Remove rows with invalid prices
        invalid_prices = df['price'].isna() | (df['price'] <= 0)
        if invalid_prices.any():
            logger.warning(f"Removing {invalid_prices.sum()} rows with invalid prices")
            df = df[~invalid_prices]
        
        return df
    
    def _clean_date_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize date column"""
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Remove rows with invalid dates
        invalid_dates = df['date'].isna()
        if invalid_dates.any():
            logger.warning(f"Removing {invalid_dates.sum()} rows with invalid dates")
            df = df[~invalid_dates]
        
        return df
    
    def _clean_text_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean text columns"""
        text_columns = ['product_name', 'category', 'supplier', 'region']
        
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace('nan', np.nan)
        
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in optional columns"""
        # For optional columns, fill missing values with appropriate defaults
        if 'category' in df.columns:
            df['category'] = df['category'].fillna('Unknown')
        
        if 'quantity' in df.columns:
            df['quantity'] = df['quantity'].fillna(1)
        
        if 'supplier' in df.columns:
            df['supplier'] = df['supplier'].fillna('Unknown')
        
        if 'region' in df.columns:
            df['region'] = df['region'].fillna('Unknown')
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        initial_count = len(df)
        df = df.drop_duplicates()
        duplicates_removed = initial_count - len(df)
        
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate rows")
        
        return df
    
    def _validate_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and correct data types"""
        if 'quantity' in df.columns:
            df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1).astype(int)
        
        return df
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics of the cleaned data"""
        summary = {
            'total_records': len(df),
            'columns': list(df.columns),
            'date_range': {
                'start': df['date'].min().isoformat() if 'date' in df.columns else None,
                'end': df['date'].max().isoformat() if 'date' in df.columns else None
            },
            'price_stats': {
                'mean': float(df['price'].mean()) if 'price' in df.columns else None,
                'min': float(df['price'].min()) if 'price' in df.columns else None,
                'max': float(df['price'].max()) if 'price' in df.columns else None,
                'std': float(df['price'].std()) if 'price' in df.columns else None
            },
            'unique_products': df['product_name'].nunique() if 'product_name' in df.columns else 0,
            'unique_categories': df['category'].nunique() if 'category' in df.columns else 0,
            'unique_suppliers': df['supplier'].nunique() if 'supplier' in df.columns else 0
        }
        
        return summary
