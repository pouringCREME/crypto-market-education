# Crypto Strategy Research & Education Framework

A **mixed-modality** personal framework for learning cryptocurrency trading, developing and testing strategies safely, and generating research-grade signal insights — with zero live execution risk by default.

> **This is a personal strategy development and education tool, not a trading bot.**
> There is no live order execution engine. Signal generation is for research and manual consideration only.

---

## ⚠️ Important Legal Notice

**Please read [DISCLAIMER.md](DISCLAIMER.md) before proceeding.**

- This software is provided for **personal education and strategy research only**
- **No live trading execution engine is implemented** — signals are for manual review
- Cryptocurrency trading involves **substantial risk of loss**
- Nothing here constitutes financial, investment, or trading advice
- Compliance with local laws and regulations is **your responsibility**
- Past simulated performance does not predict future real-world results
- Consult qualified financial and legal professionals before risking real money

---

## System Modalities

This framework operates in four clearly separated modes. Each has hard boundaries.

### 🎓 Mode 1: LEARN (Educational Simulation)
- **Data**: Fully simulated — no real market data
- **Money**: Virtual only — zero financial risk
- **Execution**: Simulated orders against virtual portfolio
- **Purpose**: Understand trading mechanics, order types, risk concepts
- **Suitable for**: Anyone, any experience level

### 🔬 Mode 2: RESEARCH (Strategy Development)
- **Data**: Simulated or historical replay
- **Money**: Virtual only
- **Execution**: Backtested / paper results only
- **Purpose**: Develop, tune, and validate strategies before ever considering real money
- **Suitable for**: Learners wanting to build systematic thinking about markets

### 📄 Mode 3: PAPER (Real Data, Virtual Money)
- **Data**: Real market data feeds (when connected)
- **Money**: Virtual only — zero financial risk
- **Execution**: Simulated against live prices
- **Purpose**: Test strategies under real conditions without financial exposure
- **Suitable for**: Strategies that have been validated in RESEARCH mode

### 📊 Mode 4: SIGNAL (Insights & Analysis Only)
- **Data**: Live or historical
- **Money**: None involved
- **Execution**: None — signals are informational output for manual review only
- **Purpose**: Generate structured trading signals and analysis for human decision-making
- **Note**: This is NOT automated trading. Signals require human review and manual action.

> ⛔ **LIVE MODE**: The `LIVE_TRADING` enum exists in code for forward-compatibility only.
> There is **no execution engine implemented**. Selecting live mode will log a warning and refuse to execute.
> If you want to act on signals, that is a manual decision entirely your own responsibility.

---

## Risk Warnings

### Automated Trading Risks (if you ever build real execution)
- Automated systems can lose money extremely rapidly
- Software bugs can cause cascading losses with no manual check
- Market volatility can overcome any risk controls
- Algorithmic flaws lead to systematic, repeating losses

### Financial Risk
- You can lose **all** capital deployed in real trading
- Leveraged positions can exceed your initial investment
- Liquidity crises can prevent you from exiting positions
- Slippage in volatile markets can dramatically worsen outcomes

### Regulatory & Legal Risk
- Cryptocurrency trading regulations vary widely by jurisdiction
- Professional trading may require licences you do not hold
- Tax obligations apply to trading profits in most jurisdictions
- Always verify your legal position before any real activity

---

## Architecture

