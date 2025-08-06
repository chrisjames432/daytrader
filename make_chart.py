#!/usr/bin/env python3
"""
BITX Candlestick Chart Generator
===============================
Creates 1-minute candlestick chart for BITX over 2 days.
Includes after-market data.
"""

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import os
import json
from matplotlib.patches import Rectangle

def fetch_bitx_data(symbol="BITX", days=2):
    """
    Fetch 1-minute BITX data for given days including after-market.
    
    Args:
        symbol (str): Stock symbol to fetch
        days (int): Number of days of data to fetch
        
    Returns:
        pandas.DataFrame: 1-minute stock data with OHLCV and indicators
    """
    print(f"📊 Fetching {days}-day 1-minute data for {symbol} (including after-market)...")
    
    ticker = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    stock_data = ticker.history(
        start=start_date.strftime('%Y-%m-%d'),
        end=end_date.strftime('%Y-%m-%d'),
        interval='5m',
        prepost=True  # Include after-market data
    )
    
    if stock_data.empty:
        raise ValueError(f"No data available for {symbol}")
    
    # Add technical indicators
    stock_data['EMA5'] = stock_data['Close'].ewm(span=5).mean()
    stock_data['SMA8'] = stock_data['Close'].rolling(window=8).mean()
    
    # Add date column for daily calculations
    stock_data = stock_data.reset_index()
    stock_data['Date'] = stock_data['Datetime'].dt.date
    stock_data = stock_data.set_index('Datetime')
    
    print(f"✅ Retrieved {len(stock_data)} 1-minute candles with indicators")
    return stock_data

def get_daily_stats(stock_data):
    """
    Calculate daily high/low statistics.
    
    Args:
        stock_data (DataFrame): Stock data with Date column
        
    Returns:
        dict: Daily statistics
    """
    daily_stats = {}
    
    for date in stock_data['Date'].unique():
        day_data = stock_data[stock_data['Date'] == date]
        daily_stats[str(date)] = {
            'high': float(day_data['High'].max()),
            'low': float(day_data['Low'].min()),
            'open': float(day_data['Open'].iloc[0]),
            'close': float(day_data['Close'].iloc[-1]),
            'volume': int(day_data['Volume'].sum()),
            'candles': len(day_data)
        }
    
    return daily_stats

def draw_daily_boxes(ax, stock_data, sampled_data):
    """
    Draw boxes around daily high/low ranges.
    
    Args:
        ax: Matplotlib axis
        stock_data: Full stock data
        sampled_data: Sampled data for x-axis alignment
    """
    # Get daily ranges
    for date in stock_data['Date'].unique():
        day_data = stock_data[stock_data['Date'] == date]
        day_high = day_data['High'].max()
        day_low = day_data['Low'].min()
        
        # Find corresponding x positions in sampled data
        day_sampled = sampled_data[sampled_data['Date'] == date]
        if len(day_sampled) > 0:
            x_start = day_sampled.index[0]
            x_end = day_sampled.index[-1]
            x_start_pos = list(sampled_data.index).index(x_start)
            x_end_pos = list(sampled_data.index).index(x_end)
            
            # Draw box
            width = x_end_pos - x_start_pos + 1
            height = day_high - day_low
            
            rect = Rectangle((x_start_pos - 0.5, day_low), width, height,
                           facecolor='none', edgecolor='blue', linewidth=2, alpha=0.7)
            ax.add_patch(rect)
            
            # Add daily labels
            ax.text(x_start_pos, day_high + (day_high - day_low) * 0.05, 
                   f'{date}\nH: ${day_high:.2f}\nL: ${day_low:.2f}',
                   fontsize=8, ha='left', va='bottom',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor="lightblue", alpha=0.8))

def draw_candlestick(ax, x, open_price, high_price, low_price, close_price, width=0.8):
    """
    Draw a single candlestick.
    
    Args:
        ax: Matplotlib axis
        x: X position
        open_price: Opening price
        high_price: High price
        low_price: Low price
        close_price: Closing price
        width: Candlestick width
    """
    # Determine color
    color = 'green' if close_price >= open_price else 'red'
    
    # Draw high-low line
    ax.plot([x, x], [low_price, high_price], color='black', linewidth=1)
    
    # Draw body
    body_height = abs(close_price - open_price)
    body_bottom = min(open_price, close_price)
    
    rect = Rectangle((x - width/2, body_bottom), width, body_height, 
                    facecolor=color, edgecolor='black', linewidth=0.5, alpha=0.8)
    ax.add_patch(rect)
    """
    Draw a single candlestick.
    
    Args:
        ax: Matplotlib axis
        x: X position
        open_price: Opening price
        high_price: High price
        low_price: Low price
        close_price: Closing price
        width: Candlestick width
    """
    # Determine color
    color = 'green' if close_price >= open_price else 'red'
    
    # Draw high-low line
    ax.plot([x, x], [low_price, high_price], color='black', linewidth=1)
    
    # Draw body
    body_height = abs(close_price - open_price)
    body_bottom = min(open_price, close_price)
    
    rect = Rectangle((x - width/2, body_bottom), width, body_height, 
                    facecolor=color, edgecolor='black', linewidth=0.5, alpha=0.8)
    ax.add_patch(rect)

