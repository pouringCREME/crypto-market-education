# Copilot Guidelines for the Politics Repository

## Objective
To maximize the efficiency, accuracy, and quality of contributions to the Politics repository's educational crypto trading framework by providing comprehensive guidelines for using GitHub Copilot as a coding assistant while maintaining educational focus and legal compliance.

---

## 1. Code Quality Standards

### Python Code Standards
- **PEP 8 Compliance**: Follow Python PEP 8 style guidelines for consistent formatting
- **Type Hints**: Use type hints for function parameters and return values (e.g., `def calculate_position_size(portfolio_value: float, risk_percent: float) -> float:`)
- **Docstrings**: Include comprehensive docstrings using Google or NumPy style for all classes and functions
- **Import Organization**: Organize imports in standard library → third-party → local modules order
- **Line Length**: Maintain 88 characters per line (Black formatter standard)

### Modular Architecture
- **Plugin System**: Leverage the existing plugin architecture for new educational modules
- **Configuration Management**: Use the `ConfigurationManager` class for all configurable components
- **Insert Points**: Utilize designated insert points for adding new functionality without breaking existing code
- **Educational Compliance**: Ensure all new code maintains educational-only focus and includes appropriate disclaimers

### Code Organization
```python
# Example of proper code organization
class EducationalTradingModule(EducationalPlugin):
    """Educational module for trading concepts with proper structure."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize with educational compliance validation."""
        super().__init__(config)
        # Implementation here
```

---

## 2. Error Reduction Strategies

### Static Analysis and Linting
- **Flake8**: Use for general Python linting and style enforcement
- **mypy**: Implement type checking to catch type-related errors early
- **Black**: Apply automatic code formatting for consistency
- **isort**: Organize imports automatically
- **bandit**: Security linting for Python code

### Robust Error Handling
```python
# Educational trading simulation error handling example
def execute_educational_trade(trade_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute educational trade with comprehensive error handling."""
    try:
        # Validate educational compliance first
        if not self.validate_educational_mode():
            raise ValueError("Educational mode must be enabled")
        
        # Process trade simulation
        result = self._process_simulation_trade(trade_data)
        
        # Log educational activity for audit trail
        self.audit_logger.log_educational_activity(
            activity="simulation_trade",
            details={"virtual_only": True, "educational_purpose": True}
        )
        
        return result
        
    except ValueError as e:
        logger.error(f"Educational validation error: {e}")
        return {"error": str(e), "educational_reminder": "This is simulation only"}
    except Exception as e:
        logger.exception(f"Unexpected error in educational simulation: {e}")
        return {"error": "Simulation failed", "support_note": "Contact educational support"}
```

### Input Validation
- **Schema Validation**: Use pydantic or similar for data validation
- **Educational Boundaries**: Validate all inputs maintain educational context
- **Simulation Limits**: Enforce reasonable limits for educational scenarios
- **Legal Compliance**: Validate all operations comply with educational-only requirements

---

## 3. High-Quality Solution Development

### Problem-Solving Approach
1. **Educational Context First**: Ensure all solutions maintain educational focus
2. **Compliance Validation**: Verify legal and regulatory compliance
3. **User Safety**: Prioritize user understanding and safe learning environment
4. **Scalable Architecture**: Design for extensibility through insert points

### Algorithm Efficiency
- **Time Complexity**: Document and optimize for educational scenarios (typically O(n) or O(n log n) acceptable)
- **Memory Usage**: Consider memory efficiency for educational simulations
- **Educational Value**: Balance performance with educational clarity