```
src/
├── simulation/                 # ✅ FULLY IMPLEMENTED
│   └── trading_simulation.py  # Educational portfolio + market simulator
│
├── trading/                    # ⚠️ PARTIAL — signal generation only
│   ├── automated_engine.py    # Mode orchestration (no live execution)
│   ├── market_data.py         # Simulated data (real feeds: not yet connected)
│   ├── risk_manager.py        # Position sizing + risk validation (solid)
│   └── strategy_engine.py     # Signal generation (MA, momentum, patterns)
│
├── config/                    # ✅ FULLY IMPLEMENTED
│   ├── configuration.py       # Config management + component registry
│   └── default_config.json    # Default settings
│
├── plugins/                   # ✅ IMPLEMENTED
│   └── plugin_system.py       # Extensible plugin architecture
│
└── education/                 # ✅ (READMEs + extension points)
    ├── basics/
    └── risk_management/

examples/
├── educational_demo.py        # Safe learning walkthrough
└── automated_trading_demo.py  # Signal + risk demo (RESEARCH/PAPER only)

docs/
├── ARCHITECTURE.md            # Honest implementation status map
├── TECHNICAL_IMPLEMENTATION.md
└── EDUCATIONAL_ROADMAP.md
```

### What is implemented vs. what is not

| Feature | Status | Notes |
|---|---|---|
| Educational simulation | ✅ Complete | Virtual portfolio, order sim, P&L |
| Risk position sizing | ✅ Complete | Kelly-adjacent math, validation |
| MA crossover signals | ✅ Working | Simple but sound skeleton |
| Momentum signals | ✅ Working | Needs real data to be meaningful |
| Pattern detection | ⚠️ Approximate | Simplified — not production TA |
| Multi-timeframe fusion | ⚠️ Vote-count only | Weighted consensus, no true MTF logic |
| Real market data feeds | ❌ Not connected | Falls back to simulation |
| Live order execution | ❌ Not implemented | No exchange API, no execution engine |
| Sharpe ratio | ❌ Always 0 | `daily_returns` never populated yet |
| True VaR | ❌ Approximation | Fixed 5% — not statistically valid |
| Backtesting engine | ❌ Not yet built | Listed as future insert point |

---

## Quick Start

### Educational Mode (safe — start here)
```bash
# Read the disclaimer first
cat DISCLAIMER.md

# Run educational demo
PYTHONPATH=src python examples/educational_demo.py
```

### Research / Signal Mode
```bash
# Run strategy signal demo (no real money, no execution)
PYTHONPATH=src python examples/automated_trading_demo.py
# Select option 1 (Educational) or 2 (Paper) when prompted
# Option 3 (Live) will refuse to execute — no execution engine exists
```

---

## Configuration & Extensibility

The framework is designed around extension points. See `src/config/default_config.json` and `src/config/configuration.py` for the insert-point architecture.

### Adding a Strategy
```python
from trading import StrategyEngine, StrategyConfig, StrategyType

config = StrategyConfig(
    name="my_strategy",
    strategy_type=StrategyType.TREND_FOLLOWING,
    parameters={"ma_fast": 10, "ma_slow": 30},
    risk_per_trade=0.01,       # 1% max risk per trade
    target_assets=["BTC", "ETH"]
)
strategy_engine.register_strategy(config)
```

### Supported Simulated Assets
BTC, ETH, SOL, ADA, LTC — plus meme coin simulation (DOGE, SHIB, PEPE) at appropriately elevated volatility.

---

## Legal & Compliance

### Educational / Research Use
- No special licences required for simulation and signal research
- Safe to use for personal learning at any level

### If You Ever Connect Real Execution
- Professional trading licences **may be required** in your jurisdiction
- Tax obligations apply to all trading profits
- KYC/AML requirements apply on all regulated exchanges
- Consult a qualified financial and legal professional first

---

## License

This project is released under the [MIT License](LICENSE).
Copyright (c) pouringCREME. All rights reserved.

---

## Contributing

Contributions should focus on:
- **Educational value** — better explanations, more scenarios
- **Strategy research tools** — backtesting engine, signal analytics
- **Risk accuracy** — proper VaR, real Sharpe, correlation matrices
- **Honest documentation** — never overstate what is implemented

All contributions must include appropriate disclaimers and maintain the educational-first philosophy.

---

**Remember**: This framework's primary value is helping you think clearly and systematically about markets — safely, with virtual money, before any real decision is ever considered. Start in LEARN mode. Stay there longer than you think you need to.
