from __future__ import print_function

from urllib.error import HTTPError
from urllib.request import Request, urlopen
import sys


user_agent = ('cookiecutter-toolforge ('
              'https://github.com/lucaswerkmeister/cookiecutter-toolforge)')
url = ('https://toolsadmin.wikimedia.org/tools/api/toolname/'
       '{{ cookiecutter.tool_identifier }}')
request = Request(url, headers={'User-Agent': user_agent})
try:
    urlopen(request).close()
except HTTPError:
    # Striker returns HTTP 406 Not Acceptable for invalid tool names
    print('\033[1m', file=sys.stderr)  # ANSI SGR 1: bold text
    print('Invalid tool name', file=sys.stderr)
    print('\033[0m', file=sys.stderr)  # ANSI SGR 0: reset/normal
    print('''

The toolsadmin API indicates that "{{ cookiecutter.tool_identifier }}"
is not a valid title for a new tool. Either a tool of the same name
already exists, or the name is not a valid tool name at all. Tool
names must be valid MediaWiki user names, and they must not be blocked
titles on Wikitech; as of November 2018, this means that they cannot
include the name of a Wikimedia project, such as "wikipedia-something"
or "wikidata-other", due to the global title blacklist (see T190707).

'''.strip(), file=sys.stderr)
    print('\033[1m', file=sys.stderr)  # ANSI SGR 1: bold text
    print('You should probably choose a different name.', file=sys.stderr)
    print('\033[0m', file=sys.stderr)  # ANSI SGR 0: reset/normal
    try:
        reply = input('Continue anyways? [y/N] ')
    except EOFError:
        print()  # line break after prompt
        reply = ''
    if not reply.lower().startswith('y'):
        sys.exit(1)
