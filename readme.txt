To run the Server on localhost :  uvicorn main:my_rest_app --reload

Before running server make sure that:
1. All the packages mentioned in requirements.txt is installed on your machine/Server.
2. Define  DB_URL environment variable with correct database URL.
    for e.g. posgtres URL  : "postgresql://username:password:host/dbname"

