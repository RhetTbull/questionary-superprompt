# questionary-superprompt

An extension to the python questionary package that provides additional features for the prompt method.

## Overview

This includes a single function, `superprompt()` who's signature is identical to `questionary.prompt()` but extends the vanilla `prompt()` to add nested prompts, repeated prompts to ask the same question multiple times, and an `if` function which allows nested prompts to be asked only if a given critiera is met.  `superprompt()` aims to be 100% backwards compatible with `prompt()`.

## Synopsis

### if option for questions

The `if` option asks additional questions if the answer to the previous question matches the if condition. The if condition may be a value or a `callable`. If it is a `callable`, the `callable` will be called with the answer to the previous question and should return `True` or `False`. If you need to ask multiple questions based on the value of a previous question, this is easier than using a `when` option in each subsequent question.

```python
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
            {"name": "question2", "type": "text", "message": "Enter some text"},
            {"name": "question3", "type": "text", "message": "Enter some more text"},
        ],
    ],
}

pprint(superprompt(questions))
```

```
$ python examples/example_if.py
? Ask more questions? Yes
? Enter some text Hello
? Enter some more text World
{'ask_more_questions': True, 'question2': 'Hello', 'question3': 'World'}

$ python examples/example_if.py
? Ask more questions? No
{'ask_more_questions': False}
```