### Design Patterns
```python
# Factory pattern for educational modules
class EducationalModuleFactory:
    """Factory for creating educational modules with compliance checks."""
    
    @staticmethod
    def create_module(module_type: str, config: Dict[str, Any]) -> EducationalPlugin:
        """Create educational module with automatic compliance validation."""
        modules = {
            "risk_management": RiskManagementEducationPlugin,
            "market_analysis": MarketAnalysisEducationPlugin,
            "portfolio_simulation": PortfolioSimulationPlugin
        }
        
        if module_type not in modules:
            raise ValueError(f"Unknown educational module: {module_type}")
        
        module = modules[module_type](config)
        
        # Validate educational compliance
        if not module.validate_educational_compliance():
            raise ValueError(f"Module {module_type} fails educational compliance")
        
        return module
```

### Code Review Standards
- **Educational Focus Review**: Verify all changes maintain educational purpose
- **Legal Compliance Check**: Ensure no real trading capabilities are introduced
- **Documentation Review**: Validate educational documentation and disclaimers
- **Security Review**: Check for any potential security vulnerabilities
- **Performance Review**: Assess impact on educational simulation performance

---

## 4. Testing Standards and Coverage

### Unit Testing Requirements
- **Minimum Coverage**: Maintain 85% code coverage for all educational modules
- **Educational Scenarios**: Test all educational learning paths and scenarios
- **Compliance Testing**: Verify educational-only operation in all tests
- **Error Handling**: Test error conditions and edge cases

```python
# Example test structure
import pytest
from unittest.mock import patch, MagicMock

class TestEducationalTradingSystem:
    """Test suite for educational trading system."""
    
    def test_educational_compliance_validation(self):
        """Test that system enforces educational-only mode."""
        system = EducationalTradingSystem()
        
        # Should reject any real trading attempts
        with pytest.raises(ValueError, match="Educational-only mode"):
            system.enable_real_trading()
        
        # Should require disclaimers
        assert system.requires_disclaimer()
        assert system.is_educational_only()
    
    def test_simulation_trade_execution(self):
        """Test educational trade simulation."""
        system = EducationalTradingSystem()
        trade_data = {
            "symbol": "BTC-USD",
            "quantity": 0.1,
            "type": "educational_simulation"
        }
        
        result = system.execute_educational_trade(trade_data)
        
        assert result["virtual_only"] is True
        assert "educational_reminder" in result
        assert result["status"] == "simulation_complete"
```

### Integration Testing
- **Module Interaction**: Test interactions between educational components
- **Configuration Management**: Validate configuration updates and insert points
- **Plugin System**: Test plugin loading and educational compliance validation
- **Educational Workflows**: End-to-end testing of learning scenarios

### Educational Scenario Testing
```python
def test_complete_educational_workflow():
    """Test complete educational learning workflow."""
    # Initialize educational framework
    framework = EducationalFramework()
    
    # Test beginner learning path
    learner = framework.create_learner_profile("beginner")
    
    # Progress through educational modules
    modules = ["basics", "risk_management", "simulation"]
    for module_name in modules:
        module = framework.load_educational_module(module_name)
        result = module.complete_learning_objectives(learner)
        
        assert result["completed"] is True
        assert result["educational_value"] > 0.8
        assert "real_trading" not in result
```

### Security and Compliance Testing
- **No Real Trading**: Automated tests to ensure no real trading capabilities
- **Data Protection**: Validate educational data handling and privacy
- **Legal Compliance**: Regular compliance audits and validation
- **Simulation Boundaries**: Test that simulations cannot access real markets

---

## 5. Continuous Improvement Processes

### Automated Quality Assurance
```yaml
# GitHub Actions workflow example for quality assurance
name: Educational Framework Quality Check
on: [push, pull_request]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install flake8 mypy black isort bandit pytest pytest-cov
      
      - name: Lint with flake8
        run: flake8 src/ examples/ --max-line-length=88
      
      - name: Type check with mypy
        run: mypy src/
      
      - name: Security check with bandit
        run: bandit -r src/
      
      - name: Run educational compliance tests
        run: pytest tests/compliance/ -v
      
      - name: Run full test suite with coverage
        run: pytest --cov=src --cov-report=html --cov-min=85
```

