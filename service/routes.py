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
Product Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Product
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Product
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_product():
    """Create a product"""
    app.logger.info("Request to create a product")
    check_content_type("application/json")

    product = Product()
    product.deserialize(request.get_json())
    product.create()

    message = product.serialize()
    location_url = url_for("get_product", product_id=product.id, _external=True)

    app.logger.info("Product with ID [%s] created.", product.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# Helper functions for list_products
######################################################################
def parse_query_parameter(param_value, convert_func, error_msg):
    """Parse and convert a query parameter"""
    if not param_value:
        return None

    try:
        return convert_func(param_value)
    except ValueError:
        abort(status.HTTP_400_BAD_REQUEST, error_msg)


def find_products_by_query_params(product_id, name, description, price, price_lt):
    """Find products based on query parameters"""
    if product_id or name or description or price:
        return Product.find_by_attributes(
            product_id=product_id,
            name=name,
            description=description,
            price=price
        )
    if price_lt:
        return Product.query.filter(Product.price < price_lt).all()
    return Product.all()


######################################################################
# LIST ALL PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns all of the Products"""
    app.logger.info("Request for product list")

    # Process query parameters
    product_id = parse_query_parameter(
        request.args.get("id"),
        int,
        "Invalid product ID format"
    )

    price = parse_query_parameter(
        request.args.get("price"),
        float,
        "Invalid price format"
    )

    price_lt = parse_query_parameter(
        request.args.get("price_lt"),
        float,
        "Invalid price_lt format"
    )

    name = request.args.get("name")
    description = request.args.get("description")

    # Find products by the provided attributes
    products = find_products_by_query_params(
        product_id, name, description, price, price_lt
    )

    results = [product.serialize() for product in products]
    app.logger.info("Returning %d products", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# RETRIEVE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Retrieve a single Product
    This endpoint will return a Product based on its id
    """
    app.logger.info("Request for product with id: %s", product_id)

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Update a Product
    This endpoint will update a Product based on the body that is posted
    """
    app.logger.info("Request to update product with id: %s", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()

    app.logger.info("Product with ID [%s] updated.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a Product
    This endpoint will delete a Product based on the id specified in the path
    """
    app.logger.info("Request to delete product with id: %s", product_id)

    product = Product.find(product_id)
    if product:
        product.delete()

    app.logger.info("Product with ID [%s] delete complete.", product_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# LIKE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>/like", methods=["PUT"])
def like_product(product_id):
    """
    Like a Product
    This endpoint will increment the like count of a product
    """
    app.logger.info("Request to like product with id: %s", product_id)

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    product.likes += 1
    product.update()

    app.logger.info("Product with ID [%s] liked.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# HEALTH ENDPOINT
######################################################################
@app.route("/health", methods=["GET"])
def health():
    """Health Status"""
    return jsonify({"status": "OK"}), status.HTTP_200_OK


######################################################################
# UTILITY FUNCTIONS
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be set")

    if request.headers["Content-Type"] != content_type:
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )
