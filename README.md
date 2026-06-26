# Market Signal Analysis Skill

Codex skill for professional technical market analysis across stocks, ETFs, indices, sectors, boards, themes, and other liquid investment markets.

The skill combines classic OHLCV technical analysis with statistical signal weighting, multi-timeframe scoring, sector rotation analysis, and a bubble-momentum framework for markets where valuation alone is not a useful timing tool.

## What It Covers

- Multi-timeframe technical analysis: hourly, daily, weekly, monthly.
- Common indicators: moving averages, MACD, RSI, KDJ/stochastic, Bollinger Bands, ATR, volume, momentum, relative strength, breakout, and divergence.
- Probability-style buy/sell/hold views with matched bullish and bearish evidence.
- Sector and theme analysis: breadth, rotation, leading-stock strength, benchmark-relative strength, volume confirmation, and policy/liquidity caveats.
- Bubble-market analysis: trend/momentum score, bubble-risk score, bold/cautious decision matrix, double-top versus second-breakout interpretation, and exhaustion signals.
- U.S. macro liquidity and Federal Reserve policy-regime analysis: inflation/labor second derivative, Treasury issuance, term premium, SOFR-IORB pressure, ON RRP/TGA/reserves, AI/capex support, and market transmission.
- A-share-specific caveats such as price limits, T+1, retail participation, policy narratives, financing, ETF/fund flows, and large shareholder sell-down announcements.
- Optional deep-learning/Transformer-oriented design guidance for quantitative signal models.

## Installation

Clone this repository into your Codex skills directory:

```powershell
git clone https://github.com/222222222l/market-signal-analysis-skill.git $env:USERPROFILE\.codex\skills\market-signal-analysis
```

If you already have a local copy, update it with:

```powershell
cd $env:USERPROFILE\.codex\skills\market-signal-analysis
git pull
```

Restart Codex or reload skills after installation if your environment does not discover new skills automatically.

## Usage Examples

Ask Codex questions such as:

```text
Use market-signal-analysis to analyze NVDA across daily and weekly timeframes.
```

```text
Analyze whether the AI hardware sector is still in a strong trend or has entered a bubble-risk phase.
```

```text
Quantify whether this sector is broadening or narrowing based on leaders, breadth, volume, and relative strength.
```

```text
Build a cautious/bold decision view for this theme after a second breakout.
```

```text
Classify the current U.S. macro liquidity state and Fed policy bias using inflation, Treasury issuance, SOFR-IORB, reserves, AI capex, and market transmission.
```

## Repository Layout

```text
.
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- references/
|   |-- deep-learning-extension.md
|   |-- market-profiles.md
|   |-- output-format.md
|   |-- research-and-optimization-roadmap.md
|   |-- research-basis.md
|   |-- sector-bubble-analysis.md
|   |-- signal-taxonomy.md
|   |-- statistical-weighting.md
|   `-- us-macro-liquidity-fed-policy.md
`-- scripts/
    |-- analyze_ohlcv.py
    `-- train_market_transformer_demo.py
```

## Key Reference

`references/sector-bubble-analysis.md` contains the sector and bubble-momentum framework:

- Trend/momentum score `T`.
- Bubble-risk score `R`.
- Bold/cautious matrix.
- Double-top and second-breakout interpretation.
- Sector breadth checklist.
- A-share policy and liquidity caveats.

`references/us-macro-liquidity-fed-policy.md` contains the U.S. macro liquidity and Fed policy-regime framework:

- Five-variable dashboard: inflation/labor, fiscal/term premium, liquidity plumbing, AI/capex, market transmission.
- Scenario state machine: baseline bear steepening, inflation bear flattening, fiscal issuance shock, plumbing tightening, traditional recession/disinflation.
- SOFR-IORB, ON RRP, TGA, reserves, SRF/repo, and term-premium rules of thumb.
- Fed reaction and cross-asset playbook mapping.

## Validation

The skill folder follows the Codex skill structure:

- Required `SKILL.md` with YAML frontmatter.
- Optional `agents/` metadata.
- Optional `references/` documentation for progressive disclosure.
- Optional `scripts/` utilities.

## Disclaimer

This skill is for market analysis and decision support only. It does not provide personalized investment advice, guaranteed returns, or risk-free trading signals. Market probabilities should be treated as uncertain scenarios and validated against current data, liquidity, transaction costs, and the user's own risk constraints.
