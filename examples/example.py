from pprint import pprint

from superprompt import superprompt

if __name__ == "__main__":
    questions = [
        {
            "name": "burger",
            "type": "confirm",
            "message": "Would you like to order a burger?",
            # if: value, list --> if return value == value, then run prompt on list
            "if": [
                True,
                [
                    {
                        "name": "fries",
                        "message": "Would you like fries with that?",
                        "type": "confirm",
                    },
                    {
                        "name": "chili-fries",
                        "message": "Would you like chili on your fries?",
                        "type": "confirm",
                        "when": lambda x: x["fries"],
                    },
                    {
                        "name": "onion-rings",
                        "message": "Would you like onion rings?",
                        "type": "confirm",
                        "when": lambda x: not x["fries"],
                    },
                    {
                        "name": "toppings",
                        "type": "dict",
                        "message": "This message is not used or needed as the message for each dict question will be used.",
                        "questions": [
                            {
                                "name": "print_message",
                                "type": "print",
                                "message": "Toppings & Special Requests",
                                "style": "bold italic fg:darkred",
                            },
                            {
                                "name": "condiments",
                                "message": "Select your condiments:",
                                "type": "checkbox",
                                "choices": ["mustard", "mayonnaise", "green chiles"],
                            },
                            {
                                "name": "extras",
                                "message": "This message isn't shown (or needed)",
                                "type": "dict",
                                "questions": [
                                    {
                                        "name": "special_requests",
                                        "type": "text",
                                        "message": "List any special requests: ",
                                        "filter": lambda x: x.upper(),
                                    },
                                    {
                                        "name": "allergies",
                                        "type": "text",
                                        "message": "If you have a food allergy, list it here:",
                                        "multiple_message": "If you have another food allergy, list it here:",
                                        "multiple": 2,  # <-- ask for exactly 2 values
                                    },
                                ],
                            },
                        ],
                    },
                ],
            ],
        },
        {
            "name": "books",
            "type": "confirm",
            "message": "Would you like to tell me about some of your favorite books?",
            "if": [
                lambda x: x,
                [
                    {
                        "name": "books",  # <-- repeating the name means previous name value will be replaced by this new value
                        "message": "Not needed, see multiple_message",
                        # if multiple, allows multiple values for this name
                        "multiple": -3,  # <-- if < 0, will prompt for at most abs(multiple) values
                        "multiple_message": "Add another book?",  # <-- asked before repeating
                        # if type == "list", then a list of prompts, also, type= "dict" returns a dict of name: value
                        "type": "list",
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
                ],
            ],
        },
    ]
    print("\n\n")
    answers = superprompt(questions)
    pprint(answers)
