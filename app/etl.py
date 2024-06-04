import httpx
from datetime import datetime, date
import pandas as pd
from statistics import mean, stdev
from database import engine_alvo as engine

url = "http://127.0.0.1:8000/data_in_day/"

# Conta o número de dados no banco alvo
data_url = httpx.get("http://127.0.0.1:8000/alvo/data")
if (data_url.json()):
    data_df = pd.DataFrame.from_dict(data_url.json())
    data_num = data_df.shape[0]
else:
    data_num = 0

def convert_to_date(data_str):
    try:
        data_dt = datetime.strptime(data_str, "%Y-%m-%d")
        data = data_dt.date()
        return data
    except ValueError:
        print("Invalid format. Use YYYY-MM-DD format")
        return None

while True:
    yn = input("Do you want to get the signal from a day (y/n)?")

    if yn.lower() == 'n':
        print("End of script")
        break
    else:
        data_str = input("Write the day you want to get the signal from (YYYY-MM-DD): ")
        data = convert_to_date(data_str)
        params = {"day": data}

        if data:
            r = httpx.get(url, params=params)
            df = pd.DataFrame.from_dict(r.json())
            
            wind_speed = []
            power = []
            
            for i, row in df.iterrows():
                wind_speed.append(row['wind_speed'])
                power.append(row['power'])

                if (i+1) % 10 == 0:
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
                    data = pd.DataFrame({
                        'id': list(range(data_num, data_num+8)),
                        'timestamp': [row['timestamp']] * 8,
                        # 'timestamp': [datetime.strptime(row['timestamp'], "%Y-%m-%dT%H:%M:%S")] * 8,
                        'signal_id': list(range(1,9)),
                        'value': [wind_speed_mean, wind_speed_max, wind_speed_min, wind_speed_sd,
                                power_mean, power_max, power_min, power_sd]
                    })
                    data_num += 8
                    data.to_sql(name='data', con=engine, if_exists='append', index=False)



