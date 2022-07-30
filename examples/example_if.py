"""Demo `if` option for superprompt"""

from pprint import pprint

from superprompt import superprompt

questions = {
    "name": "ask_more_questions",
    "type": "confirm",
    "message": "Ask more questions?",
    "if": [
        True,
        [
            {"name": "question2", "type": "text", "message": "Enter some text:"},
            {"name": "question3", "type": "text", "message": "Enter some more text:"},
        ],
    ],
}

pprint(superprompt(questions))
