# MAG7 Multipost Project

This folder contains a comprehensive Twitter thread system for analyzing and posting MAG7 (Magnificent 7) stock analyses as a multi-tweet thread.

## 📁 Files

### Scripts
- **`mag7_multipost.py`** - Main comprehensive script that creates a full Twitter thread
- **`dry_run_preview.py`** - Safe dry-run script that generates HTML preview
- **`mag7.txt`** - List of MAG7 stocks and their symbols

## 🔍 Dry Run Mode

The script now supports **dry-run mode** that creates an HTML preview instead of posting to Twitter:

### HTML Preview Features
- **Twitter-like styling** - Looks like actual Twitter threads
- **Individual tweet divs** - Each post in its own styled container
- **Performance indicators** - Color-coded gains/losses
- **Character counts** - Shows if tweets fit in 280 characters
- **Chart previews** - Embedded images show exactly what will be posted
- **Thread structure** - Main tweet + replies in correct order

### Viewing the Preview
1. Run the dry-run script
2. Open `mag7_post/twitter_thread_preview.html` in VS Code
3. Right-click → "Open with Live Server" or use the VS Code preview extension
4. Review the entire thread before posting

## 🚀 What It Does

This script creates a **complete Twitter thread** with:

1. **🔥 Main summary tweet** - Overview of all MAG7 performance
2. **📊 Individual stock tweets** - One tweet per stock with chart and analysis
3. **🏆 Performance ranking** - Stocks ordered by best to worst performance
4. **📈 Candlestick charts** - 5-day 1-hour charts for each stock
5. **🤖 AI analysis** - Individual analysis for each stock + enhanced analysis with market context

## 📊 Features

### Chart Creation
- **5-day line charts** with 1-hour intervals
- **After-market data** included for complete picture
- **Day separators** with weekday labels
- **Price and % change** prominently displayed
- **High-quality WebP format** optimized for Twitter

### AI Analysis System
- **Individual analysis** for each stock first
- **Market summary** analysis of all 7 stocks combined
- **Enhanced re-analysis** incorporating market context
- **Twitter-optimized** short, punchy content (under 120 chars)

### Twitter Thread Structure
```
🔥 Main Tweet: Market summary + thread announcement
├── 1/7 Best Performer (highest % gain)
├── 2/7 Second best
├── 3/7 Third best
├── 4/7 Middle performer
├── 5/7 Fifth place
├── 6/7 Second worst
└── 7/7 Worst performer (lowest % gain)
```

## 🏃‍♂️ Quick Start

### Prerequisites
```bash
pip install yfinance pandas matplotlib mplfinance numpy tweepy python-dotenv openai pymongo
```

### Environment Setup
Create a `.env` file in the root directory with:
```
# OpenAI
OPENAIKEY=your_openai_api_key

# MongoDB (optional - for company data)
MONGODBURI=your_mongodb_connection_string

# Twitter API
API_KEY=your_twitter_api_key
API_SECRET=your_twitter_api_secret
ACCESS_TOKEN=your_twitter_access_token
ACCESS_SECRET=your_twitter_access_secret
```

### Run Dry-Run Preview (Recommended)
```bash
cd mag7_multipost_project
python dry_run_preview.py
```
This will:
- Generate all charts and analysis
- Create an HTML preview file: `mag7_post/twitter_thread_preview.html`
- **NOT post to Twitter** - safe for testing
- Open the HTML file in VS Code to see what the thread would look like

### Run Live Posting (Posts to Twitter)
```bash
cd mag7_multipost_project
# Edit mag7_multipost.py and change: main(dry_run=False)
python mag7_multipost.py
```

**⚠️ WARNING: This will immediately post to Twitter! Use dry-run first.**

## 📈 Workflow Steps

The script automatically executes these phases:

### Phase 1: Data Collection
- Downloads 5-day 1-hour data for all MAG7 stocks
- Includes pre-market and after-market trading data
- Validates data quality and completeness

### Phase 2: Chart Generation
- Creates candlestick charts for each stock
- Adds day labels, price info, and % changes
- Saves charts as high-quality WebP images

### Phase 3: Individual Analysis
- AI analyzes each stock's chart individually
- Generates short, Twitter-optimized insights
- Focuses on 5-day price action and trends

