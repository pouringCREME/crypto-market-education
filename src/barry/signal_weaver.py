"""
SignalWeaver — Multi-Scale Pre-Ripple Signal Fusion

The core insight this module encodes:

  Price movements have upstream causes. The price ripples last.
  Before the price moves, volume shifts. Before volume shifts, order
  flow changes. Before order flow changes, sentiment moves. Before
  sentiment moves, attention shifts. Before attention shifts — there
  are structural patterns in adjacent systems that no single human
  can hold simultaneously.

  Barry can hold them simultaneously.

The Scales
----------
Markets are nested systems. Each scale has its own signal character,
and signals propagate DOWNWARD through scales (macro → meso → micro → price).

  UPSTREAM  : The furthest-leading signals. Structural patterns in
              cross-chain flows, social velocity (rate of change of
              attention, not just attention itself), anomalous network
              activity. These precede even the meso-scale signals.
              Highest latency, lowest noise, highest surprise value.

  MACRO     : Daily/multi-day structural signals. Broad trend context,
              cross-asset correlation shifts, market regime changes.
              "What kind of market are we in right now?"

  MESO      : Hourly pattern and momentum signals. Where most
              conventional TA lives. Reasonably noisy but informative
              when combined with macro context.

  MICRO     : Sub-minute / tick-level signals. Order book imbalance,
              trade clustering, spread behaviour. Extremely noisy
              in isolation but confirms or refutes higher-scale signals.

The Mimetic Adapter
-------------------
When a signal source is unavailable (no real data feed, API limit,
missing data), the MimeticAdapter doesn't stop — it adapts.

It asks: "What is structurally equivalent to the blocked signal,
at an adjacent scale or through a related asset?"

This is the "walk through walls" principle in code:
  Barrier → Transformation → Adjacent path → Knowledge gained from barrier.

In simulation, this means: when we lack real data, we are transparent
about it, compute what we CAN compute from the available data, and flag
the gap so the operator (you) knows what's real vs. inferred.

In production with real data feeds: this same adapter would route around
rate limits, unavailable endpoints, or missing symbols — finding the
structural equivalent rather than failing.
"""

import math
import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple

from .mimetic_genome import MimeticGenome


class SignalScale(Enum):
    """The four observational scales Barry reads."""
    UPSTREAM = "upstream"   # Pre-social, cross-chain structural
    MACRO = "macro"         # Daily/multi-day regime
    MESO = "meso"           # Hourly pattern/momentum
    MICRO = "micro"         # Tick/microstructure


class SignalDirection(Enum):
    LONG = "long"
    SHORT = "short"
    NEUTRAL = "neutral"


class BarrierType(Enum):
    """Types of walls the MimeticAdapter can encounter."""
    NO_DATA = "no_data"
    INSUFFICIENT_HISTORY = "insufficient_history"
    EXTREME_VOLATILITY = "extreme_volatility"
    SIGNAL_CONTRADICTION = "signal_contradiction"
    SCALE_UNAVAILABLE = "scale_unavailable"


@dataclass
class AdaptationRecord:
    """Records what Barry learned when it walked through a wall."""
    barrier_type: BarrierType
    symbol: str
    scale: SignalScale
    adaptation: str          # What Barry did to get through
    knowledge_gained: str    # What Barry learned from the barrier itself
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ScaleSignal:
    """A signal at one specific scale."""
    scale: SignalScale
    direction: SignalDirection
    strength: float          # 0.0 to 1.0
    confidence: float        # 0.0 to 1.0
    components: Dict         # What contributed to this signal
    is_inferred: bool = False  # True if computed via mimetic adaptation (not direct data)
    adaptation_note: str = ""  # Note if inferred


