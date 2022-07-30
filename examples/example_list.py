"""Demo `list` type for superprompt"""

from pprint import pprint

from superprompt import superprompt

questions = {
    "name": "list_values",
    "type": "list",
    "message": "message isn't needed for special list type",
    # every "list" type must include a "questions" option of questions to ask
    "questions": [
        {"name": "title", "type": "text", "message": "Enter book title:"},
        {"name": "author", "type": "text", "message": "Enter book author:"},
    ],
}

pprint(superprompt(questions))
