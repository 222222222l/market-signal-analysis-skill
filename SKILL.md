---
name: market-signal-analysis
description: Market-signal analysis for stocks, ETFs, sectors, indices, and liquid markets. Use for OHLCV or structured market data to compute indicators, evaluate trend stage and trend-end levels including Granville moving-average rules, analyze single-stock fundamentals plus technicals, filter noisy company news from hard operating signals, estimate short-term and long-term price zones, apply multi-cycle overlay analysis from economic/Kondratieff/dollar-liquidity cycles to industry and sector cycles with Bayesian buffer-cushion and black-swan overlays, verify official government and regulator data through component decomposition, bias/water estimation, and cross-validation, analyze A-share broad/sector ETF macro trading regimes such as index stabilization, ETF-share contraction, turnover concentration, main-line crowding, and retail risk control, and assess multi-timeframe buy/sell/hold signals, sector rotation, breadth, sentiment, liquidity, macro-regime context, and cautious probability-weighted evidence.
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

## Trend Stage and Trend End Analysis

When the user asks about trend direction, stage trend, uptrend/downtrend ending, Vegas channel, Granville rules, channel position, formal trend break, "where the trend ends", "whether the main rise is over", staged stop/risk levels, trend-following holding rules, or Chinese-language phrases for main-rise, cooling-off, breakdown, or topping, read references/trend-stage-analysis.md before producing a view.

Use trend-stage analysis as a weighted evidence dashboard, not as a one-indicator verdict. Select or reweight indicators by asset type and market structure: broad indices need MA/Vegas/breadth confirmation; high-beta A-share themes need MA20/MA50, ATR/Chandelier, failed-breakout, turnover heat, and breadth; crypto/futures need wider volatility and leverage/liquidation context; low-liquidity small caps need lower confidence.

Separate early risk-reduction signals from formal trend-end signals. In fast or parabolic trends, do not wait for the daily Vegas channel to manage risk; use MA20/MA50, 2ATR/3ATR Chandelier, Donchian 20/55-day lows, volume, and relative strength first, then use EMA144/169 and weekly structure for main-trend invalidation.

## Sector, Theme, and Bubble Momentum

When the user asks about a sector/board/theme, market main line, bubble-like trend, sentiment support, "whether to be bold or cautious", "whether the theme can keep rising", "double top versus second breakout", or "whether a sector can double", read references/sector-bubble-analysis.md before producing a view.

Use a two-score framework:

- Trend/momentum score T: measures whether price, relative strength, breadth, leadership, volume, fundamentals, and policy/liquidity still support risk-taking.
- Bubble-risk score R: measures whether valuation, short-term overextension, turnover/fund inflow heat, breadth deterioration, failed breakouts, insider sell-downs, and consensus euphoria make the trend fragile.

Do not use valuation alone as a timing signal in a bubble momentum regime. Treat "expensive but strong" differently from "expensive and weakening"; require price/volume deterioration, breadth deterioration, or failed-breakout evidence before calling a trend broken.

## A-Share Macro ETF Trading Model

When the user asks about A-share broad-index ETFs, sector-index ETFs, CSI 300, CSI A500, SSE 50, STAR 50, ChiNext, "index range-bound while retail accounts bleed", national-team or operator-capital behavior, ETF share contraction, turnover concentration, main-line crowding, when ordinary investors can hold ETFs with lower risk, or when to exit after abnormal capital behavior, read references/a-share-macro-trading-model.md before producing a view.

Use the model as an evidence-based regime classifier, not as proof of a coordinated manipulation scheme. Combine it with trend-stage analysis for index levels and sector-bubble analysis for crowded main-line ETFs. For ordinary investors, prioritize ETF holdability, hard exit conditions, and whether price, breadth, ETF shares, and leader behavior confirm each other.

## Official Data Verification

When the analysis relies on government, central-bank, exchange, regulator, or official statistical data such as CPI/PCE, GDP, employment, wages, fiscal data, credit aggregates, money supply, FX reserves, trade, property, industrial output, PMI, official fund-flow data, or regulatory disclosures, read references/official-data-verification.md before assigning probabilities.

