"""
Strategy Execution Engine

Advanced strategy management system for automated trading with pattern recognition,
multi-timeframe analysis, and educational preservation.
"""

import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import json


class StrategyType(Enum):
    """Types of trading strategies."""
    TREND_FOLLOWING = "trend_following"
    MEAN_REVERSION = "mean_reversion"
    MOMENTUM = "momentum"
    BREAKOUT = "breakout"
    ARBITRAGE = "arbitrage"
    SCALPING = "scalping"
    SWING = "swing"
    EDUCATIONAL = "educational"


class SignalStrength(Enum):
    """Signal strength classifications."""
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


class PatternType(Enum):
    """Recognized chart patterns."""
    ASCENDING_TRIANGLE = "ascending_triangle"
    DESCENDING_TRIANGLE = "descending_triangle"
    HEAD_SHOULDERS = "head_shoulders"
    DOUBLE_TOP = "double_top"
    DOUBLE_BOTTOM = "double_bottom"
    FLAG = "flag"
    PENNANT = "pennant"
    WEDGE = "wedge"
    SUPPORT_RESISTANCE = "support_resistance"


@dataclass
class TradingSignal:
    """Trading signal with strength and reasoning."""
    symbol: str
    strategy: str
    signal_type: str  # "buy", "sell", "hold"
    strength: SignalStrength
    confidence: float  # 0.0 to 1.0
    entry_price: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    reasoning: str = ""
    timeframe: str = "1h"
    timestamp: datetime = field(default_factory=datetime.now)
    pattern: Optional[PatternType] = None


@dataclass
class StrategyConfig:
    """Configuration for trading strategies."""
    name: str
    strategy_type: StrategyType
    enabled: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)
    timeframes: List[str] = field(default_factory=lambda: ["1h", "4h"])
    target_assets: List[str] = field(default_factory=list)
    risk_per_trade: float = 0.01  # 1% risk per trade
    max_positions: int = 3


