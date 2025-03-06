"""
Test Factory to make fake objects for testing
"""

import factory
from service.models import Product


class ProductFactory(factory.Factory):
    """Creates fake products that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    description = factory.Faker("name")
    price = factory.Faker(
        "pydecimal",
        left_digits=8,
        right_digits=2,
        positive=True,
        min_value=1,
        max_value=99999999.99,
    )

    # Todo: Add your other attributes here...
