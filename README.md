# Market Signal Analysis Skill

A Codex skill for causal, probability-aware analysis of stocks, ETFs, sectors, indices, and liquid macro markets.

It combines technical structure, fundamentals, breadth, valuation, liquidity, policy, actor incentives, cycles, event risk, and data-quality checks without forcing every question through every framework.

## Design

The skill uses a progressive-disclosure architecture:

1. `SKILL.md` contains only first principles, the common workflow, module routing, composition rules, and the minimum output contract.
2. `references/` contains specialized frameworks loaded only when the question needs them.
3. `scripts/` contains deterministic analysis and architecture-validation helpers.

The default rule is one primary module plus no more than two overlays. Extra modules should be loaded only when they can change the decision, probability, or risk boundary.

## Core Principles

- Fix the market and decision horizon before choosing signals.
- Gate conclusions on data source, freshness, adjustment status, and sample length.
- Separate state, flow, and expectation.
- Build a causal transmission chain before relying on correlations or historical analogies.
- Compare actors' words with costly, repeated, observable actions.
- Deduplicate correlated evidence and condition probabilities on base rates and regimes.
- Label probabilities as empirical, model-implied, or scenario weights.
- Give paths, ranges, time windows, and invalidation conditions instead of unsupported point targets.
- State the strongest opposing case and what evidence would falsify the preferred view.

## Coverage

- OHLCV, trend, breakout, momentum, volume, MACD, RSI, KDJ, divergence, volatility, and multi-timeframe structure.
- Granville and Vegas rules, trend-stage classification, ATR/Chandelier risk levels, reversal and reclaim/retest signals.
- Sector breadth, leadership, rotation, crowding, high-valuation narrative bubbles, and exhaustion risk.
- A-share broad/sector ETF regimes, index-versus-breadth divergence, turnover concentration, and policy-capital effects.
- Single-stock fundamentals, valuation, announcement/news quality, governance, capital supply, and technical boundaries.
- Official-data decomposition, measurement-bias ranges, revisions, and independent cross-checks.
- Policy-maker and market-decision-maker incentives, direct/indirect games, and Nash-like equilibrium analysis.
- Economic, credit, liquidity, inventory, capex, industry, and market-cycle overlays.
- Rolling Fourier/FFT rhythm, HP/BK pre-filtering, endpoint-safe detrending, cycle stability, noise energy, and frequency-domain correlation.
- U.S. liquidity, Fed policy, Treasury issuance, term premium, reserve plumbing, macro stress, and cross-asset transmission.
- Futures/options expiry, FOMC and macro releases, Treasury auctions, index rebalances, and thin-liquidity dates.
- Optional Transformer/TFT market-model and publishable research design.

## Installation

```powershell
git clone https://github.com/222222222l/market-signal-analysis-skill.git $env:USERPROFILE\.codex\skills\market-signal-analysis
```

To update an existing clone:

```powershell
git -C $env:USERPROFILE\.codex\skills\market-signal-analysis pull
```

Reload Codex skills if the environment does not discover changes automatically.

## Usage Examples

```text
Use market-signal-analysis to determine whether this ETF is in a healthy pullback or a formal trend break.
```

```text
Analyze whether this high-valuation sector is expensive but strengthening or expensive and weakening.
```

```text
Classify U.S. liquidity and Fed policy, then map the result into Nasdaq, Treasuries, USD, and gold scenarios.
```

```text
Verify the official employment data, model policy and market actors' best responses, and identify the likely equilibrium.
```

## Repository Layout

```text
.
|-- SKILL.md                         # compact router and invariants
|-- agents/
|   `-- openai.yaml                 # Codex UI metadata
|-- references/
|   |-- signal-taxonomy.md
|   |-- statistical-weighting.md
|   |-- market-profiles.md
|   |-- output-format.md
|   |-- trend-stage-analysis.md
|   |-- sector-bubble-analysis.md
|   |-- a-share-macro-trading-model.md
|   |-- single-stock-fundamental-technical-analysis.md
|   |-- official-data-verification.md
|   |-- actor-optimal-path-analysis.md
|   |-- cycle-overlay-analysis.md
|   |-- fourier-cycle-analysis.md
|   |-- us-macro-liquidity-fed-policy.md
|   |-- macro-stress-derivative-analysis.md
|   |-- special-date-event-risk.md
|   |-- deep-learning-extension.md
|   `-- research-and-optimization-roadmap.md
`-- scripts/
    |-- analyze_ohlcv.py
    |-- train_market_transformer_demo.py
    `-- validate_skill_graph.py
```

## Validation

Run the architecture check after modifying routes or references:

```powershell
python scripts/validate_skill_graph.py
```

Run the Codex skill validator when available:

```powershell
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

The architecture validator enforces a compact `SKILL.md`, verifies that every specialized reference is routed directly from it, and catches broken or orphaned references.

## Disclaimer

This skill provides uncertain market analysis and decision support, not guaranteed returns or personalized financial advice. Validate current data, liquidity, costs, tax constraints, and risk capacity before acting.
