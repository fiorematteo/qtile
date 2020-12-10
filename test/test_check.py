# Copyright (c) 2020 Tycho Andersen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import shutil
import subprocess
import tempfile
import textwrap


def run_qtile_check(config):
    # make sure we have mypy so we can type check the config
    if shutil.which("mypy") is None:
        raise Exception("missing mypy in test environment")
    cmd = os.path.join(os.path.dirname(__file__), '..', 'bin', 'qtile')
    argv = [cmd, "check", "-c", config]
    try:
        subprocess.check_call(argv)
    except subprocess.CalledProcessError:
        return False
    else:
        return True


def test_check_default_config():
    # the default config should always be ok
    default_config = os.path.join(os.path.dirname(__file__), '..', 'libqtile', 'resources', 'default_config.py')
    assert run_qtile_check(default_config)


def check_literal_config(config):
    with tempfile.NamedTemporaryFile(suffix=".py") as temp:
        temp.write(textwrap.dedent(config).encode('utf-8'))
        temp.flush()
        return run_qtile_check(temp.name)


def test_check_bad_syntax():
    assert not check_literal_config("""
        meshuggah rocks!
    """)


def test_check_bad_key_arg():
    assert not check_literal_config("""
            Key([1], 1)
    """)


def test_check_good_key_arg():
    assert check_literal_config("""
        from libqtile.config import Key
        from libqtile.command import lazy

        keys = [Key(["mod4"], "x", lazy.kill())]
    """)