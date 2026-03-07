"""
Barry — Personal Strategy Research Agent

Named for clarity in a sea of generic bot names.
Barry is an agent, not just a bot. The distinction matters.

Barry's purpose is to surface pre-ripple signals: patterns that exist
upstream of price action, visible only by holding many things simultaneously
— something human cognition cannot do, but AI can.

Barry operates on the MimeticGenome principle:
  - Strategy parameters are genetic: they can evolve, breed, mutate
  - Barriers become knowledge sources: when blocked, adapt and learn
  - Signals carry reasoning: not just WHAT but WHY and HOW UPSTREAM

This is a research and signal generation tool. Barry does not execute trades.
Barry thinks. You decide.

Architecture:
  MimeticGenome     — Barry's strategy DNA (evolvable parameters)
  SignalWeaver      — Multi-scale pre-ripple signal fusion
  InsightEngine     — Translates signal patterns into human-readable reasoning
  Barry             — The agent that orchestrates all of the above
"""

from .mimetic_genome import MimeticGenome, GenomePool, CrossoverMethod
from .signal_weaver import SignalWeaver, SignalScale, PreRippleSignal
from .insight_engine import InsightEngine, InsightDepth
from .barry import Barry, BarryConfig, EvolutionResult

__all__ = [
    "Barry",
    "BarryConfig",
    "EvolutionResult",
    "MimeticGenome",
    "GenomePool",
    "CrossoverMethod",
    "SignalWeaver",
    "SignalScale",
    "PreRippleSignal",
    "InsightEngine",
    "InsightDepth",
]
