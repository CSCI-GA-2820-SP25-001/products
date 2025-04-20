"""
Models for Product

All of the models are stored in this module
"""

import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class Product(db.Model):
    """
    Class that represents a Product
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    description = db.Column(db.String(256))
    price = db.Column(db.Numeric(10, 2))
    likes = db.Column(db.Integer, nullable=False, default=0)

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        """Returns a string representation of the Product"""
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """Creates a Product in the database"""
        logger.info("Creating %s", self.name)
        self.id = None
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """Updates a Product in the database"""
        logger.info("Saving %s", self.name)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Deletes a Product from the database"""
        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "likes": self.likes,
        }

    def deserialize(self, data):
        """Deserializes a Product from a dictionary"""
        try:
            self.name = data["name"]
            self.description = data["description"]
            self.price = data["price"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Product: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS (Queries)
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Products in the database"""
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Product by its ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Products with the given name"""
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_description(cls, description):
        """Returns all Products with the given description"""
        logger.info("Processing description query for %s", description)
        return cls.query.filter(cls.description == description).all()

    @classmethod
    def find_by_price(cls, price):
        """Returns all Products with the given price"""
        logger.info("Processing price query for %s", price)
        return cls.query.filter(cls.price == price).all()

    @classmethod
    def find_by_price_less_than(cls, price):
        """Returns all Products with a price less than given value"""
        logger.info("Processing price less than query for %s ...", price)
        return cls.query.filter(cls.price < price)

    @classmethod
    def find_by_attributes(
        cls, product_id=None, name=None, description=None, price=None
    ):
        """Finds Products using optional filters"""
        query = cls.query
        if product_id is not None:
            query = query.filter(cls.id == product_id)
        if name is not None:
            query = query.filter(cls.name.ilike(f"%{name}%"))
        if description is not None:
            query = query.filter(cls.description.ilike(f"%{description}%"))
        if price is not None:
            query = query.filter(cls.price == price)
        return query.all()
