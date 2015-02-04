# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# pylesswrap
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
#
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

from __future__ import unicode_literals

import subprocess
import re
import shlex
from os import path, devnull


COLOR_STRIP = re.compile(r"\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]")


def execute_command(args, cwd='.'):
    """
    Executes the given command in the given working dir, and returns a tuple with the content of
    stdout, stderr and the return code.

    :param args: list of arguments (including the command name)
    :param cwd: current working dir to work into
    :return:
    """

    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        cwd=cwd,
    )

    out, err = process.communicate()
    ret = process.poll()

    return COLOR_STRIP.sub('', out), COLOR_STRIP.sub('', err), ret


class LessError(Exception):
    pass


class Less(object):
    def __init__(self, cache, include_paths=None, less_bin='lessc'):
        self.include_paths = include_paths if include_paths is not None else []
        self.less_bin = shlex.split(less_bin)
        self.cache = cache

    def execute_command(self, args, infile):
        command = list(self.less_bin)

        if len(self.include_paths) > 0:
            command += ['--include-path={}'.format(path.pathsep.join(self.include_paths))]

        command += args

        return execute_command(command, path.realpath(path.dirname(infile)))

    def compile(self, infile, outfile):
        out, err, ret = self.execute_command([infile, outfile], infile)

        if ret:
            raise LessError('Could not compile "{}".\nReason:\n{}'.format(infile, err))

    def mtime(self, infile):
        cache_valid = infile in self.cache

        if cache_valid:
            for file_name, mtime in self.cache[infile]:
                if mtime != path.getmtime(file_name):
                    cache_valid = False
                    break

        if not cache_valid:
            self.cache[infile] = list(self.dependencies(infile))

        return max(x[1] for x in self.cache[infile])

    def dependencies(self, infile):
        out, err, ret = self.execute_command(['-M', infile, devnull], infile)

        if ret:
            raise LessError('Invalid input file "{}".\nReason:\n{}'.format(infile, err))

        yield infile, path.getmtime(infile)

        files = out.split(' ')[1:]

        i = 0
        while i < len(files):
            for j in range(i, len(files)):
                file_name = ' '.join(files[i:j + 1])

                try:
                    yield file_name, path.getmtime(file_name)
                    i = j + 1
                    break
                except OSError:
                    pass
            else:
                i += 1
