# Statistical Weighting

## Horizon Mapping

Use the user's language to select a horizon:

| User wording | Target horizon | Primary windows | Timeframe weights |
| --- | --- | --- | --- |
| short, short-term, swing, intraday, this week | intraday to 10 trading days | hourly 60-240 bars, daily 60-252 bars | hourly 0.45, daily 0.35, weekly 0.15, monthly 0.05 |
| mid, medium, intermediate, next weeks | 2 to 12 weeks | daily 126-504 bars, weekly 52-156 bars | hourly 0.10, daily 0.45, weekly 0.35, monthly 0.10 |
| long, long-term, position, investment | 3 to 24 months | weekly 104-260 bars, monthly 60-180 bars | hourly 0.00, daily 0.20, weekly 0.45, monthly 0.35 |

If the requested horizon conflicts with available data, adapt the closest valid horizon and disclose the substitution.

## U.S. Equity Default Signal Family Weights

Use these priors before symbol-specific calibration:

| Signal family | Weight | Reason |
| --- | ---: | --- |
| trend_breakout_ma | 0.24 | Strongest long-sample U.S. evidence among classic technical rules. |
| momentum_relative_strength | 0.18 | Strong intermediate-horizon U.S. equity evidence. |
| volume_confirmation | 0.14 | Improves momentum/breakout interpretation and reversal risk. |
| macd_combo | 0.11 | Useful as trend/momentum confirmation; standalone evidence is weaker. |
| rsi_kdj_oscillator | 0.10 | Useful for exhaustion/timing; penalize isolated signals. |
| divergence | 0.11 | Useful reversal warning when confirmed by price structure and volume. |
| volatility_regime | 0.07 | Controls risk, squeeze/breakout, and probability confidence. |
| multi_timeframe_agreement | 0.05 | Boosts confidence when higher and lower timeframes align. |

Weights must sum to 1.0. Market branches may override these defaults.

## Signal Scoring

For each timeframe and signal family:

1. Assign direction: bullish = +1, bearish = -1, neutral = 0.
2. Assign strength from 0.0 to 1.0 based on recency, magnitude, and confirmation.
3. Multiply by family weight and timeframe weight.
4. Deduplicate correlated signals. Example: MA20 slope and price above MA20 should not both receive full weight unless they add distinct information.
5. Penalize stale signals:
   - Triggered in the latest 1-3 bars: full credit.
   - Triggered 4-10 bars ago: 50%-80% credit.
   - Older than 10 bars: context only unless still structurally active.

Compute:

```text
net_score = sum(weighted_bullish_components) - sum(weighted_bearish_components)
raw_buy_probability = sigmoid(2.6 * net_score)
raw_sell_probability = sigmoid(-2.6 * net_score)
hold_probability = max(0, 1 - abs(raw_buy_probability - raw_sell_probability) * confidence_scale)
```

Normalize buy/sell/hold to sum to 100%.

## Historical Hit Analysis

When sufficient history exists, replace or adjust priors with symbol-specific statistics:

- Define a signal event without lookahead.
- Measure forward returns over the selected horizon.
- Track hit rate, mean return, median return, payoff ratio, Sharpe-like return/volatility, maximum adverse excursion, maximum favorable excursion, and trade count.
- Use walk-forward or train/test splits when possible.
- Apply shrinkage toward the U.S. equity default prior when samples are small.

Minimum sample guidance:

| Sample count | Use |
| ---: | --- |
| fewer than 20 | Do not use as probability evidence; list as anecdotal. |
| 20-49 | Low confidence; shrink at least 70% toward default prior. |
| 50-99 | Medium confidence; shrink 40%-60% toward default prior. |
| 100+ | Higher confidence if out-of-sample performance is stable. |

Use Wilson confidence intervals for hit rate when possible. Penalize rules whose confidence interval includes 50% and whose average return does not exceed estimated costs.

## Confidence

Report confidence as high, medium, low, or insufficient:

- High: enough bars, enough historical signal events, multiple independent signal families align, no major data-quality warnings.
- Medium: adequate bars but limited event history or partial conflict across timeframes.
- Low: small sample, strong conflict, high volatility regime, or reliance on oscillators/divergence alone.
- Insufficient: missing OHLCV, too few bars, unknown adjustment status, or no reliable timeframe.
