# Animal Rescue Day Trading Application

## Mission Statement
This application is designed to support an animal rescue operation by providing AI-powered day trading assistance. The goal is to generate consistent small profits (targeting $0.10-$0.50 moves) through quick in-and-out trades to fund veterinary bills, equipment, and rescue operations.

## Core Purpose
- **Primary Goal**: Generate trading profits to fund animal rescue operations
- **Trading Strategy**: Short-term day trades with quick entry/exit points
- **Target Profits**: Small but consistent gains ($0.10-$0.50 per share on larger positions)
- **Risk Management**: Only risk small portions of working capital to protect core rescue funding

## Application Features

### Main Interface (Tkinter Desktop App)
- **Chart Display**: Visual representation of trading instruments (starting with BITX)
- **AI Analysis**: OpenAI-powered chart analysis for trading decisions
- **Key Price Labels**: Display of critical support/resistance levels, entry/exit points
- **Trading Recommendation**: Clear "BUY" or "WAIT" suggestions
- **Auto-Refresh**: Controllable automatic analysis updates (only runs when checked)

### Tabbed Interface
1. **Main Trading Tab**: Chart + analysis + recommendations
2. **System Prompt Tab**: Editable AI system instructions
3. **User Prompt Tab**: Editable AI analysis queries

### Technical Integration
- Uses existing `make_chart.py` for BITX candlestick charts
- Integrates `ai_analyzer.py` for image analysis
- Robust error handling to prevent trading mishaps
- Data export capabilities for trade tracking

## Current Rescue Context
- Recently rescued injured puppy with broken legs
- Operating on limited funds
- Considering llama rescue (pending space/cost evaluation)
- Need for consistent income stream to expand rescue operations

---

## Questions for Development

### Technical Questions
1. **Chart Integration**: Should we auto-generate charts from `make_chart.py` or allow manual image loading (or both)?
    whatever is optimal.


2. **Refresh Timing**: How often should auto-refresh update? (every 1 minute, 5 minutes, or user-configurable?)

every 1 min show countdown timer for next update


3. **Trading Symbols**: Starting with BITX - do you want ability to switch between multiple symbols in the app?
no we only need to focus on 1 symbol and wait for optimal signal. 


4. **Data Persistence**: Should we save AI analysis history and trading recommendations for later review?
yes we need to make a history.json file with previous responses


5. **Alert System**: Would you like popup/sound alerts when AI suggests a "BUY" opportunity?
i want to just have a lable in the main view of tkinter
play a sound or use talk to speach to say trade opprotunity

### AI Analysis Questions
6. **Prompt Customization**: Do you have specific technical indicators you want the AI to focus on? (RSI, MACD, volume, etc.)
i think we should focus on ema, sma cross  5ema, 8 sma, and daily pivot points.


7. **Risk Assessment**: Should the AI also provide risk level ratings (low/medium/high) for each recommendation?
yes, the best you can do.


8. **Position Sizing**: Do you want the AI to suggest position sizes based on your available capital?

no

9. **Stop Loss/Take Profit**: Should the app suggest specific exit prices for both profit-taking and loss prevention?
yes 


### User Experience Questions
10. **Chart Timeframes**: Besides 1-minute data, do you want options for 5-minute or 15-minute charts for different perspectives?

lets focus on only 1 min chart for now


11. **Key Price Display**: How do you prefer key prices displayed? (overlay on chart, separate panel, both?)

12. **Trading Journal**: Would you like built-in trade logging to track your actual results vs. AI recommendations?
no KISS method. 
we can expand later


### Operational Questions
13. **Market Hours**: Should the app only operate during market hours or also analyze pre/post-market movements?

there should be a start button and auto refresh check box

14. **Internet Connectivity**: How should the app handle connectivity issues during critical trading moments?

dont worry about it, 

15. **Backup Plans**: If OpenAI API is down, should there be a fallback analysis method?

show error
there should be a tab with all the outputs for each function for debugging. 

### Rescue Integration Questions
16. **Profit Tracking**: Would you like a "rescue fund tracker" showing how much trading profits have contributed to animal care?
not at this time. starting simple 

17. **Goal Setting**: Should the app include targets like "Need $500 for puppy surgery" to motivate trading decisions?
not at this time. we will later versions. KISS
---

THE SYSTEM PROMPT SHOULD BE STRUCTURED AS A PROFESSIONAL STOCK DAY TRADER INFO..




## Next Steps
1. Build basic tkinter framework with tabbed interface
2. Integrate existing chart generation and AI analysis
3. Implement auto-refresh and error handling
4. Add trading recommendation display system
5. Test with BITX data and refine AI prompts

## Success Metrics
- Consistent small profits to fund rescue operations
- Quick decision-making for day trading opportunities  
- Reduced emotional trading through AI-assisted analysis
- More animals rescued and properly cared for

---

*"Every successful trade means another animal we can save."* 🐾
