# Copilot Instructions for Advanced Cryptocurrency Trading Framework

This repository contains an **advanced automated cryptocurrency trading framework** with comprehensive educational capabilities, designed for both learning trading concepts and executing real automated trading strategies.

## 🚨 Critical Context: Multi-Mode Trading System

**This software supports BOTH educational simulation AND real automated trading:**
- **Educational Mode**: Safe simulation with virtual funds only - no real money involved
- **Paper Trading Mode**: Real market data testing with virtual funds - no financial risk
- **Live Trading Mode**: REAL automated trading with actual money - SIGNIFICANT FINANCIAL RISK
- The system can connect to real exchanges and execute actual trades in live mode
- Built-in safeguards and risk management for all modes, with enhanced protections in educational mode

## Repository Structure & Architecture

### Core Components
- `src/trading/` - **Automated trading engine** (includes real-time execution, market data integration, risk management systems, and strategy engine)
- `src/education/` - Educational modules (basics, analysis, risk management)
- `src/simulation/` - Paper trading simulation environment
- `src/config/` - Configuration management with multi-mode support
- `src/plugins/` - Extensible plugin system for strategies and tools
- `examples/` - Demonstrations including automated trading and educational demos
- `docs/` - Technical documentation and implementation guides

### Key Design Patterns
- **Multi-Mode Architecture**: Seamless switching between educational, paper, and live trading modes
- **Modular Design**: Plugin-based system with clear separation of concerns
- **Insert Points**: Designed for perpetual advancement with specific extension points
- **Risk-First Design**: Comprehensive risk management and safety controls across all modes
- **Educational Integration**: Learning features preserved alongside professional trading capabilities
- **Configuration-Driven**: Flexible settings for different trading modes and learning paths

## Development Guidelines

### When Making Changes
1. **Maintain All Trading Modes**: Preserve functionality for educational, paper, and live trading modes
2. **Preserve Disclaimers**: Never remove or weaken legal disclaimers and risk warnings
3. **Follow Insert Points**: Use designated extension points in configuration system
4. **Test Across Modes**: Ensure features work correctly in all relevant modes (educational, paper, live)
5. **Prioritize Safety**: Risk management and safety controls are paramount, especially for live trading

### Code Style & Patterns
- Follow existing Python conventions and docstring patterns
- Include clear documentation for trading logic and risk controls
- Maintain clear separation between different trading modes
- Use descriptive variable names that reflect trading operations
- Document educational value alongside trading functionality

### Compliance Requirements
- All new features must include appropriate risk warnings and disclaimers
- Trading features must respect mode boundaries (educational vs paper vs live)
- Maintain comprehensive audit trail capabilities for all trading activities
- Include proper risk management controls for live trading features
- Ensure compliance with financial regulations where applicable
- Never weaken existing safety controls or risk management systems

## Common Tasks & Guidelines

### Adding Trading Strategies
```python
# Register new trading strategy via the strategy engine
from trading import StrategyEngine, StrategyConfig, StrategyType

strategy_config = StrategyConfig(
    name="custom_strategy",
    strategy_type=StrategyType.MOMENTUM,
    parameters={"volatility_threshold": 0.05},
    risk_per_trade=0.01,  # Conservative risk management
    educational_version=True  # Include educational variant
)
strategy_engine.register_strategy(strategy_config)
```

### Adding Educational Modules
```python
# Use the configuration system's insert points
config_manager.add_educational_module("new_topic", {
    "enabled": True,
    "version": "1.0.0",
    "topics": ["concept1", "concept2"],
    "prerequisites": ["basics"],
    "educational_objectives": ["learning_goal"]
})
```

### Extending Automated Trading
- Add new trading components via `src/trading/` insert points
- Implement proper risk management controls for all new features
- Ensure mode-appropriate behavior (educational vs paper vs live)
- Test thoroughly in educational and paper modes before live testing
- Include comprehensive logging and audit trails

### Extending Simulation Features
- Add new market scenarios via `src/simulation/` insert points
- Ensure all data remains simulated/virtual in paper trading mode
- Include educational explanations for new features
- Test with both educational and paper trading demos

### Plugin Development
- Follow the plugin architecture in `src/plugins/plugin_system.py`
- Include appropriate validation for the target trading mode
- Document both educational value and trading functionality
- Test integration with existing modules across all modes

## Testing & Validation

### Before Submitting Changes

