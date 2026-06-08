import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

# ----------------------------
# GET SGX STOCK LIST (AUTO + CACHED HOURLY)
# ----------------------------
CACHE_FILE = "sgx_cache.csv"

def get_sgx_stocks():
    # refresh every 1 hour
    if os.path.exists(CACHE_FILE):
        age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
        if age < timedelta(hours=1):
            df = pd.read_csv(CACHE_FILE)
            return dict(zip(df["Name"], df["Ticker"]))

    print("🌐 Refreshing SGX stock list...")

    url = "https://stockanalysis.com/list/singapore-exchange/"
    df = pd.read_html(url)[0]

    df["Ticker"] = df["Symbol"].astype(str) + ".SI"

    out = df[["Company Name", "Ticker"]].rename(
        columns={"Company Name": "Name"}
    )

    out.to_csv(CACHE_FILE, index=False)

    return dict(zip(out["Name"], out["Ticker"]))


STOCKS = get_sgx_stocks()
# ----------------------------
# ADD MISSING ETFS (MANUAL OVERRIDE)
# ----------------------------
ETF_EXTRA = {
    "Lion-OCBC Hang Seng TECH ETF": "HST.SI",
    "Lion-Phillip S-REIT ETF": "CLR.SI"
}

STOCKS.update(ETF_EXTRA)
print(f"📋 Loaded {len(STOCKS)} SGX stocks + ETFS")

# ----------------------------
# FETCH DATA (YAHOO FINANCE)
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
# EXPORT CSV
# ----------------------------
df = pd.DataFrame(
    data,
    columns=["Name", "Ticker", "Price", "Previous Close", "Market Cap (B)", "P/E"]
)

df["Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

df.to_csv("stocks.csv", index=False)

print("\n📄 stocks.csv updated successfully")
print(f"🕒 Last updated: {df['Last Updated'][0]}")