### Phase 4: Market Summary
- AI creates overall MAG7 market summary
- Identifies top performers and trends
- Synthesizes individual analyses into market view

### Phase 5: Enhanced Analysis
- Re-analyzes each stock with market context
- Incorporates summary insights for richer analysis
- Optimizes for Twitter thread format

### Phase 6: Twitter Posting
- Posts main summary tweet first
- Ranks stocks by performance (best to worst)
- Posts individual stock tweets as replies
- Includes charts, analysis, and key metrics

### Phase 7: Data Storage
- Saves all data to `mag7_post/mag7_analysis_data.json`
- Stores Twitter post IDs for tracking
- Preserves charts in `mag7_post/charts/` folder

## 📁 Output Structure

After running, creates:
```
mag7_post/
├── charts/
│   ├── AAPL_5day.webp
│   ├── MSFT_5day.webp
│   ├── GOOGL_5day.webp
│   ├── AMZN_5day.webp
│   ├── NVDA_5day.webp
│   ├── META_5day.webp
│   └── TSLA_5day.webp
├── data/
└── mag7_analysis_data.json
```

## 🎯 Example Output

### Main Tweet
```
🔥 MAG7 1H LINE CHARTS - 5 DAY ANALYSIS 🧵

NVDA leads at +8.2% while TSLA struggles at -3.1%. 
Tech showing mixed signals with growth stocks outperforming.

Thread below ordered by performance! 👇

#Mag7 #Stocks #Trading
```

### Individual Stock Tweet
```
1/7 $NVDA (+8.2%) 📊

AI chip demand driving strong momentum. 
Breaking resistance with volume support.

Price: $118.45
Range: $108.20-$119.80

#NVDA
```

## ⚙️ Customization

### Chart Settings
- **Time period**: Change `TRADING_DAYS = 5` for different ranges
- **Interval**: Modify interval in `get_stock_data_5day()`
- **Chart style**: Customize colors and appearance in `create_5day_chart()`

### AI Analysis
- **Prompts**: Edit `get_prompts()` for different analysis styles
- **Length**: Adjust `max_tokens` parameters for longer/shorter analysis
- **Temperature**: Modify for more/less creative responses

### Twitter Format
- **Thread structure**: Modify `post_twitter_thread()` for different formats
- **Ranking**: Change sorting logic in stock performance ordering
- **Rate limiting**: Adjust sleep times between posts

### Stock Selection
- **Symbols**: Modify `MAG7_SYMBOLS` list to include/exclude stocks
- **Add new stocks**: Just add symbols to the list

## 🔧 Advanced Features

### MongoDB Integration
- Fetches company descriptions and metadata
- Enhances analysis with fundamental data
- Optional - script works without MongoDB

### Error Handling
- Graceful failure handling for individual stocks
- Partial data saving if workflow fails
- Twitter API rate limiting protection

### Performance Optimization
- Concurrent data downloading (if enabled)
- Image optimization for Twitter
- Efficient data storage and retrieval

## 🚨 Important Notes

1. **Dry Run First**: Always use `dry_run_preview.py` to test before posting
2. **HTML Preview**: Open the generated HTML file in VS Code to review the thread
3. **Rate Limits**: Built-in delays prevent Twitter API limits (live mode only)
4. **Cost**: Uses OpenAI API tokens for analysis
5. **Data Usage**: Downloads substantial market data
6. **Thread Order**: Stocks posted in performance order (best first)
7. **No Live Undo**: Once posted to Twitter, tweets cannot be easily undone

## 🛠️ Troubleshooting

### Common Issues
- **API Keys**: Verify all credentials in `.env` file
- **Data Errors**: Check internet connection and market hours
- **Twitter Limits**: Ensure account has posting permissions
- **Image Upload**: Check file sizes and formats

### Debug Mode
Add debug prints by modifying the script's print statements for more verbose output.

## 📋 Dependencies

- `yfinance` - Stock data
- `pandas` - Data manipulation  
- `matplotlib` - Chart creation
- `mplfinance` - Candlestick charts
- `tweepy` - Twitter API
- `openai` - AI analysis
- `pymongo` - MongoDB (optional)
- `python-dotenv` - Environment variables

---

**Ready to create a comprehensive MAG7 Twitter thread? Just run the script!** 🚀📊
