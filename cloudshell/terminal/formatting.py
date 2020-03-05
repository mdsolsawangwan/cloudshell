#!/usr/bin/env python

# pylint: disable=bare-except

import sys
import readline

__all__ = [
    'red',
    'cyan',
    'blue',
    'green',
    'white',
    'yellow',
    'magenta',
]

# colorized formatters
#
red = lambda s: f'\u001b[31m{s}\u001b[0m'
cyan = lambda s: f'\u001b[36m{s}\u001b[0m'
blue = lambda s: f'\u001b[34m{s}\u001b[0m'
green = lambda s: f'\u001b[32m{s}\u001b[0m'
white = lambda s: f'\u001b[37;1m{s}\u001b[0m'
yellow = lambda s: f'\u001b[33m{s}\u001b[0m'
magenta = lambda s: f'\u001b[35m{s}\u001b[0m'

# prompt handlers
#
class PS1LineCounter(object):
    """
    a simple prompt that displays an incrementing count.

    >>> import sys
    >>> sys.ps1 = PS1LineCounter()
    """

    def __init__(self, prompt_str: str = None) -> None:
        self.count = 0

        self.prompt_str =      \
            prompt_str         \
            if prompt_str else \
            '[{line_no:^{col_width}}] '

    def __str__(self) -> str:
        self.count += 1

        w = len(f'{self.count}') // 2

        return self.prompt_str.format(line_no=self.count, col_width=w)

class PromptStateExpressionHandler(object):
    """
    manages custom ps1 and ps2 prompts.

    >>> import sys
    >>> sys.displayhook = PromptStateExpressionHandler()
    """

    def __init__(self, ps1_prompt: str = None, ps2_prompt: str = None):
        self.expr_count = 0
        self.line_count = 0

        self.previous_value = self

        self.ps1_str = ps1_prompt if ps1_prompt else '[{line_no:^{col_width}}]  '
        self.ps2_str = ps2_prompt if ps2_prompt else ' {space_char:>{col_width}}{delimit_char}  '

        self.ps1(self.expr_count)
        self.ps2(self.expr_count)

    def __call__(self, value):
        self.line_count += 1

        if value != self.previous_value:
            self.expr_count += 1

            self.ps1(self.expr_count)
            self.ps2(self.expr_count)

            delta = self.line_count - self.expr_count
            if delta == 1:
                self.expr_count += 1

        self.previous_value = value

        sys.__displayhook__(value)

    def col_width(self, col_value: object) -> int:
        return len(f'{col_value}') // 2

    def ps1(self, line_no: int) -> None:
        sys.ps1 = self.ps1_str.format(
            line_no=line_no, col_width=self.col_width(line_no))

    def ps2(self, line_no: int) -> None:
        sys.ps2 = self.ps2_str.format(
            space_char=' ', delimit_char='|', col_width=self.col_width(line_no))

class AutoindentHandler(object):
    """
    manages auto-indentation.
    """

    DEFAULT_TAB_CHAR = '    '

    def __init__(self, tab_char: str = None) -> None:
        self.exception_var_exists = False  # for caching the result of 'hasattr()'
        self.last_indent = ''

        self.tab_char =      \
            tab_char         \
            if tab_char else \
            AutoindentHandler.DEFAULT_TAB_CHAR

    def __call__(self) -> None:
        line = self.last_expression()

        indent_index = self.last_indent_index(line)
        indent = ''

        if len(line.strip()) > 1 and not self.last_result_was_error():
            if line.count('(') > line.count(')'):
                indent = self.calc_indentation(indent_index + 1)
            elif line.count(')') > line.count('('):
                indent = self.calc_indentation(indent_index - 1)
            elif line.count('[') > line.count(']'):
                indent = self.calc_indentation(indent_index + 1)
            elif line.count(']') > line.count('['):
                indent = self.calc_indentation(indent_index - 1)
            elif line.count('{') > line.count('}'):
                indent = self.calc_indentation(indent_index + 1)
            elif line.count('}') > line.count('{'):
                indent = self.calc_indentation(indent_index - 1)
            elif line[-1] == ':':
                indent = self.calc_indentation(indent_index + 1)
            else:
                indent = self.calc_indentation(indent_index)
        # else:
        #     indent = '\n'

        # self.last_indent = indent
        # if indent_index > 0 and line == '':
        #     indent = '\r'

        readline.insert_text(indent)

    def calc_indentation(self, num_indents: int) -> str:
        return ''.join(
            [self.tab_char for _ in range(num_indents)]
        )

    def last_expression(self) -> str:
        return readline.get_history_item(
            readline.get_current_history_length())

    def last_indent_index(self, expr: str) -> int:
        try:
            return expr.rindex(self.tab_char) // 4 + 1
        except:
            return 0

    def last_result_was_error(self) -> bool:
        if not self.exception_var_exists:
            self.exception_var_exists = hasattr(sys, 'last_type')

        if self.exception_var_exists and sys.last_type is not None:
            sys.last_type = None
            return True

        return False
