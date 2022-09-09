
## using an Object relational mapper (ORM) to contact the database
# sqlachemy is a famouse ORM

from xml.parsers.expat import model
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from .database import engine, get_db, session
from . import models, schemas
from .database import engine
from .routers import user, auth
#from .config import settings

# as far as we now use alembic to create and updates our tables we can commnet this
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# here we list all domains which are allowed to communicate with our API using a web browser
# we cann add the urls as string ("https://www.google.com") or using "*" means all domains are allowed to communicate
origins = ["*"]

# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# send each request to post or user to see where it matches
#app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
#app.include_router(vote.router)


# this message will be displayed when we send a request to localhost port 8000
# git test comment
@app.get("/")
def root():
    return {"message": "Hello worlddd!"}





print("------------------------------------initializing the roel table ---------------")
#result = engine.execute("select * from role")
#result = engine.execute("select * from role") is None
#print(result)
# for row in result:
#         print(f"{row}")

result = session.query(models.Role).filter(models.Role.name == "provider").first() is None
print(result)

if result:
    # inserting values to role db using engine
    #engine.execute("INSERT INTO role VALUES (1, 'provider')")  # autocommits
    #engine.execute("INSERT INTO role VALUES (2, 'reciepient')")  # autocommits
    #provider_role = models.Role(id=1, name="provider")
    #reciepient_role = models.Role(id=2, name="reciepient")
    #session.add(provider_role)
    #session.commit()
    #session.refresh(provider_role)

    # alternative using multy entry of Session.bulk:
    # alternative 1:
    # session.bulk_insert_mappings(models.Role,
    #                                       [
    #                                         dict(id=1, name="provider"),
    #                                         dict(id=2, name="reciepient")
    #                                       ]
    #                               )

    # alternative 2:
    roles = [
        models.Role(id=1, name="provider"),
        models.Role(id=2, name="reciepient"),
    ]

    session.bulk_save_objects(roles)
    session.commit()








































