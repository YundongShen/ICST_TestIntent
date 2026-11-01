Feature: Load wood for processing
  Scenario: User loads wood onto the machine
    Given the machine is on and ready
    And the user has selected the processing mode
    When the user loads a wood piece onto the machine feeder
    Then the machine should detect the wood
    And display "Wood detected" on the screen
