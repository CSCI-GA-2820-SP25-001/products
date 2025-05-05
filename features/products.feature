Feature: The products service back-end
    As a Product Owner
    I need a RESTful catalog service
    So that I can keep track of all products

Background:
    Given the following products
        | name     | description            | price    |  likes    |
        | Prod #1  | Our first product      | 30.00    |  100      |
        | Prod #2  | Our second product     | 4.15     |  200      |
        | Prod #3  | Another product        | 3.27     |  300      |
        | Prod #4  | So many products       | 19.95    |  400      |
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

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Prod #2"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Prod #2" in the results
    When I copy the "Id" field
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    When I press the "Search" button
    Then I should not see "Prod #2" in the results

  Scenario: Like a Product (twice)
    # This scenario inherits the same Background above
    When I visit the "Home Page"
    And I set the "Name" to "GoPro"
    And I set the "Description" to "Great camera"
    And I set the "Price" to "100.00"
    And I press the "Create" button
    Then I should see the message "Success"

    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button

    When I press the "Like" button
    Then I should see "1" in the "Likes" field
    And the product record has "1" likes in the database
    And I should see the message "Product liked"

    When I press the "Like" button again
    Then I should see "2" in the "Likes" field
    And the product record has "2" likes in the database
    And I should see the message "Product liked"