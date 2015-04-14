#-*- coding: utf8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import math


class AsciiCanvas(object):
    """
    ASCII canvas for drawing in console using ASCII chars
    """

    def __init__(self, cols, lines, fill_char=' '):
        """
        Initialize ASCII canvas
        """
        if cols < 1 or cols > 1000 or lines < 1 or lines > 1000:
            raise Exception('Canvas cols/lines must be in range [1..1000]')
        self.cols = cols
        self.lines = lines
        fill_char = self.__filter_char(fill_char, 'o')
        self.fill_char = fill_char
        self.canvas = [[fill_char] * (cols) for _ in xrange(lines)]

    def clear(self):
        """
        Fill canvas with empty chars
        """
        self.canvas = [[self.fill_char] * (self.cols) for _ in xrange(self.lines)]

    def print_out(self):
        """
        Print out canvas to console
        """
        print(self.get_canvas_as_str())

    def add_point(self, x, y, fill_char='o'):
        """
        Add point
        """
        fill_char = self.__filter_char(fill_char, 'o')
        if self.check_coord_in_range(x, y):
            self.canvas[y][x] = fill_char

    def add_line(self, x0, y0, x1, y1, fill_char='o'):
        """
        Add ASCII line (x0, y0 -> x1, y1) to the canvas, fill line with `fill_char`
        """
        fill_char = self.__filter_char(fill_char, 'o')
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
                self.canvas[y0][x0] = fill_char
            return
        # when dx >= dy use fill by x-axis, and use fill by y-axis otherwise
        if abs(dx) >= abs(dy):
            for x in xrange(x0, x1 + 1):
                y = y0 if dx == 0 else y0 + int(round((x - x0) * dy / float((dx))))
                if self.check_coord_in_range(x, y):
                    self.canvas[y][x] = fill_char
        else:
            if y0 < y1:
                for y in xrange(y0, y1 + 1):
                    x = x0 if dy == 0 else x0 + int(round((y - y0) * dx / float((dy))))
                    if self.check_coord_in_range(x, y):
                        self.canvas[y][x] = fill_char
            else:
                for y in xrange(y1, y0 + 1):
                    x = x0 if dy == 0 else x1 + int(round((y - y1) * dx / float((dy))))
                    if self.check_coord_in_range(x, y):
                        self.canvas[y][x] = fill_char

    def add_text(self, x, y, text):
        """
        Add text to canvas at position (x, y)
        """
        for i, c in enumerate(text):
            if self.check_coord_in_range(x + i, y):
                self.canvas[y][x + i] = c

    def add_rect(self, x, y, w, h, fill_char=' ', outline_char='o'):
        """
        Add rectangle filled with `fill_char` and outline with `outline_char`
        """
        fill_char = self.__filter_char(fill_char, ' ')
        outline_char = self.__filter_char(outline_char, 'o')
        for px in xrange(x, x + w):
            for py in xrange(y, y + h):
                if self.check_coord_in_range(px, py):
                    if px == x or px == x + w - 1 or py == y or py == y + h - 1:
                        self.canvas[py][px] = outline_char
                    else:
                        self.canvas[py][px] = fill_char

    def add_nine_patch_rect(self, x, y, w, h, outline_3x3_chars=None):
        """
        Add nine-patch rectangle
        """
        default_outline_3x3_chars = (
            '.', '-', '.',
            '|', ' ', '|',
            '`', '-', "'"
        )
        if not outline_3x3_chars:
            outline_3x3_chars = default_outline_3x3_chars
        # filter chars
        filtered_outline_3x3_chars = []
        for index, char in enumerate(outline_3x3_chars[0:9]):
            char = self.__filter_char(char, default_outline_3x3_chars[index])
            filtered_outline_3x3_chars.append(char)
        for px in xrange(x, x + w):
            for py in xrange(y, y + h):
                if self.check_coord_in_range(px, py):
                    if px == x and py == y:
                        self.canvas[py][px] = filtered_outline_3x3_chars[0]
                    elif px == x and y < py < y + h - 1:
                        self.canvas[py][px] = filtered_outline_3x3_chars[3]
                    elif px == x and py == y + h - 1:
                        self.canvas[py][px] = filtered_outline_3x3_chars[6]
                    elif x < px < x + w - 1 and py == y:
                        self.canvas[py][px] = filtered_outline_3x3_chars[1]
                    elif x < px < x + w - 1 and py == y + h - 1:
                        self.canvas[py][px] = filtered_outline_3x3_chars[7]
                    elif px == x + w - 1 and py == y:
                        self.canvas[py][px] = filtered_outline_3x3_chars[2]
                    elif px == x + w - 1 and y < py < y + h - 1:
                        self.canvas[py][px] = filtered_outline_3x3_chars[5]
                    elif px == x + w - 1 and py == y + h - 1:
                        self.canvas[py][px] = filtered_outline_3x3_chars[8]
                    else:
                        self.canvas[py][px] = filtered_outline_3x3_chars[4]

    def add_ellipse(self, x, y, w, h, fill_char=' ', outline_char='o'):
        """
        Add ellipse inside a rectangle filled with `fill_char` and outline with `outline_char`
        """
        if w < 1 or h < 1:
            return
        fill_char = self.__filter_char(fill_char, ' ')
        outline_char = self.__filter_char(outline_char, 'o')
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
                self.add_line(int(x0), int(y0), int(x0), int(y1), fill_char)
                self.add_line(int(x1), int(y0), int(x1), int(y1), fill_char)
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
            self.add_point(int(x0 - 1), int(y0), outline_char) 
            self.add_point(int(x1 + 1), int(y0), outline_char)
            self.add_point(int(x0 - 1), int(y1), outline_char)
            self.add_point(int(x1 + 1), int(y1), outline_char)
            y0 += 1
            y1 -= 1
        # draw outline over fill
        for outline_point in outline_points:
            px, py = outline_point
            self.add_point(px, py, outline_char)

    def check_coord_in_range(self, x, y):
        """
        Check that coordinate (x, y) is in range, to prevent out of range error
        """
        return 0 <= x < self.cols and 0 <= y < self.lines

    def get_canvas_as_str(self):
        """
        Return canvas as a string
        """
        return '\n'.join([''.join(col) for col in self.canvas])

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
