# Architecture & Implementation Status

This document is the honest technical reference for what is built, what is a stub,
and what the intended design is. It should be updated whenever implementation status changes.

---

## Implementation Status Legend

| Symbol | Meaning |
|---|---|
| ✅ | Fully implemented and reliable |
| ⚠️ | Implemented but with known accuracy limitations |
| 🔲 | Stub / skeleton — structure exists, logic incomplete |
| ❌ | Not implemented — referenced but does not exist |

---

## Component Map

### `src/simulation/trading_simulation.py` ✅

The original educational core. Fully implemented and reliable.

| Class | Status | Notes |
|---|---|---|
| `SimulatedAsset` | ✅ | Gaussian random-walk price simulation with market bias |
| `EducationalPortfolio` | ✅ | Virtual buy/sell, position tracking, cash balance |
| `Order` / `OrderStatus` | ✅ | Market orders with slippage simulation |
| `EducationalMarketSimulator` | ✅ | Multi-asset sim with market condition scenarios |
| `EducationalTradingSystem` | ✅ | Full session orchestration, metrics, risk checks |
| `EducationalStrategyRegistry` | ✅ | Plugin point for custom strategy functions |
| `EducationalAnalytics` | ✅ | Plugin point for custom metric calculations |

### `src/trading/automated_engine.py` ⚠️

Mode orchestration shell. Reliable for EDUCATIONAL and PAPER modes. LIVE mode is blocked.

| Feature | Status | Notes |
|---|---|---|
| `TradingMode` enum | ✅ | EDUCATIONAL, PAPER_TRADING, LIVE_TRADING |
| `TradingConfig` dataclass | ✅ | Risk limits, mode, targets |
| Engine start/stop | ✅ | Mode validation, status tracking |
| Educational mode toggle | ✅ | Forces EDUCATIONAL when flag active |
| Manual override | ✅ | Callback registration works |
| Performance metrics | ✅ | Tracks counts, P&L, runtime |
| LIVE_TRADING mode | ❌ | Blocked: raises `NotImplementedError`. No exec engine. |
| `_emergency_position_closure` | 🔲 | Logs only — no real positions to close |
| `_initialize_components` | 🔲 | Logs mode but does not wire real components |
| `execution_engine` | ❌ | File does not exist. Never implemented. |

### `src/trading/market_data.py` ⚠️

Simulated data generator. Real feed integration is a stub.

| Feature | Status | Notes |
|---|---|---|
| `RealTimeMarketData` class | ✅ | Threading, callbacks, tick model |
| `_simulate_market_data()` | ✅ | Gaussian random-walk, per-asset volatility profiles |
| `_stream_real_data()` | 🔲 | Falls back to simulation with a warning |
| Real exchange connection | ❌ | No ccxt, no WebSocket, no API keys |
| OHLCV aggregation | 🔲 | Structures exist but data not yet built from ticks |
| `get_trajectory_data()` | ✅ | Returns filtered tick log |

### `src/trading/risk_manager.py` ⚠️

Position sizing and trade validation are solid. Statistical metrics have known issues.

| Feature | Status | Notes |
|---|---|---|
| `calculate_position_size()` | ✅ | Risk-per-share Kelly-adjacent math, size capping |
| `validate_trade()` | ✅ | Portfolio exposure + position size checks |
| `update_position()` | ✅ | Tracks unrealized P&L, fires alerts |
| `record_daily_return()` | ✅ | Must be called externally to populate Sharpe data |
| Sharpe ratio | ⚠️ | Requires `record_daily_return()` called daily. 0.0 otherwise. |
| VaR (`portfolio_var`) | ⚠️ | Fixed 5% of exposure. Not a proper historical/parametric VaR. |
| Correlation risk | ⚠️ | Position count × 0.1 — not actual correlation |
| Alert callbacks | ✅ | Position and volatility alert system works |

### `src/trading/strategy_engine.py` ⚠️

Signal generation framework. Logic is sound for research purposes but approximated.

