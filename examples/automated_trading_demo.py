#!/usr/bin/env python3
"""
Automated Trading System Demo

Demonstrates the new automated trading capabilities while preserving
educational features. Shows real-time market data, automated strategies,
risk management, and manual override capabilities.
"""

import sys
import os
import time
import logging
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from trading import (
        AutomatedTradingEngine, TradingMode, TradingConfig,
        RealTimeMarketData, DataSource, 
        RiskManager, StrategyEngine
    )
    from config.configuration import ConfigurationManager
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required files are in place.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def print_disclaimer():
    """Print comprehensive disclaimer for automated trading."""
    print("=" * 80)
    print("AUTOMATED CRYPTOCURRENCY TRADING SYSTEM")
    print("=" * 80)
    print()
    print("⚠️  CRITICAL LEGAL DISCLAIMER:")
    print("   • This software can perform REAL automated trading")
    print("   • REAL MONEY can be at risk in live trading mode")
    print("   • Educational mode preserves safe simulation features")
    print("   • You are responsible for all trading decisions and losses")
    print("   • Automated trading involves substantial financial risk")
    print("   • Past performance does not guarantee future results")
    print("   • Proper licensing and compliance may be required")
    print()
    print("🔧 SYSTEM MODES:")
    print("   • EDUCATIONAL: Safe simulation only (recommended for learning)")
    print("   • PAPER: Real data, virtual money (testing strategies)")
    print("   • LIVE: Real data, real money (requires extreme caution)")
    print()
    print("🛡️  RISK MANAGEMENT FEATURES:")
    print("   • Automated position sizing")
    print("   • Real-time risk monitoring")
    print("   • Emergency stop capabilities")
    print("   • Manual override system")
    print("   • Educational safety limits")
    print()
    print("=" * 80)
    print()

def demonstrate_automated_engine():
    """Demonstrate automated trading engine capabilities."""
    print("🤖 Automated Trading Engine Demonstration")
    print("-" * 50)
    
    # Create configuration for educational mode
    config = TradingConfig(
        mode=TradingMode.EDUCATIONAL,  # Start in safe educational mode
        max_positions=3,
        max_portfolio_risk=0.01,  # 1% max portfolio risk
        max_position_size=0.05,   # 5% max position size
        educational_mode_active=True,
        high_frequency_mode=False,
        target_assets=["BTC", "ETH", "SOL", "DOGE"]
    )
    
    # Initialize trading engine
    print("Initializing automated trading engine...")
    engine = AutomatedTradingEngine(config)
    
    # Start the engine
    success = engine.start()
    print(f"✅ Engine started: {success}")
    
    # Display system status
    status = engine.get_system_status()
    print(f"\n📊 System Status:")
    print(f"   Mode: {status['mode']}")
    print(f"   Educational Mode: {status['educational_mode']}")
    print(f"   Manual Override: {status['manual_override']}")
    print(f"   Status: {status['status']}")
    
    # Test educational mode toggle
    print(f"\n🎓 Testing Educational Mode Controls:")
    engine.toggle_educational_mode(False)
    print("   Educational mode deactivated")
    engine.toggle_educational_mode(True)
    print("   Educational mode reactivated")
    
    # Test manual override
    print(f"\n🎮 Testing Manual Override:")
    engine.enable_manual_override()
    print("   Manual override enabled")
    engine.disable_manual_override()
    print("   Manual override disabled")
    
    # Stop the engine
    engine.stop()
    print(f"✅ Engine stopped safely")
    
    return engine

def demonstrate_market_data():
    """Demonstrate real-time market data system."""
    print("\n📈 Real-Time Market Data Demonstration")
    print("-" * 50)
    
    # Initialize market data system
    market_data = RealTimeMarketData(
        data_source=DataSource.SIMULATED,  # Safe simulation
        educational_mode=True
    )
    
    # Test data for high-volatility assets
    symbols = ["BTC", "ETH", "SOL", "DOGE", "SHIB", "PEPE"]
    
    print("Starting market data streaming...")
    success = market_data.start_streaming(symbols)
    print(f"✅ Streaming started: {success}")
    
    # Let data stream for a few seconds
    print("Collecting market data...")
    time.sleep(3)
    
    # Display current prices
    print(f"\n💰 Current Prices:")
    for symbol in symbols:
        tick = market_data.get_current_price(symbol)
        if tick:
            print(f"   {symbol}: ${tick.price:,.4f} (Vol: {tick.volatility:.1%}, Type: {tick.asset_type.value})")
    
    # Show high-volatility assets
    high_vol = market_data.get_high_volatility_assets()
    print(f"\n⚡ High-Volatility Assets: {high_vol}")
    
    # Market overview
    overview = market_data.get_market_overview()
    print(f"\n📊 Market Overview:")
    print(f"   Total Symbols: {overview['total_symbols']}")
    print(f"   High-Vol Assets: {overview['high_volatility_assets']}")
    print(f"   Avg Volatility: {overview['average_volatility']:.1%}")
    print(f"   Data Source: {overview['data_source']}")
    
    # Stop streaming
    market_data.stop_streaming()
    print("✅ Market data streaming stopped")
    
    return market_data

