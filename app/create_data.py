import pandas as pd
import random
import datetime
from fastapi.testclient import TestClient
from .database import engine_fonte, engine_alvo

class CreateData:
    def __init__(self, app):
        self.app = app
        self.client = TestClient(self.app)

        # Definindo a data inicial (27 de maio de 2024, 00:00)
        start_date = datetime.datetime(2024, 5, 27, 0, 0)
        # Cada 1440 dados = 1 dia
        data_size = 1440*10

        # Criando os dados
        data = {
            'id': list(range(1, data_size+1)),
            'timestamp': [start_date + datetime.timedelta(minutes=i) for i in range(data_size)],
            'wind_speed': [random.normalvariate(22.5, 10) for _ in range(data_size)],
            'power': [random.normalvariate(90, 5) for _ in range(data_size)],
            'ambient_temperature': [random.normalvariate(300, 10) for _ in range(data_size)]
        }

        signals = {
            'id': list(range(1,9)),
            'name': ['wind_speed_mean', 'wind_speed_max', 'wind_speed_min', 'wind_speed_sd',
                    'power_mean', 'power_max', 'power_min', 'power_sd']
        }

        alvo_data = {
            'id': [-1],
            'signal_id': [-1],
            'timestamp': [start_date],
            'value': [0.0]
        }

        # Criando o DataFrame
        self.df = pd.DataFrame(data)
        self.signals = pd.DataFrame(signals)
        self.alvo_data = pd.DataFrame(alvo_data)

    def upload_data(self):
        self.df.to_sql(name='data', con=engine_fonte, if_exists='replace')
        self.alvo_data.to_sql(name='data', con=engine_alvo, if_exists='replace')
        self.signals.to_sql(name='signal', con=engine_alvo, if_exists='replace')
