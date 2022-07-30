import pytest
import superprompt
from questionary.prompt import PromptParameterException


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
