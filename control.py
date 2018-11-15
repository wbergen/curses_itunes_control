#!/usr/bin/python

# Will Bergen - Simple Curses iTunes Control
#  - The osascript calls are expensive..
#  - Volume adjustment calls are especially delicate

import os
import curses

# String globals:
usage = "[USAGE: p: play/pause, z: shuffle on/off, >: next, <: previous, q: exit]"
usage2 = "[USAGE: arrow up/down: volume up/down, any OTHER key: update info]"
unavail_msg = " No Information Available..."


# Safely get title, artist, album from iTunes
def track_info():
	info = "info"
	shuff = title = artist = album = "--"
	p = os.popen('./get_info')
	while 1:
		line = p.readline()
		if not line:
			break
		info = line.rstrip()

	# Try Expansion:
	try:
		(title, artist, album) = info.split(",")
	except ValueError:
		if (title == "--"):
			title = unavail_msg
		if (artist == "--"):
			artist = unavail_msg
		if (album == "--"):
			album = unavail_msg

	# Remove Leading Spaces...
	return [title, artist[1:], album[1:]]

# Safely get the iTunes player state & shuffle status:
def get_status():
	info = "info"
	shuff = state = "--"
	p = os.popen('./get_p_state')
	while 1:
		line = p.readline()
		if not line:
			break
		info = line.rstrip()

	# Try Expansion:
	try:
		(shuff, state) = info.split(",")
	except ValueError:
		if (shuff == "--"):
			shuff = unavail_msg
		if (state == "--"):
			state = unavail_msg

	# Remove Leading Space...
	return [shuff, state[1:]]

# Get the system volume:
def get_volume():
	info = "info"
	p = os.popen('./get_vol')
	while 1:
		line = p.readline()
		if not line:
			break
		info = line.rstrip()
	return info

# Static Text:
def draw_labels():
	screen.addstr(0,0, usage, curses.color_pair(RED_TEXT))
	screen.addstr(1,0, usage2, curses.color_pair(RED_TEXT))
	screen.addstr(2,0, "Title:", curses.color_pair(BLUE_TEXT))
	screen.addstr(3,0, "Artist:", curses.color_pair(BLUE_TEXT))
	screen.addstr(4,0, "Album:", curses.color_pair(BLUE_TEXT))
	screen.addstr(5,0, "Shuffle:", curses.color_pair(BLUE_TEXT))
	screen.addstr(6,0, "Player Status:", curses.color_pair(BLUE_TEXT))
	screen.addstr(7,0, "Volume:", curses.color_pair(BLUE_TEXT))
	screen.addstr(8,0, "Last Action:", curses.color_pair(BLUE_TEXT))


# Init curses, screen:
screen = curses.initscr()
curses.start_color()
curses.init_color(0,0,0,0)

mypad = curses.newpad(40,60)
mypad_pos = 0
mypad.refresh(mypad_pos, 0, 5, 5, 10, 60)

curses.noecho()    # don't echo the keys on the screen
curses.cbreak()    # don't wait enter for input
curses.curs_set(0) # don't show cursor.

# Colors:
RED_TEXT = 1
curses.init_pair(RED_TEXT, curses.COLOR_RED, curses.COLOR_BLACK)

GREEN_TEXT = 2
curses.init_pair(GREEN_TEXT, curses.COLOR_GREEN, curses.COLOR_BLACK)

BLUE_TEXT = 3
curses.init_pair(BLUE_TEXT, curses.COLOR_BLUE, curses.COLOR_BLACK)

# Main:
def main(screen):

	last_action = "None"

	while True:
		# Clear for new draw:
		screen.erase()

		# Get and Draw Current Infos:
		t_info = track_info()
		s_info = get_status()
		screen.addstr(2,20, t_info[0], 					curses.color_pair(GREEN_TEXT))
		screen.addstr(3,20, t_info[1], 					curses.color_pair(GREEN_TEXT))
		screen.addstr(4,20, t_info[2], 					curses.color_pair(GREEN_TEXT))
		screen.addstr(5,20, s_info[0].capitalize(), 	curses.color_pair(GREEN_TEXT))
		screen.addstr(6,20, s_info[1].capitalize(),		curses.color_pair(GREEN_TEXT))
		screen.addstr(7,20, get_volume(), 				curses.color_pair(GREEN_TEXT))
		screen.addstr(8,20, last_action.capitalize(), 	curses.color_pair(GREEN_TEXT))

		# Draw the static text:
		draw_labels();

		# [BLOCKING] Get an input char:
		c = screen.getch()
		
		## Switch on input:
		# > for next:
		if c == ord('>'):
			os.popen("./next")
			last_action = "Next"

		# < for previous:
		elif c == ord('<'):
			os.popen("./prev")
			last_action = "Previous"

		# p will play/pause:
		elif c == ord('p'):
			os.popen("./tog_pp")
			last_action = "Play/Pause"

		# z will toggle shuffle:
		elif c == ord('z'):
			os.popen("./tog_shuffle")
			last_action = "Shuffle On/Off"

		# up_arrow turns volume up:
		elif c == curses.KEY_UP:
			os.popen("./vol_up -q")
			last_action = "Volume Up"

		# down_arrow turns volume down:
		elif c == curses.KEY_DOWN:
			os.popen("./vol_down -q")
			last_action = "Volume Down"

		# q will exit:
		elif c == ord('q'):
			break

		# Update/Draw:
		screen.refresh()

# Go:
curses.wrapper(main)