def demonstrate_risk_management():
    """Demonstrate risk management system."""
    print("\n⚠️  Risk Management System Demonstration")
    print("-" * 50)
    
    # Initialize risk manager in educational mode
    risk_manager = RiskManager(
        educational_mode=True,
        max_portfolio_risk=0.01,  # 1% max portfolio risk
        max_position_size=0.05    # 5% max position size
    )
    
    print("Risk manager initialized with educational safety limits")
    
    # Test position sizing
    print(f"\n📏 Position Sizing Test:")
    entry_price = 45000.0
    stop_loss = 44100.0  # 2% stop loss
    
    position_size, is_valid = risk_manager.calculate_position_size(
        "BTC", entry_price, stop_loss
    )
    
    print(f"   Entry Price: ${entry_price:,.2f}")
    print(f"   Stop Loss: ${stop_loss:,.2f}")
    print(f"   Calculated Position Size: {position_size:.6f} BTC")
    print(f"   Position Valid: {is_valid}")
    
    # Test trade validation
    print(f"\n✅ Trade Validation Test:")
    is_valid, violations = risk_manager.validate_trade(
        "BTC", position_size, entry_price, stop_loss
    )
    
    print(f"   Trade Valid: {is_valid}")
    if violations:
        print(f"   Violations: {violations}")
    else:
        print(f"   No violations - trade approved")
    
    # Update position and test risk metrics
    print(f"\n�� Risk Metrics Test:")
    current_price = 45450.0  # Price moved up
    risk_manager.update_position("BTC", position_size, entry_price, current_price, stop_loss)
    
    metrics = risk_manager.calculate_portfolio_risk()
    print(f"   Portfolio Value: ${metrics.portfolio_value:,.2f}")
    print(f"   Total Exposure: ${metrics.total_exposure:,.2f}")
    print(f"   Max Position Risk: {metrics.max_position_risk:.1%}")
    print(f"   Risk Score: {metrics.risk_score:.0f}/100")
    
    # Educational risk summary
    summary = risk_manager.get_educational_risk_summary()
    print(f"\n🎓 Educational Risk Summary:")
    print(f"   Portfolio Health: {summary['portfolio_health']}")
    print(f"   Risk Score: {summary['risk_score']}")
    print(f"   Active Positions: {summary['total_positions']}")
    print(f"   Recommendations:")
    for rec in summary['recommendations']:
        print(f"     • {rec}")
    
    return risk_manager

def demonstrate_strategy_engine():
    """Demonstrate strategy execution engine."""
    print("\n🧠 Strategy Engine Demonstration")
    print("-" * 50)
    
    # Initialize strategy engine
    strategy_engine = StrategyEngine(educational_mode=True)
    
    print("Strategy engine initialized with default strategies")
    
    # Show registered strategies
    performance = strategy_engine.get_strategy_performance()
    print(f"\n📋 Registered Strategies:")
    for name, perf in performance.items():
        enabled = "✅" if perf['enabled'] else "❌"
        print(f"   {enabled} {name}: {perf['signals_generated']} signals generated")
    
    # Generate mock market data for signal generation
    print(f"\n🔍 Generating Trading Signals:")
    mock_market_data = {
        "BTC": {
            "current_price": 45000.0,
            "ohlcv": {
                "1h": [
                    {"open": 44000, "high": 44200, "low": 43800, "close": 44100, "volume": 1000},
                    {"open": 44100, "high": 44500, "low": 44000, "close": 44300, "volume": 1200},
                    {"open": 44300, "high": 44800, "low": 44200, "close": 44600, "volume": 1500},
                    {"open": 44600, "high": 45200, "low": 44500, "close": 45000, "volume": 1800},
                ] * 5  # Repeat to have enough data
            }
        },
        "ETH": {
            "current_price": 3000.0,
            "ohlcv": {
                "1h": [
                    {"open": 2950, "high": 2970, "low": 2940, "close": 2960, "volume": 500},
                    {"open": 2960, "high": 2990, "low": 2950, "close": 2980, "volume": 600},
                    {"open": 2980, "high": 3020, "low": 2970, "close": 3000, "volume": 700},
                ] * 7  # Repeat to have enough data
            }
        }
    }
    
    signals = strategy_engine.generate_signals(mock_market_data)
    
    print(f"   Generated {len(signals)} trading signals")
    for signal in signals:
        print(f"   📊 {signal.symbol} {signal.signal_type.upper()}: {signal.strength.value}")
        print(f"      Strategy: {signal.strategy}")
        print(f"      Confidence: {signal.confidence:.1%}")
        print(f"      Entry: ${signal.entry_price:.2f}")
        print(f"      Stop: ${signal.stop_loss:.2f}" if signal.stop_loss else "      Stop: None")
        print(f"      Reasoning: {signal.reasoning}")
        print()
    
    return strategy_engine

