"""Test if option for superprompt"""

from tests.utils import KeyInputs, ask_with_patched_input, make_dict_style_asker

QUESTIONS_VALUE = {
    "type": "confirm",
    "name": "ask_more",
    "message": "Ask you more questions?",
    "if": [True, {"type": "text", "name": "some_text", "message": "enter some text"}],
}

QUESTIONS_LAMBDA = {
    "type": "confirm",
    "name": "ask_more",
    "message": "Ask you more questions?",
    "if": [
        lambda x: x,
        {"type": "text", "name": "some_text", "message": "enter some text"},
    ],
}


def test_if_conditional_value():
    """Test if option when True and value conditional is a value"""
    questions = make_dict_style_asker(QUESTIONS_VALUE)
    answers = "y" + "foo" + KeyInputs.ENTER
    result_dict = ask_with_patched_input(questions, answers)
    assert result_dict == {"ask_more": True, "some_text": "foo"}


def test_if_conditional_value():
    """Test if option when True and value conditional is a value"""
    questions = make_dict_style_asker(QUESTIONS_LAMBDA)
    answers = "y" + "foo" + KeyInputs.ENTER
    result_dict = ask_with_patched_input(questions, answers)
    assert result_dict == {"ask_more": True, "some_text": "foo"}


def test_if_false_conditional():
    """Test if option when conditional is False"""
    questions = make_dict_style_asker(QUESTIONS_LAMBDA)
    answers = "n" + KeyInputs.ENTER
    result_dict = ask_with_patched_input(questions, answers)
    assert result_dict == {"ask_more": False}
