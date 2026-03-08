# Barry — TypeScript Port for CLEAN-BOT Integration

Three files written at `the_real_squid/CLEAN-BOT_HANDOFF/src/barry/`:

## Files

### `genome.ts`
- `MimeticGenome` — 14 evolvable parameters, `mutate()`, `crossover()`, `describe()`
- `GenomePool` — 8 competing genomes, `updateFitness()`, `evolve()`, `best()`, `summary()`
- `GENOME_BOUNDS` — hard safety limits on all parameters
- `CrossoverMethod` enum (UNIFORM / SINGLE_POINT / BLEND)
- Each genome in the pool maps **1:1 to an ArchetypeV3 on-chain record**

### `weaver.ts`
- `SignalWeaver` — 4-scale signal fusion (upstream / macro / meso / micro)
- `MimeticAdapter` — wall-walker: handles missing data, extreme vol, contradictions
- `PreRippleSignal` — fused output with origin scale, ripple distance, per-scale descriptions
- `_readUpstream()` is a **clearly marked stub** — hook for real upstream feed

### `barry.ts`
- `Barry` class — the trade loop interface:
  - `updatePrices(prices)` — feed every tick
  - `perceive(symbol)` → `PreRippleSignal | null`
  - `recordTradeResult(genomeId, pnl)` → auto-evolves after `evolveEvery` trades
  - `evolve()` → `EvolutionResult` — wire this to ArchetypeV3
  - `breedPair()` → `[id1, id2]` — for `breedArchetypes()` on V3
  - `activeGenomeId()` — tag outgoing trades with this

## The Trade Loop

```typescript
const barry = new Barry({ symbols: ["WETH/USDC"], populationSize: 8 });

// On every price tick:
barry.updatePrices({ "WETH/USDC": currentPrice });
const signal = barry.perceive("WETH/USDC");

if (signal && signal.direction !== SignalDirection.NEUTRAL
    && signal.confidence >= 0.4) {
  const genomeId = signal.genomeId;
  const pnl      = await executeTrade(signal.direction);
  barry.recordTradeResult(genomeId, pnl); // auto-evolves every 10 trades
}

// After evolve() — sync to ArchetypeV3:
const [best, second] = barry.breedPair();
await archetypeV3.breedArchetypes(best, second);
```

## ArchetypeV3 Wiring (now complete)

**`barry/archetypeConnector.ts`** — `ArchetypeConnector` class:
- `bootstrap(barry)` — creates on-chain archetypes for initial genome pool
- `recordTrade(genomeId, pnlUsd)` → `ArchetypeV3.recordTrade(id, milliUsd, win)`
  Fire-and-forget, never blocks the trade loop
- `syncEvolution(barry)` → `breedArchetypes()` when parents have 10+ on-chain trades,
  `createArchetype()` as fallback (first gen, immigrants, breeding cooldown)

**Param mapping** (14 genome params → 5 on-chain ArchetypeV3 params):

| On-chain param    | From genome param   | Formula                  |
|-------------------|---------------------|--------------------------|
| lookback [1–600]  | maFast              | ×6                       |
| thresholdBP [10–1000] | patternSensitivity | ×1000               |
| riskMultiplierBP [50–300] | riskPerTrade | ×6000              |
| cooldown [1–600]  | momentumWindow      | ×10                      |
| explorationBP [10–2000] | curiosity     | ×2000                    |

The other 9 params live off-chain in Barry only.

**`index.ts` changes:**
- Barry + ArchetypeConnector instantiated after `verifyConnection()`
- Per-tick: `barry.updatePrices()` + `barry.perceive()` logged as advisory signal
- After `didExecute=true`: PnL computed from pre/post balance snapshot,
  → `barry.recordTradeResult()` + `archetypeConnector.recordTrade()`
  → if `barry.shouldEvolve()`: `barry.evolve()` + `archetypeConnector.syncEvolution()`

**`config.ts`**: `ARCHETYPE_V3_ADDRESS` env var → `CONTRACTS.archetypeV3`
When unset, Barry runs fully off-chain (no gas, no sync).

## What Still Needs Wiring

- `_readUpstream()` stub in `weaver.ts` → real upstream feed (social velocity, on-chain flows)
- Deploy `MimicArchetypeV3.sol` and set `ARCHETYPE_V3_ADDRESS=<deployed addr>` in `.env`
- Authorize the CLEAN-BOT wallet: `archetypeV3.authorizeCaller(walletAddress)`

## No New Dependencies

Zero external imports. `genome.ts` uses `Math.random()` for IDs.
All `console` type errors are pre-existing missing `@types/node` — resolved by `npm install`.
