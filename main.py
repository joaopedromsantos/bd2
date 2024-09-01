import threading
import time
import random
from pymongo import MongoClient


def sensor(nome_sensor: str, intervalo: int):
    # Criando documento
    sensor_doc = {
        "nomeSensor": nome_sensor,
        "valorSensor": 0,
        "unidadeMedida": "Cº",
        "sensorAlarmado": False
    }

    db_collection.insert_one(sensor_doc)

    while True:
        number = random.randint(30, 40)
        print(f'{number} Cº - {nome_sensor}')

        # Atualizando o documento com o valor mais recente
        sensor_doc["valorSensor"] = number

        if number > 38:
            # Marcar o sensor como alarmado
            sensor_doc["sensorAlarmado"] = True

            db_collection.update_one(
                {"nomeSensor": nome_sensor},
                {"$set": sensor_doc}
            )
            print(f'Atenção, temperatura muito alta no {nome_sensor}')
            break

        # Atualizando o documento no banco
        db_collection.update_one(
            {"nomeSensor": nome_sensor},
            {"$set": sensor_doc}
        )

        time.sleep(intervalo)


client = MongoClient('mongodb://localhost:27017')
db = client['bancoiot']
db_collection = db.sensores

# Criando threads para cada sensor
s1 = threading.Thread(target=sensor, args=("Sensor 1", 3))
s2 = threading.Thread(target=sensor, args=("Sensor 2", 4))
s3 = threading.Thread(target=sensor, args=("Sensor 3", 5))

s1.start()
s2.start()
s3.start()
