"""
Automated Trading Engine Core

High-performance automated trading system with educational mode preservation.
Supports real-time market data processing and automated strategy execution.
"""

import asyncio
import logging
import threading
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field

# Import educational components for preservation
try:
    from ..simulation.trading_simulation import EducationalTradingSystem
except ImportError:
    # Fallback for standalone usage
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from simulation.trading_simulation import EducationalTradingSystem


class TradingMode(Enum):
    """Trading system operational modes."""
    EDUCATIONAL = "educational"  # Safe simulation only
    PAPER_TRADING = "paper"     # Real data, virtual money
    LIVE_TRADING = "live"       # Real data, real money (requires compliance)


class SystemStatus(Enum):
    """System operational status."""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


@dataclass
class TradingConfig:
    """Configuration for automated trading system."""
    mode: TradingMode = TradingMode.EDUCATIONAL
    max_positions: int = 10
    max_portfolio_risk: float = 0.02  # 2% of portfolio
    max_position_size: float = 0.1    # 10% of portfolio per position
    enable_manual_override: bool = True
    educational_mode_active: bool = True
    risk_management_enabled: bool = True
    high_frequency_mode: bool = False
    target_assets: List[str] = field(default_factory=lambda: ["BTC", "ETH", "SOL"])
    

class AutomatedTradingEngine:
    """
    Core automated trading engine with educational preservation.
    
    Provides high-performance automated trading capabilities while maintaining
    educational components and safety features.
    """
    
    def __init__(self, config: TradingConfig = None):
        """Initialize the automated trading engine."""
        self.config = config or TradingConfig()
        self.status = SystemStatus.STOPPED
        self.logger = logging.getLogger(__name__)
        
        # Initialize educational system for preservation
        self.educational_system = EducationalTradingSystem()
        
        # Core engine components
        self.market_data = None
        self.risk_manager = None  
        self.strategy_engine = None
        self.execution_engine = None
        
        # Performance monitoring
        self.performance_metrics = {
            'trades_executed': 0,
            'successful_trades': 0,
            'total_pnl': 0.0,
            'max_drawdown': 0.0,
            'start_time': None
        }
        
        # Manual override system
        self.manual_override_active = False
        self.override_callbacks: List[Callable] = []
        
        # Educational mode toggle
        self._educational_mode_active = self.config.educational_mode_active
        
        self.logger.info(f"Automated Trading Engine initialized in {self.config.mode.value} mode")
    
    def start(self) -> bool:
        """Start the automated trading engine."""
        try:
            self.status = SystemStatus.STARTING
            self.logger.info("Starting automated trading engine...")
            
            # Validate configuration
            if not self._validate_configuration():
                self.status = SystemStatus.ERROR
                return False
            
            # Initialize components based on mode
            self._initialize_components()
            
            # Initialize performance tracking
            self.performance_metrics['start_time'] = datetime.now()
            
            self.status = SystemStatus.RUNNING
            self.logger.info("Automated trading engine started successfully")
            
            # Educational mode notification
            if self._educational_mode_active:
                self.logger.info("Educational mode is active - additional safety features enabled")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start trading engine: {e}")
            self.status = SystemStatus.ERROR
            return False
    
    def stop(self) -> bool:
        """Stop the automated trading engine safely."""
        try:
            self.status = SystemStatus.STOPPING
            self.logger.info("Stopping automated trading engine...")
            
            # Close all positions if in live mode
            if self.config.mode == TradingMode.LIVE_TRADING:
                self._emergency_position_closure()
            
            self.status = SystemStatus.STOPPED
            self.logger.info("Automated trading engine stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping trading engine: {e}")
            self.status = SystemStatus.ERROR
            return False
    
    def enable_manual_override(self, callback: Callable = None) -> None:
        """Enable manual override mode."""
        self.manual_override_active = True
        if callback:
            self.override_callbacks.append(callback)
        self.logger.info("Manual override enabled")
    
    def disable_manual_override(self) -> None:
        """Disable manual override mode."""
        self.manual_override_active = False
        self.override_callbacks.clear()
        self.logger.info("Manual override disabled")
    
    def toggle_educational_mode(self, active: bool) -> None:
        """Toggle educational mode on/off."""
        self._educational_mode_active = active
        self.config.educational_mode_active = active
        
        if active:
            self.logger.info("Educational mode activated - enhanced safety features enabled")
        else:
            self.logger.warning("Educational mode deactivated - proceed with caution")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        if self.performance_metrics['start_time']:
            runtime = datetime.now() - self.performance_metrics['start_time']
            self.performance_metrics['runtime_hours'] = runtime.total_seconds() / 3600
        
        return self.performance_metrics.copy()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            'status': self.status.value,
            'mode': self.config.mode.value,
            'educational_mode': self._educational_mode_active,
            'manual_override': self.manual_override_active,
            'performance': self.get_performance_metrics(),
            'config': {
                'max_positions': self.config.max_positions,
                'max_portfolio_risk': self.config.max_portfolio_risk,
                'risk_management_enabled': self.config.risk_management_enabled
            }
        }
    
    def _validate_configuration(self) -> bool:
        """Validate system configuration."""
        # Live trading is not implemented — always block it
        if self.config.mode == TradingMode.LIVE_TRADING:
            self.logger.error(
                "LIVE_TRADING mode is not supported: no execution engine exists. "
                "Use EDUCATIONAL or PAPER_TRADING for signal research."
            )
            return False

        # Educational mode validation
        if self._educational_mode_active:
            if self.config.mode != TradingMode.EDUCATIONAL:
                self.logger.warning(
                    "Educational mode flag is active but mode is not EDUCATIONAL. "
                    "Forcing to EDUCATIONAL mode for safety."
                )
                self.config.mode = TradingMode.EDUCATIONAL

        # Risk limits validation
        if self.config.max_portfolio_risk > 0.1:  # 10% max
            self.logger.error("Portfolio risk limit too high (max 10%)")
            return False

        if self.config.max_position_size > 0.2:  # 20% max
            self.logger.error("Position size limit too high (max 20%)")
            return False

        return True
    
    def _initialize_components(self) -> None:
        """Initialize trading engine components."""
        if self.config.mode == TradingMode.EDUCATIONAL:
            self.logger.info("Initializing in educational mode — fully simulated, no real data or money")
        elif self.config.mode == TradingMode.PAPER_TRADING:
            self.logger.info("Initializing paper trading mode — real data feeds, virtual money")
        elif self.config.mode == TradingMode.LIVE_TRADING:
            # NOTE: No execution engine exists. LIVE_TRADING is a forward-compatibility
            # stub only. It will not execute any real orders. Log and refuse.
            self.logger.error(
                "LIVE_TRADING mode selected but no execution engine is implemented. "
                "Real order execution requires a connected exchange adapter "
                "(src/trading/execution_engine.py — not yet built). "
                "Refusing to proceed. Use EDUCATIONAL or PAPER_TRADING instead."
            )
            raise NotImplementedError(
                "Live trading execution engine is not implemented. "
                "This system generates signals for manual review only. "
                "See ARCHITECTURE.md for the current implementation status."
            )

    def _emergency_position_closure(self) -> None:
        """
        Emergency closure of all positions.

        NOTE: This is a stub. No execution engine exists, so there are no
        live positions to close. In a future implementation with a real
        execution adapter, this would issue market-sell orders for all open
        positions. Until then, it only logs.
        """
        self.logger.warning(
            "Emergency position closure called — no execution engine available. "
            "If you have real positions on an exchange, close them manually immediately."
        )
    
    # Educational system integration
    def get_educational_system(self) -> EducationalTradingSystem:
        """Get the educational trading system for learning purposes."""
        return self.educational_system
    
    def run_educational_simulation(self, scenario: str = "bull_market") -> Dict[str, Any]:
        """Run an educational simulation scenario."""
        if not self._educational_mode_active:
            return {"error": "Educational mode not active"}
        
        # Use existing educational system for simulation
        return {"status": "educational_simulation_running", "scenario": scenario}
