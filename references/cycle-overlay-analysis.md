# Cycle Overlay Analysis

Use this reference when a request asks about macro cycles, Kondratieff cycles, dollar-liquidity tides, credit/inventory cycles, industry prosperity cycles, sector rotation cycles, multi-cycle resonance, cycle weighting, or Bayesian trend probabilities.

Cycle analysis should improve evidence discipline. It should not turn vague long-cycle stories into deterministic forecasts. Treat long cycles as priors; require current data to confirm them.

## Cycle Hierarchy

Analyze from slow to fast, then reconcile from fast back to slow:

| Layer | Typical Horizon | Main Evidence | Use |
| --- | ---: | --- | --- |
| Kondratieff / technology-capex background | 20-60 years | General-purpose technology, infrastructure waves, commodity supercycles, geopolitical supply chains | Low-frequency prior; not a timing signal by itself. |
| Global dollar tide / external liquidity | 1-7 years | Fed policy, real rates, DXY, U.S. reserves/RRP/TGA, global credit spreads, USD funding stress, capital flows | Affects valuation multiples, EM liquidity, commodities, and high-duration assets. |
| Domestic economic and credit cycle | 1-5 years | GDP/PMI, credit impulse, fiscal impulse, PPI/CPI, property, exports, industrial profits, employment | Sets aggregate demand, pricing power, and risk appetite. |
| Policy and institutional cycle | 3-36 months | fiscal subsidies, procurement, regulation, industrial policy, anti-corruption, supply-side controls, state-capital allocation | Can create or destroy industry demand and valuation support. |
| Industry supply-demand cycle | 3 months-5 years | capacity, utilization, inventory, order backlog, product prices, spreads, capex, import/export volume | Core profit-cycle signal for sectors and stocks. |
| Sector market cycle | 1 week-18 months | relative strength, breadth, turnover, fund flow, earnings revisions, valuation percentile, leadership | Confirms whether investors are pricing the cycle. |
| Single-security cycle | days-24 months | company fundamentals, events, technical stage, float supply, insider actions | Converts cycle view into actionable risk levels. |

## Signal Scoring

For each layer, assign a direction score and reliability:

- Direction score `s`: `+2` strong upswing, `+1` improving, `0` neutral/mixed, `-1` deteriorating, `-2` contraction/stress.
- Reliability `r`: `0.3` weak/noisy, `0.5` partial evidence, `0.7` good evidence, `1.0` high-confidence multi-source confirmation.
- Time alignment: downgrade reliability when the cycle evidence is stale, lagging, or only narrative.

Use current, measurable data where possible:

- Growth: PMI, industrial production, retail sales, exports, fixed asset investment, credit impulse.
- Inflation/pricing: PPI, CPI, commodity prices, product price indices, industry spreads.
- Liquidity: rates, credit spreads, money/credit growth, dollar index, funding stress, equity turnover.
- Industry: capacity utilization, inventory days, backlog, order intake, utilization, revenue and margin revisions.
- Market: relative strength, breadth, volume, valuation, fund flows, earnings revisions.

## Horizon Weights

Select weights by the user's horizon. Normalize weights to 1.0 after removing unavailable layers.

### Short-Term Trading: days to 4 weeks

| Layer | Weight |
| --- | ---: |
| Sector market cycle and technical structure | 0.30 |
| Single-security event/float/liquidity cycle | 0.20 |
| Industry price/inventory short-cycle | 0.20 |
| Domestic policy/liquidity impulse | 0.15 |
| Global dollar tide | 0.10 |
| Long-cycle/Kondratieff background | 0.05 |

### Medium-Term Allocation: 1 to 6 months

| Layer | Weight |
| --- | ---: |
| Industry supply-demand cycle | 0.30 |
| Sector market cycle and earnings revisions | 0.20 |
| Domestic economic/credit cycle | 0.18 |
| Policy/institutional cycle | 0.15 |
| Global dollar tide | 0.10 |
| Long-cycle/Kondratieff background | 0.07 |

