# conn_string = "host='localhost' dbname='restUser' user='postgres' password='mohit123'"
# DB_URL = "postgresql://postgres:mohit123@localhost:5432/restUser"
import os
DB_URL = os.environ['DB_URL']
