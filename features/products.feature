Feature: The products service back-end
    As a Product Owner
    I need a RESTful catalog service
    So that I can keep track of all products

Background:
    Given the following products
        | Name     | Description            | Price    |
        | Prod #1  | Our first product      | 30.00    |
        | Prod #2  | Our second product     | 4.15     |
        | Prod #3  | Another product        | 3.27     |
        | Prod #4  | So many products       | 19.95    |
Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Products RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Happy"
    And I set the "Description" to "New Product"
    And I set the "Price" to "1000000"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Happy" in the "Name" field
    And I should see "New Product" in the "Description" field
    And I should see "1000000" in the "Price" field

Scenario: List all Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Prod #1" in the results
    And I should see "Prod #2" in the results
    And I should see "Prod #3" in the results
    And I should see "Prod #4" in the results

Scenario: Search for Descriptions
    When I visit the "Home Page"
    And I set the "Description" to "Our first product"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Prod #1" in the results


Scenario: Search for Price
    When I visit the "Home Page"
    And I set the "Price" to "4.15"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Prod #2" in the results


Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Prod #3"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Prod #3" in the "Name" field
    And I should see "Another product" in the "Description" field
    When I change "Name" to "New Prod Name"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "New Prod Name" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "New Prod Name" in the results
    And I should not see "Prod #3" in the results