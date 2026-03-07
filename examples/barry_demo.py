#!/usr/bin/env python3
"""
Barry the Duck — Research Agent Demo

This demonstrates Barry in action:
  1. Single-genome mode: basic signal research
  2. Deep insight mode: full reasoning output
  3. Population/evolution mode: genome pool breeding
  4. Wall-walking demonstration: mimetic adaptation in action

Barry does not execute trades. Barry thinks. You decide.

Run:
    PYTHONPATH=src python examples/barry_demo.py
"""

import sys
import os
import time
import random
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

logging.basicConfig(level=logging.WARNING)  # Quiet logs for demo — Barry speaks for himself

try:
    from barry import Barry, BarryConfig
    from barry.mimetic_genome import MimeticGenome, GenomePool
    from barry.insight_engine import InsightDepth
    from barry.signal_weaver import SignalScale
except ImportError as e:
    print(f"\n  Import error: {e}")
    print("  Run from repo root: PYTHONPATH=src python examples/barry_demo.py\n")
    sys.exit(1)


def separator(title: str = "", width: int = 60):
    if title:
        pad = max(0, (width - len(title) - 2) // 2)
        print(f"\n{'─' * pad} {title} {'─' * pad}")
    else:
        print(f"\n{'─' * width}")


def simulated_price_feed(
    symbols: list,
    base_prices: dict = None,
    steps: int = 40,
    scenario: str = "mixed",
) -> list:
    """
    Generate a sequence of simulated price updates.
    scenario: "bull", "bear", "volatile", "compression", "mixed"
    """
    if base_prices is None:
        base_prices = {"BTC": 45000, "ETH": 3000, "SOL": 100,
                       "DOGE": 0.08, "SHIB": 0.000025}

    prices = {s: base_prices.get(s, 100.0) for s in symbols}
    history = []

    for step in range(steps):
        new_prices = {}
        for symbol in symbols:
            p = prices[symbol]

            if scenario == "bull":
                drift = random.gauss(0.001, 0.002)
            elif scenario == "bear":
                drift = random.gauss(-0.001, 0.002)
            elif scenario == "volatile":
                drift = random.gauss(0, 0.012)
            elif scenario == "compression":
                # Prices compress — smaller and smaller moves
                scale = max(0.0005, 0.005 - step * 0.0001)
                drift = random.gauss(0, scale)
            else:  # mixed
                phase = step // 10
                if phase == 0:
                    drift = random.gauss(0.0008, 0.002)
                elif phase == 1:
                    drift = random.gauss(-0.0005, 0.004)
                elif phase == 2:
                    drift = random.gauss(0, 0.001)
                else:
                    drift = random.gauss(0.0012, 0.003)

            # Meme coins more volatile
            if symbol in ("DOGE", "SHIB", "PEPE"):
                drift *= 2.5

            new_prices[symbol] = max(p * 0.001, p * (1 + drift))
            prices[symbol] = new_prices[symbol]

        history.append(dict(new_prices))

    return history


def demo_1_basic_barry():
    separator("DEMO 1: Basic Barry")
    print("  Single genome, standard insight depth.")
    print("  Barry watches BTC, ETH, SOL in a mixed market scenario.\n")

    barry = Barry(BarryConfig(
        symbols=["BTC", "ETH", "SOL"],
        insight_depth=InsightDepth.STANDARD,
        min_confidence=0.38,
        name="Barry",
    ))

    barry.print_manifesto()

    # Feed price history
    print("  Feeding 40 price updates to Barry...\n")
    feed = simulated_price_feed(["BTC", "ETH", "SOL"], steps=40, scenario="mixed")
    for tick in feed:
        barry.update_prices(tick)

    # Final perception
    insights = barry.perceive()

    if insights:
        print(f"  Barry surfaces {len(insights)} insight(s):\n")
        for insight in insights:
            print(insight.to_text(InsightDepth.STANDARD))
            print()
    else:
        print("  Barry: quiet. No signals above threshold this cycle.")
        print("  (Markets are sometimes quiet. That is also information.)\n")

    barry.print_status()


def demo_2_deep_insight():
    separator("DEMO 2: Deep Insight Mode (with Wall-Walking)")
    print("  Barry in deep insight mode — full reasoning, adaptation log,")
    print("  and knowledge gained from walls.\n")
    print("  Scenario: volatile market — Barry will hit walls and adapt.\n")

    # A curious Barry — more likely to explore, hit walls, learn
    curious_genome = MimeticGenome(
        name="Barry",
        curiosity=0.85,
        micro_weight=0.1,
        meso_weight=0.3,
        macro_weight=0.3,
        upstream_weight=0.3,   # Upstream-dominant — looking furthest ahead
        momentum_window=8.0,
        confidence_threshold=0.38,
    )

    barry = Barry(
        config=BarryConfig(
            symbols=["BTC", "DOGE", "SOL"],
            insight_depth=InsightDepth.DEEP,
            min_confidence=0.35,
        ),
        genome=curious_genome,
    )

    # Sparse history to force wall-walking on some symbols
    print("  Feeding sparse data (will trigger mimetic adaptation)...\n")

    # Give BTC lots of history, DOGE very little (forces wall-walking)
    btc_feed = simulated_price_feed(["BTC"], steps=50, scenario="volatile")
    for tick in btc_feed:
        barry.update_prices(tick)

    doge_feed = simulated_price_feed(["DOGE"], steps=3, scenario="volatile")
    for tick in doge_feed:
        barry.update_prices(tick)

    sol_feed = simulated_price_feed(["SOL"], steps=35, scenario="bull")
    for tick in sol_feed:
        barry.update_prices(tick)

    insights = barry.perceive()

    if insights:
        for insight in insights:
            print(insight.to_text(InsightDepth.DEEP))
            print()
    else:
        print("  No insights above threshold. Try adjusting min_confidence or scenario.\n")


def demo_3_population_evolution():
    separator("DEMO 3: Population Mode — Genome Evolution")
    print("  Barry maintains a pool of genomes that evolve together.")
    print("  You provide fitness feedback. The structure selects.\n")

    barry = Barry(BarryConfig(
        symbols=["BTC", "ETH"],
        population=True,
        population_size=8,
        insight_depth=InsightDepth.BRIEF,
        min_confidence=0.35,
        name="Barry",
    ))

    print(f"  Initial population: {barry.pool.size} genomes, generation 0")
    pop_summary = barry.pool.summary()
    print(f"  Avg curiosity: {pop_summary['avg_curiosity']:.2f}")
    print()

    # Run 3 generations
    for gen in range(3):
        separator(f"Generation {gen + 1}")

        # Feed price data
        feed = simulated_price_feed(["BTC", "ETH"], steps=30, scenario="mixed")
        for tick in feed:
            barry.update_prices(tick)

        # Perceive with current best genome
        insights = barry.perceive()

        print(f"  Active genome: {barry.genome.genome_id}")
        print(f"  Insights generated: {len(insights)}")
        for insight in insights:
            print(f"    {insight.to_text(InsightDepth.BRIEF)}")

        # Simulate fitness feedback
        # In reality, you'd evaluate whether the signals were useful
        # Here we simulate a noisy fitness signal
        for genome in barry.pool.population:
            simulated_fitness = random.gauss(0.0, 1.0)
            # Reward upstream-heavy genomes slightly (they look furthest ahead)
            if genome.upstream_weight > 0.3:
                simulated_fitness += 0.2
            barry.provide_fitness_feedback(genome.genome_id, simulated_fitness)

        # Evolve
        result = barry.evolve()
        if result:
            print(f"\n  {result.note}")

    barry.print_status()


def demo_4_wall_walking_focus():
    separator("DEMO 4: The Mimetic Adapter — Walking Through Walls")
    print("  Barry deliberately placed in a situation with multiple data gaps")
    print("  to demonstrate the wall-walking (mimetic adaptation) principle.\n")
    print("  Watch: every wall Barry hits teaches it something.\n")

    barry = Barry(BarryConfig(
        symbols=["BTC", "NEWCOIN", "PEPE"],
        insight_depth=InsightDepth.DEEP,
        min_confidence=0.2,  # Low threshold to surface even inferred signals
        name="Barry",
    ))

    # NEWCOIN has zero history (never been in the system)
    # PEPE has only 2 ticks (below minimum for most calculations)
    # BTC has reasonable history

    btc_feed = simulated_price_feed(["BTC"], steps=25, scenario="volatile")
    for tick in btc_feed:
        barry.update_prices(tick)

    pepe_feed = simulated_price_feed(["PEPE"], base_prices={"PEPE": 0.000001}, steps=2)
    for tick in pepe_feed:
        barry.update_prices(tick)

    # NEWCOIN deliberately gets zero price updates — Barry has never seen it

    insights = barry.perceive()

    print(f"  Barry produced {len(insights)} insight(s) despite data walls:\n")
    for insight in insights:
        print(insight.to_text(InsightDepth.DEEP))
        print()

    # Show the adaptation log
    all_adaptations = []
    for insight in insights:
        all_adaptations.extend(insight.adaptations_encountered)
        all_adaptations.extend(insight.knowledge_from_walls)

    if all_adaptations:
        separator("What Barry learned from the walls")
        for item in all_adaptations:
            if item:
                print(f"  ◈ {item}")


def demo_5_barry_brief():
    separator("DEMO 5: Brief Mode — Fast Overview")
    print("  All symbols, brief insight format. The daily check-in view.\n")

    barry = Barry(BarryConfig(
        symbols=["BTC", "ETH", "SOL", "DOGE", "ADA"],
        insight_depth=InsightDepth.BRIEF,
        min_confidence=0.35,
        name="Barry",
    ))

    # Feed varied scenarios per asset
    scenarios = {"BTC": "compression", "ETH": "bull", "SOL": "bear",
                 "DOGE": "volatile", "ADA": "mixed"}

    for sym, scenario in scenarios.items():
        feed = simulated_price_feed([sym], steps=35, scenario=scenario)
        for tick in feed:
            barry.update_prices(tick)

    print("  Barry's current read:\n")
    insights = barry.perceive()

    if insights:
        for insight in insights:
            print(f"  {insight.to_text(InsightDepth.BRIEF)}")
    else:
        print("  Barry: nothing notable right now. Markets appear quiet.")

    print()
    session = barry.insight_engine.get_session_summary()
    print(f"  Session: {session['insights_generated']} insights, "
          f"{session['walls_walked_through']} walls walked, "
          f"{session['high_conviction']} high conviction")


def main():
    print("\n" + "═" * 60)
    print("  BARRY THE DUCK — PERSONAL STRATEGY RESEARCH AGENT")
    print("  MimeticLORE Kernel v0.1")
    print("═" * 60)
    print()
    print("  IMPORTANT: Barry is a research and signal tool only.")
    print("  Barry does not execute trades. You make all decisions.")
    print("  All prices here are simulated. No real money involved.")
    print()

    demos = [
        ("1", "Basic Barry — standard signals",      demo_1_basic_barry),
        ("2", "Deep insight with wall-walking",       demo_2_deep_insight),
        ("3", "Population evolution",                 demo_3_population_evolution),
        ("4", "Mimetic adapter focus",                demo_4_wall_walking_focus),
        ("5", "Brief mode — fast overview",           demo_5_barry_brief),
        ("a", "Run all demos",                        None),
    ]

    print("  Select a demo:")
    for key, label, _ in demos:
        print(f"    [{key}] {label}")
    print()

    try:
        choice = input("  Choice (or press Enter for all): ").strip().lower() or "a"
    except (KeyboardInterrupt, EOFError):
        choice = "a"

    print()

    if choice == "a":
        demo_1_basic_barry()
        demo_2_deep_insight()
        demo_3_population_evolution()
        demo_4_wall_walking_focus()
        demo_5_barry_brief()
    else:
        found = False
        for key, label, fn in demos:
            if key == choice and fn is not None:
                fn()
                found = True
                break
        if not found:
            print(f"  Unknown choice '{choice}' — running all demos.")
            demo_1_basic_barry()
            demo_2_deep_insight()
            demo_3_population_evolution()
            demo_4_wall_walking_focus()
            demo_5_barry_brief()

    print("\n" + "═" * 60)
    print("  Barry session complete.")
    print("  Remember: Barry thinks. You decide.")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Barry: session ended. The walls will still be there tomorrow.")
