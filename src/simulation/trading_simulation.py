"""
Educational Crypto Trading Simulation System

This module provides a safe paper trading environment for educational purposes only.
No real money or actual trading is involved.
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import json


class OrderType(Enum):
    """Types of orders for educational simulation."""
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    STOP_LIMIT = "stop_limit"


class OrderStatus(Enum):
    """Order status for tracking."""
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    PARTIALLY_FILLED = "partially_filled"


class MarketCondition(Enum):
    """Market conditions for educational scenarios."""
    BULL = "bull_market"
    BEAR = "bear_market"
    SIDEWAYS = "sideways"
    VOLATILE = "high_volatility"


@dataclass
class SimulatedAsset:
    """Represents a cryptocurrency for educational simulation."""
    symbol: str
    name: str
    current_price: float
    price_history: List[Tuple[datetime, float]] = field(default_factory=list)
    volatility: float = 0.02  # Daily volatility for simulation
    
    def update_price(self, market_condition: MarketCondition = MarketCondition.SIDEWAYS) -> float:
        """
        Update asset price based on market conditions.
        This is purely for educational simulation.
        """
        # Base random movement
        random_factor = random.normalvariate(0, self.volatility)
        
        # Apply market condition bias
        condition_bias = {
            MarketCondition.BULL: 0.001,     # Slight upward bias
            MarketCondition.BEAR: -0.001,    # Slight downward bias
            MarketCondition.SIDEWAYS: 0,     # No bias
            MarketCondition.VOLATILE: 0      # No bias but higher volatility
        }
        
        # Increase volatility for volatile market
        if market_condition == MarketCondition.VOLATILE:
            random_factor *= 2
        
        # Calculate new price
        price_change = self.current_price * (random_factor + condition_bias[market_condition])
        new_price = max(0.01, self.current_price + price_change)  # Prevent negative prices
        
        # Update price and history
        self.current_price = new_price
        self.price_history.append((datetime.now(), new_price))
        
        # Keep only last 1000 price points
        if len(self.price_history) > 1000:
            self.price_history = self.price_history[-1000:]
        
        return new_price


@dataclass
class Order:
    """Represents a trading order for educational simulation."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str = ""
    order_type: OrderType = OrderType.MARKET
    side: str = "buy"  # "buy" or "sell"
    quantity: float = 0
    price: Optional[float] = None
    stop_price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: float = 0
    filled_price: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
    filled_timestamp: Optional[datetime] = None


@dataclass
class Position:
    """Represents a position in a cryptocurrency."""
    symbol: str
    quantity: float
    average_price: float
    current_price: float = 0
    unrealized_pnl: float = 0
    
    def update_current_price(self, new_price: float) -> None:
        """Update current price and calculate unrealized P&L."""
        self.current_price = new_price
        self.unrealized_pnl = (new_price - self.average_price) * self.quantity