Never use an official headline number alone as a high-confidence market signal. Decompose sub-components, estimate possible measurement bias or "water", cross-check with independent data, and explain contradictions. If sub-component or cross-check data is missing, reduce confidence and state the limitation.

## Multi-Cycle Overlay Analysis

When the user asks about economic cycles, Kondratieff cycles, dollar tides, liquidity cycles, credit cycles, inventory cycles, industry cycles, sector cycles, cyclical resonance, cycle weighting, Bayesian trend probability, buffer cushions, black-swan risk, macro-financial regime, or which industries are in rising/declining prosperity phases under multiple cycles, read references/cycle-overlay-analysis.md before producing a view.

Use cycle analysis as a structured prior and confirmation layer, not as deterministic prophecy. Long cycles such as Kondratieff/technology-capex waves should receive low tactical weight unless confirmed by current orders, pricing power, capacity utilization, profit revisions, and market relative strength. For macro-financial analysis, always reconcile five directions: fundamentals/cycles, sentiment/bubble, official-data water, buffer cushions, and jump-event risk. Avoid double-counting the same evidence across macro, industry, and technical buckets.

## Single-Stock Fundamental and Technical Analysis

When the user asks about an individual stock's fundamentals, whether to cut losses or hold, whether company news is real catalyst or noise, whether a "good story" changes the investment thesis, where short-term or long-term price may go, or how to combine financial statements, announcements, valuation, and technical levels, read references/single-stock-fundamental-technical-analysis.md before producing a view.

Treat company announcements, market rumors, and concept labels as evidence with different reliability. Do not upgrade a stock because of broad narrative words such as cooperation, layout, empowerment, robot, AI, semiconductor, low-altitude, overseas expansion, or strategic transformation unless the signal has a verifiable amount, timeline, delivery path, financial-statement impact, and price/volume confirmation. Separate "company is not bad" from "stock has positive expected return from this price."

## U.S. Macro Liquidity and Fed Policy

When the user asks about U.S. liquidity, Fed hawkish/dovish direction, rate-cut/rate-hike probability, Treasury issuance, term premium, reserve scarcity, SOFR-IORB pressure, ON RRP, TGA, QT/QE, discount-window borrowing, primary credit, recession versus inflation, or macro transmission into equities/bonds/gold/USD, read references/us-macro-liquidity-fed-policy.md before producing a view.

When the user asks about early crisis detection, first-derivative or second-derivative macro signals, marginal deterioration, acceleration, contagion, transmission chains, or whether a liquidity/funding stress signal is only local or becoming systemic, also read references/macro-stress-derivative-analysis.md.

Classify the macro state before labeling the Fed as hawkish or dovish. Use five jointly evaluated variable groups: inflation/labor momentum, fiscal issuance and term premium, liquidity plumbing, AI/capex and real-demand support, and market transmission. Do not treat one data release or one headline as sufficient evidence for a regime change.

## Deep Learning Extension

When the user asks about Transformer models, deep learning, pretraining, fine-tuning, dynamic indicator weights, long-context daily sequences, target-price prediction, return-distribution prediction, or quantitative decision models, read references/deep-learning-extension.md before designing or coding the model.

Use the extension as a decision-first design: predict normalized returns, risk, and position utility rather than optimizing only next-close price error. Prefer single-timeframe long-context daily modeling for the first version when the user wants self-attention over long continuous samples.

When the user asks about publishable research positioning, related work, literature-backed improvements, benchmark datasets, standard training/evaluation datasets, ablation plans, or paper-quality experimental design, read references/research-and-optimization-roadmap.md.

## Required Signal Families

Always consider these families when data supports them:

