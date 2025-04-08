######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Test cases for product Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from unittest.mock import patch

from wsgi import app
from service.models import Product, DataValidationError, db
from tests.factories import ProductFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "/products"


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProduct(TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    # Create
    def test_create_product(self):
        """It should create a Product"""
        product = ProductFactory()
        product.create()
        self.assertIsNotNone(product.id)
        found = Product.all()
        self.assertEqual(len(found), 1)
        data = Product.find(product.id)
        self.assertEqual(data.name, product.name)
        self.assertEqual(data.description, product.description)
        self.assertEqual(data.price, product.price)

    def test_create_a_product(self):
        """It should Create a Product and assert that it exists"""
        product = Product(
            name="Headphone", description="Noise cancelling", price=100.00
        )
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Headphone")
        self.assertEqual(product.description, "Noise cancelling")
        self.assertEqual(product.price, 100.00)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)

    @patch("service.models.db.session.commit")
    def test_add_product_failed(self, exception_mock):
        """It should not create a product on database error"""
        exception_mock.side_effect = Exception()
        product = ProductFactory()
        self.assertRaises(DataValidationError, product.create)

    # Read
    def test_read_product(self):
        """It should Read a product"""
        product = ProductFactory()
        product.create()

        # Read it back
        found_product = Product.find(product.id)

        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)

    # Delete
    def test_delete_a_product(self):
        """It should Delete a product from the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        product = products[0]
        product.delete()
        products = Product.all()
        self.assertEqual(len(products), 0)

    @patch("service.models.db.session.commit")
    def test_delete_product_failed(self, exception_mock):
        """It should not delete a product on database error"""
        exception_mock.side_effect = Exception()
        product = ProductFactory()
        self.assertRaises(DataValidationError, product.delete)

    # Update
    def test_update_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.create()
        self.assertIsNotNone(product.id)
        product.description = "Updated description"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "Updated description")
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].description, "Updated description")

    @patch("service.models.db.session.commit")
    def test_update_product_failed(self, exception_mock):
        """It should not update a product on database error"""
        exception_mock.side_effect = Exception()
        product = ProductFactory()
        self.assertRaises(DataValidationError, product.update)

    # Delete
    def test_delete_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    # List
    def test_list_all_products(self):
        """It should List all products in the database"""
        products = Product.all()
        self.assertEqual(products, [])
        for _ in range(5):
            product = ProductFactory()
            product.create()
        products = Product.all()
        self.assertEqual(len(products), 5)

    # Serialization
    def test_serialize_a_product(self):
        """It should serialize a Product"""
        product = ProductFactory()
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], product.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], product.name)
        self.assertIn("description", data)
        self.assertEqual(data["description"], product.description)
        self.assertIn("price", data)
        self.assertEqual(data["price"], product.price)

    def test_deserialize_a_product(self):
        """It should de-serialize a Product"""
        data = ProductFactory().serialize()
        product = Product()
        product.deserialize(data)
        self.assertNotEqual(product, None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.description, data["description"])
        self.assertEqual(product.price, data["price"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a Product with missing data"""
        data = {"id": 1, "name": "Monitor"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    # Find
    def test_find_product_by_id(self):
        """It should Find a Product by ID"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        logging.debug(products)
        for product in products:
            found = Product.find(product.id)
            self.assertEqual(found.id, product.id)
            self.assertEqual(found.name, product.name)
            self.assertEqual(found.description, product.description)
            self.assertEqual(found.price, product.price)
