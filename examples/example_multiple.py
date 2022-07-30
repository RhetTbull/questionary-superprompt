"""Demo `multiple` option for superprompt"""

from pprint import pprint

from questionary import print as qprint

from superprompt import superprompt

questions = {
    "name": "books",
    "type": "text",
    "message": "Name of a book you like:",
    "multiple": 3,  # <-- if multiple > 0, asks exactly multiple times
    "multiple_message": "Name of another book you like:",  # <-- used in place of `message` after the first question is asked
}
qprint("Ask for exactly 3 values (multiple=3)")
pprint(superprompt(questions))

questions = {
    "name": "books",
    "type": "text",
    "message": "Name of a book you like:",
    "multiple": -2,  # <-- if multiple < 0, asks up to abs(multiple) times
    "multiple_message": "Enter another book?",  # <-- used in place of `message` for the continuation prompt
}

qprint("Ask for up to 2 values (multiple=-2)")
pprint(superprompt(questions))
