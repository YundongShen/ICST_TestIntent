Feature: Process wood plank
  Scenario: User processes a wood plank
    Given the wood is loaded onto the machine
    And the desired thickness is set
    When the user presses the "Start Processing" button
    Then the machine should process the wood
    And the wood should come out at the specified thickness
