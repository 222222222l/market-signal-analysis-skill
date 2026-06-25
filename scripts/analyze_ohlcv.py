#!/usr/bin/env python3
"""Analyze OHLCV CSV data and emit technical signal probabilities as JSON."""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


FAMILY_WEIGHTS = {
    "trend_breakout_ma": 0.24,
    "momentum_relative_strength": 0.18,
    "volume_confirmation": 0.14,
    "macd_combo": 0.11,
    "rsi_kdj_oscillator": 0.10,
    "divergence": 0.11,
    "volatility_regime": 0.07,
    "multi_timeframe_agreement": 0.05,
}

TIMEFRAME_WEIGHTS = {
    "short": {"hourly": 0.45, "daily": 0.35, "weekly": 0.15, "monthly": 0.05},
    "mid": {"hourly": 0.10, "daily": 0.45, "weekly": 0.35, "monthly": 0.10},
    "long": {"hourly": 0.00, "daily": 0.20, "weekly": 0.45, "monthly": 0.35},
}


@dataclass
class Bar:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


def parse_float(value: str) -> float:
    if value is None or str(value).strip() == "":
        return float("nan")
    return float(str(value).replace(",", "").strip())


def normalize_columns(fieldnames: Iterable[str]) -> Dict[str, str]:
    aliases = {
        "timestamp": {"timestamp", "date", "datetime", "time"},
        "open": {"open", "o"},
        "high": {"high", "h"},
        "low": {"low", "l"},
        "close": {"close", "c", "adj_close", "adjusted_close"},
        "volume": {"volume", "vol", "v"},
    }
    normalized = {name.lower().strip(): name for name in fieldnames}
    result = {}
    for target, names in aliases.items():
        for name in names:
            if name in normalized:
                result[target] = normalized[name]
                break
    missing = [key for key in aliases if key not in result]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    return result


def load_bars(path: str) -> List[Bar]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        cols = normalize_columns(reader.fieldnames)
        bars = []
        for row in reader:
            bar = Bar(
                timestamp=str(row[cols["timestamp"]]),
                open=parse_float(row[cols["open"]]),
                high=parse_float(row[cols["high"]]),
                low=parse_float(row[cols["low"]]),
                close=parse_float(row[cols["close"]]),
                volume=parse_float(row[cols["volume"]]),
            )
            if any(math.isnan(x) for x in [bar.open, bar.high, bar.low, bar.close, bar.volume]):
                continue
            bars.append(bar)
    bars.sort(key=lambda item: item.timestamp)
    return bars


