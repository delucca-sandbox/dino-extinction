Feature: create a new dinossaur

  Scenario: be able to create a new dinossaur
     Given a fake data provider
       And a valid new dinossaur request
       And an existing battle
      When we ask to create a new dinossaur
      Then we receive the status of the creation
       And the dinossaur was created

  Scenario: must provide all required params
      Given a set of new dinossaur requests
          | battleId | xPosition | yPosition |
          |          | 1         | 1         |
          | 1        |           | 1         |
          | 1        | 1         |           |
        And an existing battle
        And a snapshot of all battles
       When we ask to create a new dinossaur
       Then we receive an dino error
        And the dinossaur was not created

  Scenario: must provide an valid battleId
     Given a fake data provider
       And a valid new dinossaur request
       And an non-existing battle
       And a snapshot of all battles
      When we ask to create a new dinossaur
      Then we receive an dino error

 Scenario: should not accept a dinossaur into a taken position
    Given a fake data provider
      And a valid new dinossaur request
      And an existing battle
      And and a dinossaur already at that place
      And a snapshot of all battles
     When we ask to create a new dinossaur
     Then we receive an dino error
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
    Then we receive an dino error
     And the dinossaur was not created

Scenario: should be able to insert multiple dinossaurs
   Given a set of new dinossaur requests
       | battleId | xPosition | yPosition |
       | 1        | 5         | 49        |
       | 1        | 49        | 50        |
       | 2        | 50        | 50        |
     And an existing battle
    When we ask to create a new dinossaur
    Then we receive the status of the creation
     And the dinossaur was created
