import yfinance as yf
import pandas as pd
from datetime import datetime

TICKERS = [
    "F9D.SI",
    "9CI.SI",
    "A17U.SI",
    "HMN.SI",
    "C38U.SI",
    "D05.SI",
    "Q5T.SI",
    "O10.SI",
    "J69U.SI",
    "F17.SI",
    "H02.SI",
    "S41.SI",
    "BEW.SI",
    "BN4.SI",
    "AJBU.SI",   # Keppel DC REIT (IMPORTANT FIX)
    "K71U.SI",
    "JYEU.SI",
    "ME8U.SI",
    "M44U.SI",   # FIXED
    "CJLU.SI",
    "O39.SI",
    "VC2.SI",
    "U06.SI",
    "S20.SI",
    "U11.SI",
    "F34.SI"
]


data = []

for ticker in TICKERS:
    try:
        t = yf.Ticker(ticker)
        info = t.info
        
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        prev  = info.get("previousClose")

        data.append([ticker, price, prev])
        print(f"✅ {ticker} — {price}")
        
    except Exception as e:
        print(f"❌ {ticker} — {e}")

df = pd.DataFrame(data, columns=["Ticker","Price","Previous Close"])
df["Last Updated"] = datetime.now()

df.to_csv("stocks.csv", index=False)

print("📄 CSV updated")
