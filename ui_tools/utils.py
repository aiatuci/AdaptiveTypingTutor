"""
Utility methods for the UI.
"""


from typing import Union, Iterable


def replace_words(words: Union[str, Iterable], replacement_dict: dict) -> Union[str, list]:
    """
    Replaces words in a string or as iterable with the values in a dictionary, if there's a match.
    Otherwise, return the original string.
    
    Returns a string or list of strings, depending on the input.
    """

    def replace_word(word: str) -> str:
        for key, value in replacement_dict.items():
            word = word.replace(key, value)

    if isinstance(words, str):
        return replace_words(words)

    if isinstance(words, Iterable):
        return [replace_word(word) for word in words]