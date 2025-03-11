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
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Todo: Place your REST API code here ...

######################################################################
# LIST ALL PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def get_all_products():
    """Returns all of the products"""
    app.logger.info("Request for products list")

    products = []

    # Parse any arguments from the query string
    id = request.args.get("id")
    name = request.args.get("name")
    description = request.args.get("description")
    price = request.args.get("price")

    if id:
        app.logger.info("Find by id: %d", int(id))
        products = products.find_by_products(category)
    elif name:
        app.logger.info("Find by name: %s", name)
        products = products.find_by_name(name)
    elif description:
        products = products.find_by_description(description)
    elif price:
        app.logger.info("Find by price: %f", float(price))
        products = products.find_by_price(price)
    else:
        app.logger.info("Find all")
        products = products.all()

    results = [products.serialize() for products in products]
    app.logger.info("Returning %d products", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