def demonstrate_integrated_system():
    """Demonstrate the integrated automated trading system."""
    print("\n🔗 Integrated System Demonstration")
    print("-" * 50)
    
    print("This demonstrates how all components work together:")
    print("1. Market data feeds real-time prices")
    print("2. Strategy engine generates trading signals")
    print("3. Risk manager validates and sizes trades")
    print("4. Automated engine executes approved trades")
    print("5. Educational mode preserves safety features")
    print()
    
    # Show educational integration
    print("🎓 Educational Integration:")
    print("   • All components include educational mode")
    print("   • Conservative risk limits enforced")
    print("   • Manual override always available")
    print("   • Performance tracking for learning")
    print("   • Pattern recognition for education")
    print()
    
    print("⚡ High-Frequency Capabilities:")
    print("   • Real-time market data processing")
    print("   • Multi-timeframe analysis")
    print("   • High-volatility asset support")
    print("   • Pattern recognition")
    print("   • Automated position management")
    print()
    
    print("🛡️  Safety Features:")
    print("   • Emergency stop functionality")
    print("   • Risk limit enforcement")
    print("   • Educational mode toggle")
    print("   • Manual override system")
    print("   • Comprehensive logging")

def interactive_mode_selection():
    """Allow user to select trading mode."""
    print("🎛️  Trading Mode Selection")
    print("-" * 30)
    print("1. Educational Mode (Safe simulation - RECOMMENDED)")
    print("2. Paper Trading (Real data, virtual money)")
    print("3. Live Trading (Real money - HIGH RISK)")
    print()
    
    while True:
        try:
            choice = input("Select mode (1-3): ").strip()
            if choice == "1":
                return TradingMode.EDUCATIONAL, True
            elif choice == "2":
                print("⚠️  Paper trading uses real market data but virtual money")
                confirm = input("Continue? (yes/no): ").lower().strip()
                if confirm == "yes":
                    return TradingMode.PAPER_TRADING, False
            elif choice == "3":
                print("🚨 DANGER: Live trading involves REAL MONEY")
                print("   This can result in significant financial losses")
                print("   Ensure you understand the risks and have proper controls")
                confirm = input("I understand the risks and want to proceed (type 'CONFIRM'): ").strip()
                if confirm == "CONFIRM":
                    return TradingMode.LIVE_TRADING, False
                else:
                    print("Live trading cancelled - returning to educational mode")
                    return TradingMode.EDUCATIONAL, True
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\nDefaulting to educational mode for safety")
            return TradingMode.EDUCATIONAL, True

def main():
    """Main demonstration function."""
    print_disclaimer()
    
    # Get user confirmation and mode selection
    print("Do you understand the risks and disclaimers? (yes/no): ", end="")
    response = input().lower().strip()
    
    if response != "yes":
        print("Please review the disclaimer and understand the risks.")
        return
    
    # Mode selection
    mode, educational_mode = interactive_mode_selection()
    
    print(f"\n�� Starting demonstration in {mode.value} mode...")
    print(f"Educational features: {'Enabled' if educational_mode else 'Disabled'}")
    print()
    
    # Run demonstrations
    try:
        # Core components
        engine = demonstrate_automated_engine()
        market_data = demonstrate_market_data()
        risk_manager = demonstrate_risk_management()
        strategy_engine = demonstrate_strategy_engine()
        
        # Integrated system overview
        demonstrate_integrated_system()
        
        print("\n🎉 Automated Trading System Demo Complete!")
        print("\nKey Features Demonstrated:")
        print("   ✅ Automated trading engine with mode control")
        print("   ✅ Real-time market data with high-volatility support")
        print("   ✅ Advanced risk management system")
        print("   ✅ Multi-strategy execution engine")
        print("   ✅ Educational mode preservation")
        print("   ✅ Manual override capabilities")
        print("   ✅ Pattern recognition and multi-timeframe analysis")
        
        print("\nNext Steps:")
        print("   • Configure strategies for your trading style")
        print("   • Set appropriate risk limits")
        print("   • Test thoroughly in educational/paper mode")
        print("   • Ensure proper compliance before live trading")
        print("   • Always maintain manual oversight")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("This is expected during development - components are being integrated")
    
    print("\n" + "=" * 80)
    print("REMEMBER: Always use proper risk management and never trade")
    print("with money you cannot afford to lose!")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo ended by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please report issues for system improvement.")
