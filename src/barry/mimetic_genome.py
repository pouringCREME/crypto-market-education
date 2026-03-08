"""
MimeticGenome — Strategy DNA for the Barry Agent

Every Barry instance carries a genome: a structured, evolvable set of
parameters that define its character as a signal-finder and pattern-reader.

Why genetic encoding?
---------------------
Markets are non-stationary. A strategy that works in one regime fails in
another. Instead of hand-tuning a single strategy forever, we maintain a
*population* of strategy genomes — each with slightly different "personalities"
— and evolve them over time by selecting for fitness (return, risk-adjusted
performance, drawdown resistance).

This is the kernel of the MimeticLORE concept: strategies breed, adapt, and
select — not through human intuition alone, but through the structure itself
acting as the arbiter.

Genome Parameters
-----------------
The genome encodes three families of traits:

  PERCEPTION — how Barry reads the world
    ma_fast, ma_slow          : trend detection periods
    momentum_window           : lookback for momentum calculation
    volatility_window         : rolling volatility estimation
    pattern_sensitivity       : 0–1, how readily Barry flags patterns
    curiosity                 : 0–1, weight given to anomalous/unusual signals
                                (high curiosity = more exploration, more noise,
                                 but higher chance of finding novel signals)

  SCALE WEIGHTS — where Barry looks (the multi-scale pre-ripple concept)
    micro_weight              : weight on sub-minute microstructure signals
    meso_weight               : weight on hourly momentum/pattern signals
    macro_weight              : weight on daily/cross-asset structural signals
    upstream_weight           : weight on signals that precede the above
                                (social velocity, on-chain flows, etc.)

  RISK CHARACTER — how Barry manages exposure
    risk_per_trade            : fraction of portfolio risked per signal (0–0.05)
    stop_loss_atr_multiple    : stop distance in ATR units
    confidence_threshold      : minimum signal confidence to surface (0–1)
    conviction_decay          : how quickly old signals lose weight

All parameters are bounded. Evolution cannot push them outside safe ranges.
"""

import math
import random
import uuid
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class CrossoverMethod(Enum):
    """Methods for breeding two genomes into offspring."""
    UNIFORM = "uniform"          # Each gene inherited from either parent randomly
    SINGLE_POINT = "single_point"  # Split genome at one point, take each half
    BLEND = "blend"              # Offspring gene = weighted average of parents


# Hard bounds for every genome parameter.
# Evolution cannot exceed these — they encode fundamental safety limits.
GENOME_BOUNDS: Dict[str, Tuple[float, float]] = {
    # Perception
    "ma_fast":              (3,    50),
    "ma_slow":              (10,   200),
    "momentum_window":      (5,    60),
    "volatility_window":    (10,   100),
    "pattern_sensitivity":  (0.1,  0.95),
    "curiosity":            (0.0,  1.0),

    # Scale weights (will be normalised to sum to 1.0)
    "micro_weight":         (0.0,  1.0),
    "meso_weight":          (0.0,  1.0),
    "macro_weight":         (0.0,  1.0),
    "upstream_weight":      (0.0,  1.0),

    # Risk character
    "risk_per_trade":       (0.001, 0.05),
    "stop_loss_atr_multiple": (1.0, 5.0),
    "confidence_threshold": (0.3,  0.9),
    "conviction_decay":     (0.5,  0.99),
}


@dataclass
class MimeticGenome:
    """
    The genetic encoding of a Barry strategy instance.

    Each parameter can be mutated or inherited through crossover.
    Genomes carry identity (id, generation, lineage) so their evolutionary
    history can be traced.
    """
    # Identity
    genome_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    generation: int = 0
    parent_ids: List[str] = field(default_factory=list)
    name: str = "Barry"

    # --- Perception genes ---
    ma_fast: float = 10.0
    ma_slow: float = 30.0
    momentum_window: float = 14.0
    volatility_window: float = 20.0
    pattern_sensitivity: float = 0.6
    curiosity: float = 0.4          # 0 = pure exploitation, 1 = pure exploration

    # --- Scale weight genes ---
    micro_weight: float = 0.2
    meso_weight: float = 0.4
    macro_weight: float = 0.25
    upstream_weight: float = 0.15

    # --- Risk character genes ---
    risk_per_trade: float = 0.01
    stop_loss_atr_multiple: float = 2.0
    confidence_threshold: float = 0.55
    conviction_decay: float = 0.85

    # Fitness tracking (set externally after evaluation)
    fitness_score: float = 0.0
    evaluation_count: int = 0

    def __post_init__(self):
        self._clamp_all()
        self._normalise_scale_weights()

    def _clamp_all(self) -> None:
        """Ensure all parameters are within hard bounds."""
        for param, (low, high) in GENOME_BOUNDS.items():
            current = getattr(self, param)
            setattr(self, param, max(low, min(high, current)))

    def _normalise_scale_weights(self) -> None:
        """Scale weights must sum to 1.0 for proper fusion."""
        total = self.micro_weight + self.meso_weight + self.macro_weight + self.upstream_weight
        if total > 0:
            self.micro_weight /= total
            self.meso_weight /= total
            self.macro_weight /= total
            self.upstream_weight /= total
        else:
            # Fallback to equal weights
            self.micro_weight = self.meso_weight = self.macro_weight = self.upstream_weight = 0.25

    @property
    def ma_fast_int(self) -> int:
        return max(2, int(round(self.ma_fast)))

    @property
    def ma_slow_int(self) -> int:
        return max(self.ma_fast_int + 2, int(round(self.ma_slow)))

    @property
    def momentum_window_int(self) -> int:
        return max(3, int(round(self.momentum_window)))

    @property
    def volatility_window_int(self) -> int:
        return max(5, int(round(self.volatility_window)))

    def mutate(self, mutation_rate: float = 0.15, mutation_scale: float = 0.1) -> "MimeticGenome":
        """
        Produce a mutated offspring of this genome.

        mutation_rate  : probability any given gene mutates (0–1)
        mutation_scale : max fractional change on mutation (0–1)

        Curiosity influences mutation: high-curiosity genomes mutate more
        readily, exploring a wider space. Low-curiosity genomes conserve
        successful patterns.
        """
        child = deepcopy(self)
        child.genome_id = str(uuid.uuid4())[:8]
        child.generation = self.generation + 1
        child.parent_ids = [self.genome_id]
        child.fitness_score = 0.0
        child.evaluation_count = 0

        # Curiosity amplifies mutation
        effective_rate = mutation_rate * (1.0 + child.curiosity * 0.5)
        effective_scale = mutation_scale * (1.0 + child.curiosity * 0.3)

        for param, (low, high) in GENOME_BOUNDS.items():
            if random.random() < effective_rate:
                current = getattr(child, param)
                span = high - low
                delta = random.gauss(0, span * effective_scale)
                new_val = max(low, min(high, current + delta))
                setattr(child, param, new_val)

        child._clamp_all()
        child._normalise_scale_weights()
        return child

    def crossover(
        self,
        other: "MimeticGenome",
        method: CrossoverMethod = CrossoverMethod.UNIFORM,
        blend_alpha: float = 0.5,
    ) -> Tuple["MimeticGenome", "MimeticGenome"]:
        """
        Breed this genome with another, producing two offspring.

        Returns a (child_a, child_b) tuple. Both inherit from both parents,
        but with different gene allocations.
        """
        params = list(GENOME_BOUNDS.keys())

        def make_child(primary: "MimeticGenome", secondary: "MimeticGenome") -> "MimeticGenome":
            child = deepcopy(primary)
            child.genome_id = str(uuid.uuid4())[:8]
            child.generation = max(primary.generation, secondary.generation) + 1
            child.parent_ids = [primary.genome_id, secondary.genome_id]
            child.fitness_score = 0.0
            child.evaluation_count = 0

            if method == CrossoverMethod.UNIFORM:
                for param in params:
                    if random.random() < 0.5:
                        setattr(child, param, getattr(secondary, param))

            elif method == CrossoverMethod.SINGLE_POINT:
                split = random.randint(1, len(params) - 1)
                for param in params[split:]:
                    setattr(child, param, getattr(secondary, param))

            elif method == CrossoverMethod.BLEND:
                for param in params:
                    a_val = getattr(primary, param)
                    b_val = getattr(secondary, param)
                    setattr(child, param, blend_alpha * a_val + (1 - blend_alpha) * b_val)

            child._clamp_all()
            child._normalise_scale_weights()
            return child

        return make_child(self, other), make_child(other, self)

    def describe(self) -> Dict:
        """Human-readable summary of this genome's character."""
        scale_dominant = max(
            [("micro", self.micro_weight), ("meso", self.meso_weight),
             ("macro", self.macro_weight), ("upstream", self.upstream_weight)],
            key=lambda x: x[1]
        )[0]

        character = (
            "explorative" if self.curiosity > 0.7
            else "balanced" if self.curiosity > 0.3
            else "conservative"
        )

        return {
            "id": self.genome_id,
            "name": self.name,
            "generation": self.generation,
            "lineage": self.parent_ids,
            "character": character,
            "dominant_scale": scale_dominant,
            "trend_sensitivity": f"fast={self.ma_fast_int}/slow={self.ma_slow_int}",
            "momentum_lookback": self.momentum_window_int,
            "risk_per_trade": f"{self.risk_per_trade:.1%}",
            "confidence_threshold": f"{self.confidence_threshold:.0%}",
            "curiosity": f"{self.curiosity:.2f}",
            "fitness": f"{self.fitness_score:.4f}",
            "evaluations": self.evaluation_count,
            "scale_weights": {
                "micro": f"{self.micro_weight:.2f}",
                "meso": f"{self.meso_weight:.2f}",
                "macro": f"{self.macro_weight:.2f}",
                "upstream": f"{self.upstream_weight:.2f}",
            },
        }


