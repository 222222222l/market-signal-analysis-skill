---
name: market-signal-analysis
description: Professional technical market signal analysis for stocks, ETFs, sectors/boards, themes, indices, and other liquid investment markets. Use when Codex needs to analyze OHLCV market data, upstream agent/API market data, or user-provided price history to identify buy/sell/hold signals, compute common technical indicators such as volume, moving averages, MACD, RSI, KDJ/stochastic, Bollinger Bands, ATR, momentum, breakout, top divergence, and bottom divergence, score signals across hourly/daily/weekly/monthly timeframes, evaluate sector/theme rotation, breadth, leading-stock strength, bubble momentum, sentiment support, and bubble-risk exhaustion, adapt analysis for short-term/mid-term/long-term user horizons, and produce statistically weighted buy/sell/hold or bold/cautious probabilities with matched signal evidence. Default assumptions and weights target the mature U.S. equity market, with branchable market profiles for other markets.
---

# Market Signal Analysis

## Core Rule

Analyze technical signals only from sufficient OHLCV data or structured upstream agent/API data. If data is missing, stale, too short, split-adjustment status is unknown, or the timeframe cannot be inferred, state the limitation before producing probabilities. Never present technical probabilities as guaranteed returns or personalized financial advice.

## Workflow

1. Identify the market, symbol, asset type, data frequency, data range, and user horizon.
2. Default to `us_equity` when the market is not specified. Use references/market-profiles.md when a different market is specified.
3. Map the user's wording to a horizon:
   - short-term: intraday to 10 trading days.
   - mid-term: 2 to 12 weeks.
   - long-term: 3 to 24 months.
4. Normalize OHLCV data by split/dividend adjustment status when available. Reject or qualify data with impossible OHLC values, missing volume on equity assets, duplicate timestamps, or fewer than the minimum bars in references/statistical-weighting.md.
5. Compute indicators and candidate signals. Use scripts/analyze_ohlcv.py for CSV data, or implement the same schema when data arrives from an upstream agent/API.
6. Score signal families with the U.S. equity default weights in references/statistical-weighting.md unless a market branch overrides them.
7. Calibrate scores with historical hit analysis when enough in-sample data exists. Penalize weak sample sizes, high turnover, high drawdown, high correlation among duplicate indicators, and unvalidated parameter searches.
8. Produce a probability-style technical view with matched evidence, opposing evidence, confidence, and caveats.

## Sector, Theme, and Bubble Momentum

When the user asks about a sector/board/theme, market main line, bubble-like trend, sentiment support, "whether to be bold or cautious", "whether the theme can keep rising", "double top versus second breakout", or "whether a sector can double", read references/sector-bubble-analysis.md before producing a view.

Use a two-score framework:

- Trend/momentum score T: measures whether price, relative strength, breadth, leadership, volume, fundamentals, and policy/liquidity still support risk-taking.
- Bubble-risk score R: measures whether valuation, short-term overextension, turnover/fund inflow heat, breadth deterioration, failed breakouts, insider sell-downs, and consensus euphoria make the trend fragile.

Do not use valuation alone as a timing signal in a bubble momentum regime. Treat "expensive but strong" differently from "expensive and weakening"; require price/volume deterioration, breadth deterioration, or failed-breakout evidence before calling a trend broken.

## Deep Learning Extension

When the user asks about Transformer models, deep learning, pretraining, fine-tuning, dynamic indicator weights, long-context daily sequences, target-price prediction, return-distribution prediction, or quantitative decision models, read references/deep-learning-extension.md before designing or coding the model.

Use the extension as a decision-first design: predict normalized returns, risk, and position utility rather than optimizing only next-close price error. Prefer single-timeframe long-context daily modeling for the first version when the user wants self-attention over long continuous samples.

When the user asks about publishable research positioning, related work, literature-backed improvements, benchmark datasets, standard training/evaluation datasets, ablation plans, or paper-quality experimental design, read references/research-and-optimization-roadmap.md.

## Required Signal Families

Always consider these families when data supports them:

- Trend and breakout: moving average slope/cross, price above/below MA20/MA50/MA200, 20-day/55-day/channel breakout, support/resistance break.
- Momentum and relative strength: 3/6/12-month momentum for mid/long horizons, rate of change, trend continuation.
- Volume confirmation: volume expansion on breakout, volume drying on pullback, price-volume divergence, relative volume.
- Sector breadth and rotation: share of constituents above MA20/MA50/MA120, new highs versus new lows, advance/decline ratio, leader versus laggard contribution, intra-sector rotation continuity, and whether gains are broad or only driven by one or two leaders.
- Bubble momentum and exhaustion: overextension above MA20/MA50, gap/limit-up clustering, failed second breakouts, double-top invalidation, long upper shadows, blow-off volume, fund inflow/financing/turnover heat, and insider sell-down or inquiry-transfer pressure.
- MACD: line/signal cross, histogram acceleration/deceleration, zero-line regime, bullish/bearish divergence.
- RSI: overbought/oversold, centerline confirmation, bullish/bearish divergence, failure swing when detectable.
- KDJ/stochastic: K/D/J cross, high/low zone reversal, overbought/oversold persistence.
- Divergence: top divergence and bottom divergence using price swing highs/lows versus MACD histogram/line, RSI, or KDJ.
- Volatility and risk regime: ATR expansion/contraction, Bollinger Band squeeze/expansion, gap risk when available.
- Multi-timeframe agreement: align hourly, daily, weekly, and monthly signals according to the user's horizon.

## References

Read these files as needed:

- references/research-basis.md: empirical research used to prioritize U.S. equity default weights.
- references/statistical-weighting.md: scoring, horizon windows, sample-size rules, and default weights.
- references/sector-bubble-analysis.md: sector/theme breadth, rotation, leadership, bubble momentum score, bubble-risk score, bold/cautious decision matrix, and A-share policy/liquidity caveats.
- references/signal-taxonomy.md: exact signal definitions and evidence schema.
- references/market-profiles.md: U.S. equity default profile and branch rules for other markets.
- references/output-format.md: required answer format.
- references/deep-learning-extension.md: Transformer/TFT-style pretraining, fine-tuning, dynamic feature weighting, objective functions, and model output schema for quantitative decision support.
- references/research-and-optimization-roadmap.md: paper-oriented related research, executable model optimization roadmap, standard dataset candidates, recommended benchmark plan, and ablation matrix.

## Script

Use `scripts/analyze_ohlcv.py` when the user provides CSV OHLCV data or when upstream agent/API data can be exported to CSV.

```powershell
python scripts/analyze_ohlcv.py --input prices.csv --market us_equity --horizon short
```

Expected columns are `timestamp,open,high,low,close,volume`. Case-insensitive aliases such as `date`, `time`, `o`, `h`, `l`, `c`, and `vol` are accepted. The script returns JSON with indicator snapshots, matched bullish/bearish signals, score components, probabilities, and warnings.

Use `scripts/train_market_transformer_demo.py` when the user asks for a trainable model architecture demo. It expects panel CSV data with at least `timestamp,symbol,market,open,high,low,close,volume`; all additional numeric columns are treated as candidate model features.

```powershell
python scripts/train_market_transformer_demo.py --input panel_daily_features.csv --lookback 256 --horizon 1 --epochs 5
```

The demo outputs expected return, p10/p50/p90 return quantiles, up probability, downside risk, position score, and averaged dynamic feature weights.
