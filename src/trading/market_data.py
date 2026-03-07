"""
Real-Time Market Data Processing System

High-performance market data integration with support for multiple timeframes,
high-volatility assets, and educational mode preservation.
"""

import asyncio
import json
import logging
import threading
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from collections import deque


class DataSource(Enum):
    """Market data source types."""
    SIMULATED = "simulated"      # Educational simulation
    HISTORICAL = "historical"    # Historical data replay
    REAL_TIME = "real_time"     # Live market data
    HYBRID = "hybrid"           # Mix of real-time and simulated


class AssetType(Enum):
    """Asset classification for targeted trading."""
    CRYPTOCURRENCY = "crypto"
    MEME_COIN = "meme"
    NFT_TOKEN = "nft"
    NEW_LAUNCH = "new_launch"
    STABLECOIN = "stable"


@dataclass
class MarketTick:
    """Real-time market data tick."""
    symbol: str
    price: float
    volume: float
    timestamp: datetime
    bid: float = 0.0
    ask: float = 0.0
    spread: float = 0.0
    volatility: float = 0.0
    asset_type: AssetType = AssetType.CRYPTOCURRENCY
    

@dataclass
class OHLCV:
    """OHLCV candlestick data."""
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: datetime
    timeframe: str = "1m"


class RealTimeMarketData:
    """
    Real-time market data processing system with multi-timeframe analysis.
    
    Supports high-volatility assets, pattern recognition, and educational mode.
    """
    
    def __init__(self, 
                 data_source: DataSource = DataSource.SIMULATED,
                 educational_mode: bool = True):
        """Initialize market data system."""
        self.data_source = data_source
        self.educational_mode = educational_mode
        self.logger = logging.getLogger(__name__)
        
        # Data storage
        self.current_prices: Dict[str, MarketTick] = {}
        self.price_history: Dict[str, deque] = {}
        self.ohlcv_data: Dict[str, Dict[str, deque]] = {}  # symbol -> timeframe -> data
        
        # Supported timeframes for multi-timeframe analysis
        self.timeframes = ["1m", "5m", "15m", "1h", "4h", "1d"]
        
        # High-volatility asset tracking
        self.high_volatility_assets = set()
        self.volatility_threshold = 0.05  # 5% volatility threshold
        
        # Event callbacks
        self.price_callbacks: List[Callable[[MarketTick], None]] = []
        self.volatility_callbacks: List[Callable[[str, float], None]] = []
        
        # Data streaming
        self.streaming = False
        self.stream_thread = None
        
        # Pattern recognition data
        self.pattern_buffer = {}
        self.trajectory_log = []
        
        self.logger.info(f"Market Data initialized - Source: {data_source.value}, Educational: {educational_mode}")
    
    def start_streaming(self, symbols: List[str]) -> bool:
        """Start real-time data streaming for specified symbols."""
        try:
            if self.streaming:
                self.logger.warning("Data streaming already active")
                return True
            
            # Initialize data structures
            for symbol in symbols:
                self.price_history[symbol] = deque(maxlen=1000)
                self.ohlcv_data[symbol] = {}
                for timeframe in self.timeframes:
                    self.ohlcv_data[symbol][timeframe] = deque(maxlen=500)
            
            # Start streaming based on data source
            if self.data_source == DataSource.SIMULATED or self.educational_mode:
                self.stream_thread = threading.Thread(
                    target=self._simulate_market_data, 
                    args=(symbols,),
                    daemon=True
                )
            else:
                self.stream_thread = threading.Thread(
                    target=self._stream_real_data,
                    args=(symbols,),
                    daemon=True
                )
            
            self.streaming = True
            self.stream_thread.start()
            
            self.logger.info(f"Started streaming data for {len(symbols)} symbols")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start data streaming: {e}")
            return False
    
    def stop_streaming(self) -> bool:
        """Stop data streaming."""
        try:
            self.streaming = False
            if self.stream_thread and self.stream_thread.is_alive():
                self.stream_thread.join(timeout=5.0)
            
            self.logger.info("Data streaming stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping data streaming: {e}")
            return False
    
    def get_current_price(self, symbol: str) -> Optional[MarketTick]:
        """Get current price for a symbol."""
        return self.current_prices.get(symbol)
    
    def get_price_history(self, symbol: str, periods: int = 100) -> List[MarketTick]:
        """Get price history for a symbol."""
        if symbol not in self.price_history:
            return []
        return list(self.price_history[symbol])[-periods:]
    
    def get_ohlcv(self, symbol: str, timeframe: str, periods: int = 100) -> List[OHLCV]:
        """Get OHLCV data for multi-timeframe analysis."""
        if symbol not in self.ohlcv_data or timeframe not in self.ohlcv_data[symbol]:
            return []
        return list(self.ohlcv_data[symbol][timeframe])[-periods:]
    
    def get_high_volatility_assets(self) -> List[str]:
        """Get list of currently high-volatility assets."""
        return list(self.high_volatility_assets)
    
    def register_price_callback(self, callback: Callable[[MarketTick], None]) -> None:
        """Register callback for price updates."""
        self.price_callbacks.append(callback)
    
    def register_volatility_callback(self, callback: Callable[[str, float], None]) -> None:
        """Register callback for volatility alerts."""
        self.volatility_callbacks.append(callback)
    
    def _simulate_market_data(self, symbols: List[str]) -> None:
        """Simulate market data for educational/testing purposes."""
        import random
        
        # Initialize base prices
        base_prices = {
            "BTC": 45000.0,
            "ETH": 3000.0,
            "SOL": 100.0,
            "DOGE": 0.08,  # Meme coin
            "SHIB": 0.000025,  # Meme coin
            "PEPE": 0.000001,  # Meme coin
        }
        
        # Asset type mapping
        asset_types = {
            "BTC": AssetType.CRYPTOCURRENCY,
            "ETH": AssetType.CRYPTOCURRENCY, 
            "SOL": AssetType.CRYPTOCURRENCY,
            "DOGE": AssetType.MEME_COIN,
            "SHIB": AssetType.MEME_COIN,
            "PEPE": AssetType.MEME_COIN,
        }
        
        while self.streaming:
            try:
                for symbol in symbols:
                    if symbol not in base_prices:
                        base_prices[symbol] = 100.0  # Default price for new assets
                    
                    # Simulate price movement with higher volatility for meme coins
                    asset_type = asset_types.get(symbol, AssetType.CRYPTOCURRENCY)
                    
                    # Volatility is per simulation tick (1 second).
                    # Real intra-second volatility for even meme coins is tiny.
                    # These values approximate realistic per-second ranges:
                    #   BTC/ETH: ~0.01–0.05% per second in normal conditions
                    #   Meme coins: 2–5× that, but still not ±15%/second
                    # ±15%/second was unrealistic and caused constant false alerts.
                    if asset_type == AssetType.MEME_COIN:
                        # Elevated but realistic intra-second simulation
                        change_pct = random.gauss(0, 0.002)  # ~0.2% std per tick
                        change_pct = max(-0.05, min(0.05, change_pct))  # cap at ±5%
                    elif asset_type == AssetType.NEW_LAUNCH:
                        # Higher volatility for new/micro-cap launches
                        change_pct = random.gauss(0, 0.004)  # ~0.4% std per tick
                        change_pct = max(-0.10, min(0.10, change_pct))  # cap at ±10%
                    else:
                        # Major cryptocurrencies: lower intra-second movement
                        change_pct = random.gauss(0, 0.0005)  # ~0.05% std per tick
                        change_pct = max(-0.02, min(0.02, change_pct))  # cap at ±2%
                    
                    new_price = base_prices[symbol] * (1 + change_pct)
                    base_prices[symbol] = new_price
                    
                    # Create market tick
                    tick = MarketTick(
                        symbol=symbol,
                        price=new_price,
                        volume=random.uniform(1000, 50000),
                        timestamp=datetime.now(),
                        bid=new_price * 0.999,
                        ask=new_price * 1.001,
                        spread=new_price * 0.002,
                        volatility=abs(change_pct),
                        asset_type=asset_type
                    )
                    
                    # Update current price
                    self.current_prices[symbol] = tick
                    
                    # Add to price history
                    self.price_history[symbol].append(tick)
                    
                    # Check for high volatility
                    if tick.volatility > self.volatility_threshold:
                        self.high_volatility_assets.add(symbol)
                        # Notify volatility callbacks
                        for callback in self.volatility_callbacks:
                            try:
                                callback(symbol, tick.volatility)
                            except Exception as e:
                                self.logger.error(f"Volatility callback error: {e}")
                    else:
                        self.high_volatility_assets.discard(symbol)
                    
                    # Notify price callbacks
                    for callback in self.price_callbacks:
                        try:
                            callback(tick)
                        except Exception as e:
                            self.logger.error(f"Price callback error: {e}")
                    
                    # Update trajectory log for pattern recognition
                    self.trajectory_log.append({
                        'symbol': symbol,
                        'price': new_price,
                        'timestamp': datetime.now(),
                        'volatility': tick.volatility,
                        'asset_type': asset_type.value
                    })
                    
                    # Keep trajectory log size manageable
                    if len(self.trajectory_log) > 10000:
                        self.trajectory_log = self.trajectory_log[-5000:]
                
                # Sleep between updates (1 second for simulation)
                time.sleep(1.0)
                
            except Exception as e:
                self.logger.error(f"Error in market data simulation: {e}")
                time.sleep(1.0)
    
    def _stream_real_data(self, symbols: List[str]) -> None:
        """Stream real market data (placeholder for actual implementation)."""
        self.logger.warning("Real-time data streaming not implemented - using simulation")
        # In a real implementation, this would connect to actual market data feeds
        # For now, fall back to simulation
        self._simulate_market_data(symbols)
    
    def get_market_overview(self) -> Dict[str, Any]:
        """Get comprehensive market overview."""
        total_symbols = len(self.current_prices)
        high_vol_count = len(self.high_volatility_assets)
        
        # Calculate average volatility
        if self.current_prices:
            avg_volatility = sum(tick.volatility for tick in self.current_prices.values()) / len(self.current_prices)
        else:
            avg_volatility = 0.0
        
        return {
            'total_symbols': total_symbols,
            'high_volatility_assets': high_vol_count,
            'average_volatility': avg_volatility,
            'data_source': self.data_source.value,
            'educational_mode': self.educational_mode,
            'streaming': self.streaming,
            'supported_timeframes': self.timeframes
        }
    
    def get_trajectory_data(self, symbol: str = None, hours: int = 24) -> List[Dict[str, Any]]:
        """Get trajectory data for pattern recognition."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        filtered_data = [
            entry for entry in self.trajectory_log
            if entry['timestamp'] > cutoff_time
        ]
        
        if symbol:
            filtered_data = [
                entry for entry in filtered_data 
                if entry['symbol'] == symbol
            ]
        
        return filtered_data
