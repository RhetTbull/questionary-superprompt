"""Test list type for superprompt"""

from tests.utils import KeyInputs, ask_with_patched_input, make_dict_style_asker

QUESTIONS = {
    "type": "dict",
    "name": "dict_values",
    "message": "This doesn't matter",
    "questions": [
        {
            "name": "title",  # <-- will be dict key
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


def test_dict():
    """Test dict type"""
    questions = make_dict_style_asker(QUESTIONS)
    answers = "Dune" + KeyInputs.ENTER + "Frank Herbert" + KeyInputs.ENTER
    result_dict = ask_with_patched_input(questions, answers)
    assert result_dict == {"dict_values": {"title": "Dune", "author": "Frank Herbert"}}
