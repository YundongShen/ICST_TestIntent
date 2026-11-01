Feature: Login
  Scenario: Logging in with correct credentials
    Given I am on "/login"
    When I fill in "Username" with "admin"
    And I fill in "Password" with "admin123"
    And I press "Login"
    Then I should be redirected to "/profile"
    And I should see "Welcome, admin"
