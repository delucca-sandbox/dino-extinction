# Command Reference

This is a web API. So, all of the following endpoint should have the prefix: `localhost/` in order to worker. Here are the list of all the available endpoints for this application:

* [`battles/new`](#battles/new)
* [`battles/state`](#battles/state)
* [`robots/new`](#robots/new)
* [`robots/command`](#robots/command)
* [`dinosaurs/new`](#dinosaurs/new)


## `battles/new`

Creates a new 50x50 battle. Stay focused! Because in this endpoint you will receive your battle ID and **you should not lose it** if you want to move your robots to attack.

    $ POST http://localhost/battle/new

**Parameters:**
* **size**: The size of your wanted battlefield


## `battles/state`

Get the current state of the battle, showing the robots and dinosaurs positions.

    $ GET http://localhost/battle/state

**Query String Parameters:**
* **battleId**: The id of your battle `REQUIRED`


## `robots/new`

Adds a new robot into a specific battle in a certain position and facing a certain direction. All of those parameters are required.

    $ POST http://localhost/robots/new

**Parameters:**
* **battleId**: The id of your current battle `REQUIRED`
* **xPosition**: The position of your robot in the x-axis (it should be less than 50) `REQUIRED`
* **yPosition**: The position of your robot in the y-axis (it should be less than 50) `REQUIRED`
* **direction**: What direction your robot is facing. It can be: **north**, **east**, **south** or **west** `REQUIRED`

**IMPORTANT:** You can only add robots on free spots


## `robots/command`

Instruct a robot to do some action. You can: move or attack. If you're moving, you need to specify where you're going to

$ POST http://localhost/robots/command

**Parameters:**
* **battleId**: The id of your current battle `REQUIRED`
* **robot**: The name of the robot that you're commanding `REQUIRED`
* **action**: The action you want it to do. It can be: **turn-left**, **turn-right**, **move-forward**, **move-backwards** or **attack** `REQUIRED`

**IMPORTANT:** You cannot move your robot outside of the battle


## `dinosaurs/new`

Adds a new dinosaur to your battle. I don't know why would you want to add ENEMIES, but still, you can use it

$ POST http://localhost/dinossaurs/new

**Parameters:**
* **battleId**: The id of your current battle `REQUIRED`
* **xPosition**: The position of your robot in the x-axis (it should be less than 50) `REQUIRED`
* **yPosition**: The position of your robot in the y-axis (it should be less than 50) `REQUIRED`

**IMPORTANT:** You can only add dinosaurs on free spots
