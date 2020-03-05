#!/usr/bin/env python

import rlcompleter

class Session(rlcompleter.Completer):
    """
    TODO: custom completion logic.
    """

    def complete(self, text, state):
        if state == 0:
            pass
        return super().complete(text, state)
