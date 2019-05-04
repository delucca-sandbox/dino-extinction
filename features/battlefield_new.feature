Feature: create a new battlefield

  Scenario: be able to create a new battlefield
     Given a valid request
      When we create a new battlefield
      Then we receive the battlefield ID
       And the battlefield was created
