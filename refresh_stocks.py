import yfinance as yf
import pandas as pd
from datetime import datetime

# ----------------------------
# STOCK LIST (Name → Ticker)
# ----------------------------
STOCKS = {
    "Boustead": "F9D.SI",
    "CapitaLand Investment": "9CI.SI",
    "CapLand Ascendas REIT": "A17U.SI",
    "CapLand Ascott Trust": "HMN.SI",
    "CapLand Integrated Commercial Trust": "C38U.SI",
    "DBS": "D05.SI",
    "Far East Hospitality Trust": "Q5T.SI",
    "Far East Orchard": "O10.SI",
    "Frasers Centrepoint Trust": "J69U.SI",
    "GuocoLand": "F17.SI",
    "Haw Par": "H02.SI",
    "Hong Leong Finance": "S41.SI",
    "JB Foods": "BEW.SI",
    "Keppel Corp": "BN4.SI",
    "Keppel DC REIT": "AJBU.SI",
    "Keppel REIT": "K71U.SI",
    "Lendlease REIT": "JYEU.SI",
    "Mapletree Industrial Trust": "ME8U.SI",
    "Mapletree Logistics Trust": "M44U.SI",
    "NetLink NBN Trust": "CJLU.SI",
    "OCBC": "O39.SI",
    "Olam Group": "VC2.SI",
    "Singapore Land Group": "U06.SI",
    "Straits Trading": "S20.SI",
    "UOB": "U11.SI",
    "Wilmar": "F34.SI"
}

# ----------------------------
# FETCH DATA
# ----------------------------
print("📡 Fetching live stock data...\n")

data = []

for name, ticker in STOCKS.items():
    try:
        t = yf.Ticker(ticker)
        info = t.info

        price = info.get("currentPrice") or info.get("regularMarketPrice")
        prev = info.get("previousClose")

        mktcap = info.get("marketCap")
        pe = info.get("trailingPE")

        data.append([
            name,
            ticker,
            price,
            prev,
            round(mktcap / 1e9, 2) if mktcap else None,
            round(pe, 2) if pe else None
        ])

        print(f"✅ {name} ({ticker}) — {price}")

    except Exception as e:
        print(f"❌ {name} ({ticker}) — {e}")

# ----------------------------
# EXPORT CSV (FOR GOOGLE SHEETS)
# ----------------------------
df = pd.DataFrame(
    data,
    columns=["Name", "Ticker", "Price", "Previous Close", "Market Cap (B)", "P/E"]
)

df["Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

df.to_csv("stocks.csv", index=False)

print("\n📄 stocks.csv updated successfully")
print(f"🕒 Last updated: {df['Last Updated'][0]}")
