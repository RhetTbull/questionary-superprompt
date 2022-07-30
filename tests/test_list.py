"""Test list type for superprompt"""

from tests.utils import KeyInputs, ask_with_patched_input, make_dict_style_asker

QUESTIONS = {
    "type": "list",
    "name": "list_values",
    "message": "This doesn't matter",
    "questions": [
        {
            "name": "book-title",  # <-- name is not needed for "list", if provided, not used, just passes values
            "message": "What's the title?",
            "type": "text",
        },
        {
            "name": "book-author",
            "message": "Who's the author?",
            "type": "text",
        },
    ],
}


def test_list():
    """Test list type"""
    questions = make_dict_style_asker(QUESTIONS)
    answers = "Dune" + KeyInputs.ENTER + "Frank Herbert" + KeyInputs.ENTER
    result_dict = ask_with_patched_input(questions, answers)
    assert result_dict == {"list_values": ["Dune", "Frank Herbert"]}
