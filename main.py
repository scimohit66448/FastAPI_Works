import random
import re
import faker
from DbOpsUsingSqlAlchemy import insert_user, search_user_in_db
from typing import Optional
from fastapi import FastAPI, status
from pydantic import BaseModel, StrictStr, StrictInt, validator
from fastapi.responses import JSONResponse

my_rest_app = FastAPI()

regex = re.compile('[1234567890@_!#$%^&*()<>?/}{~:]')

fake = faker.Faker()

"""This class help validate the user data from the requests"""


class User(BaseModel):
    firstname: StrictStr
    lastname: StrictStr
    age: StrictInt

    @validator('firstname')
    def firstname_length(cls, firstname):
        firstname = firstname.strip()
        if len(firstname) > 100 or len(firstname) < 1:
            raise ValueError("First Name must not be empty or greater than 100 words")
        if regex.search(firstname) is not None:
            raise ValueError("First name contains Special character or Number")
        return firstname

    @validator('lastname')
    def lastname_length(cls, lastname):
        lastname = lastname.strip()
        if len(lastname) > 100 or len(lastname) < 1:
            raise ValueError("Last Name must not be empty or greater than 100 words")
        if regex.search(lastname) is not None:
            raise ValueError("lastname contains Special character or Number")
        return lastname

    @validator('age')
    def age_below_100(cls, age):
        if age < 0:
            raise ValueError("Invalid age : age cannot be negative")
        if age > 999:
            raise ValueError("Please enter the age not more than 3 digits")
        return age


"""This API is for create a single user when user details are passed 
method:  POST"""


@my_rest_app.post("/create_user")
async def create_user(user: User):
    response = None
    response_status = None
    user_created = []
    try:
        user_list = [dict(user)]
        is_user_created = insert_user(user_list)
        if is_user_created:
            user_created = user_list
            response = "User created successfully."
            response_status = status.HTTP_201_CREATED
        else:
            raise Exception("Something went Wrong: User Creation failed")
    except Exception as e:
        response = e
        print(e)
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        return JSONResponse(status_code=response_status, content={"data": user_created, 'message': response})


"""This API generate N number of fake records in the DB " 
Method : POST
Parameter : number (number of records to be generated)
"""


@my_rest_app.post("/generate_user/{number}")
async def generate_user(number: int):
    response = " "
    users_created = []
    user_list = []
    response_status = status.HTTP_102_PROCESSING
    try:
        for user_number in range(number):
            name = fake.name().split(" ")  # this generates fake name
            user = {'firstname': name[0], 'lastname': name[1], 'age': random.randint(0, 100)}
            user_list.append(user)
            # user_created = insert_user(user)
            # if user_created:
            #     user_created_successfully += 1
            #     users_created.append(user)
        is_users_created = insert_user(user_list)
        if is_users_created:
            response = f'{len(user_list)} users created successfully '
            users_created = user_list
            response_status = status.HTTP_201_CREATED
        else:
            raise Exception(" Something went wrong: Users creation failed")

    except Exception as e:
        response = e
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        return JSONResponse(status_code=response_status, content={"data": users_created, "message": response})


@my_rest_app.get('/get_user')
async def search_user(firstname: Optional[StrictStr] = None, lastname: Optional[StrictStr] = None,
                      age: Optional[int] = None):
    param = {"firstname": firstname, "lastname": lastname, "age": age}
    response = search_user_in_db(firstname=firstname, lastname=lastname, age=age)
    response_status = status.HTTP_200_OK
    return JSONResponse(status_code=response_status, content={"data": response, 'message': "Searched the DB for data"})


@my_rest_app.get('/list_user_records/{number}')
def generate_user_record(number: int):
    response = search_user_in_db()
    response_status = status.HTTP_200_OK
    if number < len(response):
        response = response[:number]
    return JSONResponse(status_code=response_status, content={"data": response, 'message': f"produced {number} records"})
