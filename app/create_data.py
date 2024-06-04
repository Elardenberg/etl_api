import pandas as pd
import random
import datetime
from fastapi.testclient import TestClient
from .database import engine_fonte as engine

class CreateData:
    def __init__(self, app):
        self.app = app
        self.client = TestClient(self.app)

        # Definindo a data inicial (27 de maio de 2024, 00:00)
        start_date = datetime.datetime(2024, 5, 27, 0, 0)
        data_size = 200

        # Criando os dados
        data = {
            'id': list(range(1, data_size+1)),
            'timestamp': [start_date + datetime.timedelta(minutes=i) for i in range(data_size)],
            'wind_speed': [random.normalvariate(22.5, 10) for _ in range(data_size)],
            'power': [random.normalvariate(90, 5) for _ in range(data_size)],
            'ambient_temperature': [random.normalvariate(300, 10) for _ in range(data_size)]
        }

        # Criando o DataFrame
        self.df = pd.DataFrame(data)

    def upload_data(self):
        self.df.to_sql(name='data', con=engine, if_exists='replace')
