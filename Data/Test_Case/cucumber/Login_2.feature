Feature: Login


Scenario: Logging in with incorrect credentials
    Given I am on "/login"
    When I fill in "Username" with "admin"
    And I fill in "Password" with "wrongpassword"
    And I press "Login"
    Then I should see "Invalid credentials"
