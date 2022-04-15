conn_string = "host='localhost' dbname='restUser' user='postgres' password='mohit123'"
DB_URL = "postgresql://postgres:mohit123@localhost:5432/restUser"


import os

db_url = os.getenv('DB_URL')
print(db_url)