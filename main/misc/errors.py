# -*- coding: utf-8 -*-


class ViewProcessJump(Exception):
    def __init__(self, code, extra=None):
        self.code = code
        self.extra = extra
