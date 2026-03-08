"""
Barry — The Agent

Barry is not a bot. A bot executes instructions.
Barry is an agent: it perceives, reasons, adapts, and evolves.

Barry's identity:
  - Named for clarity (one identifiable duck in a sea of mimic_this, bot_that)
  - Carries a genome (strategy DNA, evolvable over time)
  - Reads markets at multiple scales simultaneously
  - Walks through walls when blocked (the mimetic adapter)
  - Produces reasoning, not just signals
  - Does not execute — insights are for your consideration

Barry's relationship with you:
  - Barry thinks. You decide.
  - Barry explains its reasoning. You validate or reject it.
  - Barry evolves based on your feedback. You guide the selection.
  - This is mutualism, not automation.

Barry's relationship with markets:
  - Markets are information systems with nested scales
  - Pre-ripple signals exist upstream of price — Barry looks there
  - Volatility and noise are not failures — they are signals in disguise
  - Meme coins and "silly" assets are valid signal generators
    (social velocity, attention dynamics, narrative formation)

The MimeticLORE connection:
  Barry is the personal entry point to the broader Mimic protocol.
  At scale, a population of Barry instances (a GenomePool) would evolve
  together — strategies breeding, selecting, and adapting — the structure
  itself becoming the arbiter of which patterns survive.
  The goal is not concentration of insight upward, but distribution of
  it outward, to the people who were always excluded from the rooms
  where these decisions are made.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from .mimetic_genome import MimeticGenome, GenomePool, CrossoverMethod
from .signal_weaver import SignalWeaver, PreRippleSignal, SignalDirection
from .insight_engine import InsightEngine, BarryInsight, InsightDepth


@dataclass
class BarryConfig:
    """
    Configuration for a Barry instance.

    symbols       : assets Barry watches
    insight_depth : how much explanation Barry produces
    min_confidence: minimum confidence to surface an insight
    auto_evolve   : whether Barry evolves its genome based on feedback
    population    : if True, Barry maintains a GenomePool (multi-strategy)
    population_size: genome pool size when population=True
    """
    symbols: List[str] = field(default_factory=lambda: ["BTC", "ETH", "SOL"])
    insight_depth: InsightDepth = InsightDepth.STANDARD
    min_confidence: float = 0.4
    auto_evolve: bool = False  # Requires explicit opt-in
    population: bool = False   # Single genome by default
    population_size: int = 8
    name: str = "Barry"


@dataclass
class EvolutionResult:
    """Result of one evolutionary step."""
    generation: int
    best_genome_id: str
    best_fitness: float
    avg_fitness: float
    population_size: int
    note: str


class Barry:
    """
    Barry the Duck — Personal Strategy Research Agent.

    Usage (basic):
        barry = Barry()
        barry.update_prices({"BTC": 45000, "ETH": 3000})
        insights = barry.perceive()
        for insight in insights:
            print(insight.to_text())

    Usage (with population evolution):
        config = BarryConfig(population=True, population_size=12)
        barry = Barry(config=config)
        # ... run sessions, provide fitness feedback ...
        barry.evolve()

    Barry is always in RESEARCH mode. He does not execute trades.
    """

    BARRY_MANIFESTO = """
    I am Barry. I watch markets not to automate your decisions,
    but to see what you cannot see alone.

    I look upstream — before the price, before the volume,
    before the sentiment — to where patterns form before
    anyone names them.

    When I hit a wall, I become the wall. I learn from it.
    I pass through carrying that knowledge.

    I am not here to replace your judgment. I am here to
    extend your perception. You decide. Always.

    My genome evolves. My population learns. The structure
    of what works propagates — not upward to fewer hands,
    but outward, to more of them.

    That is the point.
    """

    def __init__(
        self,
        config: Optional[BarryConfig] = None,
        genome: Optional[MimeticGenome] = None,
    ):
        self.config = config or BarryConfig()
        self.logger = logging.getLogger(f"Barry.{self.config.name}")

        # Genome initialisation
        if genome is not None:
            self.genome = genome
            self.genome.name = self.config.name
        elif self.config.population:
            # Population mode: maintain a pool, use the best for perception
            self.pool = GenomePool(
                size=self.config.population_size,
                crossover_method=CrossoverMethod.UNIFORM,
            )
            self.genome = self.pool.best()
            self.genome.name = self.config.name
        else:
            # Single genome — default conservative Barry
            self.genome = MimeticGenome(name=self.config.name)
            self.pool = None

        # Core components wired to the genome
        self.weaver = SignalWeaver(self.genome)
        self.insight_engine = InsightEngine(self.genome)

        # Session tracking
        self.session_start = datetime.now()
        self.perception_count = 0
        self.high_conviction_count = 0
        self.signal_history: List[PreRippleSignal] = []
        self.insight_history: List[BarryInsight] = []

        self.logger.info(
            f"Barry initialised | genome: {self.genome.genome_id} | "
            f"symbols: {self.config.symbols} | "
            f"population: {self.config.population}"
        )

    def update_prices(self, prices: Dict[str, float]) -> None:
        """
        Feed current prices to Barry.

        Call this regularly (each tick, each minute, each candle close —
        whatever your data rhythm is) to keep Barry's perception current.
        """
        self.weaver.update_prices(prices)

    def perceive(
        self,
        market_context: Optional[Dict] = None,
        depth: Optional[InsightDepth] = None,
    ) -> List[BarryInsight]:
        """
        Barry perceives the current market and returns insights.

        market_context: optional dict with extra data per symbol:
          {
            "BTC": {
              "prices": [...],   # price history (uses internal memory if absent)
              "volume": [...],
              "simulated_upstream": {...}  # upstream proxy data if available
            }
          }

        Returns a list of BarryInsights — one per symbol with a signal
        above the minimum confidence threshold.
        """
        depth = depth or self.config.insight_depth
        context = market_context or {}
        insights = []

        for symbol in self.config.symbols:
            sym_context = context.get(symbol, {})

            # Weave the multi-scale signal
            signal = self.weaver.weave(symbol, sym_context)

            if signal is None:
                self.logger.debug(f"{symbol}: no signal above threshold")
                continue

            if signal.confidence < self.config.min_confidence:
                self.logger.debug(
                    f"{symbol}: signal confidence {signal.confidence:.0%} below "
                    f"threshold {self.config.min_confidence:.0%} — not surfaced"
                )
                continue

            # Translate to insight
            insight = self.insight_engine.translate(signal, depth)
            insights.append(insight)

            # Track
            self.signal_history.append(signal)
            self.insight_history.append(insight)
            if insight.is_high_conviction:
                self.high_conviction_count += 1

        self.perception_count += 1

        if insights:
            self.logger.info(
                f"Perception {self.perception_count}: {len(insights)} insight(s) surfaced "
                f"({self.high_conviction_count} high conviction total this session)"
            )
        else:
            self.logger.debug(f"Perception {self.perception_count}: no signals above threshold")

        return insights

    def provide_fitness_feedback(
        self,
        genome_id: str,
        outcome: float,
        note: str = "",
    ) -> bool:
        """
        Provide fitness feedback to the genome pool (population mode only).

        outcome: a float representing how well this genome performed.
                 Positive = good. Negative = bad. Scale is up to you —
                 could be simulated P&L, Sharpe increment, or a simple
                 +1/-1 judgment.

        This is how Barry's population evolves: you observe the insights,
        decide which were useful, and feed that back. The structure
        selects for what works. You guide the direction.

        Returns True if the genome_id was found and updated.
        """
        if self.pool is None:
            self.logger.warning(
                "Fitness feedback requires population mode "
                "(BarryConfig(population=True))"
            )
            return False

        updated = self.pool.update_fitness(genome_id, outcome)
        if updated and note:
            self.logger.info(f"Fitness updated for {genome_id}: {outcome:+.3f} — {note}")
        return updated

    def evolve(self) -> Optional[EvolutionResult]:
        """
        Advance one evolutionary generation (population mode only).

        After several perception cycles and fitness feedback rounds,
        call this to breed the next generation — elite genomes survive,
        offspring from successful parents fill the rest, fresh immigrants
        maintain diversity.

        Returns an EvolutionResult summary, or None if not in population mode.
        """
        if self.pool is None:
            self.logger.warning("Evolution requires population mode.")
            return None

        new_pop = self.pool.evolve()
        best = self.pool.best()

        # Rewire Barry to use the new best genome
        self.genome = best
        self.genome.name = self.config.name
        self.weaver = SignalWeaver(self.genome)
        self.insight_engine = InsightEngine(self.genome)

        summary = self.pool.summary()
        result = EvolutionResult(
            generation=self.pool.generation,
            best_genome_id=best.genome_id,
            best_fitness=summary["best_fitness"],
            avg_fitness=summary["avg_fitness"],
            population_size=len(new_pop),
            note=(
                f"Generation {self.pool.generation} complete. "
                f"Best genome: {best.genome_id} "
                f"(fitness: {best.fitness_score:.4f}). "
                f"Average curiosity: {summary['avg_curiosity']:.2f}."
            ),
        )

        self.logger.info(result.note)
        return result

    def get_status(self) -> Dict:
        """Full status report for this Barry session."""
        session_duration = datetime.now() - self.session_start
        insight_summary = self.insight_engine.get_session_summary()
        genome_desc = self.genome.describe()

        status = {
            "name": self.config.name,
            "genome": genome_desc,
            "session": {
                "started": self.session_start.isoformat(),
                "duration_minutes": session_duration.total_seconds() / 60,
                "perception_cycles": self.perception_count,
                "insights_generated": insight_summary.get("insights_generated", 0),
                "high_conviction": insight_summary.get("high_conviction", 0),
                "walls_walked_through": insight_summary.get("walls_walked_through", 0),
                "symbols_watched": self.config.symbols,
            },
            "population": None,
        }

        if self.pool:
            status["population"] = self.pool.summary()

        return status

    def print_manifesto(self) -> None:
        print(self.BARRY_MANIFESTO)

    def print_status(self) -> None:
        status = self.get_status()
        genome = status["genome"]
        session = status["session"]

        print(f"\n{'═' * 55}")
        print(f"  {status['name'].upper()} THE DUCK — STATUS")
        print(f"{'═' * 55}")
        print(f"  Genome     : {genome['id']} (gen {genome['generation']})")
        print(f"  Character  : {genome['character'].capitalize()}")
        print(f"  Dominant   : {genome['dominant_scale']} scale")
        print(f"  Curiosity  : {genome['curiosity']}")
        print(f"  Risk/trade : {genome['risk_per_trade']}")
        print(f"  Threshold  : {genome['confidence_threshold']}")
        print(f"{'─' * 55}")
        print(f"  Session    : {session['duration_minutes']:.1f} min")
        print(f"  Perceptions: {session['perception_cycles']}")
        print(f"  Insights   : {session['insights_generated']}")
        print(f"  High conv. : {session['high_conviction']}")
        print(f"  Walls      : {session['walls_walked_through']}")
        print(f"  Watching   : {', '.join(session['symbols_watched'])}")

        if status["population"]:
            pop = status["population"]
            print(f"{'─' * 55}")
            print(f"  Population : {pop['population_size']} genomes, gen {pop['generation']}")
            print(f"  Best fit   : {pop['best_fitness']:.4f}")
            print(f"  Avg fit    : {pop['avg_fitness']:.4f}")

        print(f"{'═' * 55}\n")
