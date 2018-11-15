## iTunes Control via Applescript w/ Bash, Python

### Background:
I'm fairly commited to iTunes, and sometimes want to adjust the music playing from my OS X box without, you know, getting up.  The tiny individual progs got annoying to run by themselves, so here's an OS X specific iTunes control based on curses!  Loads nicely over ssh.

### Screen:
![alt text](https://m7c1.com/resources/tunes_control.png "Tunes Control OS X")

### Notes:
* This is a very simple python script, which calls tiny bash progs
* It could be easily written as all bash, or at least without all the files, but I sometimes want to call the individual actions, or use them in other scripts.

