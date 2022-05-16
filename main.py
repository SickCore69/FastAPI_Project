# Python
from typing import Optional
from enum import Enum   # To Enumarate hair color 

# Pydantic
from pydantic import BaseModel  # Para representar entidades en codigo
from pydantic import Field  # This class equal to Body, Query and Path but this is use to validate BaseModel's attibutes.
from pydantic import EmailStr   # Validate if a string is a email. 

# FastAPI
from fastapi import FastAPI
from fastapi import status  # Put the status code of a request. Its put in the path operation decorator.
from fastapi import Body    # Class to know if a parameter is type Body.
from fastapi import Query   # Class to asigment a Query parameter or a constrains parameters.
from fastapi import Path    # To create Path parameters.
from fastapi import Form    # To can use forms.
from fastapi import Header, Cookie, UploadFile, File
# from fastapi import Body, Query, Path, Form, Header, Cookie

app = FastAPI()


# Models
class HairColor(Enum):
    """ HairColor. \n
    It that inherits attributes from class Enum to enumerate attributes that it has.\n
    Attibute_name = Data that recieve
    gray = "gray" """
    brown = "brown"
    blonde = "blonde"
    red = "red" 
    black = "black"
    white = "white"

class Location(BaseModel):
    """ Location.\n
    Class that has string attributes to know where lives the user or person.
    """
    city: str
    state: str
    country: str

    class Config:
        """ Class Config 
        It used to makes schemas or creates examples inside of class """
        schema_extra = {
                "example": {
                    "city": "CDMX",
                    "state": "Estado de Mexico",
                    "country": "Mexico"
                    }
                }
class PersonBase(BaseModel):
    """ PersonBase \n
    Class to create a person with minimun attibutes.\n
    attribute_name: type_data = Path Operation(attribute required its represented by ...)\n
    Path parameters(attributes) in a BaseModel has validations Field or constrains to that an user doesn't put things that aren't allowed.\n
    Validations Field are ... that means that this attribute is required, then is min_length and max_length to specificate the length minimun and maximun that it can has the attribute. """
    first_name: str = Field(
            ...,
            min_length = 1,
            max_length = 15,
            title = "First name",
            description = "This is first name."
            )    
    last_name: str = Field(
            ...,
            min_length = 1, 
            max_length = 15,
            title = "Last name",
            description = "This is last name."
            )
    age: int = Field(
            ...,
            gt = 0,
            le = 100,
            title = "Age",
            description = "This is the age of the person."
            )    
    is_married: Optional[bool] = Field(
    default = None,
    title = "Is married?",
    description = "To know if person is married or not"
    )
    height: Optional[int] = Field(
    default = None,
    title = "Height",
    description = "Person height."
    )
    hair_color: Optional[HairColor] = Field(
    default = None,
    title = "Hair color",
    description = "Person hair color."
    )

    class Config:   # To automatic test with default dates 
        """ Class Config.\n
        Is to create examples inside of a class to faster test """    
        schema_extra = {
                "example": {
                    "first_name": "Mark",
                    "last_name": "Pole",
                    "age": 44,
                    "hair_color": "black",
                    "is_married": "True",
                    "height": 180,
                    "password": "DkvR5%6&"
                    } 
                }

class Person(PersonBase): 
    """ Person. \n
    Subclass that inherits all attributes from class PersonBase also it has its our attibute that doesn't share.\n
    first_name, last_name, age, hair_color, height and is_married from PersonBase and password it's an own attribute.\n
    return: Mark, Pole, 44, black, 180, True and DkvR5%6& """       
    password: str = Field(
            ...,
            min_length = 8
            )

    
class PersonOut(PersonBase):    
    """ Person Out.\n
    Subclass PersonOut that inherits attibutes from super class PersonBase.\n
 2 files changed, 116 insertions(+), 28 deletions(-)
    first_name, last_name, age, hair_color, height and is_married from PersonBase.\n
    return: Mark, Pole, 44, black, 180, True """
    pass

