Feature: Start wood processing machine
  Scenario: User starts the machine
    Given the wood processing machine is turned off
    When the user presses the power button
    Then the machine should turn on
    And the indicator light should be green
