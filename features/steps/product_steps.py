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
def given_the_following_products(context):
    """Clear DB then POST each table row as JSON."""
    base = f"{context.base_url}/products"

    for item in requests.get(base, timeout=30).json():
        requests.delete(f"{base}/{item['id']}", timeout=30)

    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "likes": int(row["likes"]),
        }
        context.resp = requests.post(base, json=payload, timeout=30)
        assert context.resp.status_code == HTTPStatus.CREATED


@when('I visit the "Home Page"')
def when_i_visit_home_page(context):
    context.driver.get(context.base_url)


@then('I should see "{text}" in the title')
def then_see_text_in_title(context, text):
    assert text in context.driver.title


@then('I should not see "{text}"')
def then_not_see_text(context, text):
    assert text not in context.driver.page_source


@when('I set the "{element_name}" to "{text_string}"')
def when_set_element_to_text(context, element_name, text_string):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    element.clear()
    element.send_keys(text_string)


@when('I press the "{button}" button')
def when_press_button(context, button):
    button_id = button.lower() + "-btn"
    context.driver.find_element(By.ID, button_id).click()


@then('I should see the message "{message}"')
def then_see_message(context, message):
    import re
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
def when_copy_field(context, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    context.clipboard = element.get_attribute("value")


@when('I paste the "{element_name}" field')
def when_paste_field(context, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    element.clear()
    element.send_keys(context.clipboard)


@then('the "{element_name}" field should be empty')
def then_field_should_be_empty(context, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    assert element.get_attribute("value") == ""


@then('I should see "{text_string}" in the "{element_name}" field')
def then_see_text_in_field(context, text_string, element_name):
    element_id = element_name.lower().replace(" ", "_")
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value(
            (By.ID, f"product_{element_id}"), text_string
        )
    )
    assert found


@then('I should not see "{text_string}" in the "{element_name}" field')
def then_not_see_text_in_field(context, text_string, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, f"product_{element_id}")
    value = element.get_attribute("value")
    assert text_string not in value


@then('I should see "{text}" in the results')
def then_see_text_in_results(context, text):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "search_results"), text)
    )
    assert found


@then('I should not see "{text}" in the results')
def then_not_see_text_in_results(context, text):
    name_field = context.driver.find_element(By.ID, "product_name")
    name_field.clear()
    context.driver.find_element(By.ID, "search-btn").click()
    time.sleep(1)
    element = context.driver.find_element(By.ID, "search_results")
    assert text not in element.text


@when('I press the "Like" button again')
def when_press_like_again(context):
    context.driver.find_element(By.ID, "like-btn").click()


@then('the product record has "{likes}" likes in the database')
def then_product_likes_in_db(context, likes):
    product_id = context.driver.find_element(By.ID, "product_id").get_attribute("value")
    base = f"{context.base_url}/products/{product_id}"
    resp = requests.get(base, timeout=30)
    assert resp.status_code == 200
    data = resp.json()
    assert str(data["likes"]) == likes


@given("a product exists")
def given_product_exists(context):
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
def when_update_product_name(context):
    name_field = context.driver.find_element(By.ID, "product_name")
    name_field.clear()
    name_field.send_keys("Updated Product Name")
    context.driver.find_element(By.ID, "update-btn").click()
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )


@then("I should see updated values upon retrieval")
def then_see_updated_values(context):
    context.driver.find_element(By.ID, "clear-btn").click()
    id_field = context.driver.find_element(By.ID, "product_id")
    id_field.send_keys(context.product_id)
    context.driver.find_element(By.ID, "retrieve-btn").click()
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )
    name_field = context.driver.find_element(By.ID, "product_name")
    assert name_field.get_attribute("value") == "Updated Product Name"
