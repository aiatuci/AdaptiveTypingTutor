from string import ascii_letters, punctuation


# Set of characters that we want to record
ALLOWED_CHARS: set[str] = set(
    [p for p in punctuation] + [letters for letters in ascii_letters] + ['space', 'Return', 'BackSpace'] + [str(i) for i in range(10)]
    )


KEYSYM_TRANSLATION_TABLE = {
    'space': ' ',
    'Return': 'ENTER',
    'BackSpace': 'BACKSPACE',
}