class GenomePool:
    """
    A population of MimeticGenomes that evolve together.

    This is the evolutionary container. It maintains a population, evaluates
    fitness, selects survivors, breeds offspring, and maintains diversity.

    The pool acts as a living ecosystem of strategies. Over generations,
    fit genomes proliferate; weak ones are replaced by offspring or fresh
    random immigrants (to prevent premature convergence).
    """

    def __init__(
        self,
        size: int = 12,
        elite_fraction: float = 0.25,
        immigrant_fraction: float = 0.1,
        crossover_method: CrossoverMethod = CrossoverMethod.UNIFORM,
    ):
        """
        size              : number of genomes in the population
        elite_fraction    : top fraction preserved unchanged each generation
        immigrant_fraction: fraction replaced by fresh random genomes each gen
                            (maintains genetic diversity, prevents local optima)
        """
        self.size = size
        self.elite_count = max(1, int(size * elite_fraction))
        self.immigrant_count = max(1, int(size * immigrant_fraction))
        self.crossover_method = crossover_method
        self.generation = 0
        self.history: List[Dict] = []

        # Seed the initial population
        self.population: List[MimeticGenome] = [
            self._random_genome(name="Barry") for _ in range(size)
        ]

    def _random_genome(self, name: str = "Barry") -> MimeticGenome:
        """Create a genome with randomised parameters within bounds."""
        kwargs = {"name": name, "generation": self.generation}
        for param, (low, high) in GENOME_BOUNDS.items():
            if param in ("ma_fast", "ma_slow", "momentum_window", "volatility_window"):
                # Integer-ish params: use uniform
                kwargs[param] = random.uniform(low, high)
            else:
                # Float params: use uniform
                kwargs[param] = random.uniform(low, high)
        return MimeticGenome(**kwargs)

    def update_fitness(self, genome_id: str, fitness: float) -> bool:
        """Record a fitness score for a genome by its ID."""
        for genome in self.population:
            if genome.genome_id == genome_id:
                # Rolling average fitness
                genome.fitness_score = (
                    (genome.fitness_score * genome.evaluation_count + fitness)
                    / (genome.evaluation_count + 1)
                )
                genome.evaluation_count += 1
                return True
        return False

    def evolve(self) -> List[MimeticGenome]:
        """
        Advance one generation.

        Steps:
          1. Sort by fitness
          2. Preserve elite genomes unchanged
          3. Introduce fresh immigrants for diversity
          4. Fill remainder with offspring from elite parents
          5. Return the new population
        """
        self.population.sort(key=lambda g: g.fitness_score, reverse=True)

        # Record generation summary
        self.history.append({
            "generation": self.generation,
            "best_fitness": self.population[0].fitness_score,
            "avg_fitness": sum(g.fitness_score for g in self.population) / len(self.population),
            "best_genome_id": self.population[0].genome_id,
        })

        # Keep elite
        new_population = [deepcopy(g) for g in self.population[:self.elite_count]]

        # Add immigrants
        for _ in range(self.immigrant_count):
            new_population.append(self._random_genome())

        # Fill with offspring from elite parents
        elite = self.population[:self.elite_count]
        while len(new_population) < self.size:
            parent_a = random.choice(elite)
            parent_b = random.choice(elite)
            if parent_a.genome_id != parent_b.genome_id:
                child_a, child_b = parent_a.crossover(parent_b, self.crossover_method)
                child_a = child_a.mutate()
                new_population.append(child_a)
                if len(new_population) < self.size:
                    child_b = child_b.mutate()
                    new_population.append(child_b)
            else:
                # Same parent selected — just mutate
                new_population.append(parent_a.mutate())

        self.population = new_population[:self.size]
        self.generation += 1
        return self.population

    def best(self) -> MimeticGenome:
        """Return the highest-fitness genome in the current population."""
        return max(self.population, key=lambda g: g.fitness_score)

    def summary(self) -> Dict:
        """Population summary statistics."""
        fitnesses = [g.fitness_score for g in self.population]
        return {
            "generation": self.generation,
            "population_size": len(self.population),
            "best_fitness": max(fitnesses),
            "avg_fitness": sum(fitnesses) / len(fitnesses),
            "min_fitness": min(fitnesses),
            "avg_curiosity": sum(g.curiosity for g in self.population) / len(self.population),
            "generations_logged": len(self.history),
        }
