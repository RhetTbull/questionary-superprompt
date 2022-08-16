"""superprompt extension for questionary's prompt method"""

from typing import Any, Dict, Iterable, Mapping, Optional, Union

from questionary import confirm, prompt
from questionary.constants import DEFAULT_KBI_MESSAGE
from questionary.prompt import PromptParameterException
from questionary.prompts.common import print_formatted_text

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
                     "list" and "dict".  If type is "list" or "dict",
                     then "questions" option must also be set.  "list" type returns a list of values from the questions
                     in "questions" while "dict" type returns a dict of values for questions in "questions" where the key
                     is "name" of the question and the value is the answer to the question.

                   * name - An ID for the question (to identify it in the answers :obj:`dict`).

                   * when - Callable to conditionally show the question. This function
                     takes a :obj:`dict` representing the current answers.

                   * filter - Function that the answer is passed to. The return value of this
                     function is saved as the answer.

                   * if - List or Tuple in form [condition, nested_questions]; condition is a Callable or value to conditionally ask the nested_questions.
                     If a callable, the function will be passed the answer to this question;
                     if any other value, the answer to the question will be compared to this value.

                   * questions - Union[Dict[str, Any], Iterable[Mapping[str, Any]]] of questions to ask for "list" or "dict" type.

                   * multiple - int, if positive int N, the user will be prompted for exactly N values for this question.
                     If negative, user will be be prompted to enter multiple values, but at most -N values.

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
        nested_questions = question_config.get("questions")
        multiple = question_config.pop("multiple", None)
        multiple_message = question_config.pop(
            "multiple_message", None
        ) or question_config.get("message")

        # constraint checks
        if _type in ["dict", "list"] and not nested_questions:
            raise PromptParameterException("questions")

        if _if and not isinstance(_if, (list, tuple)):
            raise ValueError(
                "'if' value must be list or tuple in form [condition, questions]"
            )

        if multiple:
            # handle multiple questions (where question is asked repeatedly)
            # multiple > 0 == ask for exactly multiple values
            # multiple < 0 == ask for no more than multiple values
            multiple_answers = []
            multiple_question = question_config.copy()

            # ask for first answer
            answers = superprompt(
                multiple_question,
                answers,
                patch_stdout,
                true_color,
                kbi_msg,
                **kwargs,
            )
            multiple_answers.append(answers[name])

            # use multiple_message on subsequent prompts
            if multiple > 0:
                multiple_question["message"] = multiple_message

            n = 1
            while n < abs(multiple):
                if multiple < 0 and not confirm(multiple_message).ask():
                    break
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

            answers[name] = multiple_answers
            continue

        if _type in ("list", "dict"):
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
            if _type == "list":
                answers[name] = [v for v in list_dict_answers.values()]
            else:
                answers[name] = list_dict_answers
            continue

        # handle 'print' type
        if _type == "print":
            try:
                message = _kwargs.pop("message")
            except KeyError as exception:
                raise PromptParameterException("message") from exception

            # questions can take 'input' arg but print_formatted_text does not
            # Remove 'input', if present, to avoid breaking during tests
            kwargs.pop("input", None)

            print_formatted_text(message, **kwargs)
            if name:
                answers[name] = None
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
                if callable(condition):
                    if not condition(answers.get(name)):
                        continue
                elif answers.get(name) != condition:
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
