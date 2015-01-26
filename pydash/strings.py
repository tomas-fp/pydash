# -*- coding: utf-8 -*-
"""String functions.

.. versionadded:: 1.1.0
"""

import re
import unicodedata

import pydash as pyd
from .helpers import NoValue
from ._compat import (
    html_unescape,
    iteritems,
    parse_qsl,
    text_type,
    urlencode,
    urlsplit,
    urlunsplit,
    _range
)


__all__ = (
    'camel_case',
    'capitalize',
    'chop',
    'chop_right',
    'chars',
    'class_case',
    'clean',
    'count_substr',
    'deburr',
    'decapitalize',
    'ends_with',
    'ensure_ends_with',
    'ensure_starts_with',
    'escape',
    'escape_reg_exp',
    'escape_re',
    'explode',
    'has_substr',
    'human_case',
    'implode',
    'insert_substr',
    'join',
    'js_match',
    'js_replace',
    'kebab_case',
    'lines',
    'number_format',
    'pad',
    'pad_left',
    'pad_right',
    'predecessor',
    'prune',
    'quote',
    're_replace',
    'repeat',
    'replace',
    'separator_case',
    'series_phrase',
    'series_phrase_serial',
    'slugify',
    'snake_case',
    'split',
    'starts_with',
    'strip_tags',
    'substr_left',
    'substr_left_end',
    'substr_right',
    'substr_right_end',
    'successor',
    'surround',
    'swap_case',
    'title_case',
    'trim',
    'trim_left',
    'trim_right',
    'trunc',
    'truncate',
    'underscore_case',
    'unescape',
    'unquote',
    'url',
    'words',
)


HTML_ESCAPES = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '`': '&#96;'
}

DEBURRED_LETTERS = {
    '\xC0': 'A',
    '\xC1': 'A',
    '\xC2': 'A',
    '\xC3': 'A',
    '\xC4': 'A',
    '\xC5': 'A',
    '\xE0': 'a',
    '\xE1': 'a',
    '\xE2': 'a',
    '\xE3': 'a',
    '\xE4': 'a',
    '\xE5': 'a',
    '\xC7': 'C',
    '\xE7': 'c',
    '\xD0': 'D',
    '\xF0': 'd',
    '\xC8': 'E',
    '\xC9': 'E',
    '\xCA': 'E',
    '\xCB': 'E',
    '\xE8': 'e',
    '\xE9': 'e',
    '\xEA': 'e',
    '\xEB': 'e',
    '\xCC': 'I',
    '\xCD': 'I',
    '\xCE': 'I',
    '\xCF': 'I',
    '\xEC': 'i',
    '\xED': 'i',
    '\xEE': 'i',
    '\xEF': 'i',
    '\xD1': 'N',
    '\xF1': 'n',
    '\xD2': 'O',
    '\xD3': 'O',
    '\xD4': 'O',
    '\xD5': 'O',
    '\xD6': 'O',
    '\xD8': 'O',
    '\xF2': 'o',
    '\xF3': 'o',
    '\xF4': 'o',
    '\xF5': 'o',
    '\xF6': 'o',
    '\xF8': 'o',
    '\xD9': 'U',
    '\xDA': 'U',
    '\xDB': 'U',
    '\xDC': 'U',
    '\xF9': 'u',
    '\xFA': 'u',
    '\xFB': 'u',
    '\xFC': 'u',
    '\xDD': 'Y',
    '\xFD': 'y',
    '\xFF': 'y',
    '\xC6': 'Ae',
    '\xE6': 'ae',
    '\xDE': 'Th',
    '\xFE': 'th',
    '\xDF': 'ss',
    '\xD7': ' ',
    '\xF7': ' '
}

# Use Javascript style regex to make Lo-Dash compatibility easier.
RE_WORDS = '/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*)|[A-Z]?[a-z]+[0-9]*|[A-Z]+|[0-9]+/g'
RE_LATIN1 = '/[\xC0-\xFF]/g'


def camel_case(text):
    """Converts `text` to camel case.

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to camel case.

    .. versionadded:: 1.1.0
    """
    text = ''.join(word.title() for word in words(text))
    return text[:1].lower() + text[1:]


def capitalize(text, lower_rest=True):
    """Capitalizes the first character of `text`.

    Args:
        text (str): String to capitalize.
        lower_rest (bool, optional): Whether to cast rest of string to lower
            case. Defaults to ``True``.

    Returns:
        str: Capitalized string.

    .. versionadded:: 1.1.0

    .. versionchanged:: 3.0.0
        Added `lower_rest` option.
    """
    text = pyd.to_string(text)
    return (text.capitalize() if lower_rest
            else text[:1].upper() + text[1:])


def chars(text):
    """Split `text` into a list of single characters.

    Args:
        text (str): String to split up.

    Returns:
        list: List of individual characters.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    return list(text)


def chop(text, step):
    """Break up `text` into intervals of length `step`.

    Args:
        text (str): String to chop.
        step (int): Interval to chop `text`.

    Returns:
        list: List of chopped characters.
              If `text` is `None` an empty list is returned.

    .. versionadded:: 3.0.0
    """
    if text is None:
        return []
    text = pyd.to_string(text)
    if step <= 0:
        chopped = [text]
    else:
        chopped = [text[i:i + step] for i in _range(0, len(text), step)]
    return chopped


def chop_right(text, step):
    """Like :func:`chop` except `text` is chopped from right.

    Args:
        text (str): String to chop.
        step (int): Interval to chop `text`.

    Returns:
        list: List of chopped characters.

    .. versionadded:: 3.0.0
    """
    if text is None:
        return []
    text = pyd.to_string(text)
    if step <= 0:
        chopped = [text]
    else:
        text_len = len(text)
        chopped = [text[-(i + step):text_len - i]
                   for i in _range(0, text_len, step)][::-1]
    return chopped


def class_case(text):
    """Like :func:`camel_case` except the first letter is capitalized.

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to class case.

    .. versionadded:: 3.0.0
    """
    return capitalize(camel_case(text), lower_rest=False)


def clean(text):
    """Trim and replace multiple spaces with a single space.

    Args:
        text (str): String to clean.

    Returns:
        str: Cleaned string.

    ..versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    return ' '.join(pyd.compact(text.split()))


def count_substr(text, subtext):
    """Count the occurrences of `subtext` in `text`.

    Args:
        text (str): Source string to count from.
        subtext (str): String to count.

    Returns:
        int: Number of occurrences of `subtext` in `text`.

    ..versionadded:: 3.0.0
    """
    if text is None or subtext is None:
        return 0
    text = pyd.to_string(text)
    subtext = pyd.to_string(subtext)
    return text.count(subtext)


def deburr(text):
    """Deburrs `text` by converting latin-1 supplementary letters to basic
    latin letters.

    Args:
        text (str): String to deburr.

    Returns:
        str: Deburred string.

    .. versionadded:: 2.0.0
    """
    text = pyd.to_string(text)
    return js_replace(RE_LATIN1,
                      text,
                      lambda match: DEBURRED_LETTERS.get(match.group(),
                                                         match.group()))


def decapitalize(text):
    """Decaptitalizes the first character of `text`.

    Args:
        text (str): String to decapitalize.

    Returns:
        str: Decapitalized string.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    return text[:1].lower() + text[1:]


def ends_with(text, target, position=None):
    """Checks if `text` ends with a given target string.

    Args:
        text (str): String to check.
        target (str): String to check for.
        position (int, optional): Position to search from. Defaults to
            end of `text`.

    Returns:
        bool: Whether `text` ends with `target`.

    .. versionadded:: 1.1.0
    """
    target = pyd.to_string(target)
    text = pyd.to_string(text)

    if position is None:
        position = len(text)

    return text[:position].endswith(target)


def ensure_ends_with(text, suffix):
    """Append a given suffix to a string, but only if the source string does
    not end with that suffix.

    Args:
        text (str): Source string to append `suffix` to.
        suffix (str): String to append to the source string if the source
            string does not end with `suffix`.

    Returns:
        str: source string possibly extended by `suffix`.

    .. versionadded:: 2.4.0
    """
    text = pyd.to_string(text)
    suffix = pyd.to_string(suffix)
    return text if text.endswith(suffix) else '{0}{1}'.format(text, suffix)


def ensure_starts_with(text, prefix):
    """Prepend a given prefix to a string, but only if the source string does
    not start with that prefix.

    Args:
        text (str): Source string to prepend `prefix` to.
        suffix (str): String to prepend to the source string if the source
            string does not start with `prefix`.

    Returns:
        str: source string possibly prefixed by `prefix`

    .. versionadded:: 2.4.0
    """
    text = pyd.to_string(text)
    prefix = pyd.to_string(prefix)
    return text if text.startswith(prefix) else '{1}{0}'.format(text, prefix)


def escape(text):
    r"""Converts the characters ``&``, ``<``, ``>``, ``"``, ``'``, and ``\``` in
    `text` to their corresponding HTML entities.

    Args:
        text (str): String to escape.

    Returns:
        str: HTML escaped string.

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
        Moved function to Strings module.
    """
    text = pyd.to_string(text)
    # NOTE: Not using _compat.html_escape because Lo-Dash escapes certain chars
    # differently (e.g. "'" isn't escaped by html_escape() but is by Lo-Dash).
    return ''.join(HTML_ESCAPES.get(char, char) for char in text)


def escape_reg_exp(text):
    """Escapes the RegExp special characters in `text`.

    Args:
        text (str): String to escape.

    Returns:
        str: RegExp escaped string.

    See Also:
        - :func:`escape_reg_exp` (main definition)
        - :func:`escape_re` (alias)

    .. versionadded:: 1.1.0
    """
    text = pyd.to_string(text)
    return re.escape(text)


escape_re = escape_reg_exp


def has_substr(text, subtext):
    """Returns whether `subtext` is included in `text`.

    Args:
        text (str): String to search.
        subtext (str): String to search for.

    Returns:
        bool: Whether `subtext` is found in `text`.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    subtext = pyd.to_string(subtext)
    return text.find(subtext) >= 0


def human_case(text):
    """Converts `text` to human case which has only the first letter
    capitalized and each word separated by a space.

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to human case.

    .. versionadded:: 3.0.0
    """
    return (pyd.chain(text)
            .snake_case()
            .re_replace('_id$', '')
            .replace('_', ' ')
            .capitalize()
            .value())


def insert_substr(text, index, subtext):
    """Insert `subtext` in `text` starting at position `index`.

    Args:
        text (str): String to add substring to.
        index (int): String index to insert into.
        subtext (str): String to insert.

    Returns:
        str: Modified string.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    subtext = pyd.to_string(subtext)
    return text[:index] + subtext + text[index:]


def join(array, separator=''):
    """Joins an iterable into a string using `separator` between each element.

    Args:
        array (iterable): Iterable to implode.
        separator (str, optional): Separator to using when joining. Defaults to
            ``''``.

    Returns:
        str: Joined string

    See Also:
        - :func:`join` (main definition)
        - :func:`implode` (alias)

    .. versionadded:: 2.0.0

    .. versionchanged:: 3.0.0
        Modified :func:`implode` to have :func:`join` as main definition and
        :func:`implode` as alias.
    """
    return pyd.to_string(separator).join(pyd.map_(array or (), pyd.to_string))


implode = join


def js_match(reg_exp, text):
    """Return list of matches using Javascript style regular expression.

    Args:
        reg_exp (str): Javascript style regular expression.
        text (str): String to evaluate.

    Returns:
        list: List of matches.

    .. versionadded:: 2.0.0
    """
    text = pyd.to_string(text)
    return js_to_py_re_find(reg_exp)(text)


def js_replace(reg_exp, text, repl):
    """Replace `text` with `repl` using Javascript style regular expression to
    find matches.

    Args:
        reg_exp (str): Javascript style regular expression.
        text (str): String to evaluate.
        repl (str): Replacement string.

    Returns:
        str: Modified string.

    .. versionadded:: 2.0.0
    """
    text = pyd.to_string(text)
    if not pyd.is_function(repl):
        repl = pyd.to_string(repl)
    return js_to_py_re_replace(reg_exp)(text, repl)


def kebab_case(text):
    """Converts `text` to kebab case (a.k.a. spinal case).

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to kebab case.

    .. versionadded:: 1.1.0
    """
    return separator_case(text, '-')


def lines(text):
    """Split lines in `text` into an array.

    Args:
        text (str): String to split.

    Returns:
        list: String split by lines.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    return text.splitlines()


def number_format(number, scale=0, decimal_separator='.', order_separator=','):
    """Format a number to scale with custom decimal and order separators.

    Args:
        number (int|float): Number to format.
        scale (int, optional): Number of decimals to include. Defaults to
            ``0``.
        decimal_separator (str, optional): Decimal separator to use. Defaults
            to ``'.'``.
        order_separator (str, optional): Order separator to use. Defaults to
            ``','``.

    Returns:
        str: Formatted number as string.

    .. versionadded:: 3.0.0
    """
    # Create a string formatter which converts number to the appropriately
    # scaled representation.
    fmt = '{{0:.{0:d}f}}'.format(scale)

    try:
        num_parts = fmt.format(number).split('.')
    except ValueError:
        text = ''
    else:
        int_part = num_parts[0]
        dec_part = (num_parts + [''])[1]

        # Reverse the integer part, chop it into groups of 3, join on
        # `order_separator`, and then unreverse the string.
        int_part = order_separator.join(chop(int_part[::-1], 3))[::-1]

        text = decimal_separator.join(pyd.compact([int_part, dec_part]))

    return text


def pad(text, length, chars=' '):
    """Pads `text` on the left and right sides if it is shorter than the
    given padding length. The `chars` string may be truncated if the number of
    padding characters can't be evenly divided by the padding length.

    Args:
        text (str): String to pad.
        length (int): Amount to pad.
        chars (str, optional): Characters to pad with. Defaults to ``" "``.

    Returns:
        str: Padded string.

    .. versionadded:: 1.1.0
    """
    # pylint: disable=redefined-outer-name
    text = pyd.to_string(text)
    text_len = len(text)
    length = max((length, text_len))

    padding = (length - text_len)
    left_pad = padding // 2
    right_pad = padding - left_pad

    text = repeat(chars, left_pad) + text + repeat(chars, right_pad)

    if len(text) > length:
        # This handles cases when `chars` is more than one character.
        text = text[left_pad:-right_pad]

    return text


def pad_left(text, length, chars=' '):
    """Pads `text` on the left side if it is shorter than the given padding
    length. The `chars` string may be truncated if the number of padding
    characters can't be evenly divided by the padding length.

    Args:
        text (str): String to pad.
        length (int): Amount to pad.
        chars (str, optional): Characters to pad with. Defaults to ``" "``.

    Returns:
        str: Padded string.

    .. versionadded:: 1.1.0
    """
    # pylint: disable=redefined-outer-name
    text = pyd.to_string(text)
    length = max((length, len(text)))
    return (repeat(chars, length) + text)[-length:]


def pad_right(text, length, chars=' '):
    """Pads `text` on the right side if it is shorter than the given padding
    length. The `chars` string may be truncated if the number of padding
    characters can't be evenly divided by the padding length.

    Args:
        text (str): String to pad.
        length (int): Amount to pad.
        chars (str, optional): Characters to pad with. Defaults to ``" "``.

    Returns:
        str: Padded string.

    .. versionadded:: 1.1.0
    """
    # pylint: disable=redefined-outer-name
    text = pyd.to_string(text)
    length = max((length, len(text)))
    return (text + repeat(chars, length))[:length]


def predecessor(char):
    """Return the predecessor character of `char`.

    Args:
        char (str): Character to find the predecessor of.

    Returns:
        str: Predecessor character.

    .. versionadded:: 3.0.0
    """
    char = pyd.to_string(char)
    return chr(ord(char) + 1)


def prune(text, length=0, omission='...'):
    """Like :func:`truncate` except it ensures that the pruned string doesn't
    exceed the original length, i.e., it avoids half-chopped words when
    truncating. If the pruned text + `omission` text is longer than the
    original text, then the original text is returned.

    Args:
        text (str): String to prune.
        length (int, optional): Target prune length. Defaults to ``0``.
        omission (str, optional): Omission text to append to the end of the
            pruned string. Defaults to ``'...'``.

    Returns:
        str: Pruned string.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    text_len = len(text)
    omission_len = len(omission)

    if text_len < (length + omission_len):
        return text

    # Replace non-alphanumeric chars with whitespace.
    def repl(match):  # pylint: disable=missing-docstring
        char = match.group(0)
        return ' ' if char.upper() == char.lower() else char

    subtext = re_replace(text[:length + 1], r'.(?=\W*\w*$)', repl)

    if re.match(r'\w\w', subtext[-2:]):
        # Last two characters are alphanumeric. Remove last "word" from end of
        # string so that we prune to the next whole word.
        subtext = re_replace(subtext, r'\s*\S+$', '')
    else:
        # Last character (at least) is whitespace. So remove that character as
        # well as any other whitespace.
        subtext = subtext[:-1].rstrip()

    subtext_len = len(subtext)

    # Only add omission text if doing so will result in a string that is
    # equal two or smaller in length than the original.
    if (subtext_len + omission_len) <= text_len:
        text = text[:subtext_len] + omission

    return text


def quote(text, quote_char='"'):
    """Quote a string with another string.

    Args:
        text (str): String to be quoted.
        quote_char (str, optional): the quote character. Defaults to ``"``.

    Returns:
        str: the quoted string.

    .. versionadded:: 2.4.0
    """
    return surround(text, quote_char)


def re_replace(text, pattern, repl, ignore_case=False, count=0):
    """Replace occurrences of regex `pattern` with `repl` in `text`.
    Optionally, ignore case when replacing. Optionally, set `count` to limit
    number of replacements.

    Args:
        text (str): String to replace.
        pattern (str): String pattern to find and replace.
        repl (str): String to substitute `pattern` with.
        ignore_clase (bool, optional): Whether to ignore case when replacing.
            Defaults to ``False``.
        count (int, optional): Maximum number of occurrences to replace.
            Defaults to ``0`` which replaces all.

    Returns:
        str: Replaced string.

    .. versionadded:: 3.0.0
    """
    return (
        replace(
            text, pattern, repl, ignore_case=ignore_case, count=count,
            escape=False
        ) if pattern is not None else pyd.to_string(text)
    )


def repeat(text, n=0):
    """Repeats the given string `n` times.

    Args:
        text (str): String to repeat.
        n (int, optional): Number of times to repeat the string.

    Returns:
        str: Repeated string.

    .. versionadded:: 1.1.0
    """
    return pyd.to_string(text) * int(n)


def replace(text, pattern, repl, ignore_case=False, count=0, escape=True):
    """Replace occurrences of `pattern` with `repl` in `text`. Optionally,
    ignore case when replacing. Optionally, set `count` to limit number of
    replacements.

    Args:
        text (str): String to replace.
        pattern (str): String pattern to find and replace.
        repl (str): String to substitute `pattern` with.
        ignore_clase (bool, optional): Whether to ignore case when replacing.
            Defaults to ``False``.
        count (int, optional): Maximum number of occurrences to replace.
            Defaults to ``0`` which replaces all.
        escape (bool, optional): Whether to escape `pattern` when searching.
            This is needed if a literal replacement is desired when `pattern`
            may contain special regular expression characters. Defaults to
            ``True``.

    Returns:
        str: Replaced string.

    .. versionadded:: 3.0.0
    """
    # pylint: disable=redefined-outer-name
    text = pyd.to_string(text)

    if pattern is None:
        return text

    pattern = pyd.to_string(pattern)

    if escape:
        pattern = re.escape(pattern)

    if not pyd.is_function(repl):
        repl = pyd.to_string(repl)

    flags = re.IGNORECASE if ignore_case else 0

    # NOTE: Can't use `flags` argument to re.sub in Python 2.6 so have to use
    # this version instead.
    return re.compile(pattern, flags=flags).sub(repl, text, count=count)


def separator_case(text, separator):
    """Splits `text` on words and joins with `separator`.

    Args:
        text (str): String to convert.
        separator (str): Separator to join words with.

    Returns:
        str: Converted string.

    .. versionadded:: 3.0.0
    """
    return separator.join(word.lower()
                          for word in words(text) if word)


def series_phrase(items, separator=', ', last_separator=' and ', serial=False):
    """Join items into a grammatical series phrase, e.g., ``"item1, item2,
    item3 and item4"``.

    Args:
        items (list): List of string items to join.
        separator (str, optional): Item separator. Defaults to ``', '``.
        last_separator (str, optional): Last item separator. Defaults to
            ``' and '``.
        serial (bool, optional): Whether to include `separator` with
            `last_separator` when number of items is greater than 2. Defaults
            to ``False``.

    Returns:
        str: Joined string.

    .. versionadded:: 3.0.0
    """
    items = pyd.chain(items).map(pyd.to_string).compact().value()
    item_count = len(items)

    separator = pyd.to_string(separator)
    last_separator = pyd.to_string(last_separator)

    if item_count > 2 and serial:
        last_separator = separator.rstrip() + last_separator

    if item_count >= 2:
        items = items[:-2] + [last_separator.join(items[-2:])]

    return separator.join(items)


def series_phrase_serial(items, separator=', ', last_separator=' and '):
    """Join items into a grammatical series phrase using a serial separator,
    e.g., ``"item1, item2, item3, and item4"``.

    Args:
        items (list): List of string items to join.
        separator (str, optional): Item separator. Defaults to ``', '``.
        last_separator (str, optional): Last item separator. Defaults to
            ``' and '``.

    Returns:
        str: Joined string.

    .. versionadded:: 3.0.0
    """
    return series_phrase(items, separator, last_separator, serial=True)


def slugify(text, separator='-'):
    """Convert `text` into an ASCII slug which can be used safely in URLs.
    Incoming `text` is converted to unicode and noramlzied using the ``NFKD``
    form. This results in some accented characters being converted to their
    ASCII "equivalent" (e.g. ``é`` is converted to ``e``). Leading and trailing
    whitespace is trimmed and any remaining whitespace or other special
    characters without an ASCII equivalent are replaced with ``-``.

    Args:
        text (str): String to slugify.
        separator (str, optional): Separator to use. Defaults to ``'-'``.

    Returns:
        str: Slugified string.

    .. versionadded:: 3.0.0
    """
    normalized = (unicodedata.normalize('NFKD', text_type(pyd.to_string(text)))
                  .encode('ascii', 'ignore')
                  .decode('utf8'))

    return separator_case(normalized, separator)


def snake_case(text):
    """Converts `text` to snake case.

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to snake case.

    See Also:
        - :func:`snake_case` (main definition)
        - :func:`underscore_case` (alias)

    .. versionadded:: 1.1.0
    """
    return separator_case(text, '_')


underscore_case = snake_case


def split(text, separator=NoValue):
    """Splits `text` on `separator`. If `separator` not provided, then `text`
    is split on whitespace. If `separator` is falsey, then `text` is split on
    every character.

    Args:
        text (str): String to explode.
        separator (str, optional): Separator string to split on. Defaults to
            ``NoValue``.

    Returns:
        list: Split string.

    See Also:
        - :func:`split` (main definition)
        - :func:`explode` (alias)

    .. versionadded:: 2.0.0

    .. versionchanged:: 3.0.0
        Changed `separator` default to ``NoValue`` and supported splitting on
        whitespace by default.
    """
    text = pyd.to_string(text)

    if separator is NoValue:
        ret = text.split()
    elif separator:
        ret = text.split(separator)
    else:
        ret = chars(text)

    return ret


explode = split


def starts_with(text, target, position=0):
    """Checks if `text` starts with a given target string.

    Args:
        text (str): String to check.
        target (str): String to check for.
        position (int, optional): Position to search from. Defaults to
            beginning of `text`.

    Returns:
        bool: Whether `text` starts with `target`.

    .. versionadded:: 1.1.0
    """
    text = pyd.to_string(text)
    target = pyd.to_string(target)
    return text[position:].startswith(target)


def strip_tags(text):
    """Removes all HTML tags from `text`.

    Args:
        text (str): String to strip.

    Returns:
        str: String without HTML tags.

    .. versionadded:: 3.0.0
    """
    return re_replace(text, r'<\/?[^>]+>', '')


def substr_left(text, subtext):
    """Searches `text` from left-to-right for `subtext` and returns a substring
    consisting of the characters in `text` that are to the left of `subtext` or
    all string if no match found.

    Args:
        text (str): String to partition.
        subtext (str): String to search for.

    Returns:
        str: Substring to left of `subtext`.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    return text.partition(subtext)[0] if subtext else text


def substr_left_end(text, subtext):
    """Searches `text` from right-to-left for `subtext` and returns a substring
    consisting of the characters in `text` that are to the left of `subtext`
    or all string if no match found.

    Args:
        text (str): String to partition.
        subtext (str): String to search for.

    Returns:
        str: Substring to left of `subtext`.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    return text.rpartition(subtext)[0] or text if subtext else text


def substr_right(text, subtext):
    """Searches `text` from right-to-left for `subtext` and returns a substring
    consisting of the characters in `text` that are to the right of `subtext`
    or all string if no match found.

    Args:
        text (str): String to partition.
        subtext (str): String to search for.

    Returns:
        str: Substring to right of `subtext`.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    return text.partition(subtext)[2] or text if subtext else text


def substr_right_end(text, subtext):
    """Searches `text` from left-to-right for `subtext` and returns a substring
    consisting of the characters in `text` that are to the right of `subtext`
    or all string if no match found.

    Args:
        text (str): String to partition.
        subtext (str): String to search for.

    Returns:
        str: Substring to right of `subtext`.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    return text.rpartition(subtext)[2] if subtext else text


def successor(char):
    """Return the successor character of `char`.

    Args:
        char (str): Character to find the successor of.

    Returns:
        str: Successor character.

    .. versionadded:: 3.0.0
    """
    char = pyd.to_string(char)
    return chr(ord(char) - 1)


def surround(text, wrapper):
    """Surround a string with another string.

    Args:
        text (str): String to surround with `wrapper`.
        wrapper (str): String by which `text` is to be surrounded.

    Returns:
        str: Surrounded string.

    .. versionadded:: 2.4.0
    """
    return '{1}{0}{1}'.format(pyd.to_string(text), pyd.to_string(wrapper))


def swap_case(text):
    """Swap case of `text` characters.

    Args:
        text (str): String to swap case.

    Returns:
        str: String with swapped case.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    return text.swapcase()


