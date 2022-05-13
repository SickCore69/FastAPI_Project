# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel  # Para representar entidades en codigo

# FastAPI
from fastapi import FastAPI 
from fastapi import Body    # Class to know if a parameter is type Body.
from fastapi import Query   # Class to asigment a Query parameter or a constrains parameters.
from fastapi import Path    # To create Path parameters.
# from fastapi import Body, Query, Path

app = FastAPI()

# Models
class Location(BaseModel):
    city: str
    state: str
    country: str

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
def create_person(
        person: Person = Body(...)):  # Request Body. def create_person(name_parameter: type_parameter = is_Body(... mains that it's required))
    return person

# Validations: Query parameter.

@app.get("/person/details") # 
def show_person(
        name: Optional[str] = Query(
        None, 
        min_length = 1, 
        max_length = 30,
        title = "Person name",
        description = "This is a name person. Its between 1 - 30 characters"
        ),
        age: int = Query(
            ..., 
            ge = 0, 
            le = 100,
            title = "Person age",    # Attribute name's description.  
            description = "This is a age person. Its between 0 - 100. Its required"   
            )   # Query parameter always must be Optional but there's a exception like a this where Query is requireds
        ):
    return {name: age}

# Validations: Path parameter.These are parameters requireds.

@app.get("/person/details/{person_ID}")  # A path parameter it sets between {}
def show_person(
        person_ID: int = Path(
        ...,
        ge = 100000, 
        lt = 999999,
        length = 6,
        title = "Person's ID",
        description = "This is the ID that must've a person. With a length 6 numbers."
        )
    ):
    return {person_ID: "It exists"}

# Validations: Request Body.

@app.put("/person/{person_ID}")
def update_person(
        person_ID: int = Path(
            ...,
            title = "Person_ID",
            description = "This is a person ID"
            gt = 100000,
            le = 999999
        ),
        person: Person = Body(...),
        location: Location = Body(...)
    ):
        result = person.dict()
        result = update(location.dict())
        return person
