"""
Background step that seeds the catalog through the REST API.
"""

from http import HTTPStatus
import requests
from behave import given, when, then


@given("the following products")
def step_impl(ctx):
    """Clear DB then POST each table row as JSON."""
    base = f"{ctx.base_url}/products"

    # wipe existing data (ignore 404)
    for item in requests.get(base, timeout=30).json():
        requests.delete(f"{base}/{item['id']}", timeout=30)

    # create rows from the feature table
    for row in ctx.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "likes": int(row["likes"]),
        }
        ctx.resp = requests.post(base, json=payload, timeout=30)
        assert ctx.resp.status_code == HTTPStatus.CREATED
