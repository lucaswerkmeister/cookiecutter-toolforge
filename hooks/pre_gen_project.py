from __future__ import print_function

try:
    from urllib.error import HTTPError
    from urllib.request import urlopen
except ImportError:
    from urllib2 import HTTPError, urlopen
import sys


try:
    urlopen('https://toolsadmin.wikimedia.org/' +
            'tools/api/toolname/' +
            '{{ cookiecutter.tool_identifier }}').close()
except HTTPError:
    # Striker returns HTTP 406 Not Acceptable for invalid tool names
    print('\033[1m', file=sys.stderr)  # ANSI SGR 1: bold text
    print('''

The toolsadmin API indicates that "{{ cookiecutter.tool_identifier }}"
is not a valid title for a new tool. Either a tool of the same name
already exists, or the name is not a valid tool name at all. Tool
names must be valid MediaWiki user names, and they must not be blocked
titles on Wikitech; as of November 2018, this means that they cannot
include the name of a Wikimedia project, such as "wikipedia-something"
or "wikidata-other", due to the global title blacklist (see T190707).
Please choose a different name.

'''.strip(), file=sys.stderr)
    print('\033[0m', file=sys.stderr)  # ANSI SGR 0: reset/normal
    sys.exit(1)
