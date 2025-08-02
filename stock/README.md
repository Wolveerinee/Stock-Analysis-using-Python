# Stock Analyzer

A Flask web application for stock market analysis with real-time data from Yahoo Finance, interactive charts, and CSV export functionality.

## Features

- Real-time stock data from Yahoo Finance
- Interactive dark-themed UI with Bootstrap 5
- Chart.js integration for price and volume visualization
- Financial metrics display (P/E ratio, market cap, dividend yield, etc.)
- Historical data table showing last 30 days
- CSV export functionality for stock data
- Responsive design for mobile and desktop

## Requirements

- Python 3.11+
- pip (Python package manager)

## Installation

1. Extract the project files to your desired directory
2. Navigate to the project directory in your terminal
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask development server:

```bash
python app.py
```

2. Open your web browser and navigate to:

```
http://localhost:5000
```

## Usage

1. Enter a stock symbol (e.g., AAPL, GOOGL, TSLA) in the search field
2. Select a time period (1 month to 5 years)
3. Click "Analyze" to fetch and display the stock data
4. Use the Price/Volume toggle to switch between chart views
5. Download historical data as CSV using the "Download CSV" button

## Project Structure

```
stock_analyzer/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── stock_analyzer.py     # Stock data processing logic
├── requirements.txt      # Python dependencies
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   └── index.html       # Main page template
└── static/             # Static assets
    ├── css/
    │   └── style.css   # Custom styles
    └── js/
        └── charts.js   # Chart functionality
```

## Dependencies

- Flask: Web framework
- yfinance: Yahoo Finance API wrapper
- pandas: Data manipulation and analysis
- numpy: Numerical computing
- gunicorn: WSGI HTTP server

## Development

The application uses:
- Flask for the web framework
- Yahoo Finance API for stock data
- Bootstrap 5 for responsive UI
- Chart.js for interactive charts
- Dark theme for better user experience

## Notes

- Stock data is provided by Yahoo Finance for informational purposes only
- The application fetches real-time data and may be subject to API limitations
- For production deployment, configure appropriate environment variables and use a production WSGI server