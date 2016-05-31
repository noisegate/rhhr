# rhhr

Solves rush hour puzzle. Initial state given by text file of the form:

```
    ....AA
    ..BBCC
    rr..EF
    GGHHEF
    ...IEF
    ...IJJ
```
useage:

```bash
    python interface.py -f ini.txt
```
##or without curses iface

eg:

```python
    import game
    game = Game("./ini.txt")
    res = game.solution()
 
    for step in res:
        print
        step.plot()
    
```

##work in progress

make sure terminal is at least 70x40, not variable yet.

not the most efficient/fastest code. just a demo.




##screenshot

![alt text](https://github.com/noisegate/rhhr/blob/master/artwork/sh.png)
  
