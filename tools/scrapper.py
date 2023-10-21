#!/usr/bin/env python

import operator
import sys

from datetime import datetime

from bs4 import BeautifulSoup

def print_stderr(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)

def _handle_file_info(data):
    (filename, extra) = data

    if not (filename and extra):
        return

    (raw_date, raw_size) = extra.rsplit(maxsplit=1)
    raw_date = raw_date.strip()
    raw_size = raw_size.strip()

    try:
        size = int(raw_size)
    except BaseException as e:
        print_stderr(e)
        return

    try:
        date = datetime.strptime(raw_date, '%d-%b-%Y %H:%M')
    except BaseException as e:
        print_stderr(e)
        return

    # TODO: namedtuple?
    return {
        'filename': filename,
        'timestamp': int(date.timestamp()),
        'size': size,
    }

def _handle_raw_info(raw_info):
    info = list(
        filter(
            operator.truth,
            map(_handle_file_info, raw_info)
        )
    )

    return info
def _parse_page(soup):
    # Take main element containing all them links + timestamp & size in-between
    pre = soup.find('pre')

    # Laziest way to access necessary data
    elements = pre.stripped_strings

    # Skip '..'
    next(elements)

    # Pair filenames with metadata
    # (would be easier if it wansn't in-between <a/>
    # but inside a separate tag
    raw_info = [
        # XXX: hacky
        (item, next(elements, None))
        for item in elements
    ]

    return raw_info

if __name__ == '__main__':
    soup = BeautifulSoup(sys.stdin, features='html.parser')

    raw_info = _parse_page(soup)

    info = _handle_raw_info(raw_info)

    # TODO: Support glob as filename filter from arguments?
    latest_by_timestamp = max(info, key=operator.itemgetter('timestamp'))

    print(latest_by_timestamp['filename'])
