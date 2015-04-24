#-*- coding: utf8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import copy
import math
from colors import *
from style import Style


class AsciiCanvas(object):
    """
    ASCII canvas for drawing in console using ASCII chars
    """

    def __init__(self, cols, lines, style=None):
        """
        Initialize ASCII canvas
        """
        if cols < 1 or cols > 1000 or lines < 1 or lines > 1000:
            raise Exception('Canvas cols/lines must be in range [1..1000]')
        self.cols = cols
        self.lines = lines
        if style is None:
            style = Style(char=' ', fg_color=default, bg_color=default, font_style=normal)
        else:
            style.char = self.__filter_char(style.char, ' ')
        self.style = style
        self.canvas = [[style] * cols for _ in xrange(lines)]

    def clear(self):
        """
        Fill canvas with default style
        """
        self.canvas = [[self.style] * self.cols for _ in xrange(self.lines)]

    def print_out(self):
        """
        Print out styled canvas to console
        """
        for line in self.canvas:
            for char_style in line:
                print_style_char(char_style)
            sys.stdout.write('\n')

    def add_point(self, x, y, style=None):
        """
        Add point
        """
        style = self.__prepare_style(style, 'o')
        if self.check_coord_in_range(x, y):
            self.canvas[y][x] = style

    def add_line(self, x0, y0, x1, y1, style=None):
        """
        Add ASCII line (x0, y0 -> x1, y1) to the canvas, fill line with `style`
        """
        style = self.__prepare_style(style, 'o')
        if x0 > x1:
            # swap A and B
            x1, x0 = x0, x1
            y1, y0 = y0, y1
        # get delta x, y
        dx = x1 - x0
        dy = y1 - y0
        # if a length of line is zero just add point
        if dx == 0 and dy == 0:
            if self.check_coord_in_range(x0, y0):
                self.canvas[y0][x0] = style
            return
        # when dx >= dy use fill by x-axis, and use fill by y-axis otherwise
        if abs(dx) >= abs(dy):
            for x in xrange(x0, x1 + 1):
                y = y0 if dx == 0 else y0 + int(round((x - x0) * dy / float((dx))))
                if self.check_coord_in_range(x, y):
                    self.canvas[y][x] = style
        else:
            if y0 < y1:
                for y in xrange(y0, y1 + 1):
                    x = x0 if dy == 0 else x0 + int(round((y - y0) * dx / float((dy))))
                    if self.check_coord_in_range(x, y):
                        self.canvas[y][x] = style
            else:
                for y in xrange(y1, y0 + 1):
                    x = x0 if dy == 0 else x1 + int(round((y - y1) * dx / float((dy))))
                    if self.check_coord_in_range(x, y):
                        self.canvas[y][x] = style

    def add_text(self, x, y, text, style=None):
        """
        Add text to canvas at position (x, y)
        """
        style = self.__prepare_style(style, ' ')
        for i, c in enumerate(text):
            if self.check_coord_in_range(x + i, y):
                text_style = Style(c, style.fg_color, style.bg_color, style.font_style)
                self.canvas[y][x + i] = text_style

    def add_rect(self, x, y, w, h, fill_style=None, outline_style=None):
        """
        Add rectangle filled with `fill_style` and outline with `outline_style`
        """
        fill_style = self.__prepare_style(fill_style, self.style.char)
        outline_style = self.__prepare_style(outline_style, 'o')
        for px in xrange(x, x + w):
            for py in xrange(y, y + h):
                if self.check_coord_in_range(px, py):
                    if px == x or px == x + w - 1 or py == y or py == y + h - 1:
                        self.canvas[py][px] = outline_style
                    else:
                        self.canvas[py][px] = fill_style

    def add_nine_patch_rect(self, x, y, w, h, nine_patch_style=None):
        """
        Add nine-patch rectangle
        """
        default_3x3_chars = (
            '.', '-', '.',
            '|', ' ', '|',
            '`', '-', "'"
        )
        if nine_patch_style is None:
            nine_patch_style = [Style(char=c) for c in default_3x3_chars]
        # prepare 3x3 styles
        prepared_3x3_styles = []
        for index, style in enumerate(nine_patch_style[0:9]):
            prepared_3x3_styles.append(self.__prepare_style(style, None))
        for px in xrange(x, x + w):
            for py in xrange(y, y + h):
                if self.check_coord_in_range(px, py):
                    if px == x and py == y:
                        self.canvas[py][px] = prepared_3x3_styles[0]
                    elif px == x and y < py < y + h - 1:
                        self.canvas[py][px] = prepared_3x3_styles[3]
                    elif px == x and py == y + h - 1:
                        self.canvas[py][px] = prepared_3x3_styles[6]
                    elif x < px < x + w - 1 and py == y:
                        self.canvas[py][px] = prepared_3x3_styles[1]
                    elif x < px < x + w - 1 and py == y + h - 1:
                        self.canvas[py][px] = prepared_3x3_styles[7]
                    elif px == x + w - 1 and py == y:
                        self.canvas[py][px] = prepared_3x3_styles[2]
                    elif px == x + w - 1 and y < py < y + h - 1:
                        self.canvas[py][px] = prepared_3x3_styles[5]
                    elif px == x + w - 1 and py == y + h - 1:
                        self.canvas[py][px] = prepared_3x3_styles[8]
                    else:
                        self.canvas[py][px] = prepared_3x3_styles[4]

    def add_ellipse(self, x, y, w, h, fill_style=None, outline_style=None):
        """
        Add ellipse inside a rectangle filled with `fill_style` and outline with `outline_style`
        """
        if w < 1 or h < 1:
            return
        fill_style = self.__prepare_style(fill_style, self.style.char)
        outline_style = self.__prepare_style(outline_style, 'o')
        # Bresenham's algorithm to plot ellipse is used
        a = w
        b = h - 1
        eight_a_square = 8 * a * a
        eight_b_square = 8 * b * b
        x_change = 4 * b * b * (1.0 - a)
        y_change = 4 * a * a * ((b & 1) + 1)
        ellipse_error = x_change + y_change + (b & 1) * a * a
        x0 = x
        x1 = x0 + w - 1
        y0 = y + h / 2
        y1 = y0 - (b & 1)
        outline_points = []
        while x0 <= x1:
            # add fill
            if x0 > x and x0 < x + w - 1:
                self.add_line(int(x0), int(y0), int(x0), int(y1), fill_style)
                self.add_line(int(x1), int(y0), int(x1), int(y1), fill_style)
            outline_points.append((int(x1), int(y0)))
            outline_points.append((int(x0), int(y0)))
            outline_points.append((int(x0), int(y1)))
            outline_points.append((int(x1), int(y1)))
            two_ellipse_error = 2 * ellipse_error
            if two_ellipse_error <= y_change:
                y0 += 1
                y1 -= 1
                y_change += eight_a_square
                ellipse_error += y_change
            if two_ellipse_error >= x_change or 2 * ellipse_error > y_change:
                x0 += 1
                x1 -= 1
                x_change += eight_b_square
                ellipse_error += x_change
        while y0 - y1 <= b:
            self.add_point(int(x0 - 1), int(y0), outline_style) 
            self.add_point(int(x1 + 1), int(y0), outline_style)
            self.add_point(int(x0 - 1), int(y1), outline_style)
            self.add_point(int(x1 + 1), int(y1), outline_style)
            y0 += 1
            y1 -= 1
        # draw outline over fill
        for outline_point in outline_points:
            px, py = outline_point
            self.add_point(px, py, outline_style)

    def check_coord_in_range(self, x, y):
        """
        Check that coordinate (x, y) is in range, to prevent out of range error
        """
        return 0 <= x < self.cols and 0 <= y < self.lines

    def get_canvas_as_str(self):
        """
        Return canvas as a string
        """
        return '\n'.join(''.join(char_style.char for char_style in line) for line in self.canvas)

    def __str__(self):
        """
        Return canvas as a string
        """
        return self.get_canvas_as_str()

    def __filter_char(self, char, default_char):
        """
        Filter input char
        """
        if not char:
            return default_char[0] if default_char else 'o'
        elif len(char) > 1:
            return char[0]
        return char

    def __prepare_style(self, style, default_char):
        """
        Prepare style
        """
        if style is None:
            default_char = self.__filter_char(default_char, self.style.char)
            style = Style(default_char, self.style.fg_color, self.style.bg_color, self.style.font_style)
            return style
        new_style = copy.deepcopy(style)
        if not style.char:
            new_style.char = self.__filter_char(default_char, self.style.char)
        else:
            new_style.char = self.__filter_char(style.char, ' ')
        if style.fg_color is None:
            new_style.fg_color = self.style.fg_color
        if style.bg_color is None:
            new_style.bg_color = self.style.bg_color
        return new_style
