Feature: Expense CRUD Operations
  As a user
  I want to manage expenses
  So that I can track my spending

  Background:
    Given the API is running

  Scenario: Create a new expense
    Given I have expense data with title "Coffee", amount "5.50", and description "Morning coffee"
    When I create an expense
    Then the response status should be 201
    And the response should contain the expense with title "Coffee"
    And the expense should have an id
    And the expense amount should be "5.50"

  Scenario: Get all expenses
    Given I have created an expense with title "Lunch", amount "15.00"
    And I have created an expense with title "Dinner", amount "25.00"
    When I get all expenses
    Then the response status should be 200
    And the response should contain 2 expenses
    And one expense should have title "Lunch"
    And one expense should have title "Dinner"

  Scenario: Get expense by ID
    Given I have created an expense with title "Groceries", amount "50.00"
    And I have saved the expense id
    When I get the expense by id
    Then the response status should be 200
    And the response should contain the expense with title "Groceries"
    And the expense id should match the saved id

  Scenario: Get non-existent expense
    Given I have an expense id that does not exist
    When I get the expense by id
    Then the response status should be 404
    And the response should contain an error message

  Scenario: Update an expense
    Given I have created an expense with title "Original", amount "10.00"
    And I have saved the expense id
    When I update the expense with title "Updated" and amount "20.00"
    Then the response status should be 200
    And the response should contain the expense with title "Updated"
    And the expense amount should be "10.00"
    And the expense id should match the saved id

  Scenario: Update non-existent expense
    Given I have an expense id that does not exist
    When I update the expense with title "Updated"
    Then the response status should be 404
    And the response should contain an error message

  Scenario: Delete an expense
    Given I have created an expense with title "To Delete", amount "5.00"
    And I have saved the expense id
    When I delete the expense
    Then the response status should be 204
    When I get the expense by id
    Then the response status should be 404

  Scenario: Delete non-existent expense
    Given I have an expense id that does not exist
    When I delete the expense
    Then the response status should be 404
    And the response should contain an error message

