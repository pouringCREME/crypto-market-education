# Copilot Instructions for Educational Crypto Trading Framework

This repository contains an **educational-only cryptocurrency trading framework** designed for learning trading concepts, market analysis, and risk management through safe simulation environments.

## 🚨 Critical Context: Educational Purpose Only

**This software is exclusively for educational purposes and contains NO real trading capabilities:**
- All trading is simulated with virtual funds only
- No real money or actual cryptocurrency trading is involved
- No connections to real exchanges or trading APIs
- All market data is simulated or historical for educational use
- Built-in safeguards prevent real trading operations

## Repository Structure & Architecture

### Core Components
- `src/education/` - Educational modules (basics, analysis, risk management)
- `src/simulation/` - Paper trading simulation environment
- `src/config/` - Configuration management with educational safeguards
- `src/plugins/` - Extensible plugin system for educational tools
- `examples/` - Educational demonstrations and usage examples
- `docs/` - Technical documentation and implementation guides

### Key Design Patterns
- **Modular Architecture**: Plugin-based system with clear separation of concerns
- **Insert Points**: Designed for perpetual advancement with specific extension points
- **Educational Safeguards**: Multiple layers preventing real trading operations
- **Configuration-Driven**: Flexible settings for different learning paths

## Development Guidelines

### When Making Changes
1. **Maintain Educational Focus**: All code must remain simulation-only
2. **Preserve Disclaimers**: Never remove or weaken legal disclaimers
3. **Follow Insert Points**: Use designated extension points in `src/config/default_config.json`
4. **Test in Simulation**: Ensure all features work in virtual environment only

### Code Style & Patterns
- Follow existing Python conventions and docstring patterns
- Include educational context in comments and documentation
- Maintain clear separation between simulation and any external data
- Use descriptive variable names that reflect educational purpose

### Compliance Requirements
- All new features must include appropriate educational disclaimers
- No code should enable real trading or money handling
- Maintain audit trail capabilities for educational review
- Include proper risk warnings in user-facing features

## Common Tasks & Guidelines

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

### Extending Simulation Features
- Add new market scenarios via `src/simulation/` insert points
- Ensure all data remains simulated/virtual
- Include educational explanations for new features
- Test with the educational demo script

### Plugin Development
- Follow the plugin architecture in `src/plugins/plugin_system.py`
- Include educational validation and safeguards
- Document learning objectives for each plugin
- Test integration with existing educational modules

## Testing & Validation

### Before Submitting Changes
1. Run the educational demo: `python examples/educational_demo.py`
2. Verify all disclaimers and educational content remain intact
3. Ensure no real trading capabilities are introduced
4. Test new features in the simulation environment
5. Check that configuration validation passes

### Key Files to Review
- `DISCLAIMER.md` - Legal disclaimers and risk warnings
- `src/config/default_config.json` - Configuration and insert points
- `examples/educational_demo.py` - Main demonstration script

## Specific Considerations

### Legal & Compliance
- This is educational software with strict compliance requirements
- All trading is simulated - no real money involved
- Regulatory compliance is built into the framework
- Age verification and jurisdiction checks are required

### Educational Focus
- Primary purpose is teaching trading concepts safely
- Emphasis on risk management and responsible trading education
- Includes learning paths for different skill levels
- Performance metrics are for educational analysis only

### Technical Architecture
- Built with Python using modular, extensible design
- Configuration-driven with JSON-based settings
- Plugin system allows for educational content expansion
- Insert points enable future enhancements while maintaining safety

## Insert Points for Extensions

The framework includes designated extension points for:
- **Educational Modules**: `src/education/modules/` or `src/education/topics/` for new learning topics
- **Simulation Scenarios**: `src/simulation/scenarios/` for market conditions
- **Analysis Tools**: `src/analysis/tools/` for educational market analysis
- **Risk Management**: `src/risk/strategies/` for risk education features
- **Plugin Architecture**: `src/plugins/strategies/` or `src/plugins/tools/` for third-party educational tools

## Important Reminders

- **Always maintain the educational-only nature** of the codebase
- **Never introduce real trading capabilities** or connections
- **Preserve all legal disclaimers** and risk warnings
- **Test thoroughly** in the simulation environment
- **Document educational value** of new features
- **Follow the modular architecture** and insert point patterns

When in doubt about educational compliance or legal requirements, refer to the `DISCLAIMER.md` file and existing patterns in the codebase.