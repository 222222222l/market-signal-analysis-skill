# Fourier Cycle Analysis

Use this reference when a request asks about Fourier transform, FFT, spectral analysis, frequency-domain signals, hidden cycles, dominant cycles, cycle stability, denoising, Fourier trend lines, high-frequency noise, frequency-domain correlation, or Fourier features for market models.

Fourier analysis is a rhythm and risk tool, not a standalone predictor. It should answer:

- Is the current move dominated by trend, swing-cycle, shock, or noise?
- Are recently observed cycles stable across rolling windows or only one-off artifacts?
- Does frequency-domain evidence confirm or weaken the existing macro/industry/technical cycle view?
- Should position size, trading frequency, or entry timing be adjusted because noise energy is rising?

Do not use a single FFT peak as a buy/sell signal. Markets are non-stationary; cycle length, amplitude, and phase drift as liquidity, policy, positioning, and industry fundamentals change.

## Conceptual Decomposition

Treat a liquid market series as:

```text
observed move = low-frequency trend + medium-frequency cycle + shock + high-frequency noise
```

Frequency-domain interpretation:

| Band | Market Meaning | Practical Use |
| --- | --- | --- |
| Low frequency | Main trend, slow liquidity or earnings cycle, long risk-appetite regime | Trend confirmation and regime filter. |
| Medium frequency | Swing cycle, sector rotation rhythm, inventory/order/rebalance rhythm | Pullback timing only when major trend agrees. |
| High frequency | Noise, event disturbance, liquidity fragmentation, short-term crowding | Position-size and trade-frequency control. |

## Data Preparation

Prefer stationary or detrended inputs:

- Log returns: `r_t = ln(P_t / P_{t-1})`.
- Detrended log price when the objective is a Fourier trend line.
- Volume growth/change rate, turnover, realized volatility, relative strength, ETF NAV returns, spread changes, or valuation/earnings-revision changes when relevant.

Avoid directly running FFT on raw price and then calling the lowest-frequency component a "cycle"; raw prices often embed trend, splits, inflation, regime shifts, and structural growth.

Minimum practical windows:

| Horizon | Rolling Window | Typical Question |
| --- | ---: | --- |
| Short-term | 60-120 trading days | Is there a recent trading rhythm or noise surge? |
| Medium-term | 252 trading days | Is a 1-6 month sector/ETF cycle recurring? |
| Long-term | 504-756 trading days | Is a multi-year macro/industry rhythm visible enough to use as weak prior? |

Use rolling windows. Do not run one static multi-year FFT and infer a permanent 30-day or 43-day cycle.

## Rolling FFT Workflow

1. Choose the input series and horizon.
2. Clean missing data, corporate-action gaps, duplicate timestamps, and impossible values.
3. Transform into log returns or detrended series.
4. Demean the series. Apply a window such as Hann/Hanning to reduce spectral leakage.
5. Run FFT or real FFT.
6. Convert frequencies into periods: `period = 1 / frequency`.
7. Ignore `freq = 0`, periods shorter than practical trading costs allow, and periods longer than roughly half the window length.
8. Record dominant peaks by power share, not only by absolute maximum.
9. Roll the window forward and test whether the same period band repeatedly appears.
10. Compare the inferred phase with price/trend behavior, but treat phase as a probability rhythm, not a deterministic clock.

Stability rule:

- High reliability: the same period band appears in at least 3 consecutive or nearby windows, with similar phase behavior and no contradiction from trend/breadth/fundamentals.
- Medium reliability: the band appears in several windows but amplitude or phase drifts.
- Low reliability: the peak appears once, only after parameter searching, or disappears after a small window change.

## Fourier Trend Line

Use Fourier low-pass filtering as a trend extraction tool:

1. Take log price.
2. Run FFT on a rolling window.
3. Keep only the lowest-frequency components that represent the target horizon.
4. Inverse-transform back into the time domain.
5. Use the reconstructed line as a smoothed trend line.

Decision rules:

| State | Interpretation | Action Bias |
| --- | --- | --- |
| Price above Fourier trend line and line slope up | Trend is supported | Hold or small add if other evidence agrees. |
| Price above line but line slope flat | Trend momentum is cooling | Avoid chasing; wait for pullback or renewed slope. |
| Price below line and line slope down | Trend damage | Reduce exposure or require right-side repair. |
| Price far above or below line | Emotional overextension risk | Do not use distance alone; combine with breadth, valuation, volume, and support/resistance. |

Avoid full-sample leakage. A historical chart may use only data known up to each date when drawing the Fourier trend line for backtesting.

## Cycle Pullback Framework

Use medium-frequency cycles only as a timing overlay:

1. Identify a stable medium-frequency band, for example 30-40 trading days.
2. Extract the band using a rolling band-pass reconstruction.
3. Require the major trend to agree with the trade direction.
4. Consider staged entry when the cycle component turns up from a low zone and price/breadth stop deteriorating.
5. Consider staged reduction when the cycle component approaches a high zone and momentum/breadth weaken.

Rules:

- If trend and cycle conflict, trend dominates.
- If fundamentals or liquidity regime deteriorates, downgrade the cycle signal.
- If high-frequency noise energy is rising sharply, reduce position size even when the cycle looks favorable.

## Noise Energy and Risk Control

Compute frequency-band energy shares:

```text
low_energy_share = sum(power in low-frequency band) / total_power
mid_energy_share = sum(power in medium-frequency band) / total_power
high_energy_share = sum(power in high-frequency band) / total_power
```

Interpretation:

