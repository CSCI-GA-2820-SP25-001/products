######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
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
"""Step Definitions for Product.feature using behave and Selenium."""

import time
import re
from http import HTTPStatus
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave import given, when, then


@given("the following products")
def step_impl(ctx):
    """Clear DB then POST each table row as JSON."""
    base = f"{ctx.base_url}/products"
    for item in requests.get(base, timeout=30).json():
        requests.delete(f"{base}/{item['id']}", timeout=30)
    for row in ctx.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "likes": int(row["likes"]),
        }
        ctx.resp = requests.post(base, json=payload, timeout=30)
        assert ctx.resp.status_code == HTTPStatus.CREATED


@when('I visit the "Home Page"')
def step_impl(context):
    """Navigate to the base URL."""
    context.driver.get(context.base_url)


@then('I should see "{text}" in the title')
def step_impl(context, text):
    """Assert text is in the document title."""
    assert text in context.driver.title


@then('I should not see "{text}"')
def step_impl(context, text):
    """Assert text is not in the document body."""
    assert text not in context.driver.page_source


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set a field value by element name."""
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    element.clear()
    element.send_keys(text_string)


@when('I press the "{button}" button')
def step_impl(context, button):
    """Click a button by name."""
    button_id = button.lower() + "-btn"
    context.driver.find_element(By.ID, button_id).click()


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Check the flash message area for a message (supports regex)."""
    if "[" in message and "]" in message:
        element = WebDriverWait(context.driver, context.wait_seconds).until(
            EC.presence_of_element_located((By.ID, "flash_message"))
        )
        pattern = re.compile(message)
        assert pattern.search(element.text)
    else:
        found = WebDriverWait(context.driver, context.wait_seconds).until(
            EC.text_to_be_present_in_element((By.ID, "flash_message"), message)
        )
        assert found


@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    """Copy a value from a field."""
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    context.clipboard = element.get_attribute("value")


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    """Paste a copied value into a field."""
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    element.clear()
    element.send_keys(context.clipboard)


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    """Verify a field is empty."""
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    assert element.get_attribute("value") == ""


@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    """Check that a field contains a specific value."""
    element_id = element_name.lower().replace(" ", "_")
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value(
            (By.ID, f"product_{element_id}"), text_string
        )
    )
    assert found


@then('I should not see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    """Ensure a value is not present in a field."""
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    value = element.get_attribute("value")
    assert text_string not in value


@then('I should see "{text}" in the results')
def step_impl(context, text):
    """Verify search results contain the expected text."""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "search_results"), text)
    )
    assert found


@then('I should not see "{text}" in the results')
def step_impl(context, text):
    """Ensure the search results do not contain specific text."""
    name_field = context.driver.find_element(By.ID, "product_name")
    name_field.clear()
    context.driver.find_element(By.ID, "search-btn").click()
    time.sleep(1)
    element = context.driver.find_element(By.ID, "search_results")
    assert text not in element.text


@when('I press the "Like" button again')
def step_impl(context):
    """Click the Like button."""
    context.driver.find_element(By.ID, "like-btn").click()


@then('the product record has "{likes}" likes in the database')
def step_impl(context, likes):
    """Validate number of likes in DB matches expected."""
    product_id = context.driver.find_element(By.ID, "product_id").get_attribute("value")
    base = f"{context.base_url}/products/{product_id}"
    resp = requests.get(base, timeout=30)
    assert resp.status_code == 200
    data = resp.json()
    assert str(data["likes"]) == likes


@given("a product exists")
def step_impl(context):
    """Create a sample product via UI for update test."""
    context.driver.get(context.base_url)
    context.driver.find_element(By.ID, "product_name").send_keys("Test Product")
    context.driver.find_element(By.ID, "product_description").send_keys("This is a test product for update")
    context.driver.find_element(By.ID, "product_price").send_keys("99.99")
    context.driver.find_element(By.ID, "create-btn").click()
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )
    context.product_id = context.driver.find_element(By.ID, "product_id").get_attribute("value")


@when('I change the Name and press "Update"')
def step_impl(context):
    """Update the product name field and click Update."""
    name_field = context.driver.find_element(By.ID, "product_name")
    name_field.clear()
    name_field.send_keys("Updated Product Name")
    context.driver.find_element(By.ID, "update-btn").click()
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )


@then("I should see updated values upon retrieval")
def step_impl(context):
    """Retrieve and check the updated product values."""
    context.driver.find_element(By.ID, "clear-btn").click()
    id_field = context.driver.find_element(By.ID, "product_id")
    id_field.send_keys(context.product_id)
    context.driver.find_element(By.ID, "retrieve-btn").click()
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )
    name_field = context.driver.find_element(By.ID, "product_name")
    assert name_field.get_attribute("value") == "Updated Product Name"
