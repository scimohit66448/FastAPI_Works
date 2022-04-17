import sqlalchemy as sql
from Constants import DB_URL

db_engine = sql.create_engine(DB_URL)
conn = db_engine.connect()
metadata = sql.MetaData()
user_table = None
try:
    user_table = sql.Table('user_nmg', metadata, autoload=True, autoload_with=db_engine)
except:
    user_table = sql.Table('user_nmg', metadata,

                           sql.Column('firstname', sql.String(100), nullable=False),
                           sql.Column('lastname', sql.String(100), nullable=False),
                           sql.Column('age', sql.Integer(), nullable=False)
                           )

    metadata.create_all(db_engine)
    print("No User table  :  Created User table")


def insert_user(user_list):
    users_created = False
    try:
        create_query = sql.insert(user_table)
        conn.execute(create_query, user_list)
        users_created = True
    except:
        pass
    finally:
        return users_created


def search_user_in_db(firstname=None, lastname=None, age=None, count=None):
    data = []
    print("Searching in DB.......")

    # query = sql.select([user_table.columns.firstname, user_table.columns.lastname, user_table.columns.age])'
    query = 'SELECT * from public.user_nmg'
    if firstname:
        firstname = firstname.lower()
        if "Where" not in query:

            query = query + " Where "
        else:
            query = query + "AND "
        query = query + f"lower(firstname) ='{firstname}'"
    if lastname:
        lastname = lastname.lower()
        if "Where" not in query:
            query = query + " Where "
        else:
            query = query + " AND "
        query = query + f"lower(lastname) ='{lastname}'"
    if age:
        if "Where" not in query:
            query = query + " Where "
        else:
            query = query + " AND "
        query = query + f"age ={age}"
    print(query)
    if count:

        query = query + f" LIMIT {count}"
    result = conn.execute(query).fetchall()
    print(result)
    try:
        data = [{'firstname': i.firstname, 'lastname': i.lastname, 'age': i.age} for i in result]
    except:
        pass

    return data
