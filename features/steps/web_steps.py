import re
import logging
from typing import Any
import requests

from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# ------------------------------------------------------------------
#  configuration
# ------------------------------------------------------------------
PREFIX = "product_"  # every input/select id = product_<field>
RESULTS_ID = "search_results"
FLASH_ID = "flash_message"


# ------------------------------------------------------------------
#  helper functions
# ------------------------------------------------------------------
def _field_id(label: str) -> str:
    return f"{PREFIX}{label.lower().replace(' ', '_')}"


def _button_id(label: str) -> str:
    return f"{label.lower().replace(' ', '_')}-btn"


def _save_png(ctx: Any, name: str) -> None:  # optional debug helper
    safe = re.sub(r"[^\w]+", "-", name)
    ctx.driver.save_screenshot(f"./captures/{safe}.png")


# ------------------------------------------------------------------
#  navigation
# ------------------------------------------------------------------
@when('I visit the "Home Page"')
def step_impl(ctx):
    ctx.driver.get(ctx.base_url)
    # _save_png(ctx, "home-page")


# ------------------------------------------------------------------
#  title / error checks
# ------------------------------------------------------------------
@then('I should see "{text}" in the title')
def step_impl(ctx, text):
    WebDriverWait(ctx.driver, 10).until(EC.title_contains(text))


@then('I should not see "404 Not Found"')
def step_impl(ctx):
    body = ctx.driver.find_element(By.TAG_NAME, "body")
    assert "404 Not Found" not in body.text


# ------------------------------------------------------------------
#  entering / selecting values
# ------------------------------------------------------------------
@when('I set the "{field}" to "{value}"')
def step_impl(ctx, field, value):
    element = ctx.driver.find_element(By.ID, _field_id(field))
    element.clear()
    element.send_keys(value)


@when('I select "{value}" in the "{field}" dropdown')
def step_impl(ctx, value, field):
    Select(ctx.driver.find_element(By.ID, _field_id(field))).select_by_visible_text(
        value
    )


# ------------------------------------------------------------------
#  copy / paste helpers
# ------------------------------------------------------------------
@when('I copy the "{field}" field')
def step_impl(ctx, field):
    element = WebDriverWait(ctx.driver, ctx.wait_seconds).until(
        EC.presence_of_element_located((By.ID, _field_id(field)))
    )
    ctx.clipboard = element.get_attribute("value")
    logging.info("Clipboard = %s", ctx.clipboard)


@when('I paste the "{field}" field')
def step_impl(ctx, field):
    element = ctx.driver.find_element(By.ID, _field_id(field))
    element.clear()
    element.send_keys(ctx.clipboard)


# ------------------------------------------------------------------
#  pressing buttons
# ------------------------------------------------------------------
@when('I press the "{button}" button')
def step_impl(ctx, button):
    ctx.driver.find_element(By.ID, _button_id(button)).click()


# ------------------------------------------------------------------
#  flash message & results assertions
# ------------------------------------------------------------------
@then('I should see the message "{msg}"')
def step_impl(ctx, msg):
    WebDriverWait(ctx.driver, ctx.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, FLASH_ID), msg)
    )


@then('I should see "{text}" in the results')
def step_impl(ctx, text):
    WebDriverWait(ctx.driver, ctx.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, RESULTS_ID), text)
    )


@then('I should not see "{text}" in the results')
def step_impl(ctx, text):
    assert text not in ctx.driver.find_element(By.ID, RESULTS_ID).text


# ------------------------------------------------------------------
#  direct‑field assertions
# ------------------------------------------------------------------
@then('the "{field}" field should be empty')
def step_impl(ctx, field):
    assert ctx.driver.find_element(By.ID, _field_id(field)).get_attribute("value") == ""


@then('I should see "{value}" in the "{field}" field')
def step_impl(ctx, value, field):
    WebDriverWait(ctx.driver, ctx.wait_seconds).until(
        EC.text_to_be_present_in_element_value((By.ID, _field_id(field)), value)
    )


@when('I change "{field}" to "{value}"')
def step_impl(ctx, field, value):
    element = ctx.driver.find_element(By.ID, _field_id(field))
    element.clear()
    element.send_keys(value)


# ----------------------------------------
#  New steps for “Like” twice + DB check
# ----------------------------------------


@when('I press the "Like" button again')
def step_press_like_again(ctx):
    """Clicks the same Like button a second time."""
    ctx.driver.find_element(By.ID, _button_id("Like")).click()


@then('the product record has "{likes}" likes in the database')
def step_check_likes_in_db(ctx, likes):
    """Fetches the product by ID and asserts its 'likes' count in the DB."""
    product_id = ctx.clipboard  # the ID you copied earlier
    resp = requests.get(f"{ctx.base_url}/products/{product_id}")
    assert (
        resp.status_code == 200
    ), f"GET /products/{product_id} returned {resp.status_code}"
    data = resp.json()
    assert data["likes"] == int(likes), f"Expected {likes} likes, got {data['likes']}"
