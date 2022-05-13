# Pydantic
from pydantic import BaseModel  # Para representar entidades en codigo

# FastAPI
from fastapi import FastAPI 
from fastapi import Body    # Class to know if a parameter is type Bodyself.
from fastapi import Query

app = FastAPI()

# Models
class Person(BaseModel): # Subclase Person that inherits to class BaseModel  
    first_name: str
    last_name: str
    age: int 
    is_married: Optional[bool] = None
    length: Optional[int] = None

@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")    # Decorator that sends a request(post) to server with url "/person/new". It can access. 
def create_person(person: Person = Body(...)):  # Request Body. def create_person(name_parameter: type_parameter = is_Body(... mains that it's obligatory))
    return person Pydantic
from pydantic import BaseModel  # Para representar entidades en codigo

# FastAPI
from fastapi import FastAPI 
from fastapi import Body    # Class to know if a parameter is type Bodyself.
from fastapi import Query

app = FastAPI()

# Models
class Person(BaseModel): # Subclase Person that inherits to class BaseModel  
    first_name: str
    last_name: str
    age: int 
    is_married: Optional[bool] = None
    length: Optional[int] = None

@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")    # Decorator that sends a request(post) to server with url "/person/new". It can access. 
def create_person(person: Person = Body(...)):  # Request Body. def create_person(name_parameter: type_parameter = is_Body(... mains that it's obligatory))
    return person
    