class EducationalPortfolio:
    """
    Educational portfolio for safe trading simulation.
    No real money involved - purely for learning.
    """
    
    def __init__(self, initial_balance: float = 10000.0):
        """Initialize with virtual funds for education."""
        self.initial_balance = initial_balance
        self.cash_balance = initial_balance
        self.positions: Dict[str, Position] = {}
        self.orders: List[Order] = []
        self.trade_history: List[Dict[str, Any]] = []
        self.performance_history: List[Dict[str, Any]] = []
        
        # Risk management limits (educational)
        self.max_position_size = 0.1  # 10% of portfolio
        self.max_daily_loss = 0.05    # 5% of portfolio
        self.daily_start_value = initial_balance
        
    def get_portfolio_value(self, asset_prices: Dict[str, float]) -> float:
        """Calculate total portfolio value."""
        total_value = self.cash_balance
        
        for symbol, position in self.positions.items():
            if symbol in asset_prices:
                position.update_current_price(asset_prices[symbol])
                total_value += position.quantity * asset_prices[symbol]
        
        return total_value
    
    def check_risk_limits(self, asset_prices: Dict[str, float]) -> List[str]:
        """Check if risk limits are exceeded (educational safety feature)."""
        warnings = []
        current_value = self.get_portfolio_value(asset_prices)
        
        # Check daily loss limit
        daily_loss = (self.daily_start_value - current_value) / self.daily_start_value
        if daily_loss > self.max_daily_loss:
            warnings.append(f"Daily loss limit exceeded: {daily_loss:.2%}")
        
        # Check individual position sizes
        for symbol, position in self.positions.items():
            if symbol in asset_prices:
                position_value = position.quantity * asset_prices[symbol]
                position_weight = position_value / current_value
                if position_weight > self.max_position_size:
                    warnings.append(f"Position size limit exceeded for {symbol}: {position_weight:.2%}")
        
        return warnings
    
    def place_order(self, order: Order) -> bool:
        """Place an order (educational simulation)."""
        # Add educational validation
        if order.quantity <= 0:
            return False
        
        # Check if we have enough cash for buy orders
        if order.side == "buy" and order.order_type == OrderType.MARKET:
            estimated_cost = order.quantity * 50000  # Rough estimate, will be updated
            if estimated_cost > self.cash_balance:
                return False
        
        # Check if we have enough quantity for sell orders
        if order.side == "sell":
            if order.symbol not in self.positions:
                return False
            if self.positions[order.symbol].quantity < order.quantity:
                return False
        
        self.orders.append(order)
        return True
    
    def execute_market_order(self, order: Order, current_price: float) -> bool:
        """Execute a market order at current price."""
        if order.status != OrderStatus.PENDING:
            return False
        
        # Simulate slippage (educational purpose)
        slippage = random.uniform(-0.001, 0.001)  # 0.1% slippage
        execution_price = current_price * (1 + slippage)
        
        # Calculate trade value
        trade_value = order.quantity * execution_price
        
        if order.side == "buy":
            # Check if we have enough cash
            if trade_value > self.cash_balance:
                order.status = OrderStatus.CANCELLED
                return False
            
            # Execute buy order
            self.cash_balance -= trade_value
            
            if order.symbol in self.positions:
                # Update existing position
                pos = self.positions[order.symbol]
                total_cost = (pos.quantity * pos.average_price) + trade_value
                total_quantity = pos.quantity + order.quantity
                pos.average_price = total_cost / total_quantity
                pos.quantity = total_quantity
            else:
                # Create new position
                self.positions[order.symbol] = Position(
                    symbol=order.symbol,
                    quantity=order.quantity,
                    average_price=execution_price
                )
        
        else:  # sell order
            # Check if we have enough quantity
            if order.symbol not in self.positions or self.positions[order.symbol].quantity < order.quantity:
                order.status = OrderStatus.CANCELLED
                return False
            
            # Execute sell order
            self.cash_balance += trade_value
            self.positions[order.symbol].quantity -= order.quantity
            
            # Remove position if quantity is zero
            if self.positions[order.symbol].quantity == 0:
                del self.positions[order.symbol]
        
        # Update order status
        order.status = OrderStatus.FILLED
        order.filled_quantity = order.quantity
        order.filled_price = execution_price
        order.filled_timestamp = datetime.now()
        
        # Record trade for educational analysis
        self.trade_history.append({
            "timestamp": order.filled_timestamp,
            "symbol": order.symbol,
            "side": order.side,
            "quantity": order.quantity,
            "price": execution_price,
            "value": trade_value
        })
        
        return True