- Trend and breakout: moving average slope/cross, Granville moving-average buy/sell rules, price above/below MA20/MA50/MA200, 20-day/55-day/channel breakout, support/resistance break.
- Trend stage and trend-end structure: MA20/50/120/200 stack and slope, daily Vegas EMA144/169, long-cycle EMA576/676 when enough data exists, 2ATR/3ATR Chandelier levels, Donchian 20/55-day highs/lows, recover/fail behavior, and weekly confirmation.
- Momentum and relative strength: 3/6/12-month momentum for mid/long horizons, rate of change, trend continuation.
- Volume confirmation: volume expansion on breakout, volume drying on pullback, price-volume divergence, relative volume.
- Sector breadth and rotation: share of constituents above MA20/MA50/MA120, new highs versus new lows, advance/decline ratio, leader versus laggard contribution, intra-sector rotation continuity, and whether gains are broad or only driven by one or two leaders.
- A-share ETF macro-trading regime: broad-index ETF share changes, index trend versus median-stock performance, top turnover concentration, theme turnover share versus market-cap share, leader high-volume distribution, policy/liquidity support confirmation, and hard downgrade/exit signals for broad and sector ETFs.
- Bubble momentum and exhaustion: overextension above MA20/MA50, gap/limit-up clustering, failed second breakouts, double-top invalidation, long upper shadows, blow-off volume, fund inflow/financing/turnover heat, and insider sell-down or inquiry-transfer pressure.
- Multi-cycle overlay: economic growth/inflation/credit phase, Kondratieff or technology-capex background, dollar liquidity tide, domestic policy and fiscal impulse, inventory and capex cycle, industry supply-demand and pricing cycle, sector market cycle, market sentiment and bubble heat, official-data water, buffer cushions, black-swan vulnerability, and Bayesian posterior trend probability after cross-validation.
- Official-data verification: headline versus sub-components, definition/sample/revision checks, estimated bias/water range, reconstructed data range, cross-checks with market prices and independent proxies, and contradiction diagnosis before turning government data into a trading signal.
- Single-stock fundamentals and event quality: revenue, deducted profit, gross margin, operating cash flow, debt and liquidity, segment revenue/profit mix, customer concentration, governance, pledge/reduction/buyback/supply pressure, valuation versus growth, and whether announcements can enter earnings or cash flow.
- U.S. macro liquidity and Fed policy: inflation second derivative, ECI/wage momentum, payroll breadth, unemployment trend, QRA and Treasury supply, ACM/term-premium impulse, SOFR-IORB and repo pressure, ON RRP/TGA/reserve balance changes, discount-window primary/secondary/seasonal credit, SRF usage, first-derivative and second-derivative stress acceleration, AI/capex support, MOVE/VIX and risk-parity/CTA transmission.
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
- references/trend-stage-analysis.md: trend-stage taxonomy, Vegas channel rules, Granville moving-average rules, fast-trend risk stack, asset-specific weighting, trend-end levels, and trend question output format.
- references/sector-bubble-analysis.md: sector/theme breadth, rotation, leadership, bubble momentum score, bubble-risk score, bold/cautious decision matrix, and A-share policy/liquidity caveats.
- references/a-share-macro-trading-model.md: A-share broad/sector ETF macro-trading regime classifier for index stabilization, ETF-share contraction, retail-loss breadth, turnover concentration, main-line crowding, operator-capital inference, ETF holdability scores, and hard exit/re-entry rules.
- references/official-data-verification.md: official government/regulator data verification framework for component decomposition, estimated bias/water, reconstructed ranges, cross-validation, contradiction handling, and confidence adjustment.
- references/cycle-overlay-analysis.md: multi-cycle hierarchy from long economic/Kondratieff/dollar-liquidity cycles to industry/sector cycles, macro-financial five-direction checklist, buffer-cushion scoring, black-swan overlay, horizon-specific weights, Bayesian posterior trend probability, cross-validation, and industry-cycle classification.
- references/single-stock-fundamental-technical-analysis.md: single-stock workflow for filtering noisy news, identifying core operating signals, scoring fundamentals, combining valuation with technical levels, and giving short-term/long-term price zones and risk-control decision trees.
- references/us-macro-liquidity-fed-policy.md: U.S. macro liquidity dashboard, Fed policy-regime state machine, Treasury issuance and term-premium analysis, SOFR-IORB/reserve plumbing checks, and macro asset-playbook mapping.
- references/macro-stress-derivative-analysis.md: level, first-derivative, and second-derivative macro stress framework for early crisis warning, acceleration scoring, and transmission-chain mapping.
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