class LoginOut(BaseModel):
    """ Login Out.\n
    Class for the user can login in API. It isn't has the password by security because loginOut is the out that will show to person.\n 
    username, message\n
    return {"username":"Any username greater to 20 characters", "massage":"Login succesfully"} """
    username: str = Field(
    ...,
    max_length = 20,
    title = "Username",
    description = "This is person's username to can log in. ",
    example = "Dr. Oc"
    )
    message: str = Field(default = "Login succesfully")

@app.get(
path = "/",
status_code = status.HTTP_200_OK
)
def home():
    """ Home\n
    Path Operation decorator to go at Home. Path, route or endpoint to access at these place("/").\n
    Function just return a json {"Hello":"World"} """
    return {"Hello": "World"}


# Request and Response Body
@app.post(path = "/person/new",
        response_model = PersonOut,
        status_code = status.HTTP_201_CREATED
        )    # Decorator that sends a request(post) to server with url "/person/new". You can access with one. 
def create_person(        
        person: Person = Body(...)
    ):
        """ Create Person
        Function to create a new person. Attribute person its type Person, its meaning that inherits attributes from class Person and then return the attribute person or the person created. this is a request body from client to sever. \n 
        recieve: All attibutes from class Person to can create a person.\n
        return: To person created in this case whould be PersonOut """
        return person


# Validations: Query parameter.
@app.get(path = "/person/details",
        status_code = status.HTTP_200_OK) 
def show_person(
        name: Optional[str] = Query(
        None, 
        min_length = 1, 
        max_length = 30,
        title = "Person name",
        description = "This is a name person. Its between 1 - 30 characters", 
        example = "Lucas"
        ),
        age: int = Query(
            ..., 
            ge = 0, 
            le = 100,
            title = "Person age",    # Attribute name's description.  
            description = "This is a age person. Its between 0 - 100. Its required",
            example = 32
            )   # Query parameter always must be Optional but there's a exception like a this where Query is requireds
        ):
    return {name: age}


# Validations: Path parameter.These are parameters requireds.
@app.get(path = "/person/details/{person_ID}",
        status_code = status.HTTP_200_OK
        )  # A path parameter it sets between {}
def show_person(
        person_ID: int = Path(
        ...,
        ge = 100000, 
        lt = 999999,
        length = 6,
        title = "Person's ID",
        description = "This is the ID that must've a person. With a length 6 numbers.",
        example = 184139
        )
    ):
    return {person_ID: "It exists"}


# Validations: Request Body.
@app.put(path = "/person/{person_ID}",
        status_code = status.HTTP_200_OK)
def update_person(
        person_ID: int = Path(
            ...,
            title = "Person_ID",
            description = "This is a person ID",
            gt = 100000,
            le = 999999,
            example = 168894
        ),
        person: Person = Body(...),

        location: Location = Body(...)       
    ):
        result = person.dict()
        result.update(location.dict())
        return result


# Forms
@app.post(
path = "/login",
response_model = LoginOut,
status_code = status.HTTP_200_OK
)
def login(
username: str = Form(...),
password: str = Form(...)
):
    return LoginOut(username = username)


# Cookies and Headres Parameters
@app.post(
path = "/contact",
status_code = status.HTTP_200_OK
)
def contact(
first_name: str = Form(
...,
min_length = 1,
max_length = 20
),
last_name: str = Form(
...,
min_length = 1,
max_length = 25
),
number_phone: int = Form(
...,
lt = 9999999999,
gt = 1111111111
),
email: EmailStr = Form(...,),
message: str = Form(
...,
min_length = 20
),
user_agent: Optional[str] = Header(default = None),
ads: Optional[str] = Cookie(default = None)
):
    return user_agent


# Files
@app.post(
        path = "/post-image",
        status_code = status.HTTP_200_OK
        )
def post_image(
        image: UploadFile = File(...)
        ):
    return {
            "Filename": image.filename,
            "Format": image.content_type,
            "Size(Kb)": round(len(image.file.read())/1024, ndigits = 2)
            }

