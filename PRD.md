# Product Requirements Document (PRD)
## Animal Rescue Day Trading Application v1.0

### Executive Summary
A tkinter-based desktop application that uses AI-powered chart analysis to identify optimal day trading opportunities on BITX, generating consistent small profits to fund animal rescue operations.

---

## Core Requirements

### 1. Application Architecture
- **Framework**: Python Tkinter desktop application
- **Primary Symbol**: BITX (1-minute candlestick charts)
- **Chart Generation**: Auto-generate using existing `make_chart.py`
- **AI Analysis**: Integrate existing `ai_analyzer.py` with OpenAI
- **Data Persistence**: `history.json` for all AI responses and analysis

### 2. User Interface Layout

#### Main Trading Tab
- **Chart Display**: BITX 1-minute candlestick with EMA5/SMA8 overlays
- **Trading Signal**: Large, prominent "BUY" or "WAIT" recommendation
- **Risk Level**: Display LOW/MEDIUM/HIGH risk assessment
- **Key Prices**: Support/Resistance levels, Stop Loss, Take Profit targets
- **Auto-Refresh Controls**: 
  - Checkbox to enable/disable auto-refresh
  - Start/Stop button for manual control
  - Countdown timer showing next update (60-second cycle)
- **Audio Alert**: Text-to-speech "Trade Opportunity" when BUY signal triggered

#### System Prompt Tab
- **Professional Trader Prompt**: Pre-configured system prompt structured for professional day trading analysis
- **Editable Text Area**: Full system prompt customization capability
- **Focus Areas**: EMA/SMA crossovers, daily pivot points, risk assessment

#### User Prompt Tab
- **Analysis Instructions**: Customizable user prompt for AI analysis requests
- **Technical Indicators**: Focus on 5 EMA, 8 SMA crossovers, pivot points
- **Editable Text Area**: Full user prompt customization capability

#### Debug Tab
- **Function Outputs**: Display outputs from all major functions
- **Error Logging**: Show API errors, connectivity issues
- **Data Inspection**: View raw chart data, AI responses
- **Troubleshooting**: Help identify issues during trading sessions

### 3. Core Functionality

#### Chart Generation & Analysis Workflow
1. **Auto-generate BITX chart** using `make_chart.py` (1-minute, 2-day data)
2. **Save chart** to `data/` folder as PNG
3. **AI Analysis** via `ai_analyzer.py` with trading-focused prompts
4. **Parse AI Response** for:
   - BUY/WAIT recommendation
   - Risk level (LOW/MEDIUM/HIGH) 
   - Entry price target
   - Stop loss price
   - Take profit price
   - Confidence level
5. **Update UI** with recommendations and key prices
6. **Log to History** - save all data to `history.json`
7. **Audio Alert** if BUY signal detected

#### Auto-Refresh System
- **1-minute cycle** when auto-refresh enabled
- **Countdown timer** showing seconds until next update
- **Manual override** with Start/Stop button
- **Error handling** - continue cycle even if single analysis fails

### 4. AI Prompt Structure

#### System Prompt Template
```
You are a professional day trader with 20+ years of experience specializing in quick scalping trades. 

Your expertise includes:
- Identifying optimal entry/exit points for 0.10-0.50 cent moves
- EMA/SMA crossover strategies (5 EMA, 8 SMA)
- Daily pivot point analysis
- Risk assessment for short-term trades
- Stop loss and take profit targeting

Analyze the provided 1-minute BITX candlestick chart and provide:
1. RECOMMENDATION: "BUY" or "WAIT" 
2. RISK_LEVEL: "LOW", "MEDIUM", or "HIGH"
3. ENTRY_PRICE: Optimal entry point
4. STOP_LOSS: Maximum acceptable loss price
5. TAKE_PROFIT: Target profit-taking price
6. CONFIDENCE: Your confidence level (1-10)
7. REASONING: Brief explanation of your analysis

Focus on EMA5/SMA8 crossovers and daily pivot levels for scalping opportunities.
```

#### User Prompt Template
```
Analyze this BITX 1-minute chart for day trading opportunities.

Current market conditions:
- Look for EMA5/SMA8 crossover signals
- Identify daily pivot point levels
- Assess volume and momentum
- Consider risk/reward ratio for quick scalp trades

Provide clear BUY or WAIT recommendation with specific entry, stop loss, and take profit prices.
Target profit: $0.10-$0.50 per share moves.
```

### 5. Data Management

#### History Logging (`history.json`)
```json
{
  "sessions": [
    {
      "timestamp": "2025-08-06T14:30:00Z",
      "chart_path": "data/BITX_candlestick_20250806_143000.png",
      "ai_response": "...",
      "recommendation": "BUY",
      "risk_level": "LOW", 
      "entry_price": 24.52,
      "stop_loss": 24.42,
      "take_profit": 24.65,
      "confidence": 8
    }
  ]
}
```

### 6. Technical Specifications

#### Dependencies
- Python 3.8+
- tkinter (built-in)
- Existing modules: `make_chart.py`, `ai_analyzer.py`
- Additional: `pyttsx3` for text-to-speech
- JSON for data persistence

#### Performance Requirements
- Chart generation: < 30 seconds
- AI analysis: < 45 seconds  
- UI updates: < 5 seconds
- Total cycle time: < 90 seconds

#### Error Handling
- API failures: Display error, continue cycle
- Chart generation issues: Log error, retry once
- Invalid AI responses: Use fallback parsing
- Network connectivity: Show connection status

### 7. Success Criteria

#### Primary Goals
- ✅ Generate actionable BUY/WAIT signals every minute
- ✅ Provide clear entry/exit prices for scalping trades
- ✅ Maintain reliable auto-refresh cycle during market hours
- ✅ Log all analysis for performance tracking

#### User Experience Goals  
- ✅ Single-click start/stop operation
- ✅ Clear visual indicators for trading signals
- ✅ Audio alerts for immediate attention
- ✅ Professional trading interface design

---

## Development Phases

### Phase 1: Core Framework (Week 1)
- Build tkinter tabbed interface
- Implement basic chart display
- Create prompt editing tabs
- Add debug output tab

### Phase 2: AI Integration (Week 1-2)  
- Integrate existing chart generation
- Connect AI analysis pipeline
- Implement response parsing
- Add history logging

### Phase 3: Auto-Refresh & Alerts (Week 2)
- Build 1-minute auto-refresh system
- Add countdown timer
- Implement text-to-speech alerts
- Add start/stop controls

### Phase 4: Testing & Refinement (Week 2-3)
- Test with live BITX data
- Refine AI prompts for accuracy
- Optimize performance
- Add error handling

---

## Mission Impact
**Every successful trade recommendation helps save more animals in need.**

Target: Generate consistent $50-200 daily profits through precise scalping trades to fund:
- Emergency veterinary care
- Medical supplies and equipment  
- Daily care and feeding costs
- Facility improvements

---

*"Precision trading for animal rescue - every cent counts, every life matters."* 🐾📈
