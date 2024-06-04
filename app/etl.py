import httpx
from datetime import datetime, date
import pandas as pd
from statistics import mean, stdev
from database import engine_alvo as engine


INF = 999999

url = "http://127.0.0.1:8000/data_in_day/"

# Conta o número de signals no banco de dados
signals_url = httpx.get("http://127.0.0.1:8000/signals/")
signals_df = pd.DataFrame.from_dict(signals_url.json())
signal_num = signals_df.shape[0]

def convert_to_date(data_str):
    try:
        data_dt = datetime.strptime(data_str, "%Y-%m-%d")
        data = data_dt.date()
        return data
    except ValueError:
        print("Invalid format. Use YYYY-MM-DD format")
        return None

data_str = input("Write the day you want to get the signal from (YYYY-MM-DD): ")
data = convert_to_date(data_str)
params = {"day": data}

if data:
    r = httpx.get(url, params=params)
    df = pd.DataFrame.from_dict(r.json())

    signal_num += 1
    signal_name = "signal_" + str(signal_num)
    signal = pd.DataFrame({'id': [signal_num],
                           'name': [signal_name]})
    signal.to_sql(name='signal', con=engine, if_exists='append', index=False)
    
    wind_speed = []
    power = []
    
    for i, row in df.iterrows():
        wind_speed.append(row['wind_speed'])
        power.append(row['power'])

        if i+1 % 10 == 0:
            wind_speed_mean = mean(wind_speed)
            wind_speed_max = max(wind_speed)
            wind_speed_min = min(wind_speed)
            wind_speed_sd = stdev(wind_speed)
            wind_speed = []
            power_mean = mean(power)
            power_max = max(power)
            power_min = min(power)
            power_sd = stdev(power)
            power = []



