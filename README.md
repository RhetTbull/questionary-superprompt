# questionary-superprompt

An extension to the python questionary package that provides additional features for the prompt method

## Overview

This includes a single function, `superprompt()` who's signature is identical to `questionary.prompt()` but extends the vanilla `prompt()` to add nested prompts, repeated prompts to ask the same question multiple times, and an `if` function which allows nested prompts to be asked only if a given critiera is met.  `superprompt()` aims to be 100% backwards compatible with `prompt()`.