| Feature | Status | Notes |
|---|---|---|
| `StrategyConfig` / `TradingSignal` | ✅ | Well-structured data models |
| `register_strategy()` | ✅ | Registry + performance tracking |
| MA crossover signals | ✅ | Simple SMA fast/slow crossover. Works for research. |
| Momentum signals | ✅ | Volume ratio + price change threshold. Sound concept. |
| Educational conservative signals | ✅ | 2x MA with wide stops |
| Multi-timeframe fusion | ⚠️ | Weighted vote count. Not true MTF confluence. |
| `_detect_triangle_patterns()` | ⚠️ | Rough approximation — checks flat highs + rising lows |
| `_detect_double_patterns()` | ⚠️ | Simple peak proximity check |
| `_detect_support_resistance()` | ⚠️ | Float-bucketing approach — likely fires rarely |
| Confidence values | ⚠️ | Hardcoded (0.7, 0.8) — not dynamically calibrated |
| RSI | ❌ | Config has RSI parameters but no RSI implementation |
| MACD | ❌ | Config has MACD parameters but no MACD implementation |
| Bollinger Bands | ❌ | Config has BB parameters but no BB implementation |

### `src/config/configuration.py` ✅

Fully implemented. Config management, component registry, insert point architecture.

### `src/plugins/plugin_system.py` ✅

Plugin registry and lifecycle. `MovingAverageAnalysisPlugin` is a working example.

---

## Data Flow (Current State)

```
[Simulated price generator]
        │
        ▼
[market_data.py: tick stream]
        │
        ▼
[strategy_engine.py: signal generation]
   - MA crossover
   - Momentum
   - Pattern detection (approximate)
        │
        ▼
[risk_manager.py: signal validation]
   - Position sizing
   - Exposure check
   - Alert generation
        │
        ▼
[automated_engine.py: coordination]
        │
        ▼
[OUTPUT: TradingSignal objects for manual review]
        │
    NO EXECUTION
    (execution_engine.py does not exist)
```

---

## Known Issues to Fix (Priority Order)

### P0 — Safety / Correctness
- [x] `LIVE_TRADING` mode now raises `NotImplementedError` (was silently doing nothing)
- [x] `_emergency_position_closure` now clearly documented as stub

### P1 — Metric Accuracy
- [x] Sharpe ratio: `record_daily_return()` method added; documented requirements
- [x] VaR: clearly documented as approximation, not valid statistical VaR
- [x] Correlation risk: clearly documented as position count proxy

### P2 — Signal Quality
- [x] Meme coin simulation volatility reduced from ±15%/tick to realistic Gaussian
- [ ] RSI implementation needed (parameters exist, code does not)
- [ ] MACD implementation needed (parameters exist, code does not)
- [ ] Support/resistance bucketing: floating-point rounding needs fix
- [ ] Confidence values: should be dynamically calibrated, not hardcoded

### P3 — Architecture Gaps
- [ ] Execution engine: if real trading desired, this is the next major build
- [ ] Real data feeds: ccxt or WebSocket integration
- [ ] Backtesting engine: listed as insert point, not yet built
- [ ] OHLCV aggregation: tick → candle pipeline incomplete

---

## Extension Points (Insert Points)

The following module paths are reserved for future implementation:

```
src/trading/execution_engine.py     ← NEXT MAJOR BUILD if live trading wanted
src/analysis/indicators.py          ← RSI, MACD, BB, ATR
src/analysis/pattern_recognition.py ← Proper TA pattern library
src/data/historical.py              ← Historical data ingestion
src/data/real_time.py               ← Exchange WebSocket feed
src/strategies/backtester.py        ← Backtesting engine
src/strategies/mean_reversion.py    ← Mean reversion strategy
src/strategies/arbitrage.py         ← Statistical arbitrage
src/risk/var_models.py              ← Proper historical/parametric VaR
src/risk/correlation_analysis.py    ← Real covariance matrix
```
