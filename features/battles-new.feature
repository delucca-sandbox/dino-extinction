Feature: create a new battle

  Scenario: be able to create a new battle
     Given a valid new battle request
      When we ask to create a new battle
      Then we receive the battle ID
       And the battle was created

  Scenario: be able to receive an error
      Given a valid new battle request
       When we create an invalid battle
       Then we receive an error
        And the battle was not created

  Scenario: be able to store a 2x2 grid
      Given a valid new battle request asking for 2x2 grid
       When we ask to create a new battle
       Then we receive the battle ID
        And we stored a 2x2 battle
