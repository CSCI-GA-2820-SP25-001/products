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
TestProduct API Service Test Suite
"""

# pylint: disable=duplicate-code
import os
import logging
from decimal import Decimal
from unittest import TestCase
from urllib.parse import quote_plus

from wsgi import app
from service.common import status
from service.models import db, Product
from .factories import ProductFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "/products"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    # def test_query_products_by_category(self):
    #     """It should Query Products by Category"""
    #     product1 = ProductFactory(category="Electronics")
    #     product2 = ProductFactory(category="Clothing")
    #     self.client.post(BASE_URL, json=product1.serialize())
    #     self.client.post(BASE_URL, json=product2.serialize())

    #     response = self.client.get(BASE_URL, query_string="category=Electronics")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     data = response.get_json()
    #     self.assertEqual(len(data), 1)
    #     self.assertEqual(data[0]["category"], "Electronics")

    def test_query_products_by_name(self):
        """It should Query Products by Name"""
        product = ProductFactory(name="iPhone")
        self.client.post(BASE_URL, json=product.serialize())

        response = self.client.get(BASE_URL, query_string="name=iPhone")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "iPhone")

    def test_query_products_by_price_lt(self):
        """It should Query Products by Price Less Than"""
        # Clear the database
        db.session.query(Product).delete()
        db.session.commit()

        # Create two products
        product1 = Product(name="Cheap Product", description="Low price", price=50)
        product2 = Product(
            name="Expensive Product", description="High price", price=150
        )

        db.session.add(product1)
        db.session.add(product2)
        db.session.commit()

        # Now test the endpoint
        response = self.client.get(BASE_URL, query_string={"price_lt": 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(float(data[0]["price"]), 50.0)  # Check that it's the cheap one

    # def test_query_products_no_matches(self):
    #     """It should return an empty list if no products match"""
    #     product = ProductFactory(category="Books")
    #     self.client.post(BASE_URL, json=product.serialize())

    #     response = self.client.get(BASE_URL, query_string="category=Electronics")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     data = response.get_json()
    #     self.assertEqual(data, [])

    def test_query_products(self):
        """It should Query Products by attributes"""
        product1 = ProductFactory(name="iPhone", description="Smartphone", price=999.99)
        product2 = ProductFactory(
            name="Samsung Galaxy", description="Android Phone", price=899.99
        )
        product3 = ProductFactory(name="MacBook", description="Laptop", price=1299.99)

        db.session.add(product1)
        db.session.add(product2)
        db.session.add(product3)
        db.session.commit()

        # Query by name
        response = self.client.get(BASE_URL, query_string={"name": "iPhone"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "iPhone")

        # Query by description
        response = self.client.get(BASE_URL, query_string={"description": "Laptop"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["description"], "Laptop")

        # Query by price
        response = self.client.get(BASE_URL, query_string={"price": "999.99"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(float(data[0]["price"]), 999.99)

        # Query by id
        response = self.client.get(BASE_URL, query_string={"id": product2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], product2.id)

        # Query no matches
        response = self.client.get(BASE_URL, query_string={"name": "NonExistent"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 0)

        # No query params (return all)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 3)

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    ############################################################
    # Utility function to bulk create products
    ############################################################
    def _create_products(self, count: int = 1) -> list:
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test product",
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    def test_query_product_with_invalid_id(self):
        """It should return 400 if id is not an integer"""
        response = self.client.get(BASE_URL + "?id=not-an-int")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_query_product_with_invalid_price(self):
        """It should return 400 if price is not a number"""
        response = self.client.get(BASE_URL + "?price=abc")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_query_product_with_invalid_price_lt(self):
        """It should return 400 if price_lt is not a number"""
        response = self.client.get(BASE_URL + "?price_lt=cheap")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_find_by_attributes(self):
        """It should find product by multiple attributes"""
        product = Product(
            name="Magic Keyboard", description="Apple keyboard", price=129.99
        )
        product.create()

        results = Product.find_by_attributes(
            product_id=product.id,
            name="Magic Keyboard",
            description="Apple keyboard",
            price=129.99,
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Magic Keyboard")
        self.assertEqual(results[0].description, "Apple keyboard")
        self.assertEqual(float(results[0].price), 129.99)

    # ----------------------------------------------------------
    # TEST CREATE PRODUCT
    # ----------------------------------------------------------
    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        logging.debug("Test Product: %s", test_product.serialize())
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["description"], test_product.description)
        self.assertEqual(Decimal(new_product["price"]), test_product.price)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["description"], test_product.description)
        self.assertEqual(Decimal(new_product["price"]), test_product.price)

    def test_create_with_bad_request(self):
        """It should not Create when sending the wrong data"""
        response = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should not Create when sending wrong media type"""
        product = ProductFactory()
        response = self.client.post(
            BASE_URL, json=product.serialize(), content_type="test/html"
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_wrong_content_type(self):
        """It should return a 415 unsupported media type"""
        headers = {"Content-Type": "text/plain"}
        resp = self.client.post(
            "/products", data="product_status=pending", headers=headers
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_no_content_type(self):
        """It should return a 415 unsupported media type"""
        resp = self.client.post("/products", data="product_status=pending")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_missing_content_type_header(self):
        """It should return 415 if no Content-Type header is present"""
        resp = self.client.post("/products", data="{}")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_wrong_content_type_header(self):
        """It should return 415 if wrong Content-Type header"""
        headers = {"Content-Type": "text/plain"}
        resp = self.client.post("/products", headers=headers, data="{}")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    # ----------------------------------------------------------
    # TEST UPDATE
    # ----------------------------------------------------------
    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = response.get_json()
        logging.debug(new_product)
        new_product["description"] = "test description"
        response = self.client.put(f"{BASE_URL}/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["description"], "test description")

    def test_update_product_with_invalid_data(self):
        """It should not Update a Product with invalid data"""
        test_product = self._create_products(1)[0]
        # Try updating with invalid data
        invalid_data = test_product.serialize()
        invalid_data["price"] = "not a number"
        response = self.client.put(f"{BASE_URL}/{test_product.id}", json=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ----------------------------------------------------------
    # TEST READ
    # ----------------------------------------------------------
    def test_get_product(self):
        """It should Get a single Product"""
        # get the id of a product
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        """It should not Get a Product thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    # ----------------------------------------------------------
    # TEST DELETE
    # ----------------------------------------------------------
    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = self._create_products(1)[0]
        print(test_product)
        print(test_product.id)
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_product(self):
        """It should Delete a Product even if it doesn't exist"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        resp = self.client.put(BASE_URL, json={"not": "allowed"})
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # ----------------------------------------------------------
    # TEST LIST
    # ----------------------------------------------------------
    def test_get_product_list(self):
        """It should Get a list of Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_get_product_list_by_name(self):
        """It should Get a list of Products by name"""
        products = self._create_products(5)
        name = products[0].name
        response = self.client.get(f"{BASE_URL}?name={quote_plus(name)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]["name"], name)

    def test_get_product_list_by_description(self):
        """It should Get a list of Products by description"""
        products = self._create_products(5)
        description = products[0].description
        response = self.client.get(f"{BASE_URL}?description={quote_plus(description)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]["description"], description)

    def test_get_product_list_by_price(self):
        """It should Get a list of Products by price"""
        products = self._create_products(5)
        price = products[0].price
        response = self.client.get(f"{BASE_URL}?price={str(price)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(float(data[0]["price"]), float(price))

    def test_like_a_product(self):
        """It should Like a Product"""
        test_product = self._create_products(1)[0]
        response = self.client.put(f"{BASE_URL}/{test_product.id}/like")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["likes"], 1)

        # Like it again
        response = self.client.put(f"{BASE_URL}/{test_product.id}/like")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["likes"], 2)

    def test_like_nonexistent_product(self):
        """It should return 404 when liking a product that does not exist"""
        response = self.client.put("/products/99999/like")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------------------------------------------------
    # TEST Health
    # ----------------------------------------------------------
    def test_health_check(self):
        """It should return status OK for the health check"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json(), {"status": "OK"})
