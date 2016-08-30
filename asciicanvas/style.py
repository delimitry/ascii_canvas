# -*- coding: utf8 -*-

class Style(object):
    """
    Style for canvas elements
    """

    def __init__(self, char=None, fg_color=None, bg_color=None, font_style=0):
        self.char = char
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.font_style = font_style