def create_candlestick_chart(stock_data, symbol="BITX", output_dir="data"):
    """
    Create candlestick chart for BITX with indicators and daily boxes.
    
    Args:
        stock_data (DataFrame): 1-minute stock data
        symbol (str): Stock symbol for labeling
        output_dir (str): Directory to save chart
        
    Returns:
        dict: Chart metadata including path and prices
    """
    print(f"📈 Creating candlestick chart for {symbol}...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Setup plot
    fig, ax = plt.subplots(figsize=(20, 12))
    
    # Sample data to avoid too many candles (every 5 minutes)
    sampled_data = stock_data.iloc[::5].copy()  # Every 5th candle
    
    # Draw candlesticks
    for i, (idx, row) in enumerate(sampled_data.iterrows()):
        draw_candlestick(ax, i, row['Open'], row['High'], row['Low'], row['Close'])
    
    # Plot moving averages
    ax.plot(range(len(sampled_data)), sampled_data['EMA5'], 
           color='red', linewidth=2, label='EMA5', alpha=0.8)
    ax.plot(range(len(sampled_data)), sampled_data['SMA8'], 
           color='black', linewidth=2, label='SMA8', alpha=0.8)
    
    # Draw daily high/low boxes
    draw_daily_boxes(ax, stock_data, sampled_data)
    
    # Format x-axis with time labels
    time_labels = [idx.strftime('%m/%d %H:%M') for idx in sampled_data.index[::60]]  # Every hour
    x_positions = list(range(0, len(sampled_data), 60))
    
    ax.set_xticks(x_positions)
    ax.set_xticklabels(time_labels, rotation=45, ha='right')
    
    # Styling
    current_price = stock_data['Close'].iloc[-1]
    current_ema5 = stock_data['EMA5'].iloc[-1]
    current_sma8 = stock_data['SMA8'].iloc[-1]
    
    ax.set_title(f"{symbol} - 2 Day Candlestick (1-min, EMA5, SMA8, Daily Boxes)", 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Price ($)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('white')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    # Add current price and indicators annotation
    info_text = f'Price: ${current_price:.2f}\nEMA5: ${current_ema5:.2f}\nSMA8: ${current_sma8:.2f}'
    ax.text(1.02, 0.98, info_text, 
           transform=ax.transAxes, fontsize=12, fontweight='bold',
           bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8),
           verticalalignment='top')
    
    # Save chart
    chart_path = f"{output_dir}/chart.png"
    plt.tight_layout()
    plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    print(f"✅ Chart saved: {chart_path}")
    
    # Prepare data for JSON export
    daily_stats = get_daily_stats(stock_data)
    
    # Convert stock data to JSON-serializable format
    export_data = []
    for idx, row in stock_data.iterrows():
        export_data.append({
            'datetime': idx.isoformat(),
            'open': float(row['Open']),
            'high': float(row['High']),
            'low': float(row['Low']),
            'close': float(row['Close']),
            'volume': int(row['Volume']),
            'ema5': float(row['EMA5']) if pd.notna(row['EMA5']) else None,
            'sma8': float(row['SMA8']) if pd.notna(row['SMA8']) else None,
            'date': str(row['Date'])
        })
    
    # Save data to JSON
    data_json_path = f"{output_dir}/data.json"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_data = {
        'symbol': symbol,
        'timestamp': timestamp,
        'current_price': float(current_price),
        'current_ema5': float(current_ema5),
        'current_sma8': float(current_sma8),
        'high_2day': float(stock_data['High'].max()),
        'low_2day': float(stock_data['Low'].min()),
        'daily_stats': daily_stats,
        'candles_total': len(stock_data),
        'candles_displayed': len(sampled_data),
        'data': export_data
    }
    
    with open(data_json_path, 'w') as f:
        json.dump(json_data, f, indent=2)
    
    print(f"✅ Data saved: {data_json_path}")
    
    # Return metadata
    return {
        'symbol': symbol,
        'chart_path': chart_path,
        'data_path': data_json_path,
        'current_price': float(current_price),
        'current_ema5': float(current_ema5),
        'current_sma8': float(current_sma8),
        'high_2day': float(stock_data['High'].max()),
        'low_2day': float(stock_data['Low'].min()),
        'daily_stats': daily_stats,
        'candles_analyzed': len(stock_data),
        'candles_displayed': len(sampled_data)
    }

def generate_bitx_chart(symbol="BITX"):
    """
    Main function to generate BITX candlestick chart.
    
    Args:
        symbol (str): Stock symbol to analyze
        
    Returns:
        dict: Complete chart metadata
    """
    stock_data = fetch_bitx_data(symbol)
    chart_info = create_candlestick_chart(stock_data, symbol)
    return chart_info

if __name__ == "__main__":
    # Generate BITX chart
    result = generate_bitx_chart("BITX")
    print(f"📊 BITX chart complete: {result}")
