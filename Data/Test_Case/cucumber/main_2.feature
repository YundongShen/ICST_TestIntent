Feature: Set cutting thickness
  Scenario: User sets the cutting thickness to 2 inches
    Given the wood processing machine is on
    And the machine display shows the default thickness
    When the user sets the cutting thickness to 2 inches
    Then the machine should display "2 inches"
    And the blade should adjust to 2 inches
