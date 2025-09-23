#!/usr/bin/env python3
"""
Educational Crypto Trading Framework - Example Usage

This script demonstrates how to use the educational framework for learning
cryptocurrency trading concepts safely and legally.

ALL TRADING IS SIMULATED - NO REAL MONEY INVOLVED
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from config.configuration import ConfigurationManager, ComponentManager
    from simulation.trading_simulation import EducationalTradingSystem, MarketCondition
    from plugins.plugin_system import PluginManager, MovingAverageAnalysisPlugin
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required files are in place.")
    sys.exit(1)


def print_disclaimer():
    """Print educational disclaimer."""
    print("=" * 70)
    print("EDUCATIONAL CRYPTOCURRENCY TRADING FRAMEWORK")
    print("=" * 70)
    print()
    print("⚠️  IMPORTANT LEGAL DISCLAIMER:")
    print("   • This software is for educational purposes ONLY")
    print("   • NO REAL MONEY or actual trading is involved")
    print("   • All trading is simulated with virtual funds")
    print("   • This is NOT financial or investment advice")
    print("   • Real trading requires proper licensing and compliance")
    print("   • Cryptocurrency trading involves substantial risk")
    print()
    print("✅ Educational Features:")
    print("   • Safe simulation environment")
    print("   • Risk management education")
    print("   • Trading concept learning")
    print("   • Performance analysis tools")
    print("   • No real market access")
    print()
    print("=" * 70)
    print()


def demonstrate_configuration_system():
    """Demonstrate the configuration management system."""
    print("🔧 Configuration System Demonstration")
    print("-" * 40)
    
    # Initialize configuration manager
    config_manager = ConfigurationManager()
    
    # Validate configuration
    errors = config_manager.validate_configuration()
    if errors:
        print("❌ Configuration errors found:")
        for error in errors:
            print(f"   • {error}")
        return False
    else:
        print("✅ Configuration is valid for educational use")
    
    # Show insert points
    insert_points = config_manager.get_insert_points()
    print(f"\n📌 Available Insert Points for Future Updates:")
    for category, points in insert_points.items():
        print(f"   {category}:")
        for point in points[:2]:  # Show first 2 for brevity
            print(f"     - {point}")
        if len(points) > 2:
            print(f"     ... and {len(points) - 2} more")
    
    print()
    return True


def demonstrate_simulation_system():
    """Demonstrate the educational trading simulation."""
    print("🎮 Trading Simulation Demonstration")
    print("-" * 40)
    
    # Initialize educational trading system
    trading_system = EducationalTradingSystem(initial_balance=10000.0)
    
    print("💰 Starting with $10,000 virtual money")
    
    # Show current market prices
    prices = trading_system.market.get_current_prices()
    print("📊 Current Simulated Prices:")
    for symbol, price in prices.items():
        print(f"   {symbol}: ${price:,.2f}")
    
    # Set a learning scenario
    trading_system.market.set_market_condition(MarketCondition.BULL)
    print("📈 Set market condition to: Bull Market (for learning trend following)")
    
    # Simulate some price movements
    print("\n⏱️  Simulating 10 price updates...")
    for i in range(10):
        new_prices = trading_system.market.update_all_prices()
    
    # Show updated prices
    print("📊 Updated Simulated Prices:")
    for symbol, price in new_prices.items():
        original_price = prices[symbol]
        change = (price - original_price) / original_price * 100
        direction = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        print(f"   {symbol}: ${price:,.2f} {direction} ({change:+.2f}%)")
    
    # Demonstrate educational metrics
    metrics = trading_system.get_educational_metrics()
    print(f"\n📈 Educational Portfolio Status:")
    print(f"   Portfolio Value: ${metrics['current_portfolio_value']:,.2f}")
    print(f"   Cash Balance: ${metrics['cash_balance']:,.2f}")
    print(f"   Total Return: {metrics['total_return']:.2%}")
    print(f"   Number of Positions: {metrics['number_of_positions']}")
    
    print()
    return trading_system


def demonstrate_plugin_system():
    """Demonstrate the educational plugin system."""
    print("🔌 Plugin System Demonstration")
    print("-" * 40)
    
    # Initialize plugin manager
    plugin_manager = PluginManager()
    
    # Register sample plugin
    success = plugin_manager.register_plugin(MovingAverageAnalysisPlugin)
    print(f"✅ Registered Moving Average Analysis Plugin: {success}")
    
    # Load the plugin
    ma_plugin = plugin_manager.load_plugin("moving_average_analysis", {
        'periods': [10, 20, 50]
    })
    
    if ma_plugin:
        print("✅ Loaded Moving Average Analysis Plugin")
        
        # Demonstrate plugin execution with sample data
        sample_data = {
            'prices': [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 111, 110, 112, 114]
        }
        
        result = plugin_manager.execute_plugin("moving_average_analysis", sample_data)
        
        if result:
            print("📊 Educational Analysis Results:")
            for ma_name, ma_data in result.get('moving_averages', {}).items():
                print(f"   {ma_name}: ${ma_data['current_value']:.2f}")
            
            print("💡 Educational Insights:")
            for insight in result.get('educational_insights', []):
                print(f"   • {insight}")
    
    # Show plugin registry
    registry = plugin_manager.get_plugin_registry()
    print(f"\n📋 Plugin Registry:")
    for name, info in registry.items():
        print(f"   {name}:")
        print(f"     Category: {info['metadata']['category']}")
        print(f"     Loaded: {'Yes' if info['loaded'] else 'No'}")
        print(f"     Objectives: {', '.join(info['metadata']['educational_objectives'][:2])}...")
    
    print()
    return plugin_manager


def demonstrate_risk_management():
    """Demonstrate educational risk management concepts."""
    print("⚠️  Risk Management Education Demonstration")
    print("-" * 40)
    
    # Example risk calculations (educational only)
    portfolio_value = 10000
    risk_per_trade = 0.01  # 1% risk per trade
    
    print("📚 Educational Risk Management Concepts:")
    print(f"   Portfolio Value: ${portfolio_value:,.2f}")
    print(f"   Risk per Trade: {risk_per_trade:.1%}")
    print(f"   Maximum Loss per Trade: ${portfolio_value * risk_per_trade:.2f}")
    
    # Position sizing example
    entry_price = 45000  # BTC price
    stop_loss_price = 44100  # 2% stop loss
    risk_amount = portfolio_value * risk_per_trade
    
    position_size = risk_amount / (entry_price - stop_loss_price)
    
    print(f"\n📏 Educational Position Sizing Example:")
    print(f"   Entry Price: ${entry_price:.2f}")
    print(f"   Stop Loss: ${stop_loss_price:.2f}")
    print(f"   Risk per Unit: ${entry_price - stop_loss_price:.2f}")
    print(f"   Position Size: {position_size:.6f} BTC")
    print(f"   Total Position Value: ${position_size * entry_price:.2f}")
    
    # Risk-reward ratio
    take_profit_price = 47700  # 6% profit target
    profit_per_unit = take_profit_price - entry_price
    loss_per_unit = entry_price - stop_loss_price
    risk_reward_ratio = profit_per_unit / loss_per_unit
    
    print(f"\n⚖️  Risk-Reward Analysis:")
    print(f"   Take Profit: ${take_profit_price:.2f}")
    print(f"   Potential Profit: ${profit_per_unit:.2f} per unit")
    print(f"   Potential Loss: ${loss_per_unit:.2f} per unit")
    print(f"   Risk-Reward Ratio: 1:{risk_reward_ratio:.1f}")
    
    if risk_reward_ratio >= 2:
        print("   ✅ Good risk-reward ratio (educational assessment)")
    else:
        print("   ⚠️  Poor risk-reward ratio (educational assessment)")
    
    print("\n💡 Educational Reminder:")
    print("   • These are theoretical calculations for learning only")
    print("   • Real trading involves additional risks and costs")
    print("   • Always use proper risk management in real scenarios")
    
    print()


def interactive_learning_session():
    """Provide an interactive learning session."""
    print("🎓 Interactive Learning Session")
    print("-" * 40)
    
    topics = [
        "1. Trading Basics and Terminology",
        "2. Technical Analysis Concepts", 
        "3. Risk Management Principles",
        "4. Simulation Trading Practice",
        "5. Performance Analysis"
    ]
    
    print("📚 Available Learning Topics:")
    for topic in topics:
        print(f"   {topic}")
    
    print("\n✨ Learning Features Available:")
    print("   • Safe simulation environment")
    print("   • Real-time educational feedback")
    print("   • Risk management training")
    print("   • Performance tracking and analysis")
    print("   • No financial risk - virtual money only")
    
    print("\n🚀 Getting Started:")
    print("   1. Review the educational roadmap in docs/EDUCATIONAL_ROADMAP.md")
    print("   2. Start with basic concepts in src/education/basics/")
    print("   3. Practice with the simulation system")
    print("   4. Gradually advance to more complex topics")
    print("   5. Always remember this is educational only!")
    
    print()


def main():
    """Main demonstration function."""
    print_disclaimer()
    
    # Get user confirmation for educational use
    print("Do you understand this is for educational purposes only? (yes/no): ", end="")
    response = input().lower().strip()
    
    if response != "yes":
        print("Please review the disclaimer and educational nature of this software.")
        return
    
    print("\n🎓 Starting Educational Demonstration...\n")
    
    # Demonstrate each component
    if not demonstrate_configuration_system():
        print("❌ Configuration system failed. Please check setup.")
        return
    
    trading_system = demonstrate_simulation_system()
    if not trading_system:
        print("❌ Simulation system failed. Please check setup.")
        return
    
    plugin_manager = demonstrate_plugin_system()
    if not plugin_manager:
        print("❌ Plugin system failed. Please check setup.")
        return
    
    demonstrate_risk_management()
    
    interactive_learning_session()
    
    print("🎉 Educational Demonstration Complete!")
    print("\nNext Steps:")
    print("   • Explore the educational modules in src/education/")
    print("   • Try the simulation system with different market scenarios")
    print("   • Learn about risk management concepts")
    print("   • Practice with the plugin system")
    print("   • Remember: This is all educational - no real trading!")
    
    print("\n" + "=" * 70)
    print("Thank you for using the Educational Crypto Trading Framework!")
    print("Always seek professional advice before real trading.")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Educational session ended by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("This is an educational framework - please report issues for learning improvement.")