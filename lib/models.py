
from sqlalchemy import (create_engine, PrimaryKeyConstraint, Column, String, Integer,ForeignKey,Table)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,backref
from sqlalchemy.orm import sessionmaker



Base = declarative_base()
engine = create_engine('sqlite:///db/restaurants.db', echo=True)
session=sessionmaker(bind=engine)
session=session()



restaurant_user=Table(
    #customers_users
    'restaurant_users',
    Base.metadata,
    Column('restaurant_id',ForeignKey('restaurants.id'),primary_key=True),
    Column('customer_id',ForeignKey('customers.id'),primary_key=True),
     extend_existing=True,
    
)

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    comment = Column(String())
    star_rating = Column(Integer())
    
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    
    def __repr__(self):
        return f'Review: {self.star_rating}'

    def get_customer(self):
        """
        Returns the Customer instance associated with this review.
        """
        return self.customer

    def get_restaurant(self):
        """
        Returns the Restaurant instance associated with this review.
        """
        return self.restaurant
    
    
    def full_review(self):
        """
        Returns a formatted string representing the full review.
        """
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    
    reviews = relationship('Review', backref=backref('customer'))
    restaurants = relationship('Restaurant', secondary=restaurant_user, back_populates='customers')

    def __repr__(self):
        return f'Customer: {self.first_name}'

    def get_reviews(self):
        """
        Returns a collection of all the reviews that the Customer has left.
        """
        return self.reviews
    
    def get_restaurants(self):
        """
        Returns a collection of all the restaurants that the Customer has reviewed.
        """
        return self.restaurants
    
    def full_name(self):
        """
        Returns the full name of the customer, with the first name and the last name concatenated.
        """
        return f"{self.first_name} {self.last_name}"
    
    
    def favorite_restaurant(self):
        """
        Returns the restaurant instance that has the highest star rating from this customer.
        """
        # Get all reviews by this customer
        customer_reviews = self.reviews

        # Find the review with the highest star rating
        highest_rating_review = max(customer_reviews, key=lambda review: review.star_rating)

        # Return the associated restaurant of the highest rated review
        return highest_rating_review.restaurant
    
    
    def add_review(self, restaurant, rating):
        """
        Creates a new review for the restaurant with the given rating.
        """
        new_review = Review(score=rating, restaurant=restaurant, customer=self, star_rating=rating)
       
       
       
       
       
    def delete_reviews(self, restaurant):
        """
        Removes all reviews by this customer for the given restaurant.
        """
        # Get all reviews by this customer for the given restaurant
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]

        # Delete the reviews from the database
        for review in reviews_to_delete:
            session.delete(review)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())
    
    reviews = relationship('Review', backref=backref('restaurant'))
    customers = relationship('Customer', secondary=restaurant_user, back_populates='restaurants')

    def __repr__(self):
        return f'Restaurant: {self.name}'

    def get_reviews(self):
        """
        Returns a collection of all the reviews for the Restaurant.
        """
        return self.reviews

    def get_customers(self):
        """
        Returns a collection of all the customers who reviewed the Restaurant.
        """
        return self.customers

    
    
    @classmethod
    def fanciest(cls, session):
        """
        Returns the restaurant instance with the highest price.
        """
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        """
        Returns a list of strings with all the reviews for this restaurant formatted as specified.
        """
        review_strings = []
        for review in self.reviews:
            review_strings.append(f"Review for {self.name} by {review.customer.full_name()}: {review.star_rating} stars.")
        return review_strings