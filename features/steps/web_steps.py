######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
######################################################################

import logging

from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions


ID_PREFIX = "product_"


@when('I visit the "Home Page"')
def step_impl(context):
    """Visit the home page."""
    context.driver.get(context.base_url)


@then('I should see "{text_string}" in the title')
def step_impl(context, text_string):
    """Verify text appears in the page title."""
    WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.title_contains(text_string)
    )


@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    """Verify text does not appear on the page."""
    body = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    assert text_string not in body.text


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set the value of an input field."""

    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    # The feature uses ID 1 for the first background product.
    # PostgreSQL may assign a different actual ID.
    if element_name.lower() == "id" and text_string == "1":
        text_string = str(context.product_ids["Hat"])

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    element.clear()
    element.send_keys(text_string)


@when('I select "{text_string}" in the "{element_name}" dropdown')
def step_impl(context, text_string, element_name):
    """Select an option from a dropdown."""

    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    Select(element).select_by_visible_text(text_string)


@then('I should see "{text_string}" in the "{element_name}" dropdown')
def step_impl(context, text_string, element_name):
    """Verify the selected dropdown option."""

    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    selected = Select(element).first_selected_option

    assert selected.text == text_string


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    """Verify an input field is empty."""

    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    assert element.get_attribute("value") == ""


@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    """Copy the value of a field."""

    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    context.clipboard = element.get_attribute("value")

    logging.info(
        "Clipboard contains: %s",
        context.clipboard
    )


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    """Paste the previously copied field value."""

    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    element.clear()
    element.send_keys(context.clipboard)


@when('I press the "{button_name}" button')
def step_impl(context, button_name):
    """Press a button on the page."""

    button_id = button_name.lower().replace(" ", "_") + "-btn"

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, button_id)
        )
    )

    context.driver.execute_script(
        "arguments[0].click();",
        element
    )


@then('I should see "{text_string}" in the results')
def step_impl(context, text_string):
    """Verify text appears in the results."""

    WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        lambda driver: text_string in driver.find_element(
            By.TAG_NAME,
            "body"
        ).text
    )


@then('I should not see "{text_string}" in the results')
def step_impl(context, text_string):
    """Verify text does not appear in the results."""

    body = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    assert text_string not in body.text


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Verify a message appears on the page."""

    WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        lambda driver: message in driver.find_element(
            By.TAG_NAME,
            "body"
        ).text
    )


@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    """Verify text appears in an input field."""

    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        lambda driver: text_string in driver.find_element(
            By.ID,
            element_id
        ).get_attribute("value")
    )


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Change the value of an input field."""

    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    element.clear()
    element.send_keys(text_string)