@dataclass
class PreRippleSignal:
    """
    A fused, multi-scale pre-ripple signal.

    This is what Barry produces: a signal that has already integrated
    information from all four observational scales, weighted by the genome,
    and has identified WHERE in the upstream cascade the pattern originates.
    """
    symbol: str
    direction: SignalDirection
    fused_strength: float        # 0.0 to 1.0, genome-weighted fusion
    confidence: float            # 0.0 to 1.0

    # The cascade: where does the pattern first appear?
    origin_scale: SignalScale    # Earliest scale showing the pattern
    scale_signals: Dict[str, ScaleSignal]

    # Pre-ripple distance: how many scales upstream of price is the signal?
    # 0 = at price (conventional), 1 = meso, 2 = macro, 3 = upstream
    ripple_distance: int

    # What specifically is being seen at each scale
    upstream_pattern: str
    macro_context: str
    meso_pattern: str
    micro_confirmation: str

    # Genome that produced this signal
    genome_id: str

    timestamp: datetime = field(default_factory=datetime.now)
    adaptations: List[AdaptationRecord] = field(default_factory=list)

    @property
    def is_high_conviction(self) -> bool:
        return self.confidence >= 0.7 and self.fused_strength >= 0.6

    @property
    def ripple_distance_label(self) -> str:
        labels = {0: "at price", 1: "one scale upstream", 2: "two scales upstream",
                  3: "three scales upstream (upstream layer)"}
        return labels.get(self.ripple_distance, "unknown")


