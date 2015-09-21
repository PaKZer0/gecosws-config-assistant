#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

# This file is part of Guadalinex
#
# This software is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__author__ = "Antonio Hernández <ahernandez@emergya.com>"
__copyright__ = "Copyright (C) 2011, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"


###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys
import glob

try:
    import DistUtilsExtra.auto
    from distutils.core import setup, Command
    from DistUtilsExtra.command import *
except ImportError:
    print >> sys.stderr, 'To build gecos-config-assistant you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'

def get_datafiles(datadir):
    source = ''
    datafiles = []
    for root, dirs, files in os.walk(datadir):
        sources = []
        for f in files:
            sources.append(os.path.join(root,f))
        root_s = root.split('/')
        root_s.remove(datadir)
        root = str.join('/', root_s)
        datafiles.append(['share/gecosws-config-assistant/'+root, sources])
    return datafiles

datafiles = get_datafiles('data')
datafiles.append(('share/applications/', glob.glob('data/gecos-config-assistant.desktop')))


def update_desktop_file(datadir):

    try:
        fin = file('gecos-config-assistant.desktop.in', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            if 'Icon=' in line:
                line = "Icon=%s\n" % (datadir + 'media/wizard1.png')
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find gecos-config-assistant.desktop.in")
        sys.exit(1)


def copy_pages(pages_path):
    pass


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
#        values = {'__firstboot_data_directory__': "'%s'" % (
#                                        self.prefix + '/share/gecosws-config-assistant/'),
#                  '__version__': "'%s'" % self.distribution.get_version(),
#                  '__firstboot_prefix__': "'%s'" % self.prefix}
#        update_desktop_file(self.prefix + '/share/gecosws-config-assistant/')
#        DistUtilsExtra.auto.install_auto.run(self)
        return true


class Clean(Command):
    description = "custom clean command that forcefully removes dist/build directories and update data directory"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('rm -rf ./build ./dist')
        update_data_path(prefix, oldvalue)


class Check(Command):
    description = "Run unit tests"

    user_options = [
        ('module=', 'm', 'The test module to run'),
        ]

    def initialize_options(self):
        self.module = None

    def finalize_options(self):
        pass

    def get_command_name(self):
        return 'test'

    def run(self):
        import unittest
        from tests.dto.NTPServerTest import NTPServerTest
        from tests.dto.NetworkInterfaceTest import NetworkInterfaceTest
        from tests.dto.WorkstationDataTest import WorkstationDataTest
        from tests.dto.GecosAccessDataTest import GecosAccessDataTest
        from tests.dto.LocalUserTest import LocalUserTest
        from tests.dto.UserAuthenticationMethodTest import UserAuthenticationMethodTest
        from tests.dto.LocalUsersAuthMethodTest import LocalUsersAuthMethodTest
        from tests.dto.ADSetupDataTest import ADSetupDataTest
        from tests.dto.LDAPSetupDataTest import LDAPSetupDataTest
        from tests.dto.ADAuthMethodTest import ADAuthMethodTest
        from tests.dto.LDAPAuthMethodTest import LDAPAuthMethodTest
        from tests.dto.SystemStatusTest import SystemStatusTest

        suite = unittest.TestSuite()
        suite.addTest(NTPServerTest())
        suite.addTest(NetworkInterfaceTest())
        suite.addTest(WorkstationDataTest())
        suite.addTest(GecosAccessDataTest())
        suite.addTest(LocalUserTest())
        suite.addTest(UserAuthenticationMethodTest())
        suite.addTest(LocalUsersAuthMethodTest())
        suite.addTest(ADSetupDataTest())
        suite.addTest(LDAPSetupDataTest())
        suite.addTest(ADAuthMethodTest())
        suite.addTest(LDAPAuthMethodTest())
        suite.addTest(SystemStatusTest())
        
        
        return unittest.TextTestRunner(verbosity=2).run(suite)    
        
        
##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='gecosws-config-assistant',
    version='0.8.0-0gecos4',
    license='GPL-2',
    author='David Amian',
    author_email='damian@emergya.com',
    description='First start assistant for helping to connect a GECOS \
workstation to different services',
    url='https://github.com/gecos-team/gecosws-config-assistant',

    keywords=['python', 'gnome', 'guadalinex', 'gecos'],

    packages=[
        'dto',
    ],

    package_dir={
        'dto': 'dto',
        },

    scripts=[
#        'bin/gecos-config-assistant',
#        'bin/gecos-config-assistant-launcher'
    ],
    data_files = datafiles,
    cmdclass={
        'install': InstallAndUpdateDataDirectory,
        "build": build_extra.build_extra,
        "build_i18n":  build_i18n.build_i18n,
        'check': Check,
    }
)