class EducationalMarketSimulator:
    """
    Market simulator for educational trading practice.
    Generates realistic market data for learning purposes.
    """
    
    def __init__(self):
        """Initialize the educational market simulator."""
        self.assets: Dict[str, SimulatedAsset] = {}
        self.market_condition = MarketCondition.SIDEWAYS
        self.simulation_speed = 1.0  # 1.0 = real time, higher = faster
        
        # Initialize common cryptocurrencies for education
        self._initialize_educational_assets()
    
    def _initialize_educational_assets(self) -> None:
        """Initialize simulated cryptocurrency assets for education."""
        initial_prices = {
            "BTC": 45000.0,  # Bitcoin
            "ETH": 3000.0,   # Ethereum
            "LTC": 150.0,    # Litecoin
            "ADA": 0.50,     # Cardano (educational example)
            "DOT": 25.0,     # Polkadot (educational example)
        }
        
        for symbol, price in initial_prices.items():
            self.assets[symbol] = SimulatedAsset(
                symbol=symbol,
                name=f"{symbol} (Educational Simulation)",
                current_price=price,
                volatility=random.uniform(0.015, 0.03)  # 1.5% to 3% daily volatility
            )
    
    def set_market_condition(self, condition: MarketCondition) -> None:
        """Set market condition for educational scenarios."""
        self.market_condition = condition
        print(f"Market condition set to: {condition.value}")
    
    def update_all_prices(self) -> Dict[str, float]:
        """Update all asset prices based on current market condition."""
        current_prices = {}
        
        for symbol, asset in self.assets.items():
            new_price = asset.update_price(self.market_condition)
            current_prices[symbol] = new_price
        
        return current_prices
    
    def get_current_prices(self) -> Dict[str, float]:
        """Get current prices for all assets."""
        return {symbol: asset.current_price for symbol, asset in self.assets.items()}
    
    def get_price_history(self, symbol: str, periods: int = 100) -> List[Tuple[datetime, float]]:
        """Get price history for technical analysis education."""
        if symbol in self.assets:
            return self.assets[symbol].price_history[-periods:]
        return []


class EducationalTradingSystem:
    """
    Complete educational trading system combining portfolio and market simulation.
    For learning purposes only - no real trading capabilities.
    """
    
    def __init__(self, initial_balance: float = 10000.0):
        """Initialize the educational trading system."""
        self.portfolio = EducationalPortfolio(initial_balance)
        self.market = EducationalMarketSimulator()
        self.running = False
        
        # Educational features
        self.learning_objectives = []
        self.performance_analytics = {}
        
    def start_simulation(self) -> None:
        """Start the educational simulation."""
        self.running = True
        print("Educational trading simulation started")
        print("Remember: This is for learning only - no real money involved")
        
        # Set daily start value for risk management
        current_prices = self.market.get_current_prices()
        self.portfolio.daily_start_value = self.portfolio.get_portfolio_value(current_prices)
    
    def stop_simulation(self) -> None:
        """Stop the educational simulation."""
        self.running = False
        print("Educational trading simulation stopped")
    
    def simulate_trading_session(self, duration_minutes: int = 60) -> Dict[str, Any]:
        """
        Simulate a trading session for educational purposes.
        Returns session results for analysis.
        """
        if not self.running:
            self.start_simulation()
        
        session_results = {
            "start_time": datetime.now(),
            "duration_minutes": duration_minutes,
            "price_updates": [],
            "executed_trades": [],
            "portfolio_snapshots": []
        }
        
        # Simulate price updates
        for minute in range(duration_minutes):
            # Update market prices
            new_prices = self.market.update_all_prices()
            session_results["price_updates"].append({
                "timestamp": datetime.now(),
                "prices": new_prices.copy()
            })
            
            # Process pending orders
            for order in self.portfolio.orders:
                if order.status == OrderStatus.PENDING and order.order_type == OrderType.MARKET:
                    if order.symbol in new_prices:
                        success = self.portfolio.execute_market_order(order, new_prices[order.symbol])
                        if success:
                            session_results["executed_trades"].append({
                                "timestamp": order.filled_timestamp,
                                "order_id": order.id,
                                "symbol": order.symbol,
                                "side": order.side,
                                "quantity": order.quantity,
                                "price": order.filled_price
                            })
            
            # Check risk limits
            warnings = self.portfolio.check_risk_limits(new_prices)
            if warnings:
                print(f"Risk Warning: {warnings}")
            
            # Take portfolio snapshot every 10 minutes
            if minute % 10 == 0:
                portfolio_value = self.portfolio.get_portfolio_value(new_prices)
                session_results["portfolio_snapshots"].append({
                    "timestamp": datetime.now(),
                    "portfolio_value": portfolio_value,
                    "cash_balance": self.portfolio.cash_balance,
                    "positions": {symbol: pos.quantity for symbol, pos in self.portfolio.positions.items()}
                })
        
        return session_results
    
    def get_educational_metrics(self) -> Dict[str, Any]:
        """
        Calculate educational performance metrics for learning analysis.
        """
        current_prices = self.market.get_current_prices()
        current_value = self.portfolio.get_portfolio_value(current_prices)
        
        metrics = {
            "total_return": (current_value - self.portfolio.initial_balance) / self.portfolio.initial_balance,
            "current_portfolio_value": current_value,
            "cash_balance": self.portfolio.cash_balance,
            "number_of_trades": len(self.portfolio.trade_history),
            "number_of_positions": len(self.portfolio.positions),
            "positions": {}
        }
        
        # Position details
        for symbol, position in self.portfolio.positions.items():
            if symbol in current_prices:
                position.update_current_price(current_prices[symbol])
                metrics["positions"][symbol] = {
                    "quantity": position.quantity,
                    "average_price": position.average_price,
                    "current_price": position.current_price,
                    "unrealized_pnl": position.unrealized_pnl,
                    "unrealized_pnl_pct": position.unrealized_pnl / (position.average_price * position.quantity) if position.quantity > 0 else 0
                }
        
        return metrics


