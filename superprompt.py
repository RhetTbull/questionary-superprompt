"""superprompt extension for questionary's prompt method"""

from typing import Any, Dict, Iterable, Mapping, Optional, Union

from pprint import pprint

from questionary import prompt, confirm
from questionary.constants import DEFAULT_KBI_MESSAGE


def superprompt(
    questions: Union[Dict[str, Any], Iterable[Mapping[str, Any]]],
    answers: Optional[Mapping[str, Any]] = None,
    patch_stdout: bool = False,
    true_color: bool = False,
    kbi_msg: str = DEFAULT_KBI_MESSAGE,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Prompt the user for input on all the questions.

    Catches keyboard interrupts and prints a message.

    See :func:`unsafe_prompt` for possible question configurations.

    Args:
        questions: A list of question configs representing questions to
                   ask. A question config may have the following options:

                   * type - The type of question.  Implements two additional types beyond those supported by prompt/unsafe_prompt:
                     "nested_list" and "nested_dict".  If type is "nested_list" or "nested_dict",
                     then "questions" option must also be set.  "nested_list" type returns a list of values from the questions
                     in "questions" while "nested_dict" type returns a dict of values for questions in "questions" where the key
                     is "name" of the question and the value is the answer to the question.

                   * name - An ID for the question (to identify it in the answers :obj:`dict`).

                   * when - Callable to conditionally show the question. This function
                     takes a :obj:`dict` representing the current answers.

                   * filter - Function that the answer is passed to. The return value of this
                     function is saved as the answer.

                   * if - List or Tuple in form [condition, nested_questions]; condition is a Callable to conditionally ask the nested_questions.
                     This function will be passed the answer to this question.

                   * questions - Union[Dict[str, Any], Iterable[Mapping[str, Any]]] of questions to ask for "nested_list" or "nested_dict" type.

                   * multiple - Union[bool, int], if True or positive int, allows multiple values for this question.
                     User will be prompted to enter additional values if True or will be prompted for exactly N values if multiple is int N.

                   * multiple_message - str, if passed, will be used as the message prompt when prompting user for additional values for
                     questions where "multiple" == True.

                   Additional options correspond to the parameter names for
                   particular question types.

        answers: Default answers.

        patch_stdout: Ensure that the prompt renders correctly if other threads
                      are printing to stdout.

        kbi_msg: The message to be printed on a keyboard interrupt.
        true_color: Use true color output.

        color_depth: Color depth to use. If ``true_color`` is set to true then this
                     value is ignored.

        type: Default ``type`` value to use in question config.
        filter: Default ``filter`` value to use in question config.
        name: Default ``name`` value to use in question config.
        when: Default ``when`` value to use in question config.
        default: Default ``default`` value to use in question config.
        kwargs: Additional options passed to every question.

    Returns:
        Dictionary of question answers.
    """
    if isinstance(questions, dict):
        questions = [questions]

    answers = dict(answers or {})

    for question_config in questions:
        question_config = dict(question_config)
        # get options from the question_config dict
        # some of the options are popped out of the dict because prompt() doesn't recognize them
        # questions is left in the dict and will be handled by recursive calls to superprompt
        name = question_config.get("name")
        _type = question_config.get("type")
        _if = question_config.pop("if", None)
        nested_questions = question_config.get("questions", None)
        multiple = question_config.pop("multiple", None)
        multiple_max = question_config.pop("multiple_max", 0)
        multiple_message = (
            question_config.pop("multiple_message", None)
            or question_config.get("message")
            or f"Add another value for {name}?"
        )

        # constraint checks
        if multiple_max and multiple_max < 1:
            raise ValueError(f"multiple_max must be a positive integer: {multiple_max}")

        if _type in ["nested_dict", "nested_list"] and not nested_questions:
            raise ValueError(
                "missing questions: questions are required when using type=nested_dict or type=nested_list"
            )

        if multiple and type(multiple) == int and multiple < 0:
            raise ValueError(
                f"multiple must be either bool or positive int: {multiple}"
            )

        if _if:
            if not isinstance(_if, (list, tuple)):
                raise ValueError(
                    "'if' value must be list or tuple in form [condition, questions]"
                )
            if not callable(_if[0]):
                raise ValueError(
                    "'if' condition needs to be a function not {type(_if[0])}"
                )

        if multiple:
            multiple_answers = []
            # repeat until told not to
            if type(multiple) == int:

                def condition(n):
                    return n < multiple  # pylint: disable=cell-var-from-loop

            else:

                def condition(n):  # pylint: disable=unused-argument
                    return True

            n = 0
            while condition(n):
                multiple_question = question_config.copy()
                answers = superprompt(
                    multiple_question,
                    answers,
                    patch_stdout,
                    true_color,
                    kbi_msg,
                    **kwargs,
                )
                multiple_answers.append(answers[name])
                n += 1
                if n == multiple_max:
                    break

                if multiple_max and not confirm(multiple_message).ask():
                    break

            answers[name] = multiple_answers
            continue

        if _type in ("nested_list", "nested_dict"):
            list_dict_questions = nested_questions
            list_dict_answers = {}
            list_dict_answers = superprompt(
                list_dict_questions,
                list_dict_answers,
                patch_stdout,
                true_color,
                kbi_msg,
                **kwargs,
            )
            if _type == "nested_list":
                answers[name] = [v for v in list_dict_answers.values()]
            else:
                answers[name] = list_dict_answers
            continue

        # ordinary question, call prompt
        # remove keys that prompt doesn't understand
        question_config.pop("questions", None)
        answers = prompt(
            question_config, answers, patch_stdout, true_color, kbi_msg, **kwargs
        )

        # handle "if" condition
        if _if:
            condition, nested_questions = _if
            try:
                if not condition(answers.get(name)):
                    continue
            except Exception as exception:
                raise ValueError(
                    f"Problem in 'if' check of " f"{name} question: {exception}"
                ) from exception
            answers = superprompt(
                nested_questions,
                answers,
                patch_stdout,
                true_color,
                kbi_msg,
                **kwargs,
            )

    return answers


if __name__ == "__main__":
    questions = [
        {
            "name": "burger",
            "type": "confirm",
            "message": "Would you like to order a burger?",
            # if: value, list --> if return value == value, then run prompt on list
            "if": [
                lambda x: x,
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
                        "type": "nested_dict",
                        "message": "What kind of toppings would you like?",
                        "questions": [
                            {
                                "name": "condiments",
                                "message": "Select your condiments:",
                                "type": "checkbox",
                                "choices": ["mustard", "mayonnaise", "green chiles"],
                            },
                            {
                                "name": "extras",
                                "message": "This message isn't shown (or needed)",
                                "type": "nested_list",
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
                                        "multiple_message": "Add another allergy?",
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
                        # if multiple, allows multiple values for this name
                        "multiple": True,  # <-- True to ask until user decides not to; any positive int n to ask exactly n times
                        "message": "Tell me about one of your favorite books",
                        "multiple_message": "Add another book?",  # <-- asked before repeating; if not set, just repeats the message
                        # if type == "list", then a list of prompts, also, type= "dict" returns a dict of name: value
                        "multiple_max": 3,  # <-- if passed, limits multiple to max values
                        "type": "nested_list",
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
