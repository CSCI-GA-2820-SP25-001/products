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
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Product Demo REST API Service",
            version="1.0",
            paths=url_for("list_products", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_product():
    """
    Create a Product
    This endpoint will create a Product based on the data in the body that is posted
    """
    app.logger.info("Request to Create a Product...")
    check_content_type("application/json")

    product = Product()
    # Get the data from the request and deserialize it
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    product.deserialize(data)

    # Save the new Product to the database
    product.create()
    app.logger.info("Product with new id [%s] saved!", product.id)

    # Return the location of the new Product
    location_url = url_for("get_product", product_id=product.id, _external=True)

    return (
        jsonify(product.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# UPDATE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Update a Product

    This endpoint will update a Product based the body that is posted
    """
    app.logger.info("Request to Update a product with id [%s]", product_id)
    check_content_type("application/json")

    # Attempt to find the Product and abort if not found
    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    # Update the Product with the new data
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    product.deserialize(data)

    # Save the updates to the database
    product.update()

    app.logger.info("Product with ID: %d updated.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# READ A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Retrieve a single Product

    This endpoint will return a Product based on it's id
    """
    app.logger.info("Request to Retrieve a product with id [%s]", product_id)

    # Attempt to find the Product and abort if not found
    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a Product

    This endpoint will delete a Product based the id specified in the path
    """
    app.logger.info("Request to Delete a product with id [%s]", product_id)

    # Delete the Product if it exists
    product = Product.find(product_id)
    if product:
        app.logger.info("Product with ID: %d found.", product.id)
        product.delete()

    app.logger.info("Product with ID: %d delete complete.", product_id)
    return {}, status.HTTP_204_NO_CONTENT


######################################################################
# LIST ALL PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns a list of Products with optional query parameters"""
    app.logger.info("Request for product list")

    product_id = request.args.get("id")
    name = request.args.get("name")
    description = request.args.get("description")
    price = request.args.get("price")
    price_lt = request.args.get("price_lt")

    query = Product.query

    if product_id is not None:
        try:
            product_id = int(product_id)
            query = query.filter(Product.id == product_id)
        except ValueError:
            abort(status.HTTP_400_BAD_REQUEST, "ID must be an integer.")

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))

    if description:
        query = query.filter(Product.description.ilike(f"%{description}%"))

    if price is not None:
        try:
            price = float(price)
            query = query.filter(Product.price == price)
        except ValueError:
            abort(status.HTTP_400_BAD_REQUEST, "Price must be a number.")

    if price_lt:
        try:
            price_lt = float(price_lt)
            query = query.filter(Product.price < price_lt)
        except ValueError:
            abort(status.HTTP_400_BAD_REQUEST, "price_lt must be a number.")

    products = query.all()
    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK


######################################################################
# LIKE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>/like", methods=["PUT"])
def like_product(product_id):
    """Like a product (increment the likes count)"""
    app.logger.info("Request to like product with id: %d", product_id)
    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    product.likes += 1
    product.update()

    app.logger.info("Product with ID: %d has now %d likes.", product.id, product.likes)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
