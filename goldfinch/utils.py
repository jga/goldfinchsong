"""Utilities module. Almost all **goldfinch** logic is handled by the
functions in this module. It's the workhorse of the package."""
import random
import re
from os import listdir
from os.path import isfile, join
import tweepy


def access_api(credentials):
    """
    Arguments:
        credentials (dict): Authentication and access credentials

    Returns:
        A tweepy API instance.
    """
    auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
    auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
    api = tweepy.API(auth)
    return api


def apply_abbreviations(text, abbreviations, maximum_length=117):
    """
    Abbreviates words until status text does not exceed the maximum length.

    Not all abbreviations are necessarily applied; the function iterates
    abbreviation-by-abbreviation, checking length after each substitution.

    Args:
        text (str): A tweet's status text.
        abbreviations (OrderedDict): An ``OrderedDict`` keyed to a word with its abbreviation as the value.
        maximum_length (int): Maximum character length.

    Returns:
        str: New status text
    """
    new_text = text
    for not_abbreviated, abbreviated in abbreviations.items():
        pattern = ''.join([r'\b', not_abbreviated, r'\b'])
        regex = re.compile(pattern)
        new_text = regex.sub(abbreviated, new_text)
        if len(new_text) <= maximum_length:
            return new_text
    return new_text


def assemble_elided_status(complete_words, elided_words):
    """
    Remixes the complete and elided words of a status text to match
    word original order.

    Args:
        complete_words (list): List of complete words in reverse order from original status text.
        elided_words (list): List of elided words in reverse order from original status text.

    Returns:
        str: The properly-ordered status.

    """
    elided_words.reverse()
    for elided_word in elided_words:
        complete_words.insert(0, elided_word)
    complete_words.reverse()
    return ' '.join(complete_words)


def apply_vowel_elision(text, maximum_length=117):
    """

    Removes a strings non-boundary vowels until it does not exceed the maximum character length.

    Args:
        text (str): A twitter status text.
        maximum_length (int): Maximum character length.

    Returns:
        str: Status text with whatever vowel elisions were necessary to meet length constraint.
    """
    words = text.split()
    words.reverse()
    elided_words = list()
    vowel_regex = re.compile(r'\B[aeiou]\B', re.IGNORECASE)
    while words:
        word = words.pop(0)
        elided_word = vowel_regex.sub('', word)
        elided_words.append(elided_word)
        complete_word_length = len(' '.join(words))
        elided_word_length = len(' '.join(elided_words))
        if (complete_word_length + elided_word_length) <= maximum_length:
            return assemble_elided_status(words, elided_words)
    return assemble_elided_status(words, elided_words)


def chop_words(text, maximum_length=117):
    """
    Deletes last word in a string until it does not exceed maximum length.

    Args:
        text (str): Status text.
        maximum_length (int): Maximum character length.

    Returns:
        str or ``None``

    """
    words = text.split()
    for i in range(len(words)):
        words.pop()
        chopped_text = ' '.join(words)
        if len(chopped_text) <= maximum_length:
            return chopped_text
    return None


def is_image_file(file_name):
    """
    Checks for ``.png``, ``.jpg``, ``.jgpeg``, ``.gif`` file extensions.

    Arguments:
        file_name (str): Image file name.

    Returns:
        bool: Returns ``True`` if the file name has image extension. ``False`` otherwise.
    """
    regex = re.compile(r"(.+)\.(png|jpg|jpeg|gif)$", re.IGNORECASE)
    result = regex.match(file_name)
    return True if result else False


def trim_file_extension(file_name):
    """
    Removes ``.png``, ``.jpg``, ``.jgpeg``, ``.gif`` file extensions.

    Arguments:
        file_name (str): Image file name.

    Returns:
        str: File name string without the image type extension.
    """
    regex = re.compile(r"(.+)\.(png|jpg|jpeg|gif)$", re.IGNORECASE)
    result = regex.match(file_name)
    return result.group(1)


def to_compact_text(candidate_text, maximum_length=117, text_conversions=None):
    """
    Transforms a text string so that its length is equal to or less than a
    designated maximum length.

    This is the sequence of transformations deployed:

    - Each text conversion is attempted; after each attempt, the length of
      the resulting text is checked and immediately returned if the transformed
      text does not exceed the maximum length.
    - Non-boundary vowels are removed sequentially from the last word until the first.
      A length check occurs after each word transformation and the text is immediately
      returned if does not exceed the maximum.
    - If the text is still too long, then words are deleted from last to first until
      the resulting text does not exceed the maximum length.

    Arguments:
        candidate_text (str): Original text before function processing.
        maximum_length (int): The maximum character length for the text.
        text_conversions (dict): Keys represent full-length versions of a word.
            If the string value paired with the key is an abbreviated form that may
            be used by the function in an attempt to reduce the length of the
            candidate text.

    Returns:
        str: A text string that shorter than the passed maximum length argument.

    """
    if len(candidate_text) <= maximum_length:
        return candidate_text
    else:
        compact_text = candidate_text
        compact_text = apply_abbreviations(compact_text, text_conversions, maximum_length)
        if len(compact_text) <= maximum_length:
            return compact_text
        else:
            compact_text = apply_vowel_elision(compact_text, maximum_length)
            if len(compact_text) <= maximum_length:
                return compact_text
            else:
                chopped_text = chop_words(compact_text, maximum_length)
                return chopped_text if chopped_text else ''


def extract_status_text(file_name, text_conversions, maximum_length=117):
    """

    An image link consumes 23 characters, leaving 117 for text.

    Args:
        file_name (str): An image file name. For example: ``selected_image.png``.
        text_conversions (dict): Keys represent full-length versions of a word.
            If the string value paired with the key is an abbreviated form that may
            be used by the function in an attempt to reduce the length of the
            candidate text.
        maximum_length (int): The maximum character length for the text.

    Returns:
        text (str): A string of text based on the file name.

    """
    text = trim_file_extension(file_name)
    text = text.replace('_', ' ')
    compact_text = to_compact_text(text, text_conversions=text_conversions,
                               maximum_length=maximum_length)
    return compact_text


def load_content(image_directory, text_conversions=None):
    """
    Generates content tuple after selecting random image from image directory.

    Args:
        image_directory (str): File path to image directory.
        text_conversions (dict): Keys represent full-length versions of a word.
            If the string value paired with the key is an abbreviated form that may
            be used by the function in an attempt to reduce the length of the
            candidate text.

    Returns:
        tuple or ``None``: A content tuple with image path and status text
            if an image file is available in image directory. ``None`` otherwise.

    """
    files = [file for file in listdir(image_directory) if isfile(join(image_directory, file))]
    selected_file = random.choice(files)
    if is_image_file(selected_file):
        with_full_path = join(image_directory, selected_file)
        text = extract_status_text(selected_file, text_conversions)
        content = (with_full_path, text)
        return content
    else:
        return None

