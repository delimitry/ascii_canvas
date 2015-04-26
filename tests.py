#!/usr/bin/env python
# -*- coding: utf8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import unittest
import colors
from style import Style
from asciicanvas import AsciiCanvas



class TestAsciiCanvas(unittest.TestCase):
    """
    Test cases for AsciiCanvas
    """

    def test_canvas_size(self):
        ascii_canvas = AsciiCanvas(10, 10)
        self.assertEqual(ascii_canvas.cols, 10)
        self.assertEqual(ascii_canvas.lines, 10)
        # check ranges
        with self.assertRaises(Exception):
            ascii_canvas = AsciiCanvas(-1, -1)
        with self.assertRaises(Exception):
            ascii_canvas = AsciiCanvas(0, 0)
        with self.assertRaises(Exception):
            ascii_canvas = AsciiCanvas(-10, 10)
        with self.assertRaises(Exception):
            ascii_canvas = AsciiCanvas(10, -100)
        with self.assertRaises(Exception):
            ascii_canvas = AsciiCanvas(10, 1001)
        with self.assertRaises(Exception):
            ascii_canvas = AsciiCanvas(1001, 1000)

    def test_canvas(self):
        ascii_canvas = AsciiCanvas(10, 10)
        canvas_str = (' ' * 10 + '\n') * 9 + ' ' * 10
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str)

        ascii_canvas = AsciiCanvas(1, 1, Style('#'))
        canvas_str = '#'
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str)

        ascii_canvas = AsciiCanvas(2, 1, Style('XYZ'))
        canvas_str = 'XX'
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str)

        ascii_canvas.clear()
        # must be the same as before clear
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str)

    def test_point_draw(self):
        ascii_canvas = AsciiCanvas(2, 2)
        ascii_canvas.add_point(0, 0)
        canvas_with_points_str = \
            line('o ') + \
            last('  ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_points_str, 'Incorrect canvas with lines')

        ascii_canvas = AsciiCanvas(2, 2)
        ascii_canvas.add_point(-5, -5)
        canvas_with_points_str = \
            line('  ') + \
            last('  ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_points_str, 'Incorrect canvas with lines')

        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_point(1, 1, Style('Ooo'))
        ascii_canvas.add_point(3, 3, Style('*'))
        ascii_canvas.add_point(0, 4, Style('.'))
        ascii_canvas.add_point(4, 0, Style(''))
        ascii_canvas.add_point(4, 1, Style(' '))
        canvas_with_lines_str = \
            line('    o') + \
            line(' O   ') + \
            line('     ') + \
            line('   * ') + \
            last('.    ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_lines_str, 'Incorrect canvas with lines')

    def test_line_draw(self):
        ascii_canvas = AsciiCanvas(5, 2)
        ascii_canvas.add_line(0, 0, 0, 0)
        canvas_with_lines_str = \
            line('o    ') + \
            last('     ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_lines_str, 'Incorrect canvas with lines')

        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_line(-5, -5, 10, 10, Style('****'))
        ascii_canvas.add_line(4, 0, 0, 4, Style('#'))
        canvas_with_lines_str = \
            line('*   #') + \
            line(' * # ') + \
            line('  #  ') + \
            line(' # * ') + \
            last('#   *')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_lines_str, 'Incorrect canvas with lines')

        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_line(0, 0, 4, 0, style=Style('-'))
        ascii_canvas.add_line(0, 0, 0, 3, style=Style('|'))
        canvas_with_lines_str = \
            line('|----') + \
            line('|    ') + \
            line('|    ') + \
            line('|    ') + \
            last('     ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_lines_str, 'Incorrect canvas with lines')

    def test_text_draw(self):
        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_text(-3, 2, 'hello world!!!!!')
        canvas_with_text_str = \
            line('     ') + \
            line('     ') + \
            line('lo wo') + \
            line('     ') + \
            last('     ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_text_str, 'Incorrect canvas with text')

        ascii_canvas = AsciiCanvas(5, 1)
        ascii_canvas.add_text(2, 0, '')
        canvas_with_text_str = \
            last('     ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_text_str, 'Incorrect canvas with text')

        ascii_canvas = AsciiCanvas(5, 1)
        ascii_canvas.add_text(2, 0, '\xFF')
        canvas_with_text_str = \
            last('  \xFF  ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_text_str, 'Incorrect canvas with text')

    def test_rect_draw(self):
        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_rect(0, 0, 5, 5)
        canvas_with_rect_str = \
            line('ooooo') + \
            line('o   o') + \
            line('o   o') + \
            line('o   o') + \
            last('ooooo')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with rect')

        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_rect(0, 0, 5, 5, fill_style=Style('.'), outline_style=Style('#'))
        canvas_with_rect_str = \
            line('#####') + \
            line('#...#') + \
            line('#...#') + \
            line('#...#') + \
            last('#####')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with rect')

        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_rect(4, 4, 1, 1)
        canvas_with_rect_str = \
            line('     ') + \
            line('     ') + \
            line('     ') + \
            line('     ') + \
            last('    o')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with rect')

        ascii_canvas = AsciiCanvas(2, 2)
        ascii_canvas.add_rect(1, 1, 0, 0)
        canvas_with_rect_str = \
            line('  ') + \
            last('  ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with rect')

        ascii_canvas = AsciiCanvas(2, 2)
        ascii_canvas.add_rect(1, 1, -1, -1)
        canvas_with_rect_str = \
            line('  ') + \
            last('  ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with rect')

    def test_nine_patch_rect_draw(self):
        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_nine_patch_rect(0, 0, 5, 5)
        canvas_with_rect_str = \
            line('.---.') + \
            line('|   |') + \
            line('|   |') + \
            line('|   |') + \
            last("`---'")
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with 9-patch rect')

        ascii_canvas = AsciiCanvas(5, 5)
        nine_patch_style = (
            Style('1'), Style('2'), Style('3'),
            Style('4'), Style('5'), Style('6'),
            Style('7'), Style('8'), Style('9')
        )
        ascii_canvas.add_nine_patch_rect(0, 0, 5, 5, nine_patch_style)
        canvas_with_rect_str = \
            line('12223') + \
            line('45556') + \
            line('45556') + \
            line('45556') + \
            last('78889')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with 9-patch rect')

        ascii_canvas = AsciiCanvas(2, 2)
        ascii_canvas.add_nine_patch_rect(0, 0, 2, 2)
        canvas_with_rect_str = \
            line('..') + \
            last("`'")
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with 9-patch rect')

        ascii_canvas = AsciiCanvas(2, 2)
        ascii_canvas.add_nine_patch_rect(0, 0, 0, 0)
        canvas_with_rect_str = \
            line('  ') + \
            last('  ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with 9-patch rect')

        ascii_canvas = AsciiCanvas(2, 2)
        ascii_canvas.add_nine_patch_rect(1, 1, 1, 1, nine_patch_style)
        canvas_with_rect_str = \
            line('  ') + \
            last(' 1')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with 9-patch rect')

        ascii_canvas = AsciiCanvas(2, 2)
        ascii_canvas.add_nine_patch_rect(1, 1, -1, -1)
        canvas_with_rect_str = \
            line('  ') + \
            last('  ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with 9-patch rect')

    def test_ellipse_draw(self):
        ascii_canvas = AsciiCanvas(3, 3)
        ascii_canvas.add_ellipse(0, 0, 2, 2)
        canvas_str = \
            line('oo ') + \
            line('oo ') + \
            last('   ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with ellipse')

        ascii_canvas = AsciiCanvas(3, 3)
        ascii_canvas.add_ellipse(0, 0, 1, 1)
        canvas_str = \
            line('o  ') + \
            line('   ') + \
            last('   ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with ellipse')

        ascii_canvas = AsciiCanvas(3, 3)
        ascii_canvas.add_ellipse(0, 0, 0, 0)
        canvas_str = \
            line('   ') + \
            line('   ') + \
            last('   ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with ellipse')

        ascii_canvas = AsciiCanvas(3, 3)
        ascii_canvas.add_ellipse(3, 3, -2, -2)
        canvas_str = \
            line('   ') + \
            line('   ') + \
            last('   ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with ellipse')

        ascii_canvas = AsciiCanvas(3, 3)
        ascii_canvas.add_ellipse(0, 2, 3, 1)
        canvas_str = \
            line('   ') + \
            line('   ') + \
            last('ooo')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with ellipse')

        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_ellipse(1, 1, 3, 3, Style('o'), Style('O'))
        canvas_str = \
            line('     ') + \
            line('  O  ') + \
            line(' OoO ') + \
            line('  O  ') + \
            last('     ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with ellipse')

        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_ellipse(0, 0, 4, 5)
        canvas_str = \
            line(' oo  ') + \
            line('o  o ') + \
            line('o  o ') + \
            line('o  o ') + \
            last(' oo  ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with ellipse')

        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_ellipse(0, 0, 3, 5)
        canvas_str = \
            line(' o   ') + \
            line('o o  ') + \
            line('o o  ') + \
            line('o o  ') + \
            last(' o   ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with ellipse')

        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_ellipse(0, -1, 2, 7)
        canvas_str = \
            line('oo   ') + \
            line('oo   ') + \
            line('oo   ') + \
            line('oo   ') + \
            last('oo   ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with ellipse')

        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_ellipse(0, 0, 5, 3)
        canvas_str = \
            line(' ooo ') + \
            line('o   o') + \
            line(' ooo ') + \
            line('     ') + \
            last('     ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with ellipse')

        ascii_canvas = AsciiCanvas(15, 5)
        ascii_canvas.add_ellipse(0, 0, 15, 5, Style('.'))
        canvas_str = \
            line('   ooooooooo   ') + \
            line(' oo.........oo ') + \
            line('o.............o') + \
            line(' oo.........oo ') + \
            last('   ooooooooo   ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with ellipse')

    def test_draw_order(self):
        ascii_canvas = AsciiCanvas(3, 3)
        ascii_canvas.add_text(0, 0, 'TE')
        ascii_canvas.add_text(0, 1, 'XT')
        canvas_str = \
            line('TE ') + \
            line('XT ') + \
            last('   ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with text')

        # must overlap the text
        ascii_canvas.add_rect(0, 0, 3, 3)
        canvas_str = \
            line('ooo') + \
            line('o o') + \
            last('ooo')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str, 'Incorrect canvas with rect')

    def test_output(self):
        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_point(2, 2)
        canvas_str = \
            line('     ') + \
            line('     ') + \
            line('  o  ') + \
            line('     ') + \
            last('     ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str)
        self.assertEqual(str(ascii_canvas), canvas_str)


class TestColors(unittest.TestCase):
    """
    Test cases for Colors
    """

    def test_rgb_to_terminal_color(self):
        self.assertEqual(colors.rgb_to_terminal_color((0, 0, 0)), colors.black)
        self.assertEqual(colors.rgb_to_terminal_color((255, 0, 0)), colors.light_red)
        self.assertEqual(colors.rgb_to_terminal_color((0, 255, 0)), colors.light_green)
        self.assertEqual(colors.rgb_to_terminal_color((0, 0, 255)), colors.light_blue)
        self.assertEqual(colors.rgb_to_terminal_color((44, 0, 22)), colors.black)
        self.assertEqual(colors.rgb_to_terminal_color((65, 65, 0)), colors.yellow)
        self.assertEqual(colors.rgb_to_terminal_color((140, 140, 140)), colors.dark_gray)
        self.assertEqual(colors.rgb_to_terminal_color((190, 190, 190)), colors.gray)
        self.assertEqual(colors.rgb_to_terminal_color((255, 255, 255)), colors.white)

    def test_rgb_to_terminal_rgb_ranges(self):
        with self.assertRaises(Exception):
            colors.rgb_to_terminal_color((333, 0, 0))
        with self.assertRaises(Exception):
            colors.rgb_to_terminal_color((-1, 0, 0))
        with self.assertRaises(Exception):
            colors.rgb_to_terminal_color((0, 1111, 0))
        with self.assertRaises(Exception):
            colors.rgb_to_terminal_color((0, 0, 555))
        with self.assertRaises(Exception):
            colors.rgb_to_terminal_color((0, -123, 0))
        with self.assertRaises(Exception):
            colors.rgb_to_terminal_color((0, 0, -123))


def line(s):
    return s + '\n'


def last(s):
    return s


if __name__ == '__main__':
    unittest.main(verbosity=1)
