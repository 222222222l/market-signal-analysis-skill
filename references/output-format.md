# Output Format

Use concise professional Chinese when the user writes in Chinese; otherwise match the user's language.

## Required Sections

1. Data and horizon
   - symbol/asset
   - market profile
   - data range and frequency
   - inferred horizon: short-term, mid-term, or long-term
   - confidence level

2. Probability view
   - buy probability
   - sell probability
   - hold/neutral probability
   - probability basis: prior-only, calibrated with historical hit analysis, or insufficient data

3. Matched bullish items
   - timeframe
   - signal
   - strength
   - historical hit stats when available

4. Matched bearish/risk items
   - timeframe
   - signal
   - strength
   - historical hit stats when available

5. Multi-timeframe read
   - hourly
   - daily
   - weekly
   - monthly

6. Risk and invalidation
   - data limitations
   - signals that would invalidate the current read
   - transaction cost/slippage caveat

## Probability Wording

Use wording like:

```text
技术面买入概率：62%
技术面卖出概率：24%
观望/中性概率：14%
置信度：中等
```

Avoid wording like:

```text
一定上涨
稳赚
必买
无风险
```

## If Data Is Insufficient

Do not fabricate a numeric probability. Use:

```text
当前数据不足以输出可靠概率。我可以识别到的静态信号是...，但缺少...，因此只能给出低置信度方向性观察。
```

## Trend-Stage Questions

When the user asks where a trend ends, whether an uptrend/downtrend is still intact, or how to use Vegas/ATR/MA levels, use this compact structure in addition to any probability view:

1. Data, horizon, and confidence.
2. Current trend stage: base, early reversal, healthy uptrend, acceleration, distribution/fatigue, trend break, or downtrend.
3. Key levels:
   - short warning level
   - strong warning level
   - mid-trend break level
   - formal main-trend end level
4. Weighted dashboard:
   - trend structure / MA stack
   - Vegas channel
   - momentum and relative strength
   - breakout/support structure
   - volume/turnover confirmation
   - MACD/RSI/KDJ confirmation
   - volatility and ATR trailing risk
5. Bullish evidence versus bearish/risk evidence.
6. What would upgrade the trend and what would downgrade it.
7. Risk-control language matched to the user's horizon.

## A-Share ETF Macro-Trading Questions

When the user asks about A-share broad ETFs, sector ETFs, index stabilization, operator-capital behavior, ETF-share contraction, turnover concentration, retail-loss breadth, or when ordinary investors can hold/exit ETFs, add this compact dashboard:

1. Data, horizon, and confidence.
2. A-share regime: policy-floor repair, range-stabilized liquidity extraction, main-line acceleration, crowded distribution, broad breakdown, or post-washout accumulation.
3. Broad ETF holdability score: 0-100, with the main supporting and opposing evidence.
4. Sector ETF main-line score when relevant: 0-100, with crowding/distribution risk.
5. Operator-capital pattern: broad support, range support with liquidity extraction, crowded distribution, or defensive de-risking.
6. Ordinary-investor action: batch hold, small follow, short tactical only, reduce, or wait in cash.
7. Hard exit signals and re-entry signals.

Do not say an ETF is low-risk merely because the index is stable. Require confirmation from breadth, ETF shares, turnover concentration, leader behavior, policy/liquidity support, and trend structure.

## Official Data Questions

When official government, central-bank, exchange, regulator, or official statistical data materially affects the conclusion, add this compact verification block:

1. Official data used.
2. Headline read.
3. Key sub-components and weights.
4. Data quality score: 0-5.
5. Estimated bias/water range and reconstructed range when possible.
6. Cross-checks confirming the official signal.
7. Cross-checks contradicting the official signal.
8. Likely reason for contradiction.
9. Market implication and confidence adjustment.

Never present a top-line official number as decisive if the sub-components, methodology, or independent cross-checks are unavailable.
