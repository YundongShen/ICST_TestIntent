@slow
Feature: HTTP attacks
  Background:
    Given an attack "curl" exists
    And I copy the attack files from the "examples/curl" folder
    And the following attack files exist:
      | filename       |
      | simple.attack  |
      | cookies.attack |
      | verbs.attack   |

  Scenario: cookies attack
    When I run `gauntlt cookies.attack`
    Then it should pass with:
      """
      4 steps (4 passed)
      """
