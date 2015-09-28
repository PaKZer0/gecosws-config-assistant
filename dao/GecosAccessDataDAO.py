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

__author__ = "Abraham Macias Paredes <amacias@solutia-it.es>"
__copyright__ = "Copyright (C) 2015, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

from dto.GecosAccessData import GecosAccessData
from dao.NetworkInterfaceDAO import NetworkInterfaceDAO
from util.JSONUtil import JSONUtil
from util.Template import Template

import logging
import traceback
import os
import hashlib

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class GecosAccessDataDAO(object):
    '''
    DAO class to manipulate GecosAccessData DTO objects.
    '''

    # Singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GecosAccessDataDAO, cls).__new__(
                                cls, *args, **kwargs)
            cls._instance.previous_saved_data = None
        return cls._instance


    def __init__(self):
        '''
        Constructor
        '''
        
        self.logger = logging.getLogger('GecosAccessDataDAO')
        self.data_file = '/etc/gcc.control'
           

    def load(self):
        self.logger.debug('load - BEGIN')
        data = GecosAccessData()
        
        # Check previous saved data (in memory cache)
        if self.previous_saved_data is not None:
            return self.previous_saved_data

        # Get data from data file
        jsonUtil = JSONUtil()
        json_data = jsonUtil.loadJSONFromFile(self.data_file)
        if json_data is not None:
            
            data.set_login(json_data['gcc_username'])
            data.set_url(json_data['uri_gcc'])
            
            # Password is not stored!
            data.set_password(None)
            
        if (data.get_url() is None or data.get_url().strip()==''):
            data = None
            
        self.logger.debug('load - END')
        return data


    def save(self, data):
        self.logger.debug('save - BEGIN')
        
        if data is None:
            raise ValueError('data is None')
        
        if not isinstance(data, GecosAccessData):
            raise ValueError('data is not a GecosAccessData instance')        
        
        # Insert the data in cache memory
        self.previous_saved_data = data
        
        # Get gcc_nodename from data file
        try:
            jsonUtil = JSONUtil()
            json_data = jsonUtil.loadJSONFromFile(self.data_file)
            gcc_nodename = ''
            if json_data is not None:
                gcc_nodename = json_data['gcc_nodename']
        except:
            # Can't get gcc_nodename from file, calculate it
            networkDao = NetworkInterfaceDAO()
            interfaces = networkDao.loadAll()
            no_localhost_name = None
            for inter in interfaces:
                if not inter.get_ip_address().startswith('127.0'):
                    no_localhost_name = inter.get_name()
                    break
            self.logger.debug("Selected interface name is: %s"%(no_localhost_name))
            mac = self._getHwAddr(no_localhost_name)
            gcc_nodename = hashlib.md5(mac.encode()).hexdigest()
            self.logger.debug("New node name is: %s"%(gcc_nodename))            
                    
        # Save data to data file
        template = Template()
        template.source = 'templates/gcc.control'
        template.destination = self.data_file
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00755
        template.variables = { 
            'uri_gcc':  data.get_url(), 
            'gcc_username':  data.get_login(), 
            'gcc_nodename':  gcc_nodename, 
        }        
        
        return template.save()

        
    def delete(self, data):
        self.logger.debug('delete - BEGIN')
        
        if data is None:
            raise ValueError('data is None')
        
        if not isinstance(data, GecosAccessData):
            raise ValueError('data is not a GecosAccessData instance')        
 
        # Remove data from memory
        self.previous_saved_data = None
        
        # Remove data file
        try:
            if os.path.isfile(self.data_file):
                os.remove(self.data_file)
            
        except Exception:
            self.logger.error(_('Error removing file:') + self.data_file)
            self.logger.error(str(traceback.format_exc()))             
        
        self.logger.debug('delete - END')        








