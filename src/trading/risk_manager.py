"""
Advanced Risk Management System

Comprehensive risk management for automated trading with educational preservation.
Includes position sizing, stop-loss management, and portfolio risk controls.
"""

import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import math


class RiskLevel(Enum):
    """Risk level classifications."""
    VERY_LOW = "very_low"    # Educational/Conservative
    LOW = "low"              # Conservative
    MODERATE = "moderate"    # Balanced
    HIGH = "high"           # Aggressive
    VERY_HIGH = "very_high" # Speculative


class AlertType(Enum):
    """Risk alert types."""
    POSITION_SIZE = "position_size"
    PORTFOLIO_RISK = "portfolio_risk"
    DRAWDOWN = "drawdown"
    VOLATILITY = "volatility"
    CORRELATION = "correlation"
    STOP_LOSS = "stop_loss"


@dataclass
class RiskMetrics:
    """Risk metrics calculation results."""
    portfolio_value: float
    total_exposure: float
    max_position_risk: float
    portfolio_var: float  # Value at Risk
    sharpe_ratio: float
    max_drawdown: float
    correlation_risk: float
    risk_score: float  # Overall risk score 0-100


@dataclass
class PositionRisk:
    """Individual position risk assessment."""
    symbol: str
    position_size: float
    entry_price: float
    current_price: float
    stop_loss: float
    position_value: float
    unrealized_pnl: float
    risk_amount: float
    risk_percentage: float
    volatility: float
    

