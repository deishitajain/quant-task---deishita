## 1. Strategy Rules & Execution Logic
* **Asset:** Reliance Industries Limited (`NSE:RELIANCE`)
* **Timeframe:** Daily (`1D`)
* **Indicators:** 20-period EMA (Fast Line), 50-period EMA (Slow Line)
* **Entry Signal:** Enter Long when the 20 EMA crosses above the 50 EMA.
* **Exit Signal:** Exit Position to Cash when the 20 EMA crosses below the 50 EMA.
* **Trade Model:** Long-only, discrete single-unit round trips.


## 2. 12-Month Trade Log

| Trade Number | Entry Date | Entry Price (₹) | Exit Date | Exit Price (₹) | P&L (%) |
| **1** | 2025-10-24 | 1,358.40 | 2026-02-04 | 1,482.15 | **+9.11%** |
| **2** | 2026-04-29 | 1,364.50 | 2026-05-22 | 1,302.20 | **-4.57%** |
| **3** | 2026-06-25 | 1,288.10 | 2026-07-21 | 1,263.75 | **-1.89%** |
| **4** | 2026-08-04 | 1,310.80 | 2026-08-14 | 1,291.50 | **-1.47%** |

### Summary Performance Metrics
* **Total Trades:** 4
* **Number of Winners:** 1
* **Win Rate:** 25.00%
* **Largest Single Winner:** +9.11% (Trade #1)
* **Largest Single Loser:** -4.57% (Trade #2)


## 3. Visual Artifacts

### 12-Month Full Strategy Chart
![Full Chart](main_task/screenshots/01_full_year_chart.png)

### Best Trade (+9.11% Gain)
![Best Trade](main_task/screenshots/02_best_trade.png)

### Worst Trade (-4.57% Loss)
![Worst Trade](main_task/screenshots/03_worst_trade.png)


## 4. Analytical Verdict

I would not trade this strategy with real capital in its current form. While it successfully captured a clean +9.11% expansion during the late-2025 uptrend (Trade #1), it suffered from repetitive whipsaws in the range-bound chop of 2026, producing three consecutive losses and a poor 25.00% win rate.

The fundamental weakness of the 20/50 EMA crossover is lag. Because moving averages are backward-looking smoothing functions, entries in sideways markets trigger near exhaustion highs, and exits trigger near capitulation lows. The strategy only thrives in low-volatility, highly directional trending markets. To make this deployable, it requires an **ADX regime filter** (ignoring crossover signals when ADX < 20) and a **dynamic ATR-based stop-loss** rather than waiting for a lagging reverse crossover.
