#-*- coding: utf8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import sys
from style import Style


if sys.platform == 'win32':
	import ctypes
	import struct


	handle = ctypes.windll.Kernel32.GetStdHandle(-11)


	def get_console_screen_attributes(handle):
		csbi = ctypes.create_string_buffer(22)
		ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
		(cols, rows, cur_x, cur_y, w_attrs, left, top, right, bottom, max_x, max_y) = struct.unpack('4hH6h', csbi.raw)
		return w_attrs


	def set_color(handle, color_code):
		ctypes.windll.Kernel32.SetConsoleTextAttribute(handle, color_code)


	def reset_color(handle):
		ctypes.windll.kernel32.SetConsoleTextAttribute(handle, default_attributes)


	default_attributes = get_console_screen_attributes(handle)

	normal, bold, underline = 0, 1, 4
	black, blue, green, aqua, red, purple, yellow, gray = range(0, 8)
	dark_gray, light_blue, light_green, light_aqua, light_red, light_purple, light_yellow, white = range(8, 16)
	cyan, magenta = aqua, purple
	light_cyan, light_magenta = light_aqua, light_purple
	default = -1


	def print_color_text(text, fg_color, bg_color=None, font_style=0):
		if (fg_color is not None and fg_color != default) and (bg_color is not None and bg_color != default):
			set_color(handle, bg_color * 16 + fg_color)
		elif (fg_color is None or fg_color == default) and (bg_color is not None and bg_color != default):
			set_color(handle, bg_color * 16 + (default_attributes & 0x0f))
		elif (fg_color is not None and fg_color != default) and (bg_color is None or bg_color == default):
			set_color(handle, fg_color)
		else:
			reset_color(handle)
		sys.stdout.write(text)
		reset_color(handle)


	def print_style_char(style):
		print_color_text(style.char, style.fg_color, style.bg_color, style.font_style)


	def print_test_table():
		print('=' * 4 * 16)
		print('Color table:')
		print('=' * 4 * 16)
		for bg_color in xrange(0, 16):
			for fg_color in xrange(0, 16):
				print_color_text(' %02X ' % (bg_color * 16 + fg_color), fg_color, bg_color)
			sys.stdout.write('\n')
		print('=' * 4 * 16)

else:
	normal, bold, underline = 0, 1, 4
	black, red, green, yellow, blue, magenta, cyan, gray = range(0, 8)
	dark_gray, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, white = range(60, 68)
	aqua, purple = cyan, magenta
	light_aqua, light_purple = light_cyan, light_magenta
	default = -1
	reset = '\x1b[0m'


	def print_color_text(text, fg_color, bg_color=None, font_style=0):
		if font_style is None:
			font_style = normal
		if (fg_color is not None and fg_color != default) and (bg_color is not None and bg_color != default):
			formatted = '\x1b[%d;%d;%dm' % (font_style, 40 + bg_color, 30 + fg_color)
		elif (fg_color is None or fg_color == default) and (bg_color is not None and bg_color != default):
			formatted = '\x1b[%d;%dm' % (font_style, 40 + bg_color)
		elif (fg_color is not None and fg_color != default) and (bg_color is None or bg_color == default):
			formatted = '\x1b[%d;%dm' % (font_style, 30 + fg_color)
		else:
			formatted = reset
		sys.stdout.write(formatted + text + reset)


	def print_style_char(style):
		print_color_text(style.char, style.fg_color, style.bg_color, style.font_style)


	def print_test_table():
		print('=' * 9 * 16)
		print('Color table:')
		print('=' * 9 * 16)
		for bg_color in range(0, 8) + range(60, 68):
			for fg_color in range(0, 8) + range(60, 68):
				print_color_text(' %03d;%03d ' % (40 + bg_color, 30 + fg_color), fg_color, bg_color)
			sys.stdout.write('\n')
		print('=' * 9 * 16)


if __name__ == '__main__':
	print_test_table()	
