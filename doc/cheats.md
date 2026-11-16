# Cheats

Pendant la partie, saisissez "help" pour accéder au manuel des commandes de cheat :

kill:
*Kill the player*

skip-level:
*Skip the curent level*

help:
ToDo *Dsiplay all commad manual*

reset-all:
*Reset all ghosts and set their position back to their respective corner*

lives:
*Change player's life value*
args:
        life: int

score:
*Change player's score value*
args:
         score: int

speed:
*Change player's speed value*
args:
         speed: float | str (reset can be used)

freeze:
*Freeze ghosts(they can't move)*
args:
        target: str (ghost's name or all)
        bool: bool

invincible:
*Set if the player can be hit by ghosts*
args:
         bool: bool

stop-timer:
*Stop the timer or not*
args:
         bool: bool

super:
*Set Pacman to super Pacman or not*
args:
         bool: bool