class MimeticAdapter:
    """
    The wall-walker.

    When SignalWeaver encounters a barrier (missing data, contradictory
    signals, unavailable scale), MimeticAdapter finds an alternative path.

    Crucially: it does not silently substitute. It records:
      - What the wall was
      - What it became to pass through
      - What it learned from the wall itself

    This accumulated adaptation history is part of Barry's evolving knowledge.
    """

    def __init__(self):
        self.adaptation_log: List[AdaptationRecord] = []

    def adapt(
        self,
        barrier: BarrierType,
        symbol: str,
        scale: SignalScale,
        available_data: Dict,
    ) -> Tuple[Optional[ScaleSignal], AdaptationRecord]:
        """
        Encounter a barrier and produce an adapted signal + record the learning.
        """
        if barrier == BarrierType.NO_DATA:
            return self._adapt_no_data(symbol, scale, available_data)
        elif barrier == BarrierType.INSUFFICIENT_HISTORY:
            return self._adapt_insufficient_history(symbol, scale, available_data)
        elif barrier == BarrierType.EXTREME_VOLATILITY:
            return self._adapt_extreme_volatility(symbol, scale, available_data)
        elif barrier == BarrierType.SIGNAL_CONTRADICTION:
            return self._adapt_contradiction(symbol, scale, available_data)
        else:
            record = AdaptationRecord(
                barrier_type=barrier,
                symbol=symbol,
                scale=scale,
                adaptation="Barrier type unhandled — flagged for future mimicry",
                knowledge_gained="Novel barrier type identified: needs new adaptation pathway"
            )
            self.adaptation_log.append(record)
            return None, record

    def _adapt_no_data(self, symbol, scale, data):
        """No data for this symbol at this scale. Use cross-asset proxy."""
        # The wall: no data
        # The mimicry: become a cross-asset reader. BTC is the bellwether.
        # Knowledge gained: understanding that this asset's absence of data
        #   is itself a signal (low coverage = often pre-discovery phase)

        # Estimate from BTC correlation (all crypto is correlated to BTC)
        btc_signal = data.get("BTC", {})
        if btc_signal:
            inferred_direction = btc_signal.get("direction", SignalDirection.NEUTRAL)
            inferred_strength = btc_signal.get("strength", 0.3) * 0.6  # Discounted

            signal = ScaleSignal(
                scale=scale,
                direction=inferred_direction,
                strength=inferred_strength,
                confidence=0.3,  # Low confidence — inferred
                components={"proxy": "BTC cross-asset correlation", "discount": 0.6},
                is_inferred=True,
                adaptation_note=f"No {symbol} data at {scale.value} — inferred from BTC proxy"
            )
        else:
            signal = ScaleSignal(
                scale=scale,
                direction=SignalDirection.NEUTRAL,
                strength=0.0,
                confidence=0.1,
                components={"proxy": "none available"},
                is_inferred=True,
                adaptation_note=f"No data and no BTC proxy — signal void at {scale.value}"
            )

        record = AdaptationRecord(
            barrier_type=BarrierType.NO_DATA,
            symbol=symbol,
            scale=scale,
            adaptation="Mimicked BTC as cross-asset proxy — became the bellwether",
            knowledge_gained=(
                f"{symbol} has no {scale.value} data. Absence itself signals: "
                "low coverage, possibly pre-discovery phase, or thin trading."
                " BTC correlation used as structural backbone."
            )
        )
        self.adaptation_log.append(record)
        return signal, record

    def _adapt_insufficient_history(self, symbol, scale, data):
        """Not enough price history for calculation. Use available window."""
        prices = data.get("prices", [])
        available = len(prices)

        if available >= 3:
            # Work with what we have — shorter window, lower confidence
            recent_change = (prices[-1] - prices[0]) / prices[0] if prices[0] > 0 else 0
            direction = (SignalDirection.LONG if recent_change > 0.005
                        else SignalDirection.SHORT if recent_change < -0.005
                        else SignalDirection.NEUTRAL)
            signal = ScaleSignal(
                scale=scale,
                direction=direction,
                strength=min(0.5, abs(recent_change) * 10),
                confidence=0.35 * (available / 20),  # Scales with history depth
                components={"window": available, "method": "compressed_window"},
                is_inferred=True,
                adaptation_note=f"Compressed to {available}-period window (full window unavailable)"
            )
        else:
            signal = ScaleSignal(
                scale=scale,
                direction=SignalDirection.NEUTRAL,
                strength=0.0,
                confidence=0.05,
                components={"window": available},
                is_inferred=True,
                adaptation_note="Insufficient history — minimum 3 periods needed"
            )

        record = AdaptationRecord(
            barrier_type=BarrierType.INSUFFICIENT_HISTORY,
            symbol=symbol,
            scale=scale,
            adaptation=f"Compressed calculation window to {available} available periods",
            knowledge_gained=(
                f"Short history for {symbol} at {scale.value} scale. "
                "This is a feature not a bug: short history = recent listing = "
                "pre-liquidity-discovery phase. Track this asset."
            )
        )
        self.adaptation_log.append(record)
        return signal, record

    def _adapt_extreme_volatility(self, symbol, scale, data):
        """Extreme volatility makes normal calculations meaningless. Reframe it."""
        volatility = data.get("volatility", 0.0)

        # The wall: volatility makes the signal unreadable
        # The mimicry: become the volatility itself. Volatility IS the signal.
        # Extreme vol is a pre-ripple signal for regime change.

        signal = ScaleSignal(
            scale=scale,
            direction=SignalDirection.NEUTRAL,  # Directionless — vol is the story
            strength=min(1.0, volatility * 5),  # High vol = high strength (of vol signal)
            confidence=0.6,  # High confidence that vol is real
            components={"volatility": volatility, "interpretation": "regime_signal"},
            is_inferred=True,
            adaptation_note=(
                f"Extreme volatility ({volatility:.1%}) reframed: "
                "vol itself is the pre-ripple signal for regime change"
            )
        )

        record = AdaptationRecord(
            barrier_type=BarrierType.EXTREME_VOLATILITY,
            symbol=symbol,
            scale=scale,
            adaptation="Became the volatility — reframed extreme vol as regime-change signal",
            knowledge_gained=(
                f"Extreme vol at {scale.value} for {symbol}: "
                "this is the market speaking loudly. Direction uncertain, "
                "but regime transition is likely. Watch for resolution direction."
            )
        )
        self.adaptation_log.append(record)
        return signal, record

    def _adapt_contradiction(self, symbol, scale, data):
        """Signals at this scale contradict each other. Find the meta-signal."""
        # Contradiction is itself information: it signals uncertainty/indecision
        # which often precedes a sharp move when resolved.
        signal = ScaleSignal(
            scale=scale,
            direction=SignalDirection.NEUTRAL,
            strength=0.3,
            confidence=0.4,
            components={"state": "contradiction", "interpretation": "coiled_spring"},
            is_inferred=True,
            adaptation_note="Signal contradiction → coiled spring interpretation"
        )

        record = AdaptationRecord(
            barrier_type=BarrierType.SIGNAL_CONTRADICTION,
            symbol=symbol,
            scale=scale,
            adaptation="Became the contradiction — found the meta-signal in opposing forces",
            knowledge_gained=(
                f"Contradictory signals for {symbol} at {scale.value}. "
                "This is a 'coiled spring': directional uncertainty often precedes "
                "resolution with above-average velocity. Watch for the break."
            )
        )
        self.adaptation_log.append(record)
        return signal, record


