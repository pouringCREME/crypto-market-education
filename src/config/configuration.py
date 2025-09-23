"""
Educational Crypto Trading Framework Configuration System

This module provides a flexible configuration system with insert points
for perpetual advancement and precision updates.
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime


class ConfigurationManager:
    """
    Manages educational framework configuration with support for
    dynamic updates and modular components.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize configuration manager with optional custom path."""
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 'default_config.json'
        )
        self.config = self._load_config()
        self.insert_points = self._initialize_insert_points()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Provide default configuration structure."""
        return {
            "framework": {
                "version": "1.0.0",
                "mode": "educational_only",
                "last_updated": datetime.now().isoformat()
            },
            "education": {
                "modules": {
                    "basics": {"enabled": True, "version": "1.0.0"},
                    "analysis": {"enabled": True, "version": "1.0.0"},
                    "risk_management": {"enabled": True, "version": "1.0.0"},
                    "simulation": {"enabled": True, "version": "1.0.0"}
                },
                "learning_paths": {
                    "beginner": ["basics", "analysis", "risk_management", "simulation"],
                    "intermediate": ["analysis", "risk_management", "simulation"],
                    "advanced": ["simulation", "advanced_concepts"]
                }
            },
            "simulation": {
                "initial_portfolio_value": 10000,  # Virtual money only
                "available_assets": ["BTC", "ETH", "LTC"],  # Educational symbols
                "data_source": "simulated",  # No real market data
                "update_frequency": "1m",
                "risk_limits": {
                    "max_position_size": 0.1,  # 10% of portfolio
                    "max_daily_loss": 0.05     # 5% of portfolio
                }
            },
            "analysis": {
                "indicators": {
                    "moving_averages": {"enabled": True, "periods": [10, 20, 50]},
                    "rsi": {"enabled": True, "period": 14},
                    "macd": {"enabled": True, "fast": 12, "slow": 26, "signal": 9}
                },
                "chart_timeframes": ["1m", "5m", "15m", "1h", "4h", "1d"]
            },
            "legal_compliance": {
                "educational_only": True,
                "disclaimer_required": True,
                "age_verification": True,
                "jurisdiction_check": True
            },
            "security": {
                "audit_trail": True,
                "data_encryption": True,
                "access_logging": True
            }
        }
    
    def _initialize_insert_points(self) -> Dict[str, List[str]]:
        """Initialize insert points for dynamic updates."""
        return {
            "educational_modules": [
                "src.education.basics",
                "src.education.analysis", 
                "src.education.risk_management",
                "src.education.advanced"
            ],
            "simulation_components": [
                "src.simulation.portfolio",
                "src.simulation.market_data",
                "src.simulation.order_management"
            ],
            "analysis_tools": [
                "src.analysis.indicators",
                "src.analysis.charting",
                "src.analysis.pattern_recognition"
            ],
            "risk_management": [
                "src.risk.position_sizing",
                "src.risk.stop_loss",
                "src.risk.portfolio_risk"
            ],
            "data_sources": [
                "src.data.simulated",
                "src.data.historical",
                "src.data.educational"
            ],
            "plugins": [
                "src.plugins.educational",
                "src.plugins.analysis",
                "src.plugins.reporting"
            ]
        }
    
    def get_config(self, section: str = None) -> Dict[str, Any]:
        """Get configuration section or entire config."""
        if section:
            return self.config.get(section, {})
        return self.config
    
    def update_config(self, section: str, updates: Dict[str, Any]) -> bool:
        """
        Update configuration section with new values.
        Provides insert point for component updates.
        """
        try:
            if section not in self.config:
                self.config[section] = {}
            
            self.config[section].update(updates)
            self.config["framework"]["last_updated"] = datetime.now().isoformat()
            
            # Save updated configuration
            self._save_config()
            
            # Notify components of update (insert point for observers)
            self._notify_component_update(section, updates)
            
            return True
        except Exception as e:
            print(f"Configuration update failed: {e}")
            return False
    
    def add_educational_module(self, module_name: str, module_config: Dict[str, Any]) -> bool:
        """
        Insert point for adding new educational modules.
        """
        try:
            if "education" not in self.config:
                self.config["education"] = {"modules": {}}
            
            if "modules" not in self.config["education"]:
                self.config["education"]["modules"] = {}
            
            self.config["education"]["modules"][module_name] = module_config
            self._save_config()
            
            # Add to insert points
            module_path = f"src.education.{module_name}"
            if module_path not in self.insert_points["educational_modules"]:
                self.insert_points["educational_modules"].append(module_path)
            
            return True
        except Exception as e:
            print(f"Failed to add educational module: {e}")
            return False
    
    def register_plugin(self, plugin_name: str, plugin_config: Dict[str, Any]) -> bool:
        """
        Insert point for registering new plugins.
        """
        try:
            if "plugins" not in self.config:
                self.config["plugins"] = {}
            
            self.config["plugins"][plugin_name] = plugin_config
            self._save_config()
            
            # Add to insert points
            plugin_path = f"src.plugins.{plugin_name}"
            if plugin_path not in self.insert_points["plugins"]:
                self.insert_points["plugins"].append(plugin_path)
            
            return True
        except Exception as e:
            print(f"Failed to register plugin: {e}")
            return False
    
    def get_insert_points(self) -> Dict[str, List[str]]:
        """Get available insert points for component updates."""
        return self.insert_points.copy()
    
    def validate_configuration(self) -> List[str]:
        """
        Validate configuration for legal compliance and safety.
        Returns list of validation errors.
        """
        errors = []
        
        # Ensure educational-only mode
        if not self.config.get("legal_compliance", {}).get("educational_only", False):
            errors.append("Educational-only mode must be enabled")
        
        # Ensure disclaimer is required
        if not self.config.get("legal_compliance", {}).get("disclaimer_required", False):
            errors.append("Legal disclaimer must be required")
        
        # Validate simulation limits
        sim_config = self.config.get("simulation", {})
        if sim_config.get("data_source") != "simulated":
            errors.append("Only simulated data sources allowed in educational mode")
        
        # Validate no real money
        if sim_config.get("initial_portfolio_value", 0) > 100000:  # Arbitrary limit
            errors.append("Portfolio value should be reasonable for educational use")
        
        return errors
    
    def _save_config(self) -> None:
        """Save configuration to file."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _notify_component_update(self, section: str, updates: Dict[str, Any]) -> None:
        """
        Insert point for notifying components of configuration changes.
        Components can register callbacks here for dynamic updates.
        """
        # This is an insert point where components can register
        # for configuration change notifications
        pass


class ComponentManager:
    """
    Manages educational framework components with support for
    dynamic loading and updates.
    """
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config_manager = config_manager
        self.loaded_components = {}
        self.component_registry = {}
    
    def register_component(self, component_name: str, component_class: type, 
                         insert_point: str = None) -> bool:
        """
        Register a new component with optional insert point specification.
        """
        try:
            self.component_registry[component_name] = {
                "class": component_class,
                "insert_point": insert_point,
                "loaded": False
            }
            return True
        except Exception as e:
            print(f"Failed to register component {component_name}: {e}")
            return False
    
    def load_component(self, component_name: str) -> Optional[Any]:
        """
        Load and initialize a component.
        Insert point for component instantiation.
        """
        if component_name not in self.component_registry:
            return None
        
        try:
            component_info = self.component_registry[component_name]
            if not component_info["loaded"]:
                # Insert point for component initialization
                component_config = self.config_manager.get_config()
                instance = component_info["class"](component_config)
                
                self.loaded_components[component_name] = instance
                self.component_registry[component_name]["loaded"] = True
                
                return instance
            else:
                return self.loaded_components[component_name]
        except Exception as e:
            print(f"Failed to load component {component_name}: {e}")
            return None
    
    def update_component(self, component_name: str, updates: Dict[str, Any]) -> bool:
        """
        Update component configuration.
        Insert point for component reconfiguration.
        """
        if component_name in self.loaded_components:
            try:
                component = self.loaded_components[component_name]
                if hasattr(component, 'update_config'):
                    return component.update_config(updates)
                return True
            except Exception as e:
                print(f"Failed to update component {component_name}: {e}")
                return False
        return False
    
    def get_component_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all registered components."""
        return {
            name: {
                "loaded": info["loaded"],
                "insert_point": info["insert_point"],
                "class_name": info["class"].__name__
            }
            for name, info in self.component_registry.items()
        }


# Example usage and insert points demonstration
if __name__ == "__main__":
    # Initialize configuration system
    config_manager = ConfigurationManager()
    
    # Validate configuration
    errors = config_manager.validate_configuration()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration is valid for educational use")
    
    # Display insert points
    insert_points = config_manager.get_insert_points()
    print(f"\nAvailable insert points:")
    for category, points in insert_points.items():
        print(f"  {category}:")
        for point in points:
            print(f"    - {point}")
    
    # Example of adding new educational module (insert point usage)
    new_module_config = {
        "enabled": True,
        "version": "1.0.0",
        "topics": ["advanced_options", "derivatives"],
        "prerequisites": ["basics", "analysis"]
    }
    
    success = config_manager.add_educational_module("advanced_derivatives", new_module_config)
    print(f"\nAdded new educational module: {success}")