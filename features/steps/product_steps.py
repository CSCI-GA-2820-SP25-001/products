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
Product Steps

Steps file for Product.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
from http import HTTPStatus
import requests
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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


@when('I visit the "Home Page"')
def step_impl(context):
    """Make a call to the base URL"""
    context.driver.get(context.base_url)
    # Uncomment the next line to take a screenshot of the web page
    # context.driver.save_screenshot('home_page.png')


@then('I should see "{text}" in the title')
def step_impl(context, text):
    """Check the document title for a text string"""
    assert text in context.driver.title


@then('I should not see "{text}"')
def step_impl(context, text):
    """Check that a text string is not in the body"""
    assert text not in context.driver.page_source


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set the value of an input field"""
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    element.clear()
    element.send_keys(text_string)


@when('I press the "{button}" button')
def step_impl(context, button):
    """Press a button with a specific ID"""
    button_id = button.lower() + "-btn"
    context.driver.find_element(By.ID, button_id).click()


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Check for a message in the flash area"""
    # Check if the message contains a regex pattern (enclosed in square brackets)
    import re

    if "[" in message and "]" in message:
        # This is a regex pattern
        element = WebDriverWait(context.driver, context.wait_seconds).until(
            EC.presence_of_element_located((By.ID, "flash_message"))
        )
        pattern = re.compile(message)
        assert pattern.search(element.text)
    else:
        # This is a literal string
        found = WebDriverWait(context.driver, context.wait_seconds).until(
            EC.text_to_be_present_in_element((By.ID, "flash_message"), message)
        )
        assert found


@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    """Copy a field's value to the clipboard"""
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    # Save the copied value for later use
    context.clipboard = element.get_attribute("value")


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    """Paste a previously copied value into a field"""
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    element.clear()
    element.send_keys(context.clipboard)


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    """Check that a field is empty"""
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    assert element.get_attribute("value") == ""


@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    """Check the value of an input field"""
    element_id = element_name.lower().replace(" ", "_")
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value(
            (By.ID, f"product_{element_id}"), text_string
        )
    )
    assert found


@then('I should not see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    """Check that a value is not in an input field"""
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    value = element.get_attribute("value")
    assert text_string not in value


@then('I should see "{text}" in the results')
def step_impl(context, text):
    """Check for text in the search results"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "search_results"), text)
    )
    assert found


@then('I should not see "{text}" in the results')
def step_impl(context, text):
    """Check that text is not in the search results"""
    # Clear the search field to ensure we get fresh results
    name_field = context.driver.find_element(By.ID, "product_name")
    name_field.clear()

    # Click search again to refresh the results
    context.driver.find_element(By.ID, "search-btn").click()

    # Wait for the search results to be updated
    time.sleep(1)

    # Get the search results element
    element = context.driver.find_element(By.ID, "search_results")

    # Check that the text is not in the search results
    assert text not in element.text


@when('I press the "Like" button again')
def step_impl(context):
    """Press the Like button again"""
    context.driver.find_element(By.ID, "like-btn").click()


@then('the product record has "{likes}" likes in the database')
def step_impl(context, likes):
    """Check the number of likes in the database"""
    product_id = context.driver.find_element(By.ID, "product_id").get_attribute("value")
    base = f"{context.base_url}/products/{product_id}"
    resp = requests.get(base, timeout=30)
    assert resp.status_code == 200
    data = resp.json()
    assert str(data["likes"]) == likes


@given("a product exists")
def step_impl(context):
    """Create a product for testing update functionality"""
    # Visit the home page
    context.driver.get(context.base_url)

    # Set product details
    context.driver.find_element(By.ID, "product_name").send_keys("Test Product")
    context.driver.find_element(By.ID, "product_description").send_keys(
        "This is a test product for update"
    )
    context.driver.find_element(By.ID, "product_price").send_keys("99.99")

    # Create the product
    context.driver.find_element(By.ID, "create-btn").click()

    # Wait for success message
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )

    # Save the product ID for later use
    context.product_id = context.driver.find_element(By.ID, "product_id").get_attribute(
        "value"
    )


@when('I change the Name and press "Update"')
def step_impl(context):
    """Update the product name and press the update button"""
    # Clear the name field and set a new name
    name_field = context.driver.find_element(By.ID, "product_name")
    name_field.clear()
    name_field.send_keys("Updated Product Name")

    # Press the update button
    context.driver.find_element(By.ID, "update-btn").click()

    # Wait for success message
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )


@then("I should see updated values upon retrieval")
def step_impl(context):
    """Verify the product was updated by retrieving it"""
    # Clear the form
    context.driver.find_element(By.ID, "clear-btn").click()

    # Set the product ID
    id_field = context.driver.find_element(By.ID, "product_id")
    id_field.send_keys(context.product_id)

    # Retrieve the product
    context.driver.find_element(By.ID, "retrieve-btn").click()

    # Wait for success message
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )

    # Verify the name was updated
    name_field = context.driver.find_element(By.ID, "product_name")
    assert name_field.get_attribute("value") == "Updated Product Name"