| Signal | Meaning | Risk Response |
| --- | --- | --- |
| Rising low-frequency energy with positive trend | Trend persistence improving | Increase patience; avoid premature exit. |
| Stable medium-frequency energy | Tradable rotation rhythm may exist | Use pullbacks only if trend agrees. |
| Rising high-frequency energy | Noise, event risk, or liquidity disturbance increasing | Lower leverage, reduce single-trade size, avoid overtrading. |
| All bands unstable | Structure is noisy or regime is shifting | Lower confidence and wait for clearer confirmation. |

Common high-frequency-noise catalysts: earnings clusters, policy meetings, CPI/PCE/NFP/FOMC, options expiration, index rebalancing, geopolitical shocks, liquidity squeezes, and rumor-driven markets.

## Frequency-Domain Correlation

Use frequency-domain or multi-horizon correlation to test diversification:

- Short-cycle correlation: do assets move together in daily/weekly risk-on/risk-off bursts?
- Medium-cycle correlation: do sectors rotate together over 1-3 month swings?
- Low-frequency correlation: do assets share the same dollar-liquidity, policy, inflation, or capex regime?
- Crisis resonance: do normally diversified assets become low-frequency synchronized when liquidity tightens?

Do not rely only on full-sample Pearson correlation. If two assets are low-frequency synchronized, they may fail as hedges during macro stress even if daily correlation looks modest.

## Macro Applications

Use FFT only when enough structured time series exist:

- Dollar liquidity: DXY, real yields, reserve balances, ON RRP, TGA, credit spreads, financial conditions, broad equity index returns.
- Inflation and growth rhythm: CPI/PCE components, ISM, PMI, payroll breadth, oil/commodity changes.
- Treasury and funding cycle: bill/coupon issuance, auction dates, term premium, SOFR-IORB spread, repo stress.
- Commodity and energy: inventory, seasonality, spreads, realized volatility, forward curves.

Macro use should be conservative:

- Long cycles are priors, not timing signals.
- Policy regime breaks can invalidate past cycle frequency.
- Compare FFT evidence with official-data verification, liquidity plumbing, actor optimal paths, and special-date event risk.

## Micro and Sector Applications

For stocks, ETFs, sectors, and themes, use Fourier analysis on:

- Relative strength versus benchmark.
- Turnover or volume change.
- Realized volatility and intraday range.
- Breadth such as constituents above MA20/MA50/MA120.
- Earnings-revision or order/backlog proxies when available.

Best-fit use cases:

- Sector ETF rotation rhythm.
- High-beta theme overextension and pullback timing.
- Noise detection before or after major announcements.
- Portfolio co-movement across crowded themes.

Weak use cases:

- Illiquid small caps with discontinuous trading.
- Newly listed stocks with too few bars.
- Price-limit dominated data where true volatility is censored.
- Series with major structural breaks, suspensions, or policy resets.

## Integration With Multi-Cycle Bayesian Overlay

Fourier evidence can adjust the reliability of the sector market cycle or liquidity cycle layer; it should rarely create a new thesis by itself.

Suggested adjustments:

| Fourier Evidence | Bayesian Treatment |
| --- | --- |
| Stable low-frequency trend agrees with macro/industry/technical evidence | Increase relevant cycle-layer reliability by `+0.05` to `+0.15`, capped at `1.0`. |
| Stable medium-frequency pullback rhythm agrees with trend and breadth | Add `+0.05` to `+0.15` logit for timing confidence, not fundamental upside. |
| High-frequency noise share surges | Subtract `0.05` to `0.25` logit from position confidence or reduce suggested position size. |
| FFT peak appears once or requires parameter search | No positive adjustment; mention as low-quality observation only. |
| Frequency-domain correlation shows hedge failure | Increase downside/tail vulnerability and reduce diversification confidence. |

Do not double-count:

- If the same price trend already contributed to technical momentum, FFT trend confirmation should adjust reliability, not add a separate large bullish score.
- If high-frequency noise comes from a known special date, report it through both lenses but count the risk once.

## Fourier Features for Quant Models

For machine-learning or statistical models, use periodic features when the calendar rhythm is known:

```text
sin(2*pi*t/T), cos(2*pi*t/T)
```

Possible `T` values:

- Weekday effect.
- Month-end or quarter-end.
- Earnings season.
- Intraday time bucket.
- Macro release cadence.
- Options expiration or futures delivery cycle.

Fourier features are safer when they encode known calendar periodicity than when they are mined from noisy prices without validation.

## Validation and Caveats

Require:

- Rolling-window stability.
- Sample-out or forward-window validation when enough history exists.
- Comparison with a simple moving-average or momentum baseline.
- Transaction-cost and turnover check.
- No future-data leakage in filtered trend lines.
- No parameter fishing across many window lengths without penalty.

Downgrade confidence when:

- The market regime changed materially.
- Liquidity or policy broke the historical rhythm.
- The signal disappears after a small window change.
- The series has censored volatility, suspensions, or frequent limit-up/limit-down days.
- The FFT conclusion conflicts with strong fundamentals, breadth, or liquidity evidence.

## Output Add-On

When Fourier analysis materially affects the answer, add:

1. Input series, date range, frequency, and window length.
2. Data transform used: returns, detrended log price, volatility, volume change, relative strength, or breadth.
3. Dominant period bands and rolling stability.
4. Energy split: low, medium, high frequency.
5. Fourier trend-line state when used.
6. How the FFT evidence changes the existing cycle/Bayesian view.
7. Invalidation: what signal disappearance, trend break, liquidity change, or data contradiction would reduce confidence.
