
# Synacor Challenge

This is an implementation of the [Synacor Challenge](https://challenge.synacor.com/).

I found the challenge awsome. Many thanks an Eric and Synacor for making it possible. :)

## Debugger

The embedded debugger implements the following commands:

```
  autorun   Executes the commands indicated in the file commands.
            The file may contain additionally following commands:
            "break" stops the further execution
  b addr    Set a breakpoint at address addr.
  rb idx    Register breakpoint sets a read write breakpoint when
            register idx (0-7) is read or written.
  cont      Continues the execution (exits debugger mode)
  d [n]     Disassemble instructions starting at the current ip.
            The default value for n is 1.
  n         Next, executes one instructions
  p         Prints the current state of the registers.
  set ip|rn val  Set the indicated register (r0-r7) or the ip to the
            indicated value
  st        Stack trace, prints the current content of the stack.
```

## SPOILER

Stop reading if you do not want to know about how to solve the puzzle/s.

## Debugger

The debugger command autorun accepts one more option within the commands file:

```
            "solve6027" solve the teleport puzzle by changing the
            instructions at ip 6027.
```

## Codes

### First code

The first code is already provided within the arch-specification document. In my case was
'CfGDYTQZktmZ'

### Second Code

After implmeneting the few first instructions of the VM the first output is the next code:

> Welcome to the Synacor Challenge!
> Please record your progress by putting codes like
> this one into the challenge website: MpDxeUCjtPse

### Third Code

After implementing correctly all instructions which seems to be checked (tested) by the program itself you get the third code:

> The self-test completion code is: GRyPajkrYVMd

### Forth Code

The first scene of the game you see a tablet using this gets you the next code:

> You find yourself writing "sDAZAtapyfeT" on the tablet.  Perhaps it's some kind of code?

### Fith Code

Walking around you see the following code:

> Chiseled on the wall of one of the passageways, you see:
>    qqJrDuIQPdJI
> You take note of this and keep walking.

### Sixth Code

Using the teleporter for the first time:

> You activate the teleporter!  As you spiral through time and space, you think you see a pattern in the stars...
>    bTFGmAlJfYEe
> After a few moments, you find yourself back on solid ground and a little disoriented.

### Seventh Code

Solving the puzzle

> You wake up on a sandy beach with a slight headache.  The last thing you remember is activating that teleporter... but now you can't find it anywhere in your pack.  Someone seems to have drawn a message in the sand here:
>    LwBcFitevqLg
> It begins to rain.  The message washes away.  You take a deep breath and feel firmly grounded in reality as the effects of the teleportation wear off.

## Eight Code

Getting into the vault

> You gaze into the mirror, and you see yourself gazing back.  But wait!  It looks like someone wrote on your face while you were unconscious on the beach!  Through the mirror, you see "dvvoAMpOHpVx" scrawled in charcoal on your forehead.

Which mirrored is the value: xVqHOqMAovvb
