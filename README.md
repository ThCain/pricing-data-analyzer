# 📊 Pricing Data Analyzer

A data processing and analysis tool that automates pricing calculations and generates reports from raw logistics data using **Python**, **Pandas**, and **FastAPI**.

## 🛠 Tech Stack

- **Python 3.11**
- **FastAPI** – REST API layer
- **Pandas** – Data processing & analysis
- **NumPy** – Numerical computations
- **SQLite** – Local data storage
- **OpenPyXL** – Excel report generation
- **Matplotlib** – Data visualization

## 📦 Features

- Upload raw pricing data via CSV or Excel file
- Automated data cleaning and transformation pipeline
- Calculate pricing statistics: min, max, average, variance
- Detect anomalies and outliers in pricing datasets
- Generate formatted Excel reports with summary tables
- Visualize pricing trends over time as charts
- REST API endpoints for integration with other services

## 📁 Project Structure

```
pricing-data-analyzer/
├── app/
│   ├── main.py
│   ├── routers/
│   │   ├── upload.py
│   │   └── reports.py
│   ├── services/
│   │   ├── analyzer.py
│   │   └── report_generator.py
│   ├── utils/
│   │   └── data_cleaner.py
│   └── database.py
├── sample_data/
│   └── sample_pricing.csv
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Installation

```bash
git clone https://github.com/ThCain/pricing-data-analyzer.git
cd pricing-data-analyzer
pip install -r requirements.txt
```

### Run the App

```bash
uvicorn app.main:app --reload
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload CSV/Excel pricing data |
| GET | `/analyze/{file_id}` | Run analysis on uploaded data |
| GET | `/reports/{file_id}` | Download Excel summary report |
| GET | `/stats/{file_id}` | Get statistical summary as JSON |

## 📈 Sample Output

```json
{
  "total_records": 1540,
  "average_price": 284.75,
  "min_price": 102.00,
  "max_price": 980.50,
  "outliers_detected": 12,
  "date_range": "2024-01-01 to 2024-12-31"
}
```

## 💡 Use Case

Originally designed to automate manual Excel-based pricing workflows in logistics environments, reducing analysis time significantly.

## 📄 License

MIT License

Copyright (c) 2025 Ahmet Taha Günüç

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
