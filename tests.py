#!/usr/bin/env python
#-*- coding: utf8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import unittest
from asciicanvas import AsciiCanvas


class TestAsciiCanvas(unittest.TestCase):

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
        
        ascii_canvas = AsciiCanvas(1, 1, '#')
        canvas_str = '#'
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str)
        
        ascii_canvas = AsciiCanvas(2, 1, 'XYZ')
        canvas_str = 'XX'
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str)
        
        ascii_canvas.clear()
        # must be the same as before clear
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str,)

    def test_lines_draw(self):
        ascii_canvas = AsciiCanvas(5, 2)
        ascii_canvas.add_line(0, 0, 0, 0)
        canvas_with_lines_str = \
            line('o    ') + \
            last('     ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_lines_str)

        ascii_canvas = AsciiCanvas(5, 5)
        ascii_canvas.add_line(-5, -5, 10, 10, '****')
        ascii_canvas.add_line(4, 0, 0, 4, '#')
        canvas_with_lines_str = \
            line('*   #') + \
            line(' * # ') + \
            line('  #  ') + \
            line(' # * ') + \
            last('#   *')
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
        ascii_canvas.add_rect(0, 0, 5, 5, fill_char='.', outline_char='#')
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
        outline_3x3_chars = (
            '123'
            '456'
            '789'
        )
        ascii_canvas.add_nine_patch_rect(0, 0, 5, 5, outline_3x3_chars)
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
        ascii_canvas.add_nine_patch_rect(0, 0, 2, 2)
        canvas_with_rect_str = \
            line('..') + \
            last("`'")
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_with_rect_str, 'Incorrect canvas with 9-patch rect')

        ascii_canvas = AsciiCanvas(2, 2)
        ascii_canvas.add_nine_patch_rect(1, 1, 1, 1, '123456789')
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
        canvas_str = \
            line('     ') + \
            line('     ') + \
            line('     ') + \
            line('     ') + \
            last('     ')
        self.assertEqual(ascii_canvas.get_canvas_as_str(), canvas_str)
        self.assertEqual(str(ascii_canvas), canvas_str)

def line(s):
    return s + '\n'


def last(s):
    return s


if __name__ == '__main__':
    unittest.main(verbosity=1)
