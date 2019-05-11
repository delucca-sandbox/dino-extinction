Feature: create a new dinossaur

  Scenario: be able to create a new dinossaur
     Given a valid new dinossaur request
       And an existing battle
      When we ask to create a new dinossaur
      Then we receive the status of the creation
       And the dinossaur was created

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
       And the dinossaur was not screated
