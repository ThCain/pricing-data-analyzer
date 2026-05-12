import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
import logging
from scipy import stats

logger = logging.getLogger(__name__)

class PricingAnalyzer:
    def __init__(self):
        self.outlier_methods = ['iqr', 'zscore', 'isolation_forest']
    
    def analyze_pricing_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform comprehensive analysis on pricing data"""
        try:
            logger.info(f"Starting analysis on {len(df)} records")
            
            analysis_result = {
                'basic_stats': self._calculate_basic_statistics(df),
                'outlier_analysis': self._detect_outliers(df),
                'trend_analysis': self._analyze_trends(df),
                'category_analysis': self._analyze_by_category(df),
                'supplier_analysis': self._analyze_by_supplier(df),
                'regional_analysis': self._analyze_by_region(df),
                'price_distribution': self._analyze_price_distribution(df),
                'correlation_analysis': self._analyze_correlations(df)
            }
            
            logger.info("Analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in analysis: {str(e)}")
            raise
    
    def _calculate_basic_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate basic statistical measures"""
        price_stats = df['price'].describe()
        
        stats_dict = {
            'total_records': len(df),
            'total_products': df['product_name'].nunique(),
            'total_categories': df['category'].nunique() if 'category' in df.columns else 0,
            'total_suppliers': df['supplier'].nunique() if 'supplier' in df.columns else 0,
            'total_regions': df['region'].nunique() if 'region' in df.columns else 0,
            'price_statistics': {
                'mean': float(price_stats['mean']),
                'median': float(price_stats['50%']),
                'min': float(price_stats['min']),
                'max': float(price_stats['max']),
                'std': float(price_stats['std']),
                'variance': float(price_stats['std'] ** 2),
                'q1': float(price_stats['25%']),
                'q3': float(price_stats['75%']),
                'iqr': float(price_stats['75%'] - price_stats['25%'])
            },
            'date_range': {
                'start': df['date'].min().isoformat(),
                'end': df['date'].max().isoformat(),
                'days_spanned': (df['date'].max() - df['date'].min()).days
            }
        }
        
        return stats_dict
    
    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect outliers using multiple methods"""
        prices = df['price']
        
        outliers = {}
        
        # IQR Method
        q1, q3 = prices.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        iqr_outliers = (prices < lower_bound) | (prices > upper_bound)
        
        outliers['iqr'] = {
            'count': int(iqr_outliers.sum()),
            'percentage': float(iqr_outliers.sum() / len(prices) * 100),
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound),
            'outlier_values': prices[iqr_outliers].tolist()[:20]  # Limit to first 20
        }
        
        # Z-Score Method
        z_scores = np.abs(stats.zscore(prices))
        zscore_outliers = z_scores > 3
        
        outliers['zscore'] = {
            'count': int(zscore_outliers.sum()),
            'percentage': float(zscore_outliers.sum() / len(prices) * 100),
            'threshold': 3,
            'outlier_values': prices[zscore_outliers].tolist()[:20]
        }
        
        return outliers
    
    def _analyze_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze pricing trends over time"""
        df_sorted = df.sort_values('date')
        monthly_trends = df_sorted.groupby(df_sorted['date'].dt.to_period('M')).agg({
            'price': ['mean', 'min', 'max', 'count']
        }).round(2)
        
        # Calculate month-over-month changes
        monthly_avg = monthly_trends[('price', 'mean')]
        mom_changes = monthly_avg.pct_change().fillna(0) * 100
        
        trend_analysis = {
            'monthly_averages': {str(k): float(v) for k, v in monthly_avg.to_dict().items()},
            'month_over_month_changes': {str(k): float(v) for k, v in mom_changes.to_dict().items()},
            'overall_trend': self._determine_trend_direction(monthly_avg),
            'volatility': float(monthly_avg.std() / monthly_avg.mean() * 100) if monthly_avg.mean() > 0 else 0
        }
        
        return trend_analysis
    
    def _determine_trend_direction(self, series: pd.Series) -> str:
        """Determine if trend is increasing, decreasing, or stable"""
        if len(series) < 2:
            return "insufficient_data"
        
        # Simple linear regression to determine trend
        x = np.arange(len(series))
        slope, _, _, p_value, _ = stats.linregress(x, series)
        
        if p_value < 0.05:  # Statistically significant
            if slope > 0:
                return "increasing"
            elif slope < 0:
                return "decreasing"
        
        return "stable"
    
    def _analyze_by_category(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze pricing by category"""
        if 'category' not in df.columns:
            return {'message': 'Category column not found'}
        
        category_stats = df.groupby('category')['price'].agg([
            'count', 'mean', 'median', 'min', 'max', 'std'
        ]).round(2)
        
        category_analysis = {
            'category_count': len(category_stats),
            'top_categories': category_stats.nlargest(10, 'count').to_dict(),
            'price_by_category': category_stats.to_dict(),
            'price_range_by_category': {
                cat: {
                    'min': float(group['price'].min()),
                    'max': float(group['price'].max()),
                    'range': float(group['price'].max() - group['price'].min())
                }
                for cat, group in df.groupby('category')
            }
        }
        
        return category_analysis
    
    def _analyze_by_supplier(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze pricing by supplier"""
        if 'supplier' not in df.columns:
            return {'message': 'Supplier column not found'}
        
        supplier_stats = df.groupby('supplier')['price'].agg([
            'count', 'mean', 'median', 'min', 'max', 'std'
        ]).round(2)
        
        supplier_analysis = {
            'supplier_count': len(supplier_stats),
            'top_suppliers': supplier_stats.nlargest(10, 'count').to_dict(),
            'price_by_supplier': supplier_stats.to_dict(),
            'supplier_price_comparison': {
                'lowest_avg_price': {
                    'supplier': supplier_stats['mean'].idxmin(),
                    'price': float(supplier_stats['mean'].min())
                },
                'highest_avg_price': {
                    'supplier': supplier_stats['mean'].idxmax(),
                    'price': float(supplier_stats['mean'].max())
                }
            }
        }
        
        return supplier_analysis
    
    def _analyze_by_region(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze pricing by region"""
        if 'region' not in df.columns:
            return {'message': 'Region column not found'}
        
        region_stats = df.groupby('region')['price'].agg([
            'count', 'mean', 'median', 'min', 'max', 'std'
        ]).round(2)
        
        region_analysis = {
            'region_count': len(region_stats),
            'top_regions': region_stats.nlargest(10, 'count').to_dict(),
            'price_by_region': region_stats.to_dict(),
            'regional_price_variance': float(region_stats['mean'].var())
        }
        
        return region_analysis
    
    def _analyze_price_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze the distribution of prices"""
        prices = df['price']
        
        distribution_analysis = {
            'histogram_bins': {
                'bins': 20,
                'counts': np.histogram(prices, bins=20)[0].tolist(),
                'bin_edges': np.histogram(prices, bins=20)[1].tolist()
            },
            'skewness': float(stats.skew(prices)),
            'kurtosis': float(stats.kurtosis(prices)),
            'price_ranges': {
                'under_50': (prices < 50).sum(),
                '50_to_100': ((prices >= 50) & (prices < 100)).sum(),
                '100_to_500': ((prices >= 100) & (prices < 500)).sum(),
                '500_to_1000': ((prices >= 500) & (prices < 1000)).sum(),
                'over_1000': (prices >= 1000).sum()
            }
        }
        
        return distribution_analysis
    
    def _analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations between numerical variables"""
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) < 2:
            return {'message': 'Insufficient numeric columns for correlation analysis'}
        
        correlation_matrix = df[numeric_columns].corr()
        
        correlation_analysis = {
            'correlation_matrix': {str(k): {str(k2): float(v2) for k2, v2 in v.items()} for k, v in correlation_matrix.to_dict().items()},
            'strong_correlations': self._find_strong_correlations(correlation_matrix)
        }
        
        return correlation_analysis
    
    def _find_strong_correlations(self, corr_matrix: pd.DataFrame, threshold: float = 0.7) -> List[Dict]:
        """Find pairs of variables with strong correlations"""
        strong_corrs = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    strong_corrs.append({
                        'variable1': corr_matrix.columns[i],
                        'variable2': corr_matrix.columns[j],
                        'correlation': float(corr_value),
                        'strength': 'strong positive' if corr_value > 0 else 'strong negative'
                    })
        
        return strong_corrs
