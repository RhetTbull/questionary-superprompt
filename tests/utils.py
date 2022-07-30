# -*- coding: utf-8 -*-
"""Utility functions to test input/output of superprompt, copied from questionary"""

from __future__ import annotations

import asyncio

import prompt_toolkit
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
from questionary.prompts import prompt_by_name
from questionary.utils import is_prompt_toolkit_3
from superprompt import superprompt

prompt_toolkit_version = tuple([int(v) for v in prompt_toolkit.VERSION])


class KeyInputs:
    DOWN = "\x1b[B"
    UP = "\x1b[A"
    LEFT = "\x1b[D"
    RIGHT = "\x1b[C"
    ENTER = "\r"
    ESCAPE = "\x1b"
    CONTROLC = "\x03"
    CONTROLN = "\x0e"
    CONTROLP = "\x10"
    BACK = "\x7f"
    SPACE = " "
    TAB = "\x09"
    ONE = "1"
    TWO = "2"
    THREE = "3"


def feed_cli_with_input(_type, message, texts, sleep_time=1, **kwargs):
    """
    Create a Prompt, feed it with the given user input and return the CLI
    object.
    You an provide multiple texts, the feeder will async sleep for `sleep_time`
    This returns a (result, Application) tuple.
    """

    if not isinstance(texts, list):
        texts = [texts]

    def _create_input(inp):
        prompter = prompt_by_name(_type)
        application = prompter(message, input=inp, output=DummyOutput(), **kwargs)
        if is_prompt_toolkit_3():
            loop = asyncio.new_event_loop()
            future_result = loop.create_task(application.unsafe_ask_async())

            for i, text in enumerate(texts):
                # noinspection PyUnresolvedReferences
                inp.send_text(text)

                if i != len(texts) - 1:
                    loop.run_until_complete(asyncio.sleep(sleep_time))
            result = loop.run_until_complete(future_result)
        else:
            for text in texts:
                inp.send_text(text)
            result = application.unsafe_ask()
        return result, application

    return execute_with_input_pipe(_create_input)


def patched_prompt(questions, text, **kwargs):
    """Create a prompt where the input and output are predefined."""

    def run(inp):
        # noinspection PyUnresolvedReferences
        inp.send_text(text)
        result = superprompt(questions, input=inp, output=DummyOutput(), **kwargs)
        return result

    return execute_with_input_pipe(run)


def execute_with_input_pipe(func):
    if prompt_toolkit_version < (3, 0, 29):
        inp = create_pipe_input()
        try:
            return func(inp)
        finally:
            inp.close()
    else:
        with create_pipe_input() as inp:
            return func(inp)


def make_dict_style_asker(questions):
    """Return a function that asks questions using dict style with superprompt"""

    def asker(**kwargs):
        return superprompt(questions, **kwargs)

    return asker


def ask_with_patched_input(q, text):
    """Ask question function q with text as input"""

    def run(inp):
        inp.send_text(text)
        return q(input=inp, output=DummyOutput())

    return execute_with_input_pipe(run)


def mock_confirm(answers: list[str]):
    class MockConfirm:
        """Mock confirm that yields answers from a list of values"""

        def __init__(self, *args, **kwargs):
            self.answers = answers

        def ask(self):
            return next(self)

        def __iter__(self):
            return self

        def __next__(self):
            try:
                return self.answers.pop(0).lower() == "y"
            except IndexError:
                raise StopIteration()

    return MockConfirm
