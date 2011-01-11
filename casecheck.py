#!/usr/bin/env python3.2
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Łukasz Langa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""casecheck
   ---------

   Lists all paths that would clash on a case-insensitive filesystem."""

from configparser import ConfigParser, ExtendedInterpolation
import hashlib
import os
import sys

config = ConfigParser(allow_no_value=True,
    interpolation=ExtendedInterpolation())
# built-in defaults
config.read_dict({
    'general': {
        'search-root': '/',
        'script-dir': os.path.abspath(os.path.split(__file__)[0]),
        'current-dir': os.path.abspath('.'),
        'save-results': True,
        'results-path': '${current-dir}/caecheck.log',
    },
    'skip': {
        '/dev': None,
        '/Volumes': None
    },
    'progress-bar': {
        'show': True,
        'update-interval': 5000
    }
})
# search the usual places for config files
config.read((config['general']['script-dir'] + '/casecheck.ini',
    './casecheck.ini', '~/.casecheck.ini'))

# useful globals
blacklisted = set(config['skip'].keys())
boilerplate = 10
columns = int(os.popen('stty size', 'r').read().split()[1])
width = columns - boilerplate
count = 0
if config['progress-bar'].getboolean('show'):
    step = int(config['progress-bar']['update-interval'])
else:
    step = 0
star = '◴◷◶◵'

def check_level(path, save):
    """Recursively checks for entries that only differ in case. Starts the
    search in `path`. On finding any result, invokes `save` to store it
    in a log file."""

    global count

    entries = {}
    recurse = []

    if path.startswith('//'):
        path = path[1:]

    for entry in os.listdir(path):
        full_path = os.sep.join((path, entry))
        entries.setdefault(full_path.lower(), []).append(full_path)
        if os.path.isdir(full_path) and full_path not in blacklisted:
            recurse.append(full_path)
        count += 1
        if step and count % step == 0:
            star_char = star[(count % (4 * step))//step]
            if count % (4 * step) == 0:
                count = 0
            path_show = full_path
            if len(path_show) > width:
                path_show = (full_path[:width//2] + ' ... ' +
                    full_path[-width//2:])
            msg = "  {} {}".format(star_char, path_show)
            if len(msg) < columns-1:
                msg += " " * (columns - len(msg))
            msg += "\r"
            sys.stdout.write(msg)
            sys.stdout.flush()

    for entry, entry_paths in entries.items():
        if len(entry_paths) > 1:
            if step:
                print(" " * (columns), end="\r")
            save('{}:'.format(entry))
            for p in entry_paths:
                save('  {}'.format(p))
    del entries
    for entry in recurse:
        check_level(entry, save)

if __name__ == '__main__':
    if not config['general'].getboolean('save-results'):
        config['general']['results-path'] = '/dev/null'

    with open(config['general']['results-path'], 'w') as save_file:
        def save(text):
            print(text)
            save_file.write(text)
            save_file.write('\n')
            save_file.flush()
        try:
            check_level(config['general']['search-root'], save=save)
        except KeyboardInterrupt:
            sys.exit(0)
