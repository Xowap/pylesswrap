# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# pylesswrap
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
#
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

from __future__ import unicode_literals

import time


try:
    from pipeline.compilers import CompilerBase
    from pipeline.conf import settings
    from pylesswrap.django_finders import list_dirs
    from pylesswrap.less import Less

    files_cache = {}

    class PyLessWrapCompiler(CompilerBase):
        output_extension = 'css'

        def __init__(self, *args, **kwargs):
            super(PyLessWrapCompiler, self).__init__(*args, **kwargs)
            self.less = Less(files_cache, list(set(list_dirs())), settings.PIPELINE_LESS_BINARY)

        def match_file(self, filename):
            return filename.lower().endswith('.less')

        def compile_file(self, infile, outfile, outdated=False, force=False):
            if outdated or force:
                self.less.compile(infile, outfile)

        def is_outdated(self, infile, outfile):
            try:
                return self.less.mtime(self.storage.path(infile)) \
                    > time.mktime(self.storage.modified_time(outfile).timetuple())
            except (OSError, NotImplementedError):
                return True
except ImportError:
    pass
