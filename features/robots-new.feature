Feature: create a new robot

  Scenario Outline: be able to create a new robot
     Given a fake data provider
       And a valid new robot request
       And an existing battle
      When we ask to create a new robot
      Then we get a success <message>
       And the robot was created

  Examples: Messages
    | message       |
    | Robot created |

  Scenario: must provide all required params
      Given a set of new robot requests
          | battleId | xPosition | yPosition | direction |
          |          | 1         | 1         | north     |
          | 1111     |           | 1         | north     |
          | 1111     | 1         |           | north     |
          | 1111     | 1         | 1         |           |
          | 1111     | 1         | 1         | morty     |
        And an existing battle
        And a snapshot of all battles
       When we ask to create a new robot
       Then we receive an error
        And the robot was not created

  Scenario: must provide an valid battleId
     Given a fake data provider
       And a valid new robot request
       And an non-existing battle
       And a snapshot of all battles
      When we ask to create a new robot
      Then we receive an error

 Scenario: should not accept a robot into a taken position
    Given a fake data provider
      And a valid new robot request
      And an existing battle
      And a robot already at that place
      And a snapshot of all battles
     When we ask to create a new robot
     Then we receive an error
      And the dinossaur was not created

Scenario: should not accept a robot outside of battle area
   Given a set of new dinossaur requests
       | battleId | xPosition | yPosition | direction |
       | 1111     | 51        | 49        | north     |
       | 1111     | 49        | 51        | north     |
       | 1111     | 51        | 51        | north     |
     And an existing battle
     And a snapshot of all battles
    When we ask to create a new robot
    Then we receive an error
     And the robot was not created

Scenario Outline: should be able to insert multiple dinossaurs
   Given a set of new robot requests
       | battleId | xPosition | yPosition | direction |
       | 1111     | 5         | 19        | north     |
       | 1111     | 49        | 11        | east      |
       | 1111     | 15        | 50        | west      |
     And an existing battle
    When we ask to create a new robot
    Then we get a success <message>
     And the robot was created

Examples: Messages
  | message       |
  | Robot created |
