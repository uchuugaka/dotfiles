# Copyright 2017  Lincoln Clarete
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import io
import os.path
import sys
import gnupg


def parse_kv(line):
    try:
        _, key, _, _, _, user, _, password = line.split()
        return (key, password[1:-1])
    except ValueError:
        return (None, None)

def parse_authinfo(data):
    return dict(parse_kv(line) for line in data.splitlines())

def get_sec(key):
    gpg = gnupg.GPG(gnupghome=os.path.expanduser('~/.gnupg'), use_agent=True)
    with io.open(os.path.expanduser('~/.authinfo.gpg'), 'rb') as fd:
        return parse_authinfo(gpg.decrypt_file(fd).data)[key]

if __name__ == '__main__' and len(sys.argv) == 2:
    print(get_sec(sys.argv[1]))