# Insert points for extending the educational system

class EducationalStrategyRegistry:
    """
    Registry for educational trading strategies.
    Insert point for adding new learning strategies.
    """
    
    def __init__(self):
        self.strategies = {}
    
    def register_strategy(self, name: str, strategy_func, description: str, 
                         educational_objectives: List[str]) -> None:
        """Insert point: Register new educational trading strategies."""
        self.strategies[name] = {
            "function": strategy_func,
            "description": description,
            "objectives": educational_objectives
        }
    
    def get_strategy(self, name: str) -> Optional[Dict[str, Any]]:
        """Get registered strategy for educational use."""
        return self.strategies.get(name)


class EducationalAnalytics:
    """
    Educational analytics for trade analysis and learning.
    Insert point for advanced educational metrics.
    """
    
    def __init__(self):
        self.metrics_registry = {}
    
    def register_metric(self, name: str, calculation_func, description: str) -> None:
        """Insert point: Register new educational performance metrics."""
        self.metrics_registry[name] = {
            "function": calculation_func,
            "description": description
        }
    
    def calculate_metric(self, name: str, data: Dict[str, Any]) -> Optional[float]:
        """Calculate registered metric for educational analysis."""
        if name in self.metrics_registry:
            return self.metrics_registry[name]["function"](data)
        return None


# Example usage for educational purposes
if __name__ == "__main__":
    print("=== Educational Crypto Trading Simulation ===")
    print("This is a safe learning environment with virtual money only")
    print("No real trading or financial risk involved")
    print("")
    
    # Initialize educational trading system
    trading_system = EducationalTradingSystem(initial_balance=10000.0)
    
    # Set market condition for learning scenario
    trading_system.market.set_market_condition(MarketCondition.BULL)
    
    # Start simulation
    trading_system.start_simulation()
    
    # Display current prices
    prices = trading_system.market.get_current_prices()
    print("Current simulated prices:")
    for symbol, price in prices.items():
        print(f"  {symbol}: ${price:.2f}")
    
    # Example educational trade
    buy_order = Order(
        symbol="BTC",
        order_type=OrderType.MARKET,
        side="buy",
        quantity=0.1  # Buy 0.1 BTC with virtual money
    )
    
    success = trading_system.portfolio.place_order(buy_order)
    print(f"\nPlaced educational buy order: {success}")
    
    # Simulate some trading activity
    print("\nSimulating 30-minute educational trading session...")
    session_results = trading_system.simulate_trading_session(30)
    
    # Display educational metrics
    metrics = trading_system.get_educational_metrics()
    print(f"\nEducational Portfolio Performance:")
    print(f"  Total Return: {metrics['total_return']:.2%}")
    print(f"  Portfolio Value: ${metrics['current_portfolio_value']:.2f}")
    print(f"  Cash Balance: ${metrics['cash_balance']:.2f}")
    print(f"  Number of Trades: {metrics['number_of_trades']}")
    
    if metrics['positions']:
        print("  Current Positions:")
        for symbol, pos_data in metrics['positions'].items():
            print(f"    {symbol}: {pos_data['quantity']:.4f} @ ${pos_data['average_price']:.2f}")
            print(f"      Unrealized P&L: ${pos_data['unrealized_pnl']:.2f} ({pos_data['unrealized_pnl_pct']:.2%})")
    
    print("\nRemember: This was educational simulation only!")
    print("Real trading requires proper licensing, compliance, and professional advice.")