### Long-Term Allocation: 6 to 24 months

| Layer | Weight |
| --- | ---: |
| Industry supply-demand and capex cycle | 0.28 |
| Domestic economic/credit cycle | 0.20 |
| Policy/institutional cycle | 0.17 |
| Long-cycle/Kondratieff or technology-capex background | 0.15 |
| Global dollar tide | 0.10 |
| Sector market cycle | 0.07 |
| Single-security cycle | 0.03 |

Do not over-weight a long cycle for a short-term decision. Do not over-weight technical momentum for a long-term industry prosperity call.

## Overlay Score

Calculate an effective cycle score:

```text
effective_weight_i = weight_i * reliability_i
cycle_score = sum(effective_weight_i * direction_score_i) / sum(effective_weight_i)
```

Interpretation:

| Cycle Score | State |
| ---: | --- |
| `>= +1.0` | Multi-cycle rising prosperity / strong resonance |
| `+0.4 to +1.0` | Improving or early-to-mid upswing |
| `-0.4 to +0.4` | Mixed, transition, or no durable cycle edge |
| `-1.0 to -0.4` | Deteriorating or late-cycle rollover |
| `<= -1.0` | Multi-cycle contraction / high decline risk |

Confidence is lower when the score is driven by one layer, when evidence is lagging, when policy can abruptly reverse incentives, or when market price strongly disagrees with fundamentals.

## Bayesian Trend Probability

Use Bayesian updating to turn a prior trend probability into a posterior probability.

1. Set a prior probability:
   - `0.50` when no reliable trend/fundamental prior exists.
   - Technical-only prior from trend analysis when price data is strong.
   - Fundamental prior from earnings, margin, and cash-flow quality when available.
2. Convert prior to log odds:
   - `logit(p) = ln(p / (1 - p))`
3. Add cycle evidence:
   - `posterior_logit = logit(prior) + beta * cycle_score`
   - Default `beta = 0.75` for medium-term sector calls.
   - Use `beta = 0.45` for short-term trades and `beta = 0.90` for long-term industry calls with strong data.
4. Add or subtract only non-overlapping hard evidence:
   - `+0.15 to +0.35` for confirmed price increases, backlog, earnings revisions, and breadth confirmation.
   - `-0.15 to -0.35` for margin compression, inventory buildup, financing stress, or failed price breakout.
   - Cap total manual adjustment to `+/-0.50` unless a major shock occurs.
5. Convert back:
   - `posterior_probability = 1 / (1 + exp(-posterior_logit))`

Report probabilities as scenario-weighted evidence, not certainty. If the posterior exceeds 70% only because of narrative or low-reliability long-cycle assumptions, reduce it.

## Cross-Validation

Require at least three of five evidence families before calling a sector a rising prosperity cycle:

1. Macro/policy support: credit, fiscal, regulation, procurement, or external demand helps the sector.
2. Industry hard data: prices, spreads, utilization, inventory, orders, exports, or backlog improve.
3. Financial statements: revenue, gross margin, deducted profit, cash flow, or earnings revisions improve.
4. Market confirmation: relative strength, breadth, volume, leadership, or valuation rerating confirms.
5. Micro confirmation: leading companies disclose orders, capacity utilization, delivery, or customer adoption.

For declining cycles, require at least three of:

- Demand weakening.
- Price/spread decline.
- Inventory or receivables stress.
- Margin/profit deterioration.
- Policy/regulatory headwind.
- Market relative weakness and failed rebounds.

## Output Template

When using cycle overlay, include:

1. Data date, sources, horizon, and confidence.
2. Cycle-state table by layer with direction score, reliability, and evidence.
3. Weighted cycle score and Bayesian posterior probability.
4. Cross-validation: macro/policy, industry data, financial statements, market confirmation, micro evidence.
5. Upside industries: why multiple cycles align, what could invalidate the view.
6. Downside/declining industries: what pressures overlap, what could reverse the view.
7. Ordinary-investor caution: distinguish prosperity trend from chaseable price, and name the level or evidence that would force reassessment.
