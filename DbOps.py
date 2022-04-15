import psycopg2
from Constants import conn_string

conn = None


def create_search_query():
    pass


def search_user_in_db(param=None):
    response = ""
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        query = "SELECT * FROM public.user"
        if param is not None:
            for key in param.keys():
                if param[key] is not None:
                    if "WHERE" not in query:
                        query = query + " WHERE" + " "
                    query = query + key + " = '" + str(param[key]) + "'"
                    print(key, ":", param[key])

        # print(query)
        # query = "SELECT * FROM public.user"
        query = query + ";"
        query = query.replace("\n", "")
        cur.execute(query)
        resp = cur.fetchall()
        conn.commit()
        cur.close()
        response = resp
    except Exception as e:
        response = str(e)
    finally:
        try:
            conn.close()
        except Exception as e:
            response = response + "; No valid connection to close"
        return response


def insert_user(user):
    response = False
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        user = dict(user)
        cur.execute("INSERT INTO public.user(firstname, lastname, age) Values( %s, %s,%s);",
                    (user['firstname'], user['lastname'], user['age']))
        conn.commit()
        cur.close()
        response = True
    except Exception as e:
        response = False
    finally:
        try:
            conn.close()
        except Exception as e:
            response = False
        return response


def create_table():
    try:
        global conn
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        cur.execute(
            "Create table user(id serial PRIMARY KEY, firstname varchar(100), lastname varchar(100), age int);")
        conn.commit()
    except:
        print("Table creation failed")
    finally:
        try:
            conn.close()
        except:
            print("No valid connection found")

# create_table() # Uncomment and run this file to create the table required for this operation
