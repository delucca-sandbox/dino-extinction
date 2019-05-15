Feature: create a new dinossaur

  Scenario Outline: be able to create a new dinossaur
     Given a fake data provider
       And a valid new dinossaur request
       And an existing battle
      When we ask to create a new dinossaur
      Then we get a success <message>
       And the dinossaur was created

  Examples: Messages
    |  message          |
    | Dinossaur created |

  Scenario: must provide all required params
      Given a set of new dinossaur requests
          | battleId | xPosition | yPosition |
          |          | 1         | 1         |
          | 1        |           | 1         |
          | 1        | 1         |           |
        And an existing battle
        And a snapshot of all battles
       When we ask to create a new dinossaur
       Then we receive an error
        And the dinossaur was not created

  Scenario: must provide an valid battleId
     Given a fake data provider
       And a valid new dinossaur request
       And an non-existing battle
       And a snapshot of all battles
      When we ask to create a new dinossaur
      Then we receive an error

 Scenario: should not accept a dinossaur into a taken position
    Given a fake data provider
      And a valid new dinossaur request
      And an existing battle
      And a dinossaur already at that place
      And a snapshot of all battles
     When we ask to create a new dinossaur
     Then we receive an error
      And the dinossaur was not created

Scenario: should not accept a dinossaur outside of battle area
   Given a set of new dinossaur requests
       | battleId | xPosition | yPosition |
       | 1        | 51        | 49        |
       | 1        | 49        | 51        |
       | 1        | 51        | 51        |
     And an existing battle
     And a snapshot of all battles
    When we ask to create a new dinossaur
    Then we receive an error
     And the dinossaur was not created

Scenario Outline: should be able to insert multiple dinossaurs
   Given a set of new dinossaur requests
       | battleId | xPosition | yPosition |
       | 1        | 5         | 49        |
       | 1        | 49        | 50        |
       | 2        | 50        | 50        |
     And an existing battle
    When we ask to create a new dinossaur
    Then we get a success <message>
     And the dinossaur was created

Examples: Messages
  |  message          |
  | Dinossaur created |
