Feature: command an existing robot

  Scenario Outline: be able to move a robot
     Given a fake data provider
       And a <command> command to a robot
       And an existing battle
       And an existing robot
       And a snapshot of all battles
      When we command the robot
      Then we get a success <message>
       And the robot moved

  Examples: Scenarios
    | command        | message     |
    | turn-left      | Robot moved |
    | turn-right     | Robot moved |
    | move-forward   | Robot moved |
    | move-backwards | Robot moved |

  Scenario Outline: be able to attack
     Given a fake data provider
       And an attack command to a robot
       And an existing battle
       And an existing robot
       And an existing dinossaur close to the robot
       And a snapshot of all battles
      When we command the robot
      Then we get a success <message>
       And the dinossaur was destroyed

  Examples: Messages
    | message         |
    | Robot commanded |

  Scenario: must provide all required params
      Given a set of new robot commands
          | battleId | robot | action    |
          |          | 1     | turn-left |
          | 1111     |       | turn-left |
          | 1111     | 1     |           |
          | 1111     | 1     | morty     |
        And an existing battle
        And an existing robot
        And a snapshot of all battles
       When we command the robot
       Then we receive an error
        And the battle state is the same

 Scenario Outline: should not move the robot if the place was taken
    Given a fake data provider
      And a <command> command to a robot
      And an existing battle
      And an existing robot
      And two entities, in front and backwards of the robot
      And a snapshot of all battles
     When we command the robot
     Then we receive an error
      And the battle state is the same

 Examples: Scenarios
   | command        | message         |
   | move-forward   | Robot commanded |
   | move-backwards | Robot commanded |

Scenario: should not move the robot outside of battle area
    Given a set of new robot commands
        | battleId | robot  | action         |
        | 1111     | R-1111 | move-forward   |
        | 1111     | R-1111 | move-backwards |
     And an existing 1x1 battle
     And an existing robot
     And a snapshot of all battles
    When we command the robot
    Then we receive an error
     And the battle state is the same
