import pytest
from questionary.prompt import PromptParameterException

import superprompt
from tests.utils import patched_prompt


def test_missing_message():
    with pytest.raises(PromptParameterException):
        superprompt.superprompt(
            [{"type": "confirm", "name": "continue", "default": True}]
        )


def test_missing_type():
    with pytest.raises(PromptParameterException):
        superprompt.superprompt(
            [
                {
                    "message": "Do you want to continue?",
                    "name": "continue",
                    "default": True,
                }
            ]
        )


def test_missing_name():
    with pytest.raises(PromptParameterException):
        superprompt.superprompt(
            [
                {
                    "type": "confirm",
                    "message": "Do you want to continue?",
                    "default": True,
                }
            ]
        )


def test_invalid_question_type():
    with pytest.raises(ValueError):
        superprompt.superprompt(
            [
                {
                    "type": "mytype",
                    "message": "Do you want to continue?",
                    "name": "continue",
                    "default": True,
                }
            ]
        )


def test_missing_dict_questions():
    with pytest.raises(ValueError):
        superprompt.superprompt(
            [
                {
                    "type": "dict",
                    "message": "Missing questions",
                    "name": "missing",
                }
            ]
        )


def test_missing_list_questions():
    with pytest.raises(ValueError):
        superprompt.superprompt(
            [
                {
                    "type": "list",
                    "message": "Missing questions",
                    "name": "missing",
                }
            ]
        )


def test_if_values():
    with pytest.raises(ValueError):
        superprompt.superprompt(
            [
                {
                    "type": "confirm",
                    "message": "Test",
                    "if": [lambda x: x],
                }
            ]
        )


def test_if_bad_value():
    with pytest.raises(ValueError):
        superprompt.superprompt(
            [
                {
                    "type": "confirm",
                    "message": "Test",
                    "if": "ack!",
                }
            ]
        )


def test_missing_print_message():
    """Test 'print' raises exception if missing 'message'"""
    with pytest.raises(PromptParameterException):
        superprompt.superprompt(
            [
                {
                    "name": "test",
                    "type": "print",
                }
            ]
        )


def test_print_no_name():
    """'print' type doesn't require a name so it
    should not throw PromptParameterException"""
    questions = [{"type": "print", "message": "Hello World"}]
    result = patched_prompt(questions, "")
    assert result == {}


def test_print_with_name():
    """'print' type should return {name: None} when name is provided"""
    questions = [{"name": "hello", "type": "print", "message": "Hello World"}]
    result = patched_prompt(questions, "")
    assert result == {"hello": None}
