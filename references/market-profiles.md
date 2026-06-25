# Market Profiles

## Default: us_equity

Use `us_equity` when the user asks about U.S. stocks, ETFs, U.S. indices, NYSE/Nasdaq-listed securities, or does not specify a market.

Characteristics:

- High liquidity for large caps and ETFs.
- Long historical datasets.
- Splits/dividends are common; adjusted prices are preferred for daily/weekly/monthly analysis.
- Trend, momentum, and volume-confirmed breakouts receive the highest default prior weights.
- Short-selling, options, earnings gaps, and sector rotation can materially affect interpretation.

Default signal weights are defined in references/statistical-weighting.md.

## Branching Rule

When another market is requested, create or use a branch profile that modifies only the assumptions that differ from U.S. equities:

```yaml
market: crypto_spot
base_profile: us_equity
overrides:
  session: 24_7
  volume_reliability: exchange_dependent
  timeframe_weights:
    short: { hourly: 0.55, daily: 0.30, weekly: 0.12, monthly: 0.03 }
  signal_weights:
    volatility_regime: 0.11
    volume_confirmation: 0.10
  cautions:
    - fragmented liquidity
    - exchange-specific volume
    - weekend regime changes
```

## Candidate Branch Adjustments

- A-shares: account for price limits, T+1 trading, retail participation, policy/news sensitivity, suspension risk, northbound flows when available, and different turnover behavior.
- Hong Kong equities: account for China macro/policy exposure, lower liquidity in small/mid caps, different trading holidays, and FX linkage.
- Futures: account for contract rolls, margin, leverage, tick size, expiry, contango/backwardation, and session structure.
- Forex: account for 24/5 trading, macro calendars, carry, central-bank risk, and weaker centralized volume data.
- Crypto: account for 24/7 trading, fragmented exchanges, funding rates, liquidations, and exchange-specific volume quality.

Do not silently reuse U.S. equity weights for another market without noting that the market branch is provisional.