def title_case(text):
    """Convert `text` to title case.

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to title case.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)
    # NOTE: Can't use text.title() since it doesn't handle apostrophes.
    return ' '.join(word.capitalize() for word in re.split(' ', text))


def trim(text, chars=None):
    """Removes leading and trailing whitespace or specified characters from
    `text`.

    Args:
        text (str): String to trim.
        chars (str, optional): Specific characters to remove.

    Returns:
        str: Trimmed string.

    .. versionadded:: 1.1.0
    """
    # pylint: disable=redefined-outer-name
    text = pyd.to_string(text)
    return text.strip(chars)


def trim_left(text, chars=None):
    """Removes leading  whitespace or specified characters from `text`.

    Args:
        text (str): String to trim.
        chars (str, optional): Specific characters to remove.

    Returns:
        str: Trimmed string.

    .. versionadded:: 1.1.0
    """
    # pylint: disable=redefined-outer-name
    text = pyd.to_string(text)
    return text.lstrip(chars)


def trim_right(text, chars=None):
    """Removes trailing whitespace or specified characters from `text`.

    Args:
        text (str): String to trim.
        chars (str, optional): Specific characters to remove.

    Returns:
        str: Trimmed string.

    .. versionadded:: 1.1.0
    """
    # pylint: disable=redefined-outer-name
    text = pyd.to_string(text)
    return text.rstrip(chars)


def truncate(text, length=30, omission='...', separator=None):
    """Truncates `text` if it is longer than the given maximum string length.
    The last characters of the truncated string are replaced with the omission
    string which defaults to ``...``.

    Args:
        text (str): String to truncate.
        length (int, optional): Maximum string length. Defaults to ``30``.
        omission (str, optional): String to indicate text is omitted.
        separator (mixed, optional): Separator pattern to truncate to.

    Returns:
        str: Truncated string.

    See Also:
        - :func:`truncate` (main definition)
        - :func:`trunc` (alias)

    .. versionadded:: 1.1.0

    .. versionchanged:: 3.0.0
        Made :func:`truncate` main function definition and added :func:`trunc`
        as alias.
    """
    text = pyd.to_string(text)

    if len(text) <= length:
        return text

    omission_len = len(omission)
    text_len = length - omission_len
    text = text[:text_len]

    trunc_len = len(text)

    if pyd.is_string(separator):
        trunc_len = text.rfind(separator)
    elif pyd.is_re(separator):
        last = None
        for match in separator.finditer(text):
            last = match

        if last is not None:
            trunc_len = last.start()

    return text[:trunc_len] + omission


trunc = truncate


def unescape(text):
    """The inverse of :func:`escape`. This method converts the HTML entities
    ``&amp;``, ``&lt;``, ``&gt;``, ``&quot;``, ``&#39;``, and ``&#96;`` in
    `text` to their corresponding characters.

    Args:
        text (str): String to unescape.

    Returns:
        str: HTML unescaped string.

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
        Moved to Strings module.
    """
    text = pyd.to_string(text)
    return html_unescape(text)


def unquote(text, quote_char='"'):
    """Unquote `text` by removing `quote_char` if `text` begins and ends with
    it.

    Args:
        text (str): String to unquote.

    Returns:
        str: Unquoted string.

    .. versionadded:: 3.0.0
    """
    text = pyd.to_string(text)

    if text[:1] == quote_char and text[-1] == quote_char:
        text = text[1:-1]

    return text


def url(*paths, **params):
    """Combines a series of URL paths into a single URL. Optionally, pass in
    keyword arguments to append query parameters.

    Args:
        paths (str): URL paths to combine.

    Keyword Args:
        params (str, optional): Query parameters.

    Returns:
        str: URL string.

    .. versionadded:: 2.2.0
    """
    paths = pyd.map_(paths, pyd.to_string)
    paths_list = []
    params_list = flatten_url_params(params)

    for path in paths:
        scheme, netloc, path, query, fragment = urlsplit(path)
        query = parse_qsl(query)
        params_list += query
        paths_list.append(urlunsplit((scheme, netloc, path, '', fragment)))

    path = delimitedpathjoin('/', *paths_list)
    scheme, netloc, path, query, fragment = urlsplit(path)
    query = urlencode(params_list)

    return urlunsplit((scheme, netloc, path, query, fragment))


def words(text):
    """Return list of words contained in `text`.

    Args:
        text (str): String to split.

    Returns:
        list: List of words.

    .. versionadded:: 2.0.0
    """
    return js_match(RE_WORDS, text)


#
# Utility functions not a part of main API
#


def js_to_py_re_find(reg_exp):
    """Return Python regular expression matching function based on Javascript
    style regexp.
    """
    pattern, options = reg_exp[1:].rsplit('/', 1)
    flags = re.I if 'i' in options else 0

    def find(text):  # pylint: disable=missing-docstring
        if 'g' in options:
            results = re.findall(pattern, text, flags=flags)
        else:
            results = re.search(pattern, text, flags=flags)

            if results:
                results = [results.group()]
            else:
                results = []

        return results

    return find


def js_to_py_re_replace(reg_exp):
    """Return Python regular expression substitution function based on
    Javascript style regexp.
    """
    pattern, options = reg_exp[1:].rsplit('/', 1)
    count = 0 if 'g' in options else 1
    ignore_case = 'i' in options

    def _replace(text, repl):  # pylint: disable=missing-docstring
        return re_replace(text,
                          pattern,
                          repl,
                          ignore_case=ignore_case,
                          count=count)

    return _replace


def delimitedpathjoin(delimiter, *paths):
    """Join delimited path using specified delimiter.

    >>> assert delimitedpathjoin('.', '') == ''
    >>> assert delimitedpathjoin('.', '.') == '.'
    >>> assert delimitedpathjoin('.', ['', '.a']) == '.a'
    >>> assert delimitedpathjoin('.', ['a', '.']) == 'a.'
    >>> assert delimitedpathjoin('.', ['', '.a', '', '', 'b']) == '.a.b'
    >>> ret = '.a.b.c.d.e.'
    >>> assert delimitedpathjoin('.', ['.a.', 'b.', '.c', 'd', 'e.']) == ret
    >>> assert delimitedpathjoin('.', ['a', 'b', 'c']) == 'a.b.c'
    >>> ret = 'a.b.c.d.e.f'
    >>> assert delimitedpathjoin('.', ['a.b', '.c.d.', '.e.f']) == ret
    >>> ret = '.a.b.c.1.'
    >>> assert delimitedpathjoin('.', '.', 'a', 'b', 'c', 1, '.') == ret
    >>> assert delimitedpathjoin('.', []) == ''
    """
    paths = [pyd.to_string(path) for path in pyd.flatten_deep(paths) if path]

    if len(paths) == 1:
        # Special case where there's no need to join anything.
        # Doing this because if path==[delimiter], then an extra delimiter
        # would be added if the else clause ran instead.
        path = paths[0]
    else:
        leading = delimiter if paths and paths[0].startswith(delimiter) else ''
        trailing = delimiter if paths and paths[-1].endswith(delimiter) else ''
        middle = delimiter.join([path.strip(delimiter)
                                 for path in paths if path.strip(delimiter)])
        path = ''.join([leading, middle, trailing])

    return path


def flatten_url_params(params):
    """Flatten URL params into list of tuples. If any param value is a list or
    tuple, then map each value to the param key.
    >>> params = [('a', 1), ('a', [2, 3])]
    >>> assert flatten_url_params(params) == [('a', 1), ('a', 2), ('a', 3)]
    >>> params = {'a': [1, 2, 3]}
    >>> assert flatten_url_params(params) == [('a', 1), ('a', 2), ('a', 3)]
    """
    if isinstance(params, dict):
        params = list(iteritems(params))

    flattened = []
    for param, value in params:
        if isinstance(value, (list, tuple)):
            flattened += zip([param] * len(value), value)
        else:
            flattened.append((param, value))

    return flattened
