# Command Reference

This is a web API. So, all of the following endpoint should have the prefix: `localhost/` in order to worker. Here are the list of all the available endpoints for this application:

* [`battle/new`](#battle/new)
* [`battle/state`](#battle/state)
* [`robots/new`](#robots/new)
* [`robots/command`](#robots/command)
* [`dinosaurs/new`](#dinosaurs/new)


## `battle/new`

Creates a new 50x50 battlefield. Stay focused! Because in this endpoint you will receive your battlefield ID and **you should not lose it** if you want to move your robots to attack.

    $ POST http://localhost/battle/new


## `battle/state`

Get the current state of the battlefield, showing the robots and dinosaurs positions.

    $ GET http://localhost/battle/state

**Query String Parameters:**
* **battlefield**: The id of your battlefield `REQUIRED`


## `robots/new`

Adds a new robot into a specific battlefield in a certain position and facing a certain direction. All of those parameters are required.

    $ POST http://localhost/robots/new

**Parameters:**
* **battlefield**: The id of your current battlefield `REQUIRED`
* **name**: The name of your robot `REQUIRED`
* **xPosition**: The position of your robot in the x-axis (it should be less than 50) `REQUIRED`
* **yPosition**: The position of your robot in the y-axis (it should be less than 50) `REQUIRED`
* **direction**: What direction your robot is facing. It can be: **north**, **east**, **south** or **west** `REQUIRED`

**IMPORTANT:** You can only add robots on free spots


## `robots/command`

Instruct a robot to do some action. You can: move or attack. If you're moving, you need to specify where you're going to

$ POST http://localhost/robots/command

**Parameters:**
* **battlefield**: The id of your current battlefield `REQUIRED`
* **robot**: The name of the robot that you're commanding `REQUIRED`
* **action**: The action you want it to do. It can be: **move-north**, **move-east**, **move-south**, **move-west** or **attack** `REQUIRED`

**IMPORTANT:** You cannot move your robot outside of the battlefield


## `dinosaurs/new`

Adds a new dinosaur to your battlefield. I don't know why would you want to add ENEMIES, but still, you can use it

$ POST http://localhost/dinossaurs/new

**Parameters:**
* **battlefield**: The id of your current battlefield `REQUIRED`
* **xPosition**: The position of your robot in the x-axis (it should be less than 50) `REQUIRED`
* **yPosition**: The position of your robot in the y-axis (it should be less than 50) `REQUIRED`

**IMPORTANT:** You can only add dinosaurs on free spots
