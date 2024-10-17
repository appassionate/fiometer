import re


#followed link89: https://github.com/link89/sci-parser/blob/main/sci_parser/parser.py
class Parser:

    def __init__(self, flags=re.MULTILINE, sep=':'):
        """
        Define a parser object with a set of regular expressions to match and parse text.

        :param flags: flags to pass to re.search, re.match, etc.
        :param sep: the default separator for kv_search
        """
        self._match_fns = []
        self._default_flags = flags
        self._default_sep = sep

    def kv_search(self, key, value=None, sep=None, stop_at=None, multiline=False,
                  fmt_fn=None, flags=None, v_type=lambda v: v, k_name=None):
        """
        Extract a key-value pair from text.

        :param key: the key to search for, as a string literal

        :param value: the value to search for, as a regular expression,
        the default is r'(.*?)' if multiline is True, otherwise r'(\S+)' is usedd to match a single word,
        you can define your own regular expression to match the value,
        for example, if you want to match until the end of the line, then you can use r'(.*)$'

        :param sep: the separator (regular expression) between the key and value

        :param stop_at: the text to stop at
        if multiline is True, it will stop at empty line or end of the text by default

        :param multiline: whether to match across multiple lines
        :param fmt_fn: a function to format the match object
        :param flags: flags to pass to re.search

        :param v_type: a function to convert the value to a specific type
        Note that if you define your own fmt_fn, v_type will not be used

        :param k_name: the name to use for the key in the output tuple
        """

        if k_name is None:
            k_name = key
        key = re.escape(key)

        if sep is None:
            sep = self._default_sep

        if value is None:
            value = r'(.*?)' if multiline else r'(\S+)'

        if stop_at is None:
            stop_at = r'(?:\n\s*?\n|\Z|\n\r\s*?\n\r)' if multiline else ''

        pattern = rf'{key}\s*?{sep}\s*{value}{stop_at}'
        if multiline:
            pattern = rf'(?s){pattern}'

        if fmt_fn is None:
            fmt_fn = lambda m: (k_name, v_type(m.group(1)))
        return self.re_search(pattern, fmt_fn, flags)

    def re_search(self, pattern, fmt_fn=None, flags=None):
        """
        Add a regular expression to the parser.

        :param pattern: the regular expression pattern to match
        :param fmt_fn: a function to format the match object
        :param flags: flags to pass to re.search
        """

        if flags is None:
            flags = self._default_flags
        def match_fn(text):
            return re.search(pattern, text, flags)
        self._match_fns.append((match_fn, fmt_fn))
        return self

    def parses(self, text: str):
        """
        parse string and yield the results

        :param text: the text to parse
        """
        for match_fn, fmt_fn in self._match_fns:
            match = match_fn(text)
            if match:
                text = text[match.end():]
                yield match if fmt_fn is None else fmt_fn(match)
                
    