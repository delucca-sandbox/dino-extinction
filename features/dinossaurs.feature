Feature: create a new dinossaur

  Scenario: be able to create a new dinossaur
     Given a fake data provider
       And a valid new dinossaur request
       And an existing battle
      When we ask to create a new dinossaur
      Then we receive the status of the creation
       And the dinossaur was created
       And the battle was updated

  Scenario: must provide all required params
      Given a set of invalid new dinossaur requests
          | battleId | xPosition | yPosition |
          |          | 1         | 1         |
          | 1        |           | 1         |
          | 1        | 1         |           |
       When we ask to create a new dinossaur
       Then we receive an error
        And the dinossaur was not created

  Scenario: must provide an valid battleId
     Given a valid new dinossaur request
       And an non-existing battle
      When we ask to create a new dinossaur
      Then we receive an error
       And the dinossaur was not created

 Scenario: should not accept a dinossaur into a taken position
    Given a valid new dinossaur request
      And and a dinossaur already at that place
     When we ask to create a new dinossaur
     Then we receive an error
      And the dinossaur was not created

Scenario: should not accept a dinossaur outside of battle area
   Given a set of dinossaurs requests outside of battle area
       | battleId | xPosition | yPosition |
       | 1        | 51        | 49        |
       | 1        | 49        | 51        |
       | 1        | 51        | 51        |
     And an existing battle
    When we ask to create a new dinossaur
    Then we receive an error
     And the dinossaur was not created

Scenario: should be able to insert multiple dinossaurs
   Given a valid new dinossaur request
     And and a second new dinossaur request
    When we ask to create a new dinossaur
     And we ask to create the second dinossaur
    Then we receive the status of the creation
     And both dinossaurs were created