### Performance Monitoring
- **Educational Simulation Performance**: Monitor simulation response times
- **Memory Usage Tracking**: Ensure efficient resource usage for education
- **User Learning Metrics**: Track educational effectiveness metrics
- **System Health Monitoring**: Monitor educational framework stability

### Regular Audits and Updates
- **Monthly Compliance Reviews**: Regular legal and educational compliance audits
- **Quarterly Guideline Updates**: Review and update these guidelines based on usage
- **Educational Content Updates**: Keep educational materials current with market developments
- **Community Feedback Integration**: Incorporate user feedback for continuous improvement

### Metrics and KPIs
```python
# Educational effectiveness metrics
QUALITY_METRICS = {
    "code_coverage": {"target": 85, "minimum": 80},
    "educational_compliance": {"target": 100, "minimum": 100},
    "simulation_accuracy": {"target": 95, "minimum": 90},
    "user_learning_satisfaction": {"target": 4.5, "minimum": 4.0},
    "legal_compliance_score": {"target": 100, "minimum": 100}
}
```

---

## Repository-Specific Guidelines

### Educational Framework Compliance
- **Always Educational**: Every feature must serve educational purposes only
- **No Real Money**: Absolutely no real trading or financial transactions
- **Clear Disclaimers**: Include educational disclaimers in all user-facing components
- **Simulation Only**: All trading must be clearly marked as simulation/paper trading

### Plugin Development
- **Educational Plugin Base**: Extend `EducationalPlugin` for all new plugins
- **Compliance Validation**: Implement `validate_educational_compliance()` method
- **Insert Point Usage**: Use designated insert points for extensibility
- **Educational Objectives**: Define clear learning objectives for each plugin

### Configuration Management
- **Use ConfigurationManager**: Leverage existing configuration system
- **Educational Defaults**: Ensure all defaults maintain educational focus
- **Validation Required**: Validate all configurations for educational compliance
- **Insert Points**: Use configuration insert points for updates

---

## Implementation Checklist

### For New Features
- [ ] Educational purpose clearly defined
- [ ] Legal compliance verified
- [ ] Appropriate disclaimers included
- [ ] Tests cover educational scenarios
- [ ] Documentation updated with educational context
- [ ] Code review completed with educational focus
- [ ] Performance impact assessed
- [ ] Security review completed

### For Bug Fixes
- [ ] Educational functionality preserved
- [ ] Compliance maintained
- [ ] Tests updated to prevent regression
- [ ] Educational value not compromised
- [ ] Documentation updated if needed

### For Maintenance
- [ ] Educational content kept current
- [ ] Legal compliance reviewed
- [ ] Dependencies updated safely
- [ ] Educational effectiveness measured
- [ ] User feedback incorporated

---

## Support and Resources

### Documentation
- [Educational Roadmap](docs/EDUCATIONAL_ROADMAP.md)
- [Technical Implementation Guide](docs/TECHNICAL_IMPLEMENTATION.md)
- [Legal Disclaimer](DISCLAIMER.md)

### Tools and Setup
```bash
# Development environment setup
pip install flake8 mypy black isort bandit pytest pytest-cov
pre-commit install  # If using pre-commit hooks

# Run quality checks
flake8 src/ --max-line-length=88
mypy src/
bandit -r src/
pytest --cov=src --cov-min=85
```

### Getting Help
- Review existing educational modules for patterns
- Check insert points for extensibility options
- Ensure educational compliance in all contributions
- Consult legal disclaimer for boundary guidance

---

## Conclusion

These guidelines ensure that GitHub Copilot assists in creating high-quality, educationally-focused, legally compliant code for the Politics repository's educational crypto trading framework. By following these standards, contributors can effectively use AI assistance while maintaining the educational mission and legal requirements of the project.

Remember: **All development must maintain the educational-only nature of this framework and include appropriate legal disclaimers.**