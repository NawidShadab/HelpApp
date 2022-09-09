from email.headerregistry import Address
from email.policy import default
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship





# class for making table
# class Post(Base):
#     # table name
#     __tablename__ = 'posts_table'

#     # table columns
#     id = Column(Integer, primary_key=True, nullable = False) # not null
#     title = Column(String, nullable = False)
#     content = Column(String, nullable = True)
#     published = Column(Boolean, server_default = 'True',  nullable = False)
#     create_at = Column(TIMESTAMP(timezone=True),
#                        nullable = False, server_default = text('now()'))
#     # relation between table user_login and table post(1 to many). which user creat what posts
#     owner_id = Column(Integer, ForeignKey("users_login.id", ondelete="CASCADE"), nullable = False)

#     # relationship between the User class and Post. we can see information of users who creat a post
#     owner = relationship("User")



# class for making user login table
class User(Base):
    # table name
    __tablename__ = 'users'

    # table columns
    id = Column(Integer, primary_key=True, nullable = False) # not null
    firstName = Column(String, nullable = False)
    lastName = Column(String, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    image = Column(String, nullable = False)
    #role = Column(String, nullable = False)

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE") ,nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable = False, server_default=text('now()'))



    address = relationship("Address", back_populates = "owner")
    role = relationship("Role", back_populates = "owner")


# better to send an astring as a vlaue from frontend ("provider" or "reciepant" )
class Role(Base):
    __tablename__ = 'roles'

    # table columns
    id = Column(Integer, primary_key=True, nullable = False,) # not null
    name = Column(String, nullable = False)

    owner = relationship("User", back_populates = "role")



class Address(Base):
    __tablename__ = 'addresses'

    # table columns
    id = Column(Integer, primary_key=True, nullable = False) # not null
    street = Column(String, nullable = False)
    houseNumber = Column(Integer, nullable = False)
    zip = Column(Integer, nullable = False)
    city = Column(String, nullable = False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE") ,nullable = False)

    owner = relationship("User", back_populates="address")


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, nullable = False)
    name = Column(String, nullable = False)
    age_category_id = Column(Integer, ForeignKey("age_categories.id", ondelete="CASCADE") ,nullable = False)
    sex = Column(String, nullable = False)
    size = Column(Integer, ForeignKey("sizes.id", ondelete="CASCADE") ,nullable = False)
    image = Column(String, nullable = False)
    barcode = Column(String, nullable = False)
    details_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE") ,nullable = False)

    created_at = Column(TIMESTAMP(timezone=True),
                       nullable = False, server_default=text('now()'))

    # category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE") ,nullable = False)
    # sub_category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE") ,nullable = False)
    # provider_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE") ,nullable = False)
    # reciepient_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE") ,nullable = False)
    # status_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE") ,nullable = False)

    age = relationship("AgeCategory", back_populates = "owner")
    article_size = relationship("Size", back_populates = "owner")
    # article_cat = relationship("Category", back_populates = "owner")
    # article_sub_cat = relationship("SubCategory", back_populates = "owner")
    # article_status = relationship("Status", back_populates = "owner")



class AgeCategory(Base):
    __tablename__ = 'age_categories'

    id = Column(Integer, primary_key=True, nullable = False)
    name = Column(String, nullable = False)

    owner = relationship("Article", back_populates = "age")



class Size(Base):
    __tablename__ = 'sizes'

    id = Column(Integer, primary_key=True, nullable = False)
    name = Column(String, nullable = False)

    owner = relationship("Article", back_populates = "article_size")



class Detail(Base):
    __tablename__ = 'Details'

    id = Column(Integer, primary_key=True, nullable = False)
    name = Column(String, nullable = False)

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE") ,nullable = False)
    sub_category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE") ,nullable = False)
    provider_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE") ,nullable = False)
    reciepient_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE") ,nullable = False)
    status_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE") ,nullable = False)

    article_cat = relationship("Category", back_populates = "owner")
    article_sub_cat = relationship("SubCategory", back_populates = "owner")
    article_status = relationship("Status", back_populates = "owner")

    owner = relationship("Article", back_populates = "article_size")



class Category(Base):
    __tablename__ = 'Categories'

    id = Column(Integer, primary_key=True, nullable = False)
    name = Column(String, nullable = False)

    owner = relationship("Detail", back_populates = "article_cat")



class SubCategory(Base):
    __tablename__ = 'SubCategories'

    id = Column(Integer, primary_key=True, nullable = False)
    name = Column(String, nullable = False)

    owner = relationship("Detail", back_populates = "article_sub_cat")



class Status(Base):
    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True, nullable = False)
    name = Column(String, nullable = False)

    owner = relationship("Detail", back_populates = "article_status")



# class for making votes table in postgris DB
# this table is using to see which user likes which posts.
# it hase 2 columns (user_id, post_id). the info of user id we get from users_login table (as foriegnKey)
# and the info or value for post_id clm we get from posts_table (using its primary key here as foriegn key)
# class Vote(Base):
#     __tablename__ = "votes"
#     user_id = Column(Integer, ForeignKey("users_login.id", ondelete="CASCADE"), primary_key=True)
#     post_id = Column(Integer, ForeignKey("posts_table.id", ondelete="CASCADE"), primary_key=True)



####### command to run server: uvicorn app.main_4:app --reload #########
