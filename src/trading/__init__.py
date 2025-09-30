"""
Automated Trading System Module

This module provides automated trading capabilities while preserving
educational features for learning purposes.
"""

from .automated_engine import AutomatedTradingEngine, TradingMode, TradingConfig
from .market_data import RealTimeMarketData, DataSource, MarketTick
from .risk_manager import RiskManager, RiskMetrics, PositionRisk
from .strategy_engine import StrategyEngine, TradingSignal, StrategyConfig

__all__ = [
    'AutomatedTradingEngine',
    'TradingMode', 
    'TradingConfig',
    'RealTimeMarketData',
    'DataSource',
    'MarketTick', 
    'RiskManager',
    'RiskMetrics',
    'PositionRisk',
    'StrategyEngine',
    'TradingSignal',
    'StrategyConfig'
]