class RiskManager:
    """
    Advanced risk management system for automated trading.
    
    Provides comprehensive risk controls, position sizing, and educational safety features.
    """
    
    def __init__(self, 
                 educational_mode: bool = True,
                 max_portfolio_risk: float = 0.02,
                 max_position_size: float = 0.1):
        """Initialize risk management system."""
        self.educational_mode = educational_mode
        self.max_portfolio_risk = max_portfolio_risk  # 2% default
        self.max_position_size = max_position_size    # 10% default
        self.logger = logging.getLogger(__name__)
        
        # Risk limits (more conservative in educational mode)
        if educational_mode:
            self.max_portfolio_risk = min(max_portfolio_risk, 0.01)  # 1% max in educational
            self.max_position_size = min(max_position_size, 0.05)    # 5% max in educational
        
        # Position tracking
        self.positions: Dict[str, PositionRisk] = {}
        self.portfolio_value = 10000.0  # Default starting value
        
        # Risk history
        self.risk_history: List[RiskMetrics] = []
        self.drawdown_history: List[Tuple[datetime, float]] = []
        
        # Alert system
        self.risk_alerts: List[Dict[str, Any]] = []
        self.alert_callbacks: List[callable] = []
        
        # Performance tracking
        self.daily_returns: List[float] = []
        self.peak_portfolio_value = self.portfolio_value
        
        self.logger.info(f"Risk Manager initialized - Educational: {educational_mode}")
        self.logger.info(f"Max portfolio risk: {self.max_portfolio_risk:.1%}")
        self.logger.info(f"Max position size: {self.max_position_size:.1%}")
    
    def calculate_position_size(self, 
                              symbol: str,
                              entry_price: float,
                              stop_loss_price: float,
                              risk_amount: Optional[float] = None) -> Tuple[float, bool]:
        """
        Calculate appropriate position size based on risk parameters.
        
        Returns: (position_size, is_valid)
        """
        try:
            # Use default risk amount if not provided
            if risk_amount is None:
                risk_amount = self.portfolio_value * self.max_portfolio_risk
            
            # Calculate risk per share
            risk_per_share = abs(entry_price - stop_loss_price)
            
            if risk_per_share <= 0:
                self.logger.error(f"Invalid stop loss for {symbol}: entry={entry_price}, stop={stop_loss_price}")
                return 0.0, False
            
            # Calculate position size
            position_size = risk_amount / risk_per_share
            position_value = position_size * entry_price
            
            # Check position size limits
            max_position_value = self.portfolio_value * self.max_position_size
            
            if position_value > max_position_value:
                # Reduce position size to stay within limits
                position_size = max_position_value / entry_price
                position_value = position_size * entry_price
                
                self.logger.warning(f"Position size reduced for {symbol} due to size limits")
            
            # Educational mode additional checks
            if self.educational_mode:
                # Extra conservative limits
                if position_value > self.portfolio_value * 0.03:  # 3% max in educational
                    position_size = (self.portfolio_value * 0.03) / entry_price
                    self.logger.info(f"Educational mode: reduced position size for {symbol}")
            
            return position_size, True
            
        except Exception as e:
            self.logger.error(f"Error calculating position size for {symbol}: {e}")
            return 0.0, False
    
    def validate_trade(self, 
                      symbol: str,
                      position_size: float,
                      entry_price: float,
                      stop_loss: float = None) -> Tuple[bool, List[str]]:
        """
        Validate a proposed trade against risk limits.
        
        Returns: (is_valid, list_of_violations)
        """
        violations = []
        
        try:
            position_value = position_size * entry_price
            
            # Check position size limit
            max_position_value = self.portfolio_value * self.max_position_size
            if position_value > max_position_value:
                violations.append(f"Position size exceeds limit: ${position_value:.2f} > ${max_position_value:.2f}")
            
            # Check portfolio risk limit
            if stop_loss:
                risk_amount = position_size * abs(entry_price - stop_loss)
                max_risk = self.portfolio_value * self.max_portfolio_risk
                if risk_amount > max_risk:
                    violations.append(f"Risk amount exceeds limit: ${risk_amount:.2f} > ${max_risk:.2f}")
            
            # Check total portfolio exposure
            total_exposure = sum(pos.position_value for pos in self.positions.values()) + position_value
            max_total_exposure = self.portfolio_value * 0.8  # 80% max exposure
            
            if total_exposure > max_total_exposure:
                violations.append(f"Total exposure exceeds limit: ${total_exposure:.2f} > ${max_total_exposure:.2f}")
            
            # Educational mode additional checks
            if self.educational_mode:
                if position_value > self.portfolio_value * 0.03:  # 3% max
                    violations.append("Educational mode: position size too large")
                
                if len(self.positions) >= 3:  # Max 3 positions in educational
                    violations.append("Educational mode: too many open positions")
            
            return len(violations) == 0, violations
            
        except Exception as e:
            self.logger.error(f"Error validating trade for {symbol}: {e}")
            return False, [f"Validation error: {e}"]
    
    def update_position(self, 
                       symbol: str,
                       position_size: float,
                       entry_price: float,
                       current_price: float,
                       stop_loss: float = None) -> bool:
        """Update position information for risk tracking."""
        try:
            position_value = position_size * current_price
            unrealized_pnl = position_size * (current_price - entry_price)
            
            risk_amount = 0.0
            risk_percentage = 0.0
            if stop_loss:
                risk_amount = position_size * abs(entry_price - stop_loss)
                risk_percentage = risk_amount / self.portfolio_value
            
            # Calculate volatility (simplified)
            volatility = abs(current_price - entry_price) / entry_price if entry_price > 0 else 0.0
            
            position_risk = PositionRisk(
                symbol=symbol,
                position_size=position_size,
                entry_price=entry_price,
                current_price=current_price,
                stop_loss=stop_loss or 0.0,
                position_value=position_value,
                unrealized_pnl=unrealized_pnl,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                volatility=volatility
            )
            
            self.positions[symbol] = position_risk
            
            # Check for risk alerts
            self._check_position_alerts(position_risk)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating position for {symbol}: {e}")
            return False
    
    def remove_position(self, symbol: str) -> bool:
        """Remove position from risk tracking."""
        if symbol in self.positions:
            del self.positions[symbol]
            self.logger.info(f"Position removed from risk tracking: {symbol}")
            return True
        return False
    
    def calculate_portfolio_risk(self) -> RiskMetrics:
        """Calculate comprehensive portfolio risk metrics."""
        try:
            # Current portfolio metrics
            total_exposure = sum(pos.position_value for pos in self.positions.values())
            total_pnl = sum(pos.unrealized_pnl for pos in self.positions.values())
            current_portfolio_value = self.portfolio_value + total_pnl
            
            # Max position risk
            max_position_risk = max(
                (pos.risk_percentage for pos in self.positions.values()),
                default=0.0
            )
            
            # Simplified VaR calculation (99% confidence)
            portfolio_var = total_exposure * 0.05  # 5% VaR approximation
            
            # Sharpe ratio (simplified)
            if self.daily_returns:
                avg_return = sum(self.daily_returns) / len(self.daily_returns)
                return_std = self._calculate_std(self.daily_returns)
                sharpe_ratio = avg_return / return_std if return_std > 0 else 0.0
            else:
                sharpe_ratio = 0.0
            
            # Max drawdown
            if current_portfolio_value > self.peak_portfolio_value:
                self.peak_portfolio_value = current_portfolio_value
            
            max_drawdown = (self.peak_portfolio_value - current_portfolio_value) / self.peak_portfolio_value
            
            # Correlation risk (simplified - assumes some correlation)
            correlation_risk = len(self.positions) * 0.1  # Simplified correlation factor
            
            # Overall risk score (0-100)
            risk_score = min(100, (
                max_position_risk * 100 * 2 +  # Position concentration
                (total_exposure / self.portfolio_value) * 50 +  # Exposure
                max_drawdown * 100 +  # Drawdown
                correlation_risk * 20  # Correlation
            ))
            
            metrics = RiskMetrics(
                portfolio_value=current_portfolio_value,
                total_exposure=total_exposure,
                max_position_risk=max_position_risk,
                portfolio_var=portfolio_var,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                correlation_risk=correlation_risk,
                risk_score=risk_score
            )
            
            # Store in history
            self.risk_history.append(metrics)
            if len(self.risk_history) > 1000:
                self.risk_history = self.risk_history[-500:]
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating portfolio risk: {e}")
            return RiskMetrics(
                portfolio_value=self.portfolio_value,
                total_exposure=0.0,
                max_position_risk=0.0,
                portfolio_var=0.0,
                sharpe_ratio=0.0,
                max_drawdown=0.0,
                correlation_risk=0.0,
                risk_score=0.0
            )
    
    def get_risk_alerts(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get risk alerts."""
        if active_only:
            # Filter recent alerts (last 24 hours)
            cutoff_time = datetime.now() - timedelta(hours=24)
            return [
                alert for alert in self.risk_alerts
                if alert.get('timestamp', datetime.min) > cutoff_time
            ]
        return self.risk_alerts.copy()
    
    def register_alert_callback(self, callback: callable) -> None:
        """Register callback for risk alerts."""
        self.alert_callbacks.append(callback)
    
    def _check_position_alerts(self, position: PositionRisk) -> None:
        """Check for position-specific risk alerts."""
        alerts = []
        
        # Position size alert
        if position.risk_percentage > self.max_portfolio_risk:
            alerts.append({
                'type': AlertType.POSITION_SIZE,
                'symbol': position.symbol,
                'message': f"Position risk {position.risk_percentage:.1%} exceeds limit {self.max_portfolio_risk:.1%}",
                'severity': 'high',
                'timestamp': datetime.now()
            })
        
        # Volatility alert
        if position.volatility > 0.1:  # 10% volatility
            alerts.append({
                'type': AlertType.VOLATILITY,
                'symbol': position.symbol,
                'message': f"High volatility detected: {position.volatility:.1%}",
                'severity': 'medium',
                'timestamp': datetime.now()
            })
        
        # Add alerts and notify
        for alert in alerts:
            self.risk_alerts.append(alert)
            self.logger.warning(f"Risk Alert: {alert['message']}")
            
            # Notify callbacks
            for callback in self.alert_callbacks:
                try:
                    callback(alert)
                except Exception as e:
                    self.logger.error(f"Alert callback error: {e}")
    
    def _calculate_std(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)
    
    def get_educational_risk_summary(self) -> Dict[str, Any]:
        """Get risk summary formatted for educational purposes."""
        metrics = self.calculate_portfolio_risk()
        
        return {
            'educational_mode': self.educational_mode,
            'portfolio_health': 'Good' if metrics.risk_score < 30 else 'Caution' if metrics.risk_score < 60 else 'High Risk',
            'risk_score': f"{metrics.risk_score:.0f}/100",
            'total_positions': len(self.positions),
            'portfolio_exposure': f"{(metrics.total_exposure / metrics.portfolio_value):.1%}" if metrics.portfolio_value > 0 else "0%",
            'max_position_risk': f"{metrics.max_position_risk:.1%}",
            'drawdown': f"{metrics.max_drawdown:.1%}",
            'risk_limits': {
                'max_portfolio_risk': f"{self.max_portfolio_risk:.1%}",
                'max_position_size': f"{self.max_position_size:.1%}"
            },
            'recommendations': self._get_educational_recommendations(metrics)
        }
    
    def _get_educational_recommendations(self, metrics: RiskMetrics) -> List[str]:
        """Generate educational risk management recommendations."""
        recommendations = []
        
        if metrics.risk_score > 60:
            recommendations.append("Consider reducing position sizes")
            recommendations.append("Review stop-loss placement")
        
        if metrics.max_position_risk > self.max_portfolio_risk:
            recommendations.append("Largest position exceeds risk limits")
        
        if len(self.positions) > 5:
            recommendations.append("Consider portfolio diversification")
        
        if metrics.max_drawdown > 0.1:
            recommendations.append("Review risk management strategy")
        
        if not recommendations:
            recommendations.append("Risk profile looks healthy")
        
        return recommendations
