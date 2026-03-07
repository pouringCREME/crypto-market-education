"""
InsightEngine — Translating Signals into Reasoning

Most trading systems produce signals: BUY, SELL, a number, a direction.
Barry produces insights: structured reasoning about WHY, WHERE UPSTREAM,
HOW CONFIDENT, and WHAT TO WATCH NEXT.

This is the translation layer. It takes a PreRippleSignal and produces
human-readable text that explains what Barry sees and why it matters —
not just what the conclusion is.

Why does this matter?
--------------------
If you can't understand WHY Barry generated a signal, you can't:
  - Decide whether to act on it (you are always the decision maker)
  - Improve the strategy (you need to understand what's being detected)
  - Catch errors (misaligned strategies look plausible without reasoning)
  - Learn (the insight is the education, not the signal)

Insight Depth
-------------
  BRIEF    : One line. Direction + origin + confidence.
  STANDARD : Full signal explanation. What, where, why, how confident.
  DEEP     : Full signal + genome character + adaptation log + watch conditions.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from .signal_weaver import PreRippleSignal, SignalDirection, SignalScale, ScaleSignal
from .mimetic_genome import MimeticGenome


class InsightDepth(Enum):
    BRIEF = "brief"
    STANDARD = "standard"
    DEEP = "deep"


@dataclass
class BarryInsight:
    """A structured insight from Barry about one symbol."""
    symbol: str
    headline: str                    # One-line summary
    signal_direction: str            # "LONG" / "SHORT" / "WATCHING"
    confidence_label: str            # "high" / "moderate" / "low" / "very low"
    ripple_label: str               # "three scales upstream" etc.
    origin_scale: str               # Where the pattern first appeared
    is_high_conviction: bool

    # Layered reasoning
    upstream_reasoning: str
    macro_reasoning: str
    meso_reasoning: str
    micro_reasoning: str

    # Adaptation log (walls walked through to get here)
    adaptations_encountered: List[str]
    knowledge_from_walls: List[str]

    # Genome character that produced this
    genome_character: str
    genome_id: str

    # Actionability
    watch_conditions: List[str]      # What to look for next
    caution_flags: List[str]         # Things that reduce confidence

    # Raw numbers for reference
    raw_strength: float
    raw_confidence: float

    def to_text(self, depth: InsightDepth = InsightDepth.STANDARD) -> str:
        """Render the insight as formatted text."""
        if depth == InsightDepth.BRIEF:
            return self._brief()
        elif depth == InsightDepth.STANDARD:
            return self._standard()
        else:
            return self._deep()

    def _brief(self) -> str:
        conviction = "⬆" if self.is_high_conviction else "·"
        return (
            f"{conviction} {self.symbol} | {self.signal_direction} | "
            f"{self.confidence_label} confidence | origin: {self.origin_scale} | "
            f"{self.ripple_label}"
        )

    def _standard(self) -> str:
        lines = [
            f"╔══ BARRY INSIGHT: {self.symbol} ══",
            f"║",
            f"║  {self.headline}",
            f"║",
            f"║  Direction   : {self.signal_direction}",
            f"║  Confidence  : {self.confidence_label} ({self.raw_confidence:.0%})",
            f"║  Origin      : {self.origin_scale} scale — {self.ripple_label}",
            f"║",
            f"║  What Barry sees:",
        ]
        if self.upstream_reasoning:
            lines.append(f"║    [UPSTREAM]  {self.upstream_reasoning}")
        if self.macro_reasoning:
            lines.append(f"║    [MACRO]     {self.macro_reasoning}")
        if self.meso_reasoning:
            lines.append(f"║    [MESO]      {self.meso_reasoning}")
        if self.micro_reasoning:
            lines.append(f"║    [MICRO]     {self.micro_reasoning}")

        if self.caution_flags:
            lines.append(f"║")
            lines.append(f"║  Caution:")
            for flag in self.caution_flags:
                lines.append(f"║    ⚠  {flag}")

        lines.append(f"║")
        lines.append(f"║  Watch for:")
        for cond in self.watch_conditions:
            lines.append(f"║    →  {cond}")

        lines.append(f"╚══ genome:{self.genome_id} | strength:{self.raw_strength:.2f} ══")
        return "\n".join(lines)

    def _deep(self) -> str:
        text = self._standard()
        extras = [
            f"",
            f"  ─── DEEP READ ───",
            f"  Barry's character: {self.genome_character}",
        ]

        if self.adaptations_encountered:
            extras.append(f"  Walls encountered:")
            for a in self.adaptations_encountered:
                extras.append(f"    ┆ {a}")

        if self.knowledge_from_walls:
            extras.append(f"  Knowledge gained from walls:")
            for k in self.knowledge_from_walls:
                extras.append(f"    ◈ {k}")

        return text + "\n" + "\n".join(extras)


class InsightEngine:
    """
    Translates PreRippleSignals into BarryInsights.

    Also maintains a session log of all insights produced, so patterns
    in Barry's reasoning can be reviewed over time — including whether
    Barry's walls-knowledge is accumulating usefully.
    """

    def __init__(self, genome: MimeticGenome):
        self.genome = genome
        self.insight_log: List[BarryInsight] = []

    def translate(
        self,
        signal: PreRippleSignal,
        depth: InsightDepth = InsightDepth.STANDARD,
    ) -> BarryInsight:
        """Translate a PreRippleSignal into a BarryInsight."""

        # Direction label
        direction_labels = {
            SignalDirection.LONG: "LONG / BULLISH",
            SignalDirection.SHORT: "SHORT / BEARISH",
            SignalDirection.NEUTRAL: "WATCHING / NEUTRAL",
        }
        dir_label = direction_labels[signal.direction]

        # Confidence label
        conf = signal.confidence
        if conf >= 0.75:
            conf_label = "high"
        elif conf >= 0.55:
            conf_label = "moderate"
        elif conf >= 0.35:
            conf_label = "low"
        else:
            conf_label = "very low"

        # Origin scale label
        origin_labels = {
            SignalScale.UPSTREAM: "UPSTREAM (pre-social / on-chain)",
            SignalScale.MACRO: "MACRO (structural/regime)",
            SignalScale.MESO: "MESO (momentum/pattern)",
            SignalScale.MICRO: "MICRO (price action)",
        }
        origin_label = origin_labels.get(signal.origin_scale, str(signal.origin_scale))

        # Headline
        headline = self._generate_headline(signal, dir_label, conf_label)

        # Genome character
        genome_desc = self.genome.describe()
        char = (
            f"{genome_desc['character'].capitalize()} Barry — "
            f"dominant scale: {genome_desc['dominant_scale']}, "
            f"curiosity: {genome_desc['curiosity']}"
        )

        # Adaptations and wall knowledge
        adaptation_notes = [a.adaptation for a in signal.adaptations]
        wall_knowledge = [a.knowledge_gained for a in signal.adaptations]

        # Watch conditions — what to look for next
        watch = self._generate_watch_conditions(signal)

        # Caution flags
        cautions = self._generate_cautions(signal)

        insight = BarryInsight(
            symbol=signal.symbol,
            headline=headline,
            signal_direction=dir_label,
            confidence_label=conf_label,
            ripple_label=signal.ripple_distance_label,
            origin_scale=origin_label,
            is_high_conviction=signal.is_high_conviction,
            upstream_reasoning=signal.upstream_pattern,
            macro_reasoning=signal.macro_context,
            meso_reasoning=signal.meso_pattern,
            micro_reasoning=signal.micro_confirmation,
            adaptations_encountered=adaptation_notes,
            knowledge_from_walls=wall_knowledge,
            genome_character=char,
            genome_id=self.genome.genome_id,
            watch_conditions=watch,
            caution_flags=cautions,
            raw_strength=signal.fused_strength,
            raw_confidence=signal.confidence,
        )

        self.insight_log.append(insight)
        return insight

    def _generate_headline(
        self, signal: PreRippleSignal, dir_label: str, conf_label: str
    ) -> str:
        """Generate a single-sentence summary of the insight."""
        distance = signal.ripple_distance

        if distance >= 3:
            prefix = "Upstream structural pattern"
        elif distance == 2:
            prefix = "Macro-scale regime signal"
        elif distance == 1:
            prefix = "Meso-scale momentum pattern"
        else:
            prefix = "Microstructure signal"

        conviction = "with high conviction" if signal.is_high_conviction else f"({conf_label} confidence)"

        if signal.direction == SignalDirection.NEUTRAL:
            return (
                f"{prefix} in {signal.symbol}: market at decision point — "
                f"directional resolution pending."
            )

        direction_word = "bullish" if signal.direction == SignalDirection.LONG else "bearish"
        return (
            f"{prefix} in {signal.symbol} trending {direction_word} {conviction}, "
            f"originating {signal.ripple_distance_label}."
        )

    def _generate_watch_conditions(self, signal: PreRippleSignal) -> List[str]:
        """What should the operator watch for to confirm or deny this signal?"""
        conditions = []

        if signal.ripple_distance >= 2:
            conditions.append(
                "Watch for this upstream/macro pattern to propagate to meso scale "
                "(MA crossover or volume surge) within the next few periods."
            )

        if signal.direction == SignalDirection.LONG:
            conditions.append(
                "Confirmation: price action holds above short-term MA with rising volume."
            )
            conditions.append(
                "Invalidation: price closes below the prior structure low."
            )
        elif signal.direction == SignalDirection.SHORT:
            conditions.append(
                "Confirmation: price breaks below support with expanding volume."
            )
            conditions.append(
                "Invalidation: price recovers above the prior structure high."
            )
        else:
            conditions.append(
                "Watch for directional resolution: compression often precedes a sharp move."
            )
            conditions.append(
                "The first significant volume surge will likely define the direction."
            )

        if signal.adaptations:
            conditions.append(
                f"Note: {len(signal.adaptations)} wall(s) were encountered in generating "
                "this signal — review adaptation log for data gaps."
            )

        conditions.append(
            "This is a research signal for manual consideration only. "
            "Barry does not execute. You decide."
        )
        return conditions

    def _generate_cautions(self, signal: PreRippleSignal) -> List[str]:
        """Flags that reduce confidence or require attention."""
        cautions = []

        inferred_count = sum(
            1 for s in signal.scale_signals.values()
            if s is not None and s.is_inferred
        )
        if inferred_count >= 2:
            cautions.append(
                f"{inferred_count}/4 scale signals were inferred via mimetic adaptation "
                "(not direct data). Treat with extra caution."
            )

        if signal.confidence < 0.45:
            cautions.append(
                "Overall confidence is low — multiple scales are conflicted or data-sparse."
            )

        if signal.ripple_distance == 0:
            cautions.append(
                "Signal originates at micro scale only — no upstream confirmation. "
                "High noise at this level."
            )

        upstream = signal.scale_signals.get("upstream")
        meso = signal.scale_signals.get("meso")
        if (upstream and meso and
                upstream.direction != SignalDirection.NEUTRAL and
                meso.direction != SignalDirection.NEUTRAL and
                upstream.direction != meso.direction):
            cautions.append(
                "Upstream and meso signals DISAGREE. This contradictory tension "
                "may resolve sharply — direction uncertain, but a move is likely."
            )

        return cautions

    def get_session_summary(self) -> Dict:
        """Summary of all insights generated this session."""
        if not self.insight_log:
            return {"insights_generated": 0, "note": "No insights generated yet."}

        high_conviction = [i for i in self.insight_log if i.is_high_conviction]
        long_signals = [i for i in self.insight_log
                       if i.signal_direction.startswith("LONG")]
        short_signals = [i for i in self.insight_log
                        if i.signal_direction.startswith("SHORT")]

        total_walls = sum(len(i.adaptations_encountered) for i in self.insight_log)

        return {
            "insights_generated": len(self.insight_log),
            "high_conviction": len(high_conviction),
            "long_signals": len(long_signals),
            "short_signals": len(short_signals),
            "watching_signals": len(self.insight_log) - len(long_signals) - len(short_signals),
            "walls_walked_through": total_walls,
            "symbols_covered": list({i.symbol for i in self.insight_log}),
            "genome_id": self.genome.genome_id,
        }
