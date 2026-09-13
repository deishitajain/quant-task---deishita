"""
FINOVA Quant & Trading Recruitment Task: The Chart Detective
Script: 20/50 EMA Crossover Backtesting Engine
Asset: Reliance Industries Limited (NSE:RELIANCE)
"""

import os
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_pipeline(
    ticker: str = "RELIANCE.NS",
    start_date: str = "2025-08-01",
    end_date: str = "2026-08-22",
    output_dir: str = "main_task"
):
    screenshot_dir = os.path.join(output_dir, "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    print(f"[*] Downloading daily data for {ticker}...")
    df = yf.download(ticker, start=start_date, end=end_date, interval="1d")
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    df = df.dropna(subset=['Close']).copy()

    # Calculate 20-day and 50-day EMAs
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()

    # Generate signals without look-ahead bias
    df['Regime'] = np.where(df['EMA20'] > df['EMA50'], 1, 0)
    df['Crossover'] = df['Regime'].diff()

    trades = []
    trade_id = 1
    in_pos = False
    entry_date = None
    entry_price = 0.0

    for date, row in df.iterrows():
        # Bullish Crossover: 20 EMA crosses above 50 EMA
        if row['Crossover'] == 1 and not in_pos:
            in_pos = True
            entry_date = date.strftime('%Y-%m-%d')
            entry_price = float(row['Close'])
            entry_dt = date

        # Bearish Crossover: 20 EMA crosses below 50 EMA
        elif row['Crossover'] == -1 and in_pos:
            in_pos = False
            exit_date = date.strftime('%Y-%m-%d')
            exit_price = float(row['Close'])
            exit_dt = date
            pnl_pct = ((exit_price - entry_price) / entry_price) * 100

            trades.append({
                "Trade Number": trade_id,
                "Entry Date": entry_date,
                "Entry Price": round(entry_price, 2),
                "Exit Date": exit_date,
                "Exit Price": round(exit_price, 2),
                "P&L (%)": round(pnl_pct, 2),
                "entry_dt": entry_dt,
                "exit_dt": exit_dt
            })
            trade_id += 1

    trades_df = pd.DataFrame(trades)

    # Calculate Summary Metrics
    total_trades = len(trades_df)
    winners = trades_df[trades_df['P&L (%)'] > 0]
    num_winners = len(winners)
    win_rate = (num_winners / total_trades * 100) if total_trades > 0 else 0.0
    largest_winner = trades_df['P&L (%)'].max() if total_trades > 0 else 0.0
    largest_loser = trades_df['P&L (%)'].min() if total_trades > 0 else 0.0

    print("\n" + "="*50)
    print("           RELIANCE 20/50 EMA TRADE LOG")
    print("="*50)
    display_df = trades_df.drop(columns=['entry_dt', 'exit_dt'])
    print(display_df.to_string(index=False))

    print("\n" + "="*50)
    print("              SUMMARY METRICS")
    print("="*50)
    print(f"Total Trades:          {total_trades}")
    print(f"Number of Winners:     {num_winners}")
    print(f"Win Rate:              {win_rate:.2f}%")
    print(f"Largest Single Winner: {largest_winner:+.2f}%")
    print(f"Largest Single Loser:  {largest_loser:+.2f}%")
    print("="*50)

    # Save to main_task/trade_log.csv
    csv_path = os.path.join(output_dir, "trade_log.csv")
    with open(csv_path, 'w') as f:
        display_df.to_csv(f, index=False)
        f.write("\nSummary Metric,Value\n")
        f.write(f"Total Trades,{total_trades}\n")
        f.write(f"Number of Winners,{num_winners}\n")
        f.write(f"Win Rate (%),{win_rate:.2f}%\n")
        f.write(f"Largest Single Winner (%),{largest_winner:+.2f}%\n")
        f.write(f"Largest Single Loser (%),{largest_loser:+.2f}%\n")

    # Plot 1: Full 12-Month Chart
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df.index, df['Close'], label='RELIANCE Daily Close', color='black', alpha=0.6, linewidth=1.2)
    ax.plot(df.index, df['EMA20'], label='20 EMA (Fast)', color='#e74c3c', linewidth=1.8)
    ax.plot(df.index, df['EMA50'], label='50 EMA (Slow)', color='#f39c12', linewidth=1.8)

    for t in trades:
        ax.scatter(t['entry_dt'], t['Entry Price'], marker='^', color='green', s=100, zorder=5)
        ax.scatter(t['exit_dt'], t['Exit Price'], marker='v', color='red', s=100, zorder=5)

    ax.set_title("RELIANCE Industries (NSE) - 20/50 EMA Crossover (12-Month Horizon)", fontsize=13, weight='bold')
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Price (INR)", fontsize=11)
    ax.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(screenshot_dir, "01_full_year_chart.png"), dpi=300)
    plt.close()

    # Plot 2: Best Trade Zoom
    best_trade = trades_df.loc[trades_df['P&L (%)'].idxmax()]
    pad = pd.Timedelta(days=15)
    df_best = df.loc[(df.index >= best_trade['entry_dt'] - pad) & (df.index <= best_trade['exit_dt'] + pad)]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_best.index, df_best['Close'], label='Close', color='black', linewidth=1.5)
    ax.plot(df_best.index, df_best['EMA20'], label='20 EMA', color='#e74c3c')
    ax.plot(df_best.index, df_best['EMA50'], label='50 EMA', color='#f39c12')
    ax.scatter(best_trade['entry_dt'], best_trade['Entry Price'], marker='^', color='green', s=120, label='Entry')
    ax.scatter(best_trade['exit_dt'], best_trade['Exit Price'], marker='v', color='red', s=120, label='Exit')
    ax.set_title(f"Best Trade (#{best_trade['Trade Number']}): Gain {best_trade['P&L (%)']:+.2f}%", fontsize=12, weight='bold')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(screenshot_dir, "02_best_trade.png"), dpi=300)
    plt.close()

    # Plot 3: Worst Trade Zoom
    worst_trade = trades_df.loc[trades_df['P&L (%)'].idxmin()]
    df_worst = df.loc[(df.index >= worst_trade['entry_dt'] - pad) & (df.index <= worst_trade['exit_dt'] + pad)]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_worst.index, df_worst['Close'], label='Close', color='black', linewidth=1.5)
    ax.plot(df_worst.index, df_worst['EMA20'], label='20 EMA', color='#e74c3c')
    ax.plot(df_worst.index, df_worst['EMA50'], label='50 EMA', color='#f39c12')
    ax.scatter(worst_trade['entry_dt'], worst_trade['Entry Price'], marker='^', color='green', s=120, label='Entry')
    ax.scatter(worst_trade['exit_dt'], worst_trade['Exit Price'], marker='v', color='red', s=120, label='Exit')
    ax.set_title(f"Worst Trade (#{worst_trade['Trade Number']}): Loss {worst_trade['P&L (%)']:+.2f}%", fontsize=12, weight='bold')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(screenshot_dir, "03_worst_trade.png"), dpi=300)
    plt.close()

    print("[✓] Process complete. Artifacts saved to main_task/ directory.")

if __name__ == "__main__":
    run_pipeline()