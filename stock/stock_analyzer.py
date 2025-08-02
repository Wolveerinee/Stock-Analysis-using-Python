import yfinance as yf
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

class StockAnalyzer:
    """Class to handle stock data analysis and processing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_stock_data(self, symbol, period='1y'):
        """
        Fetch stock data from Yahoo Finance
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL')
            period (str): Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        
        Returns:
            pandas.DataFrame: Stock data or None if error
        """
        try:
            stock = yf.Ticker(symbol)
            
            # Download historical data
            hist_data = stock.history(period=period)
            
            if hist_data.empty:
                self.logger.warning(f"No data found for symbol: {symbol}")
                return None
            
            return hist_data
        
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_financial_metrics(self, symbol):
        """
        Get financial metrics for a stock
        
        Args:
            symbol (str): Stock symbol
        
        Returns:
            dict: Financial metrics
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Get current price from recent data
            recent_data = stock.history(period='1d')
            current_price = recent_data['Close'].iloc[-1] if not recent_data.empty else info.get('currentPrice', 'N/A')
            
            metrics = {
                'symbol': symbol,
                'company_name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'current_price': self._format_currency(current_price),
                'market_cap': self._format_large_number(info.get('marketCap', 'N/A')),
                'pe_ratio': self._format_ratio(info.get('trailingPE', 'N/A')),
                'eps': self._format_currency(info.get('trailingEps', 'N/A')),
                'dividend_yield': self._format_percentage(info.get('dividendYield', 'N/A')),
                'beta': self._format_ratio(info.get('beta', 'N/A')),
                '52_week_high': self._format_currency(info.get('fiftyTwoWeekHigh', 'N/A')),
                '52_week_low': self._format_currency(info.get('fiftyTwoWeekLow', 'N/A')),
                'volume': self._format_large_number(info.get('volume', 'N/A')),
                'avg_volume': self._format_large_number(info.get('averageVolume', 'N/A'))
            }
            
            return metrics
        
        except Exception as e:
            self.logger.error(f"Error getting financial metrics for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'company_name': 'N/A',
                'sector': 'N/A',
                'industry': 'N/A',
                'current_price': 'N/A',
                'market_cap': 'N/A',
                'pe_ratio': 'N/A',
                'eps': 'N/A',
                'dividend_yield': 'N/A',
                'beta': 'N/A',
                '52_week_high': 'N/A',
                '52_week_low': 'N/A',
                'volume': 'N/A',
                'avg_volume': 'N/A'
            }
    
    def prepare_chart_data(self, stock_data):
        """
        Prepare data for Chart.js
        
        Args:
            stock_data (pandas.DataFrame): Stock data
        
        Returns:
            dict: Chart data
        """
        try:
            # Convert dates to strings for JSON serialization
            dates = [date.strftime('%Y-%m-%d') for date in stock_data.index]
            
            chart_data = {
                'labels': dates,
                'prices': stock_data['Close'].round(2).tolist(),
                'volumes': stock_data['Volume'].tolist(),
                'highs': stock_data['High'].round(2).tolist(),
                'lows': stock_data['Low'].round(2).tolist(),
                'opens': stock_data['Open'].round(2).tolist()
            }
            
            return chart_data
        
        except Exception as e:
            self.logger.error(f"Error preparing chart data: {str(e)}")
            return {'labels': [], 'prices': [], 'volumes': [], 'highs': [], 'lows': [], 'opens': []}
    
    def prepare_table_data(self, stock_data):
        """
        Prepare data for the table display
        
        Args:
            stock_data (pandas.DataFrame): Stock data
        
        Returns:
            list: Table data
        """
        try:
            # Get last 30 days of data for table
            recent_data = stock_data.tail(30).copy()
            
            # Calculate daily change
            recent_data['Change'] = recent_data['Close'] - recent_data['Open']
            recent_data['Change %'] = ((recent_data['Close'] - recent_data['Open']) / recent_data['Open'] * 100).round(2)
            
            table_data = []
            for date, row in recent_data.iterrows():
                table_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(row['Open'], 2),
                    'high': round(row['High'], 2),
                    'low': round(row['Low'], 2),
                    'close': round(row['Close'], 2),
                    'volume': f"{row['Volume']:,}",
                    'change': round(row['Change'], 2),
                    'change_percent': f"{row['Change %']:.2f}%"
                })
            
            # Reverse to show most recent first
            return list(reversed(table_data))
        
        except Exception as e:
            self.logger.error(f"Error preparing table data: {str(e)}")
            return []
    
    def prepare_csv_data(self, stock_data):
        """
        Prepare data for CSV export
        
        Args:
            stock_data (pandas.DataFrame): Stock data
        
        Returns:
            pandas.DataFrame: CSV data
        """
        try:
            csv_data = stock_data.copy()
            
            # Calculate additional metrics
            csv_data['Change'] = csv_data['Close'] - csv_data['Open']
            csv_data['Change %'] = ((csv_data['Close'] - csv_data['Open']) / csv_data['Open'] * 100).round(2)
            
            # Round numeric columns
            numeric_columns = ['Open', 'High', 'Low', 'Close', 'Change']
            for col in numeric_columns:
                if col in csv_data.columns:
                    csv_data[col] = csv_data[col].round(2)
            
            return csv_data
        
        except Exception as e:
            self.logger.error(f"Error preparing CSV data: {str(e)}")
            return pd.DataFrame()
    
    def _format_currency(self, value):
        """Format currency values"""
        if value == 'N/A' or value is None or (isinstance(value, float) and np.isnan(value)):
            return 'N/A'
        try:
            return f"${float(value):,.2f}"
        except (ValueError, TypeError):
            return 'N/A'
    
    def _format_large_number(self, value):
        """Format large numbers (market cap, volume)"""
        if value == 'N/A' or value is None or (isinstance(value, float) and np.isnan(value)):
            return 'N/A'
        try:
            num = float(value)
            if num >= 1e12:
                return f"${num/1e12:.2f}T"
            elif num >= 1e9:
                return f"${num/1e9:.2f}B"
            elif num >= 1e6:
                return f"${num/1e6:.2f}M"
            elif num >= 1e3:
                return f"${num/1e3:.2f}K"
            else:
                return f"${num:,.0f}"
        except (ValueError, TypeError):
            return 'N/A'
    
    def _format_percentage(self, value):
        """Format percentage values"""
        if value == 'N/A' or value is None or (isinstance(value, float) and np.isnan(value)):
            return 'N/A'
        try:
            return f"{float(value)*100:.2f}%"
        except (ValueError, TypeError):
            return 'N/A'
    
    def _format_ratio(self, value):
        """Format ratio values (P/E, Beta)"""
        if value == 'N/A' or value is None or (isinstance(value, float) and np.isnan(value)):
            return 'N/A'
        try:
            return f"{float(value):.2f}"
        except (ValueError, TypeError):
            return 'N/A'
