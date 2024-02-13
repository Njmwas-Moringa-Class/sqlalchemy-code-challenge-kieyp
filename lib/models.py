
from sqlalchemy import (create_engine, PrimaryKeyConstraint, Column, String, Integer,ForeignKey,Table)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,backref


Base = declarative_base()
engine = create_engine('sqlite:///db/restaurants.db', echo=True)


restaurant_user=Table(
    'restaurant_users',
    Base.metadata,
    Column('restaurant_id',ForeignKey('restaurants.id'),primary_key=True),
    Column('customer_id',ForeignKey('customers.id'),primary_key=True),
     extend_existing=True,
    
)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())
    
    reviews=relationship('Review',backref=backref('restaurant'))
    customers=relationship('Customer',secondary=restaurant_user,back_populates='restaurants')

    def __repr__(self):
        return f'Restaurant: {self.name}'

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    reviews=relationship('Review',backref=backref('customer'))
    restaurants=relationship('Restaurant',secondary=restaurant_user,back_populates='customers')
    
    

    def __repr__(self):
        return f'Customer: {self.first_name}'
    
class Review(Base):
    
    __tablename__='reviews'
    
    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    comment = Column(String())
    star_rating=Column(Integer())
    
    restaurant_id=Column(Integer(),ForeignKey('restaurants.id'))
    customer_id=Column(Integer(),ForeignKey('customers.id'))
    
    
    
    def __repr__(self):
        return f'review: {self.star_rating}'

   
    
    