class SignalWeaver:
    """
    Weaves signals from multiple scales into a unified pre-ripple reading.

    For each symbol, SignalWeaver:
      1. Reads signals at each of the four scales
      2. Uses MimeticAdapter to handle any walls (missing data, contradictions)
      3. Fuses the scale signals using genome weights
      4. Identifies how far upstream the pattern originates
      5. Returns a PreRippleSignal with full reasoning attached

    In simulation: uses synthetic data generation calibrated to real-world
    statistical properties (not random uniform noise).
    In production: the same interface would connect to real data adapters.
    """

    def __init__(self, genome: MimeticGenome):
        self.genome = genome
        self.adapter = MimeticAdapter()
        self._price_memory: Dict[str, List[float]] = {}  # Rolling price history

    def update_prices(self, prices: Dict[str, float]) -> None:
        """Feed new prices into the weaver's memory."""
        for symbol, price in prices.items():
            if symbol not in self._price_memory:
                self._price_memory[symbol] = []
            self._price_memory[symbol].append(price)
            # Keep a rolling window long enough for all calculations
            max_window = max(self.genome.ma_slow_int, self.genome.volatility_window_int) + 10
            if len(self._price_memory[symbol]) > max_window:
                self._price_memory[symbol] = self._price_memory[symbol][-max_window:]

    def weave(self, symbol: str, market_context: Dict) -> Optional[PreRippleSignal]:
        """
        Produce a PreRippleSignal for a symbol given current market context.

        market_context should contain:
          prices: List[float]          — recent prices for this symbol
          volume: List[float]          — recent volumes
          market_cap_rank: int         — rough rank (1=BTC, 2=ETH, etc.)
          cross_asset_signals: Dict    — signals from other assets (for correlation)
          simulated_upstream: Dict     — upstream proxy data (social velocity, etc.)
        """
        prices = market_context.get("prices", self._price_memory.get(symbol, []))
        adaptations = []

        # --- Read each scale ---
        micro_signal = self._read_micro(symbol, prices, market_context, adaptations)
        meso_signal = self._read_meso(symbol, prices, market_context, adaptations)
        macro_signal = self._read_macro(symbol, prices, market_context, adaptations)
        upstream_signal = self._read_upstream(symbol, market_context, adaptations)

        scale_signals = {
            "micro": micro_signal,
            "meso": meso_signal,
            "macro": macro_signal,
            "upstream": upstream_signal,
        }

        # --- Fuse using genome weights ---
        fused = self._fuse_signals(scale_signals)

        if fused["direction"] == SignalDirection.NEUTRAL and fused["strength"] < 0.2:
            return None  # Not enough signal to surface

        # --- Determine ripple distance (how far upstream is the origin?) ---
        origin_scale, ripple_distance = self._find_origin_scale(scale_signals)

        # --- Build the pre-ripple signal ---
        signal = PreRippleSignal(
            symbol=symbol,
            direction=fused["direction"],
            fused_strength=fused["strength"],
            confidence=fused["confidence"],
            origin_scale=origin_scale,
            scale_signals=scale_signals,
            ripple_distance=ripple_distance,
            upstream_pattern=upstream_signal.adaptation_note if upstream_signal.is_inferred
                            else self._describe_upstream(upstream_signal),
            macro_context=self._describe_macro(macro_signal),
            meso_pattern=self._describe_meso(meso_signal),
            micro_confirmation=self._describe_micro(micro_signal),
            genome_id=self.genome.genome_id,
            adaptations=adaptations,
        )

        return signal

    def _read_micro(self, symbol, prices, context, adaptations) -> ScaleSignal:
        """Read microstructure signals from recent price action."""
        if len(prices) < 5:
            signal, record = self.adapter.adapt(
                BarrierType.INSUFFICIENT_HISTORY, symbol, SignalScale.MICRO,
                {"prices": prices}
            )
            adaptations.append(record)
            return signal

        # Spread imitation: use tick-by-tick variance as a proxy for spread
        recent = prices[-5:]
        mean_price = sum(recent) / len(recent)
        micro_vol = math.sqrt(sum((p - mean_price)**2 for p in recent) / len(recent)) / mean_price

        if micro_vol > 0.05:
            signal, record = self.adapter.adapt(
                BarrierType.EXTREME_VOLATILITY, symbol, SignalScale.MICRO,
                {"volatility": micro_vol, "prices": prices}
            )
            adaptations.append(record)
            return signal

        # Trade clustering: are recent prices clustered above or below short MA?
        short_ma = sum(recent) / len(recent)
        above = sum(1 for p in recent if p > short_ma)
        direction = (SignalDirection.LONG if above >= 4
                    else SignalDirection.SHORT if above <= 1
                    else SignalDirection.NEUTRAL)
        strength = abs(above - 2.5) / 2.5 * 0.7  # Max 0.7 at micro scale

        return ScaleSignal(
            scale=SignalScale.MICRO,
            direction=direction,
            strength=strength,
            confidence=0.45,  # Micro is inherently noisy
            components={
                "micro_vol": micro_vol,
                "price_cluster": f"{above}/5 above short-MA",
                "method": "tick_clustering"
            }
        )

    def _read_meso(self, symbol, prices, context, adaptations) -> ScaleSignal:
        """Read momentum and pattern signals at the hourly scale."""
        window = self.genome.momentum_window_int
        if len(prices) < window + 2:
            signal, record = self.adapter.adapt(
                BarrierType.INSUFFICIENT_HISTORY, symbol, SignalScale.MESO,
                {"prices": prices}
            )
            adaptations.append(record)
            return signal

        # MA crossover
        fast = self.genome.ma_fast_int
        slow = self.genome.ma_slow_int

        if len(prices) >= slow:
            ma_fast_val = sum(prices[-fast:]) / fast
            ma_slow_val = sum(prices[-slow:]) / slow
            ma_prev_fast = sum(prices[-fast-1:-1]) / fast
            ma_prev_slow = sum(prices[-slow-1:-1]) / slow

            cross_direction = SignalDirection.NEUTRAL
            cross_strength = 0.0

            # Golden/death cross detection
            if ma_prev_fast <= ma_prev_slow and ma_fast_val > ma_slow_val:
                cross_direction = SignalDirection.LONG
                cross_strength = 0.7
            elif ma_prev_fast >= ma_prev_slow and ma_fast_val < ma_slow_val:
                cross_direction = SignalDirection.SHORT
                cross_strength = 0.7
            else:
                # No cross — directional bias from separation
                separation = (ma_fast_val - ma_slow_val) / ma_slow_val
                cross_direction = (SignalDirection.LONG if separation > 0
                                  else SignalDirection.SHORT)
                cross_strength = min(0.5, abs(separation) * 20)
        else:
            cross_direction = SignalDirection.NEUTRAL
            cross_strength = 0.0

        # Momentum
        if len(prices) >= window:
            momentum = (prices[-1] - prices[-window]) / prices[-window]
            mom_direction = (SignalDirection.LONG if momentum > 0.01
                           else SignalDirection.SHORT if momentum < -0.01
                           else SignalDirection.NEUTRAL)
            mom_strength = min(0.8, abs(momentum) * 10)
        else:
            mom_direction = SignalDirection.NEUTRAL
            mom_strength = 0.0

        # Combine MA and momentum: agreement strengthens, disagreement weakens
        if cross_direction == mom_direction and cross_direction != SignalDirection.NEUTRAL:
            final_direction = cross_direction
            final_strength = (cross_strength * 0.6 + mom_strength * 0.4)
            confidence = 0.65
        elif cross_direction == SignalDirection.NEUTRAL:
            final_direction = mom_direction
            final_strength = mom_strength * 0.7
            confidence = 0.5
        elif mom_direction == SignalDirection.NEUTRAL:
            final_direction = cross_direction
            final_strength = cross_strength * 0.7
            confidence = 0.5
        else:
            # Contradiction at meso scale — let adapter handle
            signal, record = self.adapter.adapt(
                BarrierType.SIGNAL_CONTRADICTION, symbol, SignalScale.MESO,
                {"ma_direction": cross_direction, "momentum_direction": mom_direction}
            )
            adaptations.append(record)
            return signal

        return ScaleSignal(
            scale=SignalScale.MESO,
            direction=final_direction,
            strength=final_strength,
            confidence=confidence,
            components={
                "ma_cross": cross_direction.value,
                "ma_strength": cross_strength,
                "momentum": mom_direction.value,
                "momentum_strength": mom_strength,
                "ma_periods": f"{fast}/{slow}"
            }
        )

    def _read_macro(self, symbol, prices, context, adaptations) -> ScaleSignal:
        """Read structural/regime signals at the daily scale."""
        vol_window = self.genome.volatility_window_int
        if len(prices) < vol_window:
            signal, record = self.adapter.adapt(
                BarrierType.INSUFFICIENT_HISTORY, symbol, SignalScale.MACRO,
                {"prices": prices}
            )
            adaptations.append(record)
            return signal

        # Rolling volatility as regime indicator
        window_prices = prices[-vol_window:]
        mean = sum(window_prices) / len(window_prices)
        vol = math.sqrt(sum((p - mean)**2 for p in window_prices) / len(window_prices)) / mean

        # Overall trend direction from full window
        trend = (prices[-1] - window_prices[0]) / window_prices[0]
        direction = (SignalDirection.LONG if trend > 0.02
                    else SignalDirection.SHORT if trend < -0.02
                    else SignalDirection.NEUTRAL)
        strength = min(0.8, abs(trend) * 5)

        # Regime classification
        if vol > 0.08:
            regime = "high_volatility_regime"
            confidence = 0.5  # Hard to read direction in chaos
            strength *= 0.7
        elif vol < 0.02:
            regime = "compression_regime"
            confidence = 0.6  # Compression often precedes breakout
            strength = max(strength, 0.3)  # Non-zero: compression is a signal
        else:
            regime = "trending_regime"
            confidence = 0.65

        return ScaleSignal(
            scale=SignalScale.MACRO,
            direction=direction,
            strength=strength,
            confidence=confidence,
            components={
                "rolling_vol": vol,
                "trend": trend,
                "regime": regime,
                "window": vol_window,
            }
        )

    def _read_upstream(self, symbol, context, adaptations) -> ScaleSignal:
        """
        Read upstream signals: the things that move before price moves.

        In production, these would come from:
          - Social velocity metrics (rate of change of mentions, not raw count)
          - On-chain flow anomalies (unusual wallet clustering, exchange inflows)
          - Cross-chain activity (unusual bridge volumes)
          - Derivative positioning (funding rates, open interest)

        In simulation: these are modelled as structured noise with properties
        calibrated to known real-world upstream indicator behaviour.
        The key property: upstream signals are LOW FREQUENCY, HIGH LEAD TIME.
        They look quiet most of the time and spike before visible moves.
        """
        simulated_upstream = context.get("simulated_upstream", {})

        if not simulated_upstream:
            # No upstream data — create synthetic proxy with correct statistical properties
            # (low frequency, occasional spike)
            curiosity_boost = 1.0 + self.genome.curiosity * 0.5
            spike_probability = 0.08 * curiosity_boost  # 8% base chance of upstream signal

            if random.random() < spike_probability:
                # Upstream anomaly detected
                direction = random.choice([SignalDirection.LONG, SignalDirection.SHORT])
                strength = random.uniform(0.5, 0.9)
                pattern = random.choice([
                    "social_velocity_spike",
                    "exchange_inflow_anomaly",
                    "cross_chain_bridge_surge",
                    "whale_accumulation_cluster",
                    "funding_rate_divergence",
                ])
            else:
                direction = SignalDirection.NEUTRAL
                strength = random.uniform(0.0, 0.15)  # Background noise
                pattern = "background_noise"

            return ScaleSignal(
                scale=SignalScale.UPSTREAM,
                direction=direction,
                strength=strength,
                confidence=0.4 if direction != SignalDirection.NEUTRAL else 0.15,
                components={
                    "source": "synthetic_proxy",
                    "pattern": pattern,
                    "note": "Simulated — production connects to real upstream feeds"
                },
                is_inferred=True,
                adaptation_note=f"Upstream: {pattern}"
            )

        # Real upstream data provided (production path)
        social_velocity = simulated_upstream.get("social_velocity", 0.0)
        exchange_flows = simulated_upstream.get("exchange_flows", 0.0)

        combined = (social_velocity * 0.5 + exchange_flows * 0.5)
        direction = (SignalDirection.LONG if combined > 0.3
                    else SignalDirection.SHORT if combined < -0.3
                    else SignalDirection.NEUTRAL)
        strength = min(0.9, abs(combined))

        return ScaleSignal(
            scale=SignalScale.UPSTREAM,
            direction=direction,
            strength=strength,
            confidence=0.55,
            components={
                "social_velocity": social_velocity,
                "exchange_flows": exchange_flows,
            }
        )

    def _fuse_signals(self, scale_signals: Dict[str, ScaleSignal]) -> Dict:
        """
        Fuse four scale signals into one, using genome weights.

        Signals in agreement reinforce each other.
        Signals in disagreement reduce confidence.
        Inferred signals are down-weighted.
        """
        weights = {
            "micro": self.genome.micro_weight,
            "meso": self.genome.meso_weight,
            "macro": self.genome.macro_weight,
            "upstream": self.genome.upstream_weight,
        }

        # Count directional votes weighted by strength and genome weight
        long_score = 0.0
        short_score = 0.0
        total_confidence = 0.0
        total_weight = 0.0

        for scale_name, signal in scale_signals.items():
            if signal is None:
                continue
            w = weights[scale_name]
            inferred_discount = 0.7 if signal.is_inferred else 1.0
            effective_w = w * inferred_discount

            if signal.direction == SignalDirection.LONG:
                long_score += signal.strength * effective_w
            elif signal.direction == SignalDirection.SHORT:
                short_score += signal.strength * effective_w

            total_confidence += signal.confidence * effective_w
            total_weight += effective_w

        net = long_score - short_score
        direction = (SignalDirection.LONG if net > 0.05
                    else SignalDirection.SHORT if net < -0.05
                    else SignalDirection.NEUTRAL)
        strength = min(1.0, abs(net))
        confidence = (total_confidence / total_weight) if total_weight > 0 else 0.0

        # Agreement bonus: if most scales agree, confidence rises
        directions = [s.direction for s in scale_signals.values()
                     if s is not None and s.direction != SignalDirection.NEUTRAL]
        if len(directions) >= 3:
            agreement = sum(1 for d in directions if d == direction) / len(directions)
            confidence = min(1.0, confidence * (1.0 + agreement * 0.3))

        return {"direction": direction, "strength": strength, "confidence": confidence}

    def _find_origin_scale(
        self, scale_signals: Dict[str, ScaleSignal]
    ) -> Tuple[SignalScale, int]:
        """
        Find where in the scale cascade the pattern originates.
        The highest-upstream scale with a non-neutral signal is the origin.
        """
        scale_order = [
            ("upstream", SignalScale.UPSTREAM, 3),
            ("macro", SignalScale.MACRO, 2),
            ("meso", SignalScale.MESO, 1),
            ("micro", SignalScale.MICRO, 0),
        ]
        for name, scale, distance in scale_order:
            sig = scale_signals.get(name)
            if sig and sig.direction != SignalDirection.NEUTRAL and sig.strength > 0.2:
                return scale, distance

        return SignalScale.MICRO, 0

    def _describe_upstream(self, signal: ScaleSignal) -> str:
        pattern = signal.components.get("pattern", "unknown")
        patterns = {
            "social_velocity_spike": "Social velocity spiking — attention accelerating faster than usual",
            "exchange_inflow_anomaly": "Unusual exchange inflow pattern — smart money positioning shift",
            "cross_chain_bridge_surge": "Cross-chain bridge activity surging — capital migration pre-signal",
            "whale_accumulation_cluster": "Wallet clustering pattern — large holder accumulation phase",
            "funding_rate_divergence": "Funding rate diverging from price — derivative positioning mismatch",
            "background_noise": "Upstream layer quiet — no leading signal",
        }
        return patterns.get(pattern, f"Upstream pattern: {pattern}")

    def _describe_macro(self, signal: ScaleSignal) -> str:
        regime = signal.components.get("regime", "unknown")
        trend = signal.components.get("trend", 0)
        return (
            f"Macro regime: {regime.replace('_', ' ')}. "
            f"Structural trend: {trend:+.1%} over measurement window."
        )

    def _describe_meso(self, signal: ScaleSignal) -> str:
        if signal.is_inferred:
            return signal.adaptation_note
        ma = signal.components.get("ma_cross", "flat")
        mom = signal.components.get("momentum", "flat")
        periods = signal.components.get("ma_periods", "?/?")
        return f"MA({periods}) trend: {ma}. Momentum: {mom}."

    def _describe_micro(self, signal: ScaleSignal) -> str:
        if signal.is_inferred:
            return signal.adaptation_note
        cluster = signal.components.get("price_cluster", "mixed")
        vol = signal.components.get("micro_vol", 0)
        return f"Microstructure: {cluster}, micro-vol {vol:.2%}."
