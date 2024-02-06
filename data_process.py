import json
import csv
import pandas as pd

def json_to_csv_fg(json_file, financial_csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    financial_headers = list(data["financialGrowth"][0].keys())
    with open(financial_csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=financial_headers)
        writer.writeheader()
        for row in data["financialGrowth"]:
            writer.writerow(row)
    
def json_to_csv_hp(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 提取header
    headers = list(data["historicalPriceFull"]["historical"][0].keys())
    headers.insert(0, "symbol")  # 插入symbol

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)

        writer.writeheader()

        # 寫入資料
        for row in data["historicalPriceFull"]["historical"]:
            row["symbol"] = data["historicalPriceFull"]["symbol"]  # 添加 "symbol"
            writer.writerow(row)

json_to_csv_fg('output_clean_date_technical.json', 'financial_growth.csv')
json_to_csv_hp('output_clean_date_technical.json', 'historical_prices.csv')

df_stock_price = pd.read_csv('historical_prices.csv')
df_financials = pd.read_csv('financial_growth.csv')
df_stock_price.set_index('date', inplace=True)
df_financials.set_index('date', inplace=True)
df_financials.rename(columns={'symbol': 'financial_symbol'}, inplace=True)
df_merged = df_stock_price.join(df_financials, how='outer')
df_merged = df_merged.drop(["financial_symbol"],axis=1)
df_merged.to_csv('merged_data.csv')
df = pd.read_csv("merged_data.csv")
d_date = None
for i in range(len(df)):
    if not pd.isna(df.iloc[i,15]):
        d_date = i
        df.loc[i,"dif_date"] = 0
        continue
    if d_date == None:
        continue
    else:
        for j in range(15,50):
            df.iloc[i,j] = df.iloc[d_date,j]
        df.loc[i,"dif_date"] = i - d_date
df['date'] = pd.to_datetime(df['date'])
data = df[df['date'] >= '2021-02-01']
data.to_csv("data.csv")
