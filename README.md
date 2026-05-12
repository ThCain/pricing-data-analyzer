# 📊 Pricing Data Analyzer

A comprehensive full-stack data processing and analysis tool that automates pricing calculations, generates detailed reports, and provides data visualizations from raw pricing data using **Python**, **FastAPI**, and **Pandas**.

## 🛠 Tech Stack

- **Python 3.13** – Core programming language
- **FastAPI** – High-performance REST API framework
- **Pandas** – Data processing & analysis
- **NumPy** – Numerical computations
- **SQLAlchemy** – Database ORM
- **SQLite** – Local data storage
- **OpenPyXL** – Excel report generation
- **Matplotlib & Seaborn** – Data visualization
- **SciPy** – Statistical analysis
- **Uvicorn** – ASGI server

## 📦 Features

### 🔄 Data Processing
- **File Upload**: Support for CSV and Excel files
- **Automated Data Cleaning**: Standardization, validation, and transformation
- **Missing Value Handling**: Intelligent imputation strategies
- **Duplicate Detection**: Automatic removal of duplicate records
- **Data Type Validation**: Ensure data integrity

### 📈 Statistical Analysis
- **Descriptive Statistics**: Mean, median, mode, variance, standard deviation
- **Outlier Detection**: Multiple methods (IQR, Z-score)
- **Trend Analysis**: Monthly price trends and patterns
- **Correlation Analysis**: Relationships between variables
- **Distribution Analysis**: Price distribution and skewness

### 📊 Reporting & Visualization
- **Excel Reports**: Multi-sheet comprehensive reports
- **Data Visualizations**: Price distribution, trends, category analysis
- **Interactive Charts**: Monthly averages, regional comparisons
- **Summary Statistics**: Quick insights and key metrics

### 🌐 API Features
- **RESTful API**: Complete CRUD operations
- **File Management**: Upload, list, delete files
- **Analysis Endpoints**: Real-time data analysis
- **Report Generation**: On-demand report creation
- **Health Monitoring**: System health checks

## 📁 Project Structure

```
pricing-data-analyzer/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── routers/
│   │   ├── upload.py           # File upload endpoints
│   │   └── reports.py          # Analysis and report endpoints
│   ├── services/
│   │   ├── analyzer.py         # Data analysis engine
│   │   └── report_generator.py # Report and visualization generation
│   └── utils/
│       └── data_cleaner.py     # Data cleaning utilities
├── sample_data/
│   └── sample_pricing.csv      # Sample dataset for testing
├── uploads/                    # Uploaded file storage
├── reports/                    # Generated Excel reports
├── visualizations/             # Generated charts and graphs
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ThCain/pricing-data-analyzer.git
cd pricing-data-analyzer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
uvicorn app.main:app --reload --port 8001
```

4. **Access the API:**
- API Base URL: `http://127.0.0.1:8001`
- Interactive Docs: `http://127.0.0.1:8001/docs`
- Health Check: `http://127.0.0.1:8001/health`

## 📡 API Endpoints

### 📤 File Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload CSV/Excel pricing data |
| `GET` | `/api/files` | List all uploaded files |
| `GET` | `/api/files/{file_id}` | Get file information |
| `DELETE` | `/api/files/{file_id}` | Delete uploaded file |

### 📊 Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/analyze/{file_id}` | Run comprehensive analysis |
| `GET` | `/api/stats/{file_id}` | Get statistical summary |
| `DELETE` | `/api/analysis/{file_id}` | Delete analysis results |

### 📈 Reports & Visualizations
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/reports/{file_id}/download` | Generate Excel report |
| `GET` | `/api/reports/{file_id}/download-file` | Download Excel file |
| `GET` | `/api/reports/{file_id}/visualizations` | Generate data visualizations |

### 🏠 System
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | System health check |

## 📊 Data Format

### Expected CSV/Excel Columns
- `product_name` (required): Product identifier
- `price` (required): Numeric price value
- `date` (required): Transaction date
- `category` (optional): Product category
- `quantity` (optional): Order quantity
- `supplier` (optional): Supplier name
- `region` (optional): Geographic region

### Sample Data Row
```csv
product_name,category,price,quantity,date,supplier,region
Laptop Pro,Electronics,1299.99,5,2024-01-15,TechSupplier,North
```

## 📈 Sample Output

### Analysis Response
```json
{
  "file_id": "uuid-string",
  "analysis_id": 123,
  "summary": {
    "total_records": 76,
    "average_price": 404.42,
    "min_price": 17.99,
    "max_price": 2999.99,
    "variance": 273014.25,
    "outliers_detected": 3,
    "date_range": "2024-01-15 to 2024-03-30",
    "unique_products": 38,
    "unique_categories": 2,
    "unique_suppliers": 2,
    "unique_regions": 4
  },
  "detailed_analysis": {
    "basic_stats": {...},
    "outlier_analysis": {...},
    "trend_analysis": {...},
    "category_analysis": {...},
    "supplier_analysis": {...},
    "regional_analysis": {...}
  }
}
```

### Generated Reports
- **Excel Report**: Multi-sheet workbook with Summary, Data, Statistics, Outliers, and Trends
- **Visualizations**: PNG charts for price distribution, trends, category analysis, and monthly averages

## 🧪 Testing

### Using Sample Data
```bash
# Upload sample data
curl -X POST -F "file=@sample_data/sample_pricing.csv" http://127.0.0.1:8001/api/upload

# Analyze uploaded data (replace {file_id} with actual ID from upload response)
curl http://127.0.0.1:8001/api/analyze/{file_id}

# Generate report
curl http://127.0.0.1:8001/api/reports/{file_id}/download
```

### Python Test Script
```python
import requests

# Upload file
files = {'file': open('sample_data/sample_pricing.csv', 'rb')}
response = requests.post('http://127.0.0.1:8001/api/upload', files=files)
file_id = response.json()['file_id']

# Run analysis
analysis = requests.get(f'http://127.0.0.1:8001/api/analyze/{file_id}')
print(analysis.json())

# Generate report
report = requests.get(f'http://127.0.0.1:8001/api/reports/{file_id}/download')
print(report.json())
```

## 💡 Use Cases

### 🏢 Business Applications
- **Pricing Strategy**: Analyze historical pricing patterns
- **Supplier Analysis**: Compare pricing across different suppliers
- **Regional Analysis**: Understand price variations by region
- **Category Management**: Optimize product category pricing
- **Anomaly Detection**: Identify pricing errors or opportunities

### 📊 Data Analysis
- **Trend Monitoring**: Track price changes over time
- **Market Research**: Analyze competitive pricing
- **Budget Planning**: Forecast pricing trends
- **Quality Control**: Detect data quality issues
- **Reporting**: Generate executive summaries

## 🔧 Configuration

### Environment Variables
```bash
# Database configuration
SQLALCHEMY_DATABASE_URL=sqlite:///./pricing_data.db

# Server configuration
HOST=0.0.0.0
PORT=8001
DEBUG=true
```

### Customization
- Modify `app/utils/data_cleaner.py` for custom data cleaning rules
- Update `app/services/analyzer.py` for custom analysis methods
- Extend `app/services/report_generator.py` for custom report formats

## 🐛 Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Issues**
   ```bash
   # Delete database file to reset
   rm pricing_data.db
   ```

3. **Port Conflicts**
   ```bash
   # Use different port
   uvicorn app.main:app --reload --port 8002
   ```

4. **File Upload Errors**
   - Ensure CSV/Excel files have required columns
   - Check file size limits
   - Verify file format compatibility

### Logging
Check server logs for detailed error information:
```bash
uvicorn app.main:app --reload --log-level debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
