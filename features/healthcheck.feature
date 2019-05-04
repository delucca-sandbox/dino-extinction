Feature: healthcheck server

  Scenario: be able to start the server
     Given a empty request to healthcheck
      Then should receive a 200 status
