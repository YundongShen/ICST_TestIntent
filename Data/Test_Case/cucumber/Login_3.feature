Feature: Login


Scenario: Visiting the profile page without being logged in
    Given I am not logged in
    When I am on "/profile"
    Then I should see "Please log in to access your profile."
