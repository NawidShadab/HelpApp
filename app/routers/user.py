from fastapi import Body, FastAPI,Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import oauth2
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, get_db
import logging

logger = logging.getLogger()

# this library helps to have the path operations related to your posts separated from the rest of the code, to keep it organized.
# we can pass also the path as prefix to not to type it for each request.
router = APIRouter(
    prefix="/users",
    tags=['Users']  # for grouping the documentation
)




# register new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db),
                  ):


    # cheking if the entered email already exists
    user_email = user.email
    user_email_db = db.query(models.User).filter(models.User.email == user_email).first()
    if user_email_db:
        raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"User with email: {user_email} already exist")

    # hash the password - user.password
    hashed_password = utils.hash(user.password)

    # update the user password with overrite it with hashed one
    user.password = hashed_password

    # better to convert the pydantic obj to dic and upack it
    #new_user = models.User(**user.dict())
    new_user = models.User(firstName=user.firstName, lastName=user.lastName, email=user.email,
                           password=user.password, image=user.image, role=user.role
                          )

    print(str(new_user.firstName))
    #user_address = models.Address(**schemas.Address_create.dict(), owner_id=user.id)



    db.add(new_user)    # add new post to DB
    db.commit() # save the post in DB
    db.refresh(new_user)    # retun the message, like Returning *

    #user_id=schemas.UserOut.id,
    # print("__________________ here", new_user.id)

    # user_address = models.Address(street=user.address.street, houseNumber=user.address.houseNumber,
    #                               zip=user.address.zip, city=user.address.city, owner_id=new_user.id )

    # db.add(user_address)
    # db.commit()
    # db.refresh(user_address)

    # addimg address info os user to address table
    user_address = create_address(user ,new_user.id, db)


    #user_out = new_user user_address
    creat_at = new_user.created_at
    print("-------------------", type(new_user))
    print("-------------------", type(user_address))
    user = schemas.UserOut(id=new_user.id, firstName=new_user.firstName, lastName=new_user.lastName, email=new_user.email, created_at=new_user.created_at)
    address = schemas.AddressResponse(id=user_address.id, owner_id=user_address.owner_id, street=user_address.street, city=user_address.city, houseNumber=user_address.houseNumber, zip=user_address.zip)
    return schemas.UserResponse(user=user, address=address)
    #return new_user



def create_address(user: schemas.UserCreate, user_id: int, db: Session = Depends(get_db)):
    user_address = models.Address(street=user.address.street, houseNumber=user.address.houseNumber,
                                   zip=user.address.zip, city=user.address.city, owner_id=user_id )

    db.add(user_address)
    db.commit()
    db.refresh(user_address)


    return user_address







# get the registered user by id
@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user),):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")


    return user
