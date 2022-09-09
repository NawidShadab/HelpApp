# the schema make us sure that the client send to API the exact piece of DATA that it needs

from datetime import datetime
import email
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from enum import Enum


############################################################
class RoleBase(BaseModel):
    name: str


class create_role(BaseModel):
    id: int
    name: str = "provider"


class Role(RoleBase):
    id: int

    class config:
        orm_mode = True

# class Role2(str, Enum):
#     provider = "provider"
#     recipient = "recipient"

#------------------------------------------------
class AddressBase(BaseModel):
    street: str
    houseNumber: int
    zip: int
    city: str

class Address_create(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int
    owner_id: int

    class config:
        orm_mode = True


class AddressOut(BaseModel):
    id: int
    street: str
    owner_id: int

    class config:
        orm_mode = True

# schema for creat users login
# which infos wie need to recieve from client as request (request body)
class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr



class UserCreate(UserBase):
    password: str
    address: Address_create
    image: str
    role_id: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# schema for user response
# which info API sends back to client (response body)


class UserOut(UserBase):
    id: int
    created_at: datetime
    role_id: int
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    user: UserOut
    address: AddressResponse

    class Config:
        orm_mode = True


############################################################
# login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


############################################################
# token Schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

############################################################


# using data validation (pydantic library) for extracting requests data: "our Schema"
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# our Schema for creat post (how should the creat post look like). it inherit from PostBase class.


class PostCreate(PostBase):
    pass


# schema for respons the user
class ResponsPost(PostBase):
    #  can be remove, because we have them in parent class (PostBase)
    # title: str
    # content: str
    # published: bool
    id: int
    create_at: datetime
    owner_id: int
    owner: UserOut  # a pydantic model (info of user who creat the posts)

    # this tell paydantic model to read the data even if its not a dict
    class Config:
        orm_mode = True


# schema for joined tables (post and vote, who voted for a post)
class PostOut(PostBase):
    Post: ResponsPost
    votes: int

    # this tell paydantic model to read the data even if its not a dict
    class Config:
        orm_mode = True


# schema for vote (like a post)
# the post_id will be take from JWT Token and its an integer
# the dir can be 0 = delete your like from a post,  or 1= like a post
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
