Feature: create a new battlefield

  Scenario: be able to create a new battlefield
     Given a valid request
      When we create a new battlefield
      Then we receive the battlefield ID
       And the battlefield was created

  Scenario: be able to receive an error
      Given a valid request
       When we create an invalid battlefield
       Then we receive an error
        And the battlefield was not created

  Scenario: be able to store a 2x2 grid
      Given a valid request asking for 2x2 grid
       When we create a new battlefield
       Then we receive the battlefield ID
        And we stored a 2x2 battlefield