> **Note:** The `PYTHONPATH=src` prefix is required so that Python can locate the project's modules when running example scripts. This is necessary because the repository uses a `src/` directory layout. If you encounter `ModuleNotFoundError`, ensure you are setting `PYTHONPATH=src` as shown below.
1. Run the educational demo: `PYTHONPATH=src python examples/educational_demo.py`
2. Run the automated trading demo: `PYTHONPATH=src python examples/automated_trading_demo.py`
3. Test in educational mode first, then paper trading mode if applicable
4. Verify all disclaimers and risk warnings remain intact and appropriate
5. Ensure risk management controls function correctly
6. Test mode boundaries (educational features stay educational, live features require proper authorization)
7. Check that configuration validation passes for all modes
8. Verify audit logging works correctly for all trading activities

### Key Files to Review
- `DISCLAIMER.md` - Comprehensive legal disclaimers and risk warnings for all trading modes
- `README.md` - Repository overview with accurate trading mode descriptions
- `src/config/configuration.py` - Configuration system with insert points for all modes
- `examples/automated_trading_demo.py` - Main trading demonstration script
- `examples/educational_demo.py` - Educational demonstration script
- `docs/TECHNICAL_IMPLEMENTATION.md` - Technical architecture and insert points

## Specific Considerations

### Legal & Compliance
- This software supports **real automated trading** with actual money in live mode
- **Significant financial risk** exists when using live trading capabilities
- Comprehensive disclaimers and risk warnings are mandatory
- Professional licensing and regulatory compliance may be required for live trading
- Age verification and jurisdiction checks are critical
- Tax obligations apply to live trading profits
- Users must consult legal and financial professionals before live trading

### Trading Modes & Risk Context
- **Educational Mode**: Safe learning environment with virtual money only
- **Paper Trading Mode**: Real market data with virtual funds for strategy testing
- **Live Trading Mode**: Real money at substantial risk - requires extreme caution
- Each mode has appropriate risk controls and safety features
- Mode boundaries must be strictly maintained
- Educational features are preserved across all modes

### Educational Integration
- Educational capabilities complement professional trading features
- Emphasis on risk management and responsible trading practices
- Includes learning paths for progressing from education to live trading
- Performance metrics serve both educational and practical purposes
- Users should master educational mode before progressing to paper or live trading

### Technical Architecture
- Built with Python using modular, extensible design
- Multi-mode configuration system supporting educational, paper, and live trading
- Comprehensive risk management across all trading modes
- Plugin system allows for both educational content and trading strategy expansion
- Insert points enable future enhancements while maintaining safety and compliance
- Event-driven architecture for real-time trading execution
- Audit trail and logging for all trading activities

## Insert Points for Extensions

The framework includes designated extension points for:
- **Automated Trading**: `src/trading/*` for new trading engine components, execution systems, and market data sources
- **Trading Strategies**: `src/strategies/*` for new algorithmic trading strategies (trend following, momentum, arbitrage, etc.)
- **Risk Management**: `src/trading/risk_manager` and `src/risk/*` for enhanced risk controls and portfolio management
- **Educational Modules**: `src/education/*` for new learning topics and educational content
- **Simulation Scenarios**: `src/simulation/*` for market conditions and paper trading scenarios
- **Analysis Tools**: `src/analysis/*` for market analysis, indicators, and pattern recognition
- **Market Data**: `src/trading/market_data` and `src/data/*` for new data sources and feeds
- **Plugin Architecture**: `src/plugins/*` for third-party strategies, tools, and educational extensions

## Important Reminders

- **Maintain all trading modes** - educational, paper, and live trading capabilities
- **Prioritize safety and risk management** - especially for live trading features
- **Preserve all legal disclaimers** and comprehensive risk warnings
- **Respect mode boundaries** - educational stays educational, live requires proper authorization
- **Test thoroughly** across all relevant modes (educational → paper → live progression)
- **Document both educational value and trading functionality** for new features
- **Implement robust risk controls** for any feature that could affect live trading
- **Follow the modular architecture** and insert point patterns
- **Maintain audit trails** for all trading activities
- **Never weaken existing safety features** or risk management systems

When in doubt about trading functionality, risk management, or legal requirements, refer to:
- `DISCLAIMER.md` - Comprehensive risk warnings and legal disclaimers
- `README.md` - Trading modes and safety practices
- `docs/TECHNICAL_IMPLEMENTATION.md` - Technical architecture and compliance integration
- Existing patterns in `src/trading/` for automated trading implementations
- Existing patterns in `src/education/` for educational features