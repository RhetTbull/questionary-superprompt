"""Test multiple options for superprompt"""

import pytest

import superprompt
from tests.utils import (
    KeyInputs,
    ask_with_patched_input,
    make_dict_style_asker,
    mock_confirm,
)

QUESTIONS_MULTIPLE_LIST = {
    "name": "books",
    "message": "Not needed, see multiple_message",
    # if multiple, allows multiple values for this name
    "multiple": 3,
    "type": "list",
    "questions": [
        {
            "name": "title",  # <-- name is not needed for "list", if provided, not used, just passes values
            "message": "What's the title?",
            "type": "text",
        },
        {
            "name": "author",
            "message": "Who's the author?",
            "type": "text",
        },
    ],
}

QUESTIONS_MULTIPLE_DICT = QUESTIONS_MULTIPLE_LIST.copy()
QUESTIONS_MULTIPLE_DICT["type"] = "dict"

ANSWERS = (
    "Dune"
    + KeyInputs.ENTER
    + "Frank Herbert"
    + KeyInputs.ENTER
    + "The Lord of the Rings"
    + KeyInputs.ENTER
    + "J.R.R. Tolkien"
    + KeyInputs.ENTER
    + "Hyperion"
    + KeyInputs.ENTER
    + "Dan Simmons"
    + KeyInputs.ENTER
)


def test_multiple_list():
    """Test multiple list"""
    questions = make_dict_style_asker(QUESTIONS_MULTIPLE_LIST)
    result_dict = ask_with_patched_input(questions, ANSWERS)
    assert result_dict == {
        "books": [
            ["Dune", "Frank Herbert"],
            ["The Lord of the Rings", "J.R.R. Tolkien"],
            ["Hyperion", "Dan Simmons"],
        ]
    }


def test_multiple_list_negative_1(monkeypatch):
    """Test multiple list with negative multiple (up to X values)"""
    new_questions = QUESTIONS_MULTIPLE_LIST.copy()
    new_questions["multiple"] = -3  # up to 3 values
    new_questions["multiple_message"] = "Enter another book?"
    questions = make_dict_style_asker(new_questions)

    monkeypatch.setattr(superprompt, "confirm", mock_confirm(["y", "y", "y"]))
    result_dict = ask_with_patched_input(questions, ANSWERS)
    assert result_dict == {
        "books": [
            ["Dune", "Frank Herbert"],
            ["The Lord of the Rings", "J.R.R. Tolkien"],
            ["Hyperion", "Dan Simmons"],
        ]
    }


def test_multiple_list_negative_2(monkeypatch):
    """Test multiple list with negative multiple (up to X values)"""
    new_questions = QUESTIONS_MULTIPLE_LIST.copy()
    new_questions["multiple"] = -3  # up to 3 values
    new_questions["multiple_message"] = "Enter another book?"
    questions = make_dict_style_asker(new_questions)

    monkeypatch.setattr(superprompt, "confirm", mock_confirm(["y", "n"]))
    result_dict = ask_with_patched_input(questions, ANSWERS)
    assert result_dict == {
        "books": [
            ["Dune", "Frank Herbert"],
            ["The Lord of the Rings", "J.R.R. Tolkien"],
        ]
    }


def test_multiple_list_negative_3(monkeypatch):
    """Test multiple list with negative multiple (up to X values)"""
    new_questions = QUESTIONS_MULTIPLE_LIST.copy()
    new_questions["multiple"] = -3  # up to 3 values
    new_questions["multiple_message"] = "Enter another book?"
    questions = make_dict_style_asker(new_questions)

    monkeypatch.setattr(superprompt, "confirm", mock_confirm(["n"]))
    result_dict = ask_with_patched_input(questions, ANSWERS)
    assert result_dict == {
        "books": [
            ["Dune", "Frank Herbert"],
        ]
    }


def test_multiple_dict():
    """Test multiple dict"""
    questions = make_dict_style_asker(QUESTIONS_MULTIPLE_DICT)
    result_dict = ask_with_patched_input(questions, ANSWERS)
    assert result_dict == {
        "books": [
            {"title": "Dune", "author": "Frank Herbert"},
            {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien"},
            {"title": "Hyperion", "author": "Dan Simmons"},
        ]
    }


def test_multiple_dict_negative_1(monkeypatch):
    """Test multiple list with negative multiple (up to X values)"""
    new_questions = QUESTIONS_MULTIPLE_DICT.copy()
    new_questions["multiple"] = -3  # up to 3 values
    new_questions["multiple_message"] = "Enter another book?"
    questions = make_dict_style_asker(new_questions)

    monkeypatch.setattr(superprompt, "confirm", mock_confirm(["y", "y", "y"]))
    result_dict = ask_with_patched_input(questions, ANSWERS)
    assert result_dict == {
        "books": [
            {"title": "Dune", "author": "Frank Herbert"},
            {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien"},
            {"title": "Hyperion", "author": "Dan Simmons"},
        ]
    }


def test_multiple_dict_negative_2(monkeypatch):
    """Test multiple list with negative multiple (up to X values)"""
    new_questions = QUESTIONS_MULTIPLE_DICT.copy()
    new_questions["multiple"] = -3  # up to 3 values
    new_questions["multiple_message"] = "Enter another book?"
    questions = make_dict_style_asker(new_questions)

    monkeypatch.setattr(superprompt, "confirm", mock_confirm(["y", "n"]))
    result_dict = ask_with_patched_input(questions, ANSWERS)
    assert result_dict == {
        "books": [
            {"title": "Dune", "author": "Frank Herbert"},
            {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien"},
        ]
    }


def test_multiple_dict_negative_3(monkeypatch):
    """Test multiple list with negative multiple (up to X values)"""
    new_questions = QUESTIONS_MULTIPLE_DICT.copy()
    new_questions["multiple"] = -3  # up to 3 values
    new_questions["multiple_message"] = "Enter another book?"
    questions = make_dict_style_asker(new_questions)

    monkeypatch.setattr(superprompt, "confirm", mock_confirm(["n"]))
    result_dict = ask_with_patched_input(questions, ANSWERS)
    assert result_dict == {
        "books": [
            {"title": "Dune", "author": "Frank Herbert"},
        ]
    }
