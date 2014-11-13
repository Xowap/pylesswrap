# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# pylesswrap
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
#
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

from django.conf import settings
from django.contrib.staticfiles.finders import get_finder
from django.test import TestCase
from activeseed.lib.pylesswrap.django_finders import FileSystemFinderDirs, \
    AppDirectoriesFinderDirs, list_dirs


class TestDjangoFinders(TestCase):
    def test_file_system_finder(self):
        finder = get_finder('django.contrib.staticfiles.finders.FileSystemFinder')
        dirs = FileSystemFinderDirs(finder)

        self.assertEqual(set(str(x) for x in settings.STATICFILES_DIRS), set(dirs.list_paths()))

    def test_app_directory_finder(self):
        finder = get_finder('django.contrib.staticfiles.finders.AppDirectoriesFinder')
        dirs = AppDirectoriesFinderDirs(finder)

        # This ain't no real test, whatever
        self.assertTrue(len(dirs.list_paths()) > 0)

    def test_list_dirs(self):
        dirs = set(list_dirs())

        # This ain't no real test, whatever
        self.assertTrue(len(dirs) > 0)
