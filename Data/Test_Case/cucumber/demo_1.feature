Feature: Calculator with reusable setup

  Background: common context
    Given I am in calc mode

  Rule: Addition and subtraction
    Background: service must be healthy
      Given the service is healthy

    Scenario: add two numbers
      Given I have numbers 2 and 3
      When I add them
      Then the result should be 5
