from decimal import Decimal
import pytest
from pytest_bdd import given, when, then, parsers
from fastapi.testclient import TestClient

from app.schemas.expense import ExpenseResponse


# Context to store data between steps
@pytest.fixture(scope="function")
def context():
    """Context fixture to store data between steps."""
    return {}


@given("the API is running")
def api_is_running(client):
    """Verify the API is running."""
    response = client.get("/health")
    assert response.status_code == 200


@given(parsers.parse('I have expense data with title "{title}", amount "{amount}", and description "{description}"'))
def have_expense_data(context, title, amount, description):
    """Store expense data in context."""
    context["expense_data"] = {
        "title": title,
        "amount": amount,
        "description": description
    }


@given(parsers.parse('I have created an expense with title "{title}", amount "{amount}"'))
def have_created_expense(client, context, title, amount):
    """Create an expense and store it in context."""
    expense_data = {
        "title": title,
        "amount": amount,
        "description": None
    }
    response = client.post("/expenses", json=expense_data)
    assert response.status_code == 201
    expense = response.json()
    if "expenses" not in context:
        context["expenses"] = []
    context["expenses"].append(expense)


@given("I have saved the expense id")
def save_expense_id(context):
    """Save the expense ID from the last created expense."""
    if "expenses" in context and context["expenses"]:
        context["expense_id"] = context["expenses"][-1]["id"]
    elif "expense" in context:
        context["expense_id"] = context["expense"]["id"]


@given("I have an expense id that does not exist")
def have_nonexistent_expense_id(context):
    """Set a non-existent expense ID."""
    context["expense_id"] = 99999


@when("I create an expense")
def create_expense(client, context):
    """Create an expense using the data in context."""
    response = client.post("/expenses", json=context["expense_data"])
    context["response"] = response
    if response.status_code == 201:
        context["expense"] = response.json()


@when("I get all expenses")
def get_all_expenses(client, context):
    """Get all expenses."""
    response = client.get("/expenses")
    context["response"] = response
    if response.status_code == 200:
        context["expenses"] = response.json()


@when("I get the expense by id")
def get_expense_by_id(client, context):
    """Get an expense by ID."""
    expense_id = context["expense_id"]
    response = client.get(f"/expenses/{expense_id}")
    context["response"] = response
    if response.status_code == 200:
        context["expense"] = response.json()


@when(parsers.parse('I update the expense with title "{title}" and amount "{amount}"'))
def update_expense_with_data(client, context, title, amount):
    """Update an expense with new data."""
    expense_id = context["expense_id"]
    update_data = {
        "title": title,
        "amount": amount
    }
    response = client.put(f"/expenses/{expense_id}", json=update_data)
    context["response"] = response
    if response.status_code == 200:
        context["expense"] = response.json()


@when(parsers.parse('I update the expense with title "{title}"'))
def update_expense_with_title(client, context, title):
    """Update an expense with new title."""
    expense_id = context["expense_id"]
    update_data = {
        "title": title
    }
    response = client.put(f"/expenses/{expense_id}", json=update_data)
    context["response"] = response
    if response.status_code == 200:
        context["expense"] = response.json()


@when("I delete the expense")
def delete_expense(client, context):
    """Delete an expense."""
    expense_id = context["expense_id"]
    response = client.delete(f"/expenses/{expense_id}")
    context["response"] = response


@then(parsers.parse('the response status should be {status_code:d}'))
def check_response_status(context, status_code):
    """Check the response status code."""
    assert context["response"].status_code == status_code


@then(parsers.parse('the response should contain the expense with title "{title}"'))
def check_expense_title(context, title):
    """Check that the expense has the expected title."""
    expense = context.get("expense") or context["expenses"][-1]
    assert expense["title"] == title


@then("the expense should have an id")
def check_expense_has_id(context):
    """Check that the expense has an ID."""
    expense = context.get("expense") or context["expenses"][-1]
    assert "id" in expense
    assert expense["id"] is not None


@then(parsers.parse('the expense amount should be "{amount}"'))
def check_expense_amount(context, amount):
    """Check that the expense has the expected amount."""
    expense = context.get("expense") or context["expenses"][-1]
    assert str(expense["amount"]) == amount


@then(parsers.parse('the response should contain {count:d} expenses'))
def check_expense_count(context, count):
    """Check that the response contains the expected number of expenses."""
    assert len(context["expenses"]) == count


@then(parsers.parse('one expense should have title "{title}"'))
def check_one_expense_has_title(context, title):
    """Check that at least one expense has the expected title."""
    titles = [expense["title"] for expense in context["expenses"]]
    assert title in titles


@then("the expense id should match the saved id")
def check_expense_id_matches(context):
    """Check that the expense ID matches the saved ID."""
    expense = context.get("expense")
    assert expense is not None
    assert expense["id"] == context["expense_id"]


@then("the response should contain an error message")
def check_error_message(context):
    """Check that the response contains an error message."""
    response_data = context["response"].json()
    assert "detail" in response_data