def sma(values: List[float], period: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(values)
    if period <= 0:
        return out
    total = 0.0
    for index, value in enumerate(values):
        total += value
        if index >= period:
            total -= values[index - period]
        if index >= period - 1:
            out[index] = total / period
    return out


def ema(values: List[float], period: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(values)
    if not values or period <= 0:
        return out
    alpha = 2 / (period + 1)
    current = values[0]
    for index, value in enumerate(values):
        current = value if index == 0 else alpha * value + (1 - alpha) * current
        if index >= period - 1:
            out[index] = current
    return out


def rsi(values: List[float], period: int = 14) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(values)
    gains: List[float] = []
    losses: List[float] = []
    for index in range(1, len(values)):
        delta = values[index] - values[index - 1]
        gains.append(max(delta, 0.0))
        losses.append(abs(min(delta, 0.0)))
        if index >= period:
            avg_gain = sum(gains[index - period:index]) / period
            avg_loss = sum(losses[index - period:index]) / period
            out[index] = 100.0 if avg_loss == 0 else 100 - 100 / (1 + avg_gain / avg_loss)
    return out


def macd(values: List[float]) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    ema12 = ema(values, 12)
    ema26 = ema(values, 26)
    line: List[Optional[float]] = [None] * len(values)
    compact = []
    compact_indexes = []
    for index, (fast, slow) in enumerate(zip(ema12, ema26)):
        if fast is not None and slow is not None:
            value = fast - slow
            line[index] = value
            compact.append(value)
            compact_indexes.append(index)
    compact_signal = ema(compact, 9)
    signal: List[Optional[float]] = [None] * len(values)
    for source_index, value in zip(compact_indexes, compact_signal):
        signal[source_index] = value
    hist = [
        None if line_value is None or signal_value is None else line_value - signal_value
        for line_value, signal_value in zip(line, signal)
    ]
    return line, signal, hist


def stochastic_kdj(bars: List[Bar], period: int = 9) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    k: List[Optional[float]] = [None] * len(bars)
    d: List[Optional[float]] = [None] * len(bars)
    j: List[Optional[float]] = [None] * len(bars)
    current_k = 50.0
    current_d = 50.0
    for index in range(len(bars)):
        if index < period - 1:
            continue
        window = bars[index - period + 1:index + 1]
        low = min(bar.low for bar in window)
        high = max(bar.high for bar in window)
        rsv = 50.0 if high == low else (bars[index].close - low) / (high - low) * 100
        current_k = 2 / 3 * current_k + 1 / 3 * rsv
        current_d = 2 / 3 * current_d + 1 / 3 * current_k
        k[index] = current_k
        d[index] = current_d
        j[index] = 3 * current_k - 2 * current_d
    return k, d, j


def atr(bars: List[Bar], period: int = 14) -> List[Optional[float]]:
    true_ranges = []
    for index, bar in enumerate(bars):
        if index == 0:
            true_ranges.append(bar.high - bar.low)
        else:
            prev_close = bars[index - 1].close
            true_ranges.append(max(bar.high - bar.low, abs(bar.high - prev_close), abs(bar.low - prev_close)))
    return sma(true_ranges, period)


def latest(values: List[Optional[float]]) -> Optional[float]:
    for value in reversed(values):
        if value is not None:
            return value
    return None


def crossed_up(a: List[Optional[float]], b: List[Optional[float]]) -> bool:
    if len(a) < 2 or len(b) < 2:
        return False
    return None not in (a[-1], a[-2], b[-1], b[-2]) and a[-2] <= b[-2] and a[-1] > b[-1]


def crossed_down(a: List[Optional[float]], b: List[Optional[float]]) -> bool:
    if len(a) < 2 or len(b) < 2:
        return False
    return None not in (a[-1], a[-2], b[-1], b[-2]) and a[-2] >= b[-2] and a[-1] < b[-1]


def swing_points(values: List[float], lookback: int = 80) -> Tuple[List[int], List[int]]:
    start = max(2, len(values) - lookback)
    highs = []
    lows = []
    for index in range(start, len(values) - 2):
        window = values[index - 2:index + 3]
        if values[index] == max(window):
            highs.append(index)
        if values[index] == min(window):
            lows.append(index)
    return highs, lows


def detect_divergence(closes: List[float], indicator: List[Optional[float]]) -> Tuple[bool, bool]:
    highs, lows = swing_points(closes)
    clean_indicator = [float("nan") if value is None else value for value in indicator]
    bearish = False
    bullish = False
    if len(highs) >= 2:
        first, second = highs[-2], highs[-1]
        bearish = closes[second] > closes[first] and clean_indicator[second] < clean_indicator[first]
    if len(lows) >= 2:
        first, second = lows[-2], lows[-1]
        bullish = closes[second] < closes[first] and clean_indicator[second] > clean_indicator[first]
    return bullish, bearish


def add_signal(signals: List[dict], family: str, signal: str, direction: str, strength: float, evidence: str) -> None:
    signals.append({
        "family": family,
        "signal": signal,
        "direction": direction,
        "strength": round(max(0.0, min(1.0, strength)), 3),
        "evidence": evidence,
    })


def analyze(bars: List[Bar], horizon: str, market: str) -> dict:
    warnings = []
    if len(bars) < 60:
        warnings.append("Fewer than 60 bars; probability confidence is low.")
    if any(bar.high < max(bar.open, bar.close) or bar.low > min(bar.open, bar.close) for bar in bars):
        warnings.append("Some OHLC rows are internally inconsistent.")

    closes = [bar.close for bar in bars]
    volumes = [bar.volume for bar in bars]
    ma20 = sma(closes, 20)
    ma50 = sma(closes, 50)
    ma200 = sma(closes, 200)
    vol20 = sma(volumes, 20)
    rsi14 = rsi(closes)
    macd_line, macd_signal, macd_hist = macd(closes)
    k, d, j = stochastic_kdj(bars)
    atr14 = atr(bars)
    signals: List[dict] = []

    close = closes[-1]
    prev_close = closes[-2] if len(closes) > 1 else close
    current_ma20 = latest(ma20)
    current_ma50 = latest(ma50)
    current_ma200 = latest(ma200)
    current_vol20 = latest(vol20)
    current_rsi = latest(rsi14)
    current_k = latest(k)
    current_d = latest(d)
    current_atr = latest(atr14)
    current_macd = latest(macd_line)
    current_macd_signal = latest(macd_signal)
    current_hist = latest(macd_hist)

    if current_ma20 and current_ma50:
        if close > current_ma20 > current_ma50:
            add_signal(signals, "trend_breakout_ma", "bullish_ma_regime", "bullish", 0.65, "Close is above MA20 and MA20 is above MA50.")
        elif close < current_ma20 < current_ma50:
            add_signal(signals, "trend_breakout_ma", "bearish_ma_regime", "bearish", 0.65, "Close is below MA20 and MA20 is below MA50.")
    if current_ma200:
        if close > current_ma200:
            add_signal(signals, "trend_breakout_ma", "above_ma200", "bullish", 0.35, "Close is above MA200.")
        else:
            add_signal(signals, "trend_breakout_ma", "below_ma200", "bearish", 0.35, "Close is below MA200.")

    if len(closes) > 21:
        prior_high = max(closes[-21:-1])
        prior_low = min(closes[-21:-1])
        rel_vol = volumes[-1] / current_vol20 if current_vol20 else 1.0
        if close > prior_high:
            strength = 0.65 + min(0.25, max(0.0, rel_vol - 1.0) / 2)
            add_signal(signals, "trend_breakout_ma", "twenty_bar_breakout", "bullish", strength, f"Close broke prior 20-bar high; relative volume {rel_vol:.2f}.")
        elif close < prior_low:
            strength = 0.65 + min(0.25, max(0.0, rel_vol - 1.0) / 2)
            add_signal(signals, "trend_breakout_ma", "twenty_bar_breakdown", "bearish", strength, f"Close broke prior 20-bar low; relative volume {rel_vol:.2f}.")
        if rel_vol > 1.3 and close > prev_close:
            add_signal(signals, "volume_confirmation", "bullish_volume_expansion", "bullish", min(1.0, rel_vol / 2.5), f"Up bar volume is {rel_vol:.2f}x the 20-bar average.")
        elif rel_vol > 1.3 and close < prev_close:
            add_signal(signals, "volume_confirmation", "bearish_volume_expansion", "bearish", min(1.0, rel_vol / 2.5), f"Down bar volume is {rel_vol:.2f}x the 20-bar average.")

    if len(closes) > 63:
        ret63 = close / closes[-64] - 1
        if ret63 > 0.08 and close > (current_ma50 or close):
            add_signal(signals, "momentum_relative_strength", "positive_3m_momentum", "bullish", min(1.0, abs(ret63) * 3), f"Approximate 3-month momentum is {ret63:.1%}.")
        elif ret63 < -0.08 and close < (current_ma50 or close):
            add_signal(signals, "momentum_relative_strength", "negative_3m_momentum", "bearish", min(1.0, abs(ret63) * 3), f"Approximate 3-month momentum is {ret63:.1%}.")

    if crossed_up(macd_line, macd_signal):
        add_signal(signals, "macd_combo", "bullish_macd_cross", "bullish", 0.65, "MACD crossed above signal line.")
    elif crossed_down(macd_line, macd_signal):
        add_signal(signals, "macd_combo", "bearish_macd_cross", "bearish", 0.65, "MACD crossed below signal line.")
    if current_macd is not None and current_macd_signal is not None and current_hist is not None:
        if current_macd > 0 and current_hist > 0:
            add_signal(signals, "macd_combo", "bullish_macd_regime", "bullish", 0.45, "MACD is above zero with positive histogram.")
        elif current_macd < 0 and current_hist < 0:
            add_signal(signals, "macd_combo", "bearish_macd_regime", "bearish", 0.45, "MACD is below zero with negative histogram.")

    if current_rsi is not None:
        if current_rsi < 30:
            add_signal(signals, "rsi_kdj_oscillator", "rsi_oversold", "bullish", 0.45, f"RSI is oversold at {current_rsi:.1f}.")
        elif current_rsi > 70:
            add_signal(signals, "rsi_kdj_oscillator", "rsi_overbought", "bearish", 0.45, f"RSI is overbought at {current_rsi:.1f}.")
        elif current_rsi > 55:
            add_signal(signals, "rsi_kdj_oscillator", "rsi_bullish_regime", "bullish", 0.35, f"RSI is in bullish regime at {current_rsi:.1f}.")
        elif current_rsi < 45:
            add_signal(signals, "rsi_kdj_oscillator", "rsi_bearish_regime", "bearish", 0.35, f"RSI is in bearish regime at {current_rsi:.1f}.")

    if current_k is not None and current_d is not None:
        if crossed_up(k, d):
            add_signal(signals, "rsi_kdj_oscillator", "bullish_kdj_cross", "bullish", 0.45 if current_k < 50 else 0.30, "K crossed above D.")
        elif crossed_down(k, d):
            add_signal(signals, "rsi_kdj_oscillator", "bearish_kdj_cross", "bearish", 0.45 if current_k > 50 else 0.30, "K crossed below D.")

    bullish_div_rsi, bearish_div_rsi = detect_divergence(closes, rsi14)
    bullish_div_macd, bearish_div_macd = detect_divergence(closes, macd_hist)
    if bullish_div_rsi or bullish_div_macd:
        add_signal(signals, "divergence", "bottom_divergence", "bullish", 0.60, "Price made a lower low while RSI or MACD made a higher low.")
    if bearish_div_rsi or bearish_div_macd:
        add_signal(signals, "divergence", "top_divergence", "bearish", 0.60, "Price made a higher high while RSI or MACD made a lower high.")

    if current_atr is not None and close:
        atr_pct = current_atr / close
        if atr_pct > 0.05:
            add_signal(signals, "volatility_regime", "high_volatility_risk", "bearish", 0.35, f"ATR is elevated at {atr_pct:.1%} of price.")
        elif atr_pct < 0.02:
            add_signal(signals, "volatility_regime", "low_volatility_constructive", "bullish", 0.20, f"ATR is contained at {atr_pct:.1%} of price.")

    bullish = 0.0
    bearish = 0.0
    for signal in signals:
        contribution = FAMILY_WEIGHTS[signal["family"]] * signal["strength"]
        if signal["direction"] == "bullish":
            bullish += contribution
        elif signal["direction"] == "bearish":
            bearish += contribution

    net = bullish - bearish
    buy_raw = 1 / (1 + math.exp(-2.6 * net))
    sell_raw = 1 / (1 + math.exp(2.6 * net))
    confidence_scale = 0.65 if len(bars) >= 200 else 0.45
    hold_raw = max(0.05, 1 - abs(buy_raw - sell_raw) * confidence_scale)
    total = buy_raw + sell_raw + hold_raw
    probabilities = {
        "buy": round(100 * buy_raw / total, 1),
        "sell": round(100 * sell_raw / total, 1),
        "hold": round(100 * hold_raw / total, 1),
    }
    probability_basis = "default_prior"

    confidence = "medium" if len(bars) >= 200 else "low"
    if len(bars) < 60:
        confidence = "insufficient"
        probability_basis = "insufficient_data"
        probabilities = {"buy": None, "sell": None, "hold": None}

    return {
        "market": market,
        "horizon": horizon,
        "bars": len(bars),
        "latest_timestamp": bars[-1].timestamp if bars else None,
        "indicator_snapshot": {
            "close": close,
            "ma20": current_ma20,
            "ma50": current_ma50,
            "ma200": current_ma200,
            "rsi14": current_rsi,
            "macd": current_macd,
            "macd_signal": current_macd_signal,
            "macd_histogram": current_hist,
            "kdj_k": current_k,
            "kdj_d": current_d,
            "kdj_j": latest(j),
            "atr14": current_atr,
        },
        "score_components": {"bullish": round(bullish, 4), "bearish": round(bearish, 4), "net": round(net, 4)},
        "probabilities": probabilities,
        "probability_basis": probability_basis,
        "confidence": confidence,
        "matched_signals": signals,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze OHLCV technical signals.")
    parser.add_argument("--input", required=True, help="Path to OHLCV CSV file.")
    parser.add_argument("--market", default="us_equity", help="Market profile name.")
    parser.add_argument("--horizon", choices=["short", "mid", "long"], default="mid")
    args = parser.parse_args()

    bars = load_bars(args.input)
    if not bars:
        raise SystemExit("No valid bars found in CSV.")
    print(json.dumps(analyze(bars, args.horizon, args.market), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
