import os
import logging
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from stock_analyzer import StockAnalyzer
import io
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize stock analyzer
stock_analyzer = StockAnalyzer()

@app.route('/')
def index():
    """Main page for stock analysis"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    """Analyze stock and return data for charts and tables"""
    try:
        symbol = request.form.get('symbol', '').strip().upper()
        period = request.form.get('period', '1y')
        
        if not symbol:
            flash('Please enter a valid stock symbol.', 'error')
            return redirect(url_for('index'))
        
        # Get stock data
        stock_data = stock_analyzer.get_stock_data(symbol, period)
        
        if stock_data is None:
            flash(f'Could not fetch data for symbol: {symbol}. Please check if the symbol is correct.', 'error')
            return redirect(url_for('index'))
        
        # Get financial metrics
        financial_metrics = stock_analyzer.get_financial_metrics(symbol)
        
        # Prepare chart data
        chart_data = stock_analyzer.prepare_chart_data(stock_data)
        
        # Prepare table data
        table_data = stock_analyzer.prepare_table_data(stock_data)
        
        return render_template('index.html', 
                             symbol=symbol,
                             period=period,
                             financial_metrics=financial_metrics,
                             chart_data=chart_data,
                             table_data=table_data,
                             show_results=True)
    
    except Exception as e:
        symbol_for_error = request.form.get('symbol', 'unknown').strip().upper()
        logging.error(f"Error analyzing stock {symbol_for_error}: {str(e)}")
        flash(f'An error occurred while analyzing {symbol_for_error}: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download_csv')
def download_csv():
    """Download stock data as CSV"""
    try:
        symbol = request.args.get('symbol', '').strip().upper()
        period = request.args.get('period', '1y')
        
        if not symbol:
            flash('No stock symbol provided for download.', 'error')
            return redirect(url_for('index'))
        
        # Get stock data
        stock_data = stock_analyzer.get_stock_data(symbol, period)
        
        if stock_data is None:
            flash(f'Could not fetch data for symbol: {symbol}', 'error')
            return redirect(url_for('index'))
        
        # Prepare CSV data
        csv_data = stock_analyzer.prepare_csv_data(stock_data)
        
        # Create CSV file in memory
        output = io.StringIO()
        csv_data.to_csv(output, index=True)
        output.seek(0)
        
        # Convert to bytes
        csv_bytes = io.BytesIO()
        csv_bytes.write(output.getvalue().encode('utf-8'))
        csv_bytes.seek(0)
        
        filename = f"{symbol}_{period}_stock_data.csv"
        
        return send_file(
            csv_bytes,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        symbol_for_error = request.args.get('symbol', 'unknown').strip().upper()
        logging.error(f"Error downloading CSV for {symbol_for_error}: {str(e)}")
        flash(f'An error occurred while downloading CSV: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    flash('An internal server error occurred. Please try again.', 'error')
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