class StrategyEngine:
    """
    Advanced strategy execution engine with pattern recognition.
    
    Supports multiple strategies, timeframes, and educational mode preservation.
    """
    
    def __init__(self, educational_mode: bool = True):
        """Initialize strategy engine."""
        self.educational_mode = educational_mode
        self.logger = logging.getLogger(__name__)
        
        # Strategy management
        self.strategies: Dict[str, StrategyConfig] = {}
        self.active_signals: List[TradingSignal] = []
        self.signal_history: List[TradingSignal] = []
        
        # Pattern recognition
        self.pattern_cache: Dict[str, List[PatternType]] = {}
        self.pattern_callbacks: List[Callable] = []
        
        # Performance tracking
        self.strategy_performance: Dict[str, Dict[str, Any]] = {}
        
        # Multi-timeframe analysis
        self.timeframe_weights = {
            "1m": 0.1,
            "5m": 0.15,
            "15m": 0.2,
            "1h": 0.25,
            "4h": 0.3,
            "1d": 0.4
        }
        
        # Initialize default strategies
        self._initialize_default_strategies()
        
        self.logger.info(f"Strategy Engine initialized - Educational: {educational_mode}")
    
    def register_strategy(self, config: StrategyConfig) -> bool:
        """Register a new trading strategy."""
        try:
            # Validate strategy configuration
            if not self._validate_strategy_config(config):
                return False
            
            self.strategies[config.name] = config
            
            # Initialize performance tracking
            self.strategy_performance[config.name] = {
                'signals_generated': 0,
                'successful_signals': 0,
                'total_pnl': 0.0,
                'win_rate': 0.0,
                'avg_hold_time': 0.0,
                'enabled': config.enabled
            }
            
            self.logger.info(f"Strategy registered: {config.name} ({config.strategy_type.value})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error registering strategy {config.name}: {e}")
            return False
    
    def generate_signals(self, market_data: Dict[str, Any]) -> List[TradingSignal]:
        """Generate trading signals based on market data and strategies."""
        signals = []
        
        try:
            for strategy_name, strategy in self.strategies.items():
                if not strategy.enabled:
                    continue
                
                # Generate signals for each target asset
                for symbol in strategy.target_assets:
                    if symbol not in market_data:
                        continue
                    
                    # Multi-timeframe analysis
                    timeframe_signals = []
                    for timeframe in strategy.timeframes:
                        signal = self._analyze_timeframe(
                            symbol, timeframe, strategy, market_data[symbol]
                        )
                        if signal:
                            timeframe_signals.append(signal)
                    
                    # Combine timeframe signals
                    combined_signal = self._combine_timeframe_signals(
                        timeframe_signals, symbol, strategy_name
                    )
                    
                    if combined_signal:
                        signals.append(combined_signal)
                        
                        # Update performance tracking
                        self.strategy_performance[strategy_name]['signals_generated'] += 1
            
            # Filter and rank signals
            signals = self._filter_signals(signals)
            
            # Store active signals
            self.active_signals = signals
            
            # Add to history
            self.signal_history.extend(signals)
            if len(self.signal_history) > 1000:
                self.signal_history = self.signal_history[-500:]
            
            self.logger.info(f"Generated {len(signals)} trading signals")
            return signals
            
        except Exception as e:
            self.logger.error(f"Error generating signals: {e}")
            return []
    
    def recognize_patterns(self, symbol: str, price_data: List[Dict[str, Any]]) -> List[PatternType]:
        """Recognize chart patterns for enhanced signal generation."""
        patterns = []
        
        try:
            if len(price_data) < 20:  # Need minimum data points
                return patterns
            
            # Extract price arrays
            highs = [d['high'] for d in price_data[-20:]]
            lows = [d['low'] for d in price_data[-20:]]
            closes = [d['close'] for d in price_data[-20:]]
            
            # Simple pattern recognition (can be expanded)
            patterns.extend(self._detect_triangle_patterns(highs, lows))
            patterns.extend(self._detect_double_patterns(highs, lows))
            patterns.extend(self._detect_support_resistance(closes))
            
            # Cache patterns
            self.pattern_cache[symbol] = patterns
            
            # Notify pattern callbacks
            for pattern in patterns:
                for callback in self.pattern_callbacks:
                    try:
                        callback(symbol, pattern)
                    except Exception as e:
                        self.logger.error(f"Pattern callback error: {e}")
            
            return patterns
            
        except Exception as e:
            self.logger.error(f"Error recognizing patterns for {symbol}: {e}")
            return []
    
    def get_strategy_performance(self, strategy_name: str = None) -> Dict[str, Any]:
        """Get performance metrics for strategies."""
        if strategy_name:
            return self.strategy_performance.get(strategy_name, {})
        return self.strategy_performance.copy()
    
    def enable_strategy(self, strategy_name: str) -> bool:
        """Enable a strategy."""
        if strategy_name in self.strategies:
            self.strategies[strategy_name].enabled = True
            self.strategy_performance[strategy_name]['enabled'] = True
            self.logger.info(f"Strategy enabled: {strategy_name}")
            return True
        return False
    
    def disable_strategy(self, strategy_name: str) -> bool:
        """Disable a strategy."""
        if strategy_name in self.strategies:
            self.strategies[strategy_name].enabled = False
            self.strategy_performance[strategy_name]['enabled'] = False
            self.logger.info(f"Strategy disabled: {strategy_name}")
            return True
        return False
    
    def register_pattern_callback(self, callback: Callable) -> None:
        """Register callback for pattern recognition."""
        self.pattern_callbacks.append(callback)
    
    def _initialize_default_strategies(self) -> None:
        """Initialize default trading strategies."""
        # Trend following strategy
        trend_config = StrategyConfig(
            name="trend_following",
            strategy_type=StrategyType.TREND_FOLLOWING,
            parameters={
                "ma_fast": 10,
                "ma_slow": 20,
                "rsi_period": 14,
                "rsi_overbought": 70,
                "rsi_oversold": 30
            },
            timeframes=["1h", "4h"],
            target_assets=["BTC", "ETH", "SOL"],
            risk_per_trade=0.01 if self.educational_mode else 0.02
        )
        self.register_strategy(trend_config)
        
        # Momentum strategy for high-volatility assets
        momentum_config = StrategyConfig(
            name="momentum_scalping",
            strategy_type=StrategyType.MOMENTUM,
            parameters={
                "volume_threshold": 1.5,
                "price_change_threshold": 0.03,
                "volatility_threshold": 0.05
            },
            timeframes=["5m", "15m"],
            target_assets=["DOGE", "SHIB", "PEPE"],  # Meme coins
            risk_per_trade=0.005 if self.educational_mode else 0.015,
            max_positions=2
        )
        self.register_strategy(momentum_config)
        
        # Educational strategy
        if self.educational_mode:
            educational_config = StrategyConfig(
                name="educational_conservative",
                strategy_type=StrategyType.EDUCATIONAL,
                parameters={
                    "conservative_entry": True,
                    "wide_stops": True,
                    "educational_explanations": True
                },
                timeframes=["1h", "4h"],
                target_assets=["BTC", "ETH"],
                risk_per_trade=0.005,  # 0.5% risk
                max_positions=2
            )
            self.register_strategy(educational_config)
    
    def _analyze_timeframe(self, symbol: str, timeframe: str, 
                          strategy: StrategyConfig, data: Dict[str, Any]) -> Optional[TradingSignal]:
        """Analyze a specific timeframe for trading signals."""
        try:
            # Get timeframe-specific data
            ohlcv_data = data.get('ohlcv', {}).get(timeframe, [])
            if len(ohlcv_data) < 20:
                return None
            
            # Strategy-specific analysis
            if strategy.strategy_type == StrategyType.TREND_FOLLOWING:
                return self._analyze_trend_following(symbol, timeframe, strategy, ohlcv_data)
            elif strategy.strategy_type == StrategyType.MOMENTUM:
                return self._analyze_momentum(symbol, timeframe, strategy, ohlcv_data)
            elif strategy.strategy_type == StrategyType.EDUCATIONAL:
                return self._analyze_educational(symbol, timeframe, strategy, ohlcv_data)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error analyzing {symbol} on {timeframe}: {e}")
            return None
    
    def _analyze_trend_following(self, symbol: str, timeframe: str, 
                                strategy: StrategyConfig, data: List[Dict]) -> Optional[TradingSignal]:
        """Analyze trend following signals."""
        if len(data) < 20:
            return None
        
        # Simple moving average crossover
        closes = [d['close'] for d in data]
        ma_fast = sum(closes[-strategy.parameters['ma_fast']:]) / strategy.parameters['ma_fast']
        ma_slow = sum(closes[-strategy.parameters['ma_slow']:]) / strategy.parameters['ma_slow']
        
        current_price = closes[-1]
        
        # Generate signal
        if ma_fast > ma_slow and closes[-1] > ma_fast:
            # Bullish signal
            return TradingSignal(
                symbol=symbol,
                strategy=strategy.name,
                signal_type="buy",
                strength=SignalStrength.MODERATE,
                confidence=0.7,
                entry_price=current_price,
                stop_loss=current_price * 0.97,  # 3% stop loss
                take_profit=current_price * 1.06,  # 6% take profit
                reasoning=f"MA crossover bullish: {ma_fast:.2f} > {ma_slow:.2f}",
                timeframe=timeframe
            )
        elif ma_fast < ma_slow and closes[-1] < ma_fast:
            # Bearish signal (for short positions)
            return TradingSignal(
                symbol=symbol,
                strategy=strategy.name,
                signal_type="sell",
                strength=SignalStrength.MODERATE,
                confidence=0.7,
                entry_price=current_price,
                stop_loss=current_price * 1.03,  # 3% stop loss for short
                take_profit=current_price * 0.94,  # 6% take profit for short
                reasoning=f"MA crossover bearish: {ma_fast:.2f} < {ma_slow:.2f}",
                timeframe=timeframe
            )
        
        return None
    
    def _analyze_momentum(self, symbol: str, timeframe: str,
                         strategy: StrategyConfig, data: List[Dict]) -> Optional[TradingSignal]:
        """Analyze momentum signals for high-volatility assets."""
        if len(data) < 10:
            return None
        
        # Calculate price change and volume
        current_price = data[-1]['close']
        prev_price = data[-2]['close']
        price_change = (current_price - prev_price) / prev_price
        
        current_volume = data[-1]['volume']
        avg_volume = sum(d['volume'] for d in data[-10:]) / 10
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        
        # Momentum signal conditions
        volume_threshold = strategy.parameters['volume_threshold']
        price_threshold = strategy.parameters['price_change_threshold']
        
        if (abs(price_change) > price_threshold and 
            volume_ratio > volume_threshold):
            
            signal_type = "buy" if price_change > 0 else "sell"
            strength = SignalStrength.STRONG if abs(price_change) > price_threshold * 2 else SignalStrength.MODERATE
            
            return TradingSignal(
                symbol=symbol,
                strategy=strategy.name,
                signal_type=signal_type,
                strength=strength,
                confidence=0.8,
                entry_price=current_price,
                stop_loss=current_price * (0.98 if signal_type == "buy" else 1.02),
                take_profit=current_price * (1.04 if signal_type == "buy" else 0.96),
                reasoning=f"Momentum: {price_change:.1%} price, {volume_ratio:.1f}x volume",
                timeframe=timeframe
            )
        
        return None
    
    def _analyze_educational(self, symbol: str, timeframe: str,
                           strategy: StrategyConfig, data: List[Dict]) -> Optional[TradingSignal]:
        """Analyze educational signals with explanations."""
        if len(data) < 15:
            return None
        
        # Conservative trend analysis
        closes = [d['close'] for d in data]
        current_price = closes[-1]
        
        # Simple trend detection
        ma_10 = sum(closes[-10:]) / 10
        ma_15 = sum(closes[-15:]) / 15
        
        if ma_10 > ma_15 * 1.02:  # 2% above longer MA
            return TradingSignal(
                symbol=symbol,
                strategy=strategy.name,
                signal_type="buy",
                strength=SignalStrength.WEAK,
                confidence=0.6,
                entry_price=current_price,
                stop_loss=current_price * 0.95,  # 5% stop loss (conservative)
                take_profit=current_price * 1.1,   # 10% take profit
                reasoning="Educational: Conservative uptrend detected. Good for learning trend following.",
                timeframe=timeframe
            )
        
        return None
    
    def _combine_timeframe_signals(self, signals: List[TradingSignal], 
                                  symbol: str, strategy_name: str) -> Optional[TradingSignal]:
        """Combine signals from multiple timeframes."""
        if not signals:
            return None
        
        # Weight signals by timeframe importance
        total_weight = 0
        weighted_confidence = 0
        signal_types = []
        
        for signal in signals:
            weight = self.timeframe_weights.get(signal.timeframe, 0.2)
            total_weight += weight
            weighted_confidence += signal.confidence * weight
            signal_types.append(signal.signal_type)
        
        if total_weight == 0:
            return None
        
        avg_confidence = weighted_confidence / total_weight
        
        # Determine consensus signal
        buy_count = signal_types.count("buy")
        sell_count = signal_types.count("sell")
        
        if buy_count > sell_count:
            consensus_signal = "buy"
        elif sell_count > buy_count:
            consensus_signal = "sell"
        else:
            return None  # No consensus
        
        # Create combined signal (use data from strongest signal)
        strongest_signal = max(signals, key=lambda s: s.confidence)
        
        return TradingSignal(
            symbol=symbol,
            strategy=strategy_name,
            signal_type=consensus_signal,
            strength=SignalStrength.STRONG if avg_confidence > 0.8 else SignalStrength.MODERATE,
            confidence=avg_confidence,
            entry_price=strongest_signal.entry_price,
            stop_loss=strongest_signal.stop_loss,
            take_profit=strongest_signal.take_profit,
            reasoning=f"Multi-timeframe consensus ({buy_count}B/{sell_count}S): {strongest_signal.reasoning}",
            timeframe="combined"
        )
    
    def _filter_signals(self, signals: List[TradingSignal]) -> List[TradingSignal]:
        """Filter and rank signals by quality."""
        # Filter by confidence threshold
        min_confidence = 0.6 if self.educational_mode else 0.5
        filtered = [s for s in signals if s.confidence >= min_confidence]
        
        # Sort by confidence and strength
        strength_order = {
            SignalStrength.VERY_STRONG: 4,
            SignalStrength.STRONG: 3,
            SignalStrength.MODERATE: 2,
            SignalStrength.WEAK: 1
        }
        
        filtered.sort(
            key=lambda s: (strength_order.get(s.strength, 0), s.confidence),
            reverse=True
        )
        
        # Limit number of signals
        max_signals = 5 if self.educational_mode else 10
        return filtered[:max_signals]
    
    def _validate_strategy_config(self, config: StrategyConfig) -> bool:
        """Validate strategy configuration."""
        if not config.name or not config.strategy_type:
            return False
        
        if config.risk_per_trade > 0.05:  # Max 5% risk
            self.logger.error(f"Risk per trade too high: {config.risk_per_trade}")
            return False
        
        if self.educational_mode and config.risk_per_trade > 0.01:
            self.logger.warning(f"Reducing risk for educational mode: {config.name}")
            config.risk_per_trade = 0.01
        
        return True
    
    def _detect_triangle_patterns(self, highs: List[float], lows: List[float]) -> List[PatternType]:
        """Detect triangle patterns (simplified)."""
        patterns = []
        
        if len(highs) < 10:
            return patterns
        
        # Simple ascending triangle detection
        recent_highs = highs[-5:]
        recent_lows = lows[-5:]
        
        # Check if highs are relatively flat and lows are ascending
        high_range = max(recent_highs) - min(recent_highs)
        low_trend = recent_lows[-1] - recent_lows[0]
        
        if high_range < (max(recent_highs) * 0.02) and low_trend > 0:
            patterns.append(PatternType.ASCENDING_TRIANGLE)
        
        return patterns
    
    def _detect_double_patterns(self, highs: List[float], lows: List[float]) -> List[PatternType]:
        """Detect double top/bottom patterns (simplified)."""
        patterns = []
        
        if len(highs) < 15:
            return patterns
        
        # Simple double top detection
        recent_highs = highs[-10:]
        max_high = max(recent_highs)
        
        # Look for two similar peaks
        peaks = [i for i, h in enumerate(recent_highs) if h > max_high * 0.98]
        if len(peaks) >= 2 and peaks[-1] - peaks[0] > 3:
            patterns.append(PatternType.DOUBLE_TOP)
        
        return patterns
    
    def _detect_support_resistance(self, closes: List[float]) -> List[PatternType]:
        """Detect support/resistance levels (simplified)."""
        patterns = []
        
        if len(closes) < 10:
            return patterns
        
        # Check for price touching similar levels multiple times
        current_price = closes[-1]
        price_levels = {}
        
        for price in closes[-10:]:
            # Group prices into levels (1% tolerance)
            level = round(price / (current_price * 0.01)) * (current_price * 0.01)
            price_levels[level] = price_levels.get(level, 0) + 1
        
        # Find levels with multiple touches
        for level, count in price_levels.items():
            if count >= 3:  # Price touched this level 3+ times
                patterns.append(PatternType.SUPPORT_RESISTANCE)
                break
        
        return patterns
