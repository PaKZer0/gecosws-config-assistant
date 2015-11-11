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

__author__ = "Francisco Fuentes Barrera <ffuentes@solutia-it.es>"
__copyright__ = "Copyright (C) 2015, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

from gi.repository import Gtk, Gdk
import time
from view import GLADE_PATH, CSS_PATH, CSS_COMMON 
"""
Abstract parent class for any Gtk window used in GECOS
"""
class GladeWindow(object):
    def __init__(self, mainController):
        raise NotImplementedError( "This is an abstract class that cannot be instantiated" )
        
    def buildUI(self, gladepath):
        self.gladepath = gladepath
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GLADE_PATH+self.gladepath)
        
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path(CSS_PATH+CSS_COMMON)
        
        self.context = Gtk.StyleContext()
        self.context.add_provider_for_screen(
            Gdk.Screen.get_default(), self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
        # main window
        self.window = self.builder.get_object("window1")
        # center frame, here we'll do the transformations to keep all in the same window
        self.frame = self.builder.get_object("frame2")
         
        self.addHandlers()
    
    def show(self):
        self.window.show_all()
        Gtk.main()
    
    def getCenterFrame(self):
        return self.frame
    
    def putInCenterFrame(self, otherChildren):
        children = self.frame.get_children()
        # delete previous children
        for child in children:
            child.destroy()
        
        # add other children
        for otherChild in otherChildren:
            child.reparent(self.frame)
        
        # show em
        self.frame.show_all()
    
    def addHandlers(self):
        self.logger.info("Adding all handlers")
        # handling common hooks
        self.addCloseHandler()
        
    def addCloseHandler(self):
        self.logger.info("Adding close handlers")
        self.builder.connect_signals({"onDeleteWindow": Gtk.main_quit})
    
    def addTranslations(self):
        raise NotImplementedError( "This is an abstract method, is not implemented" )
    
    '''Not really necesary, but coded here cos could be handy, dunno'''
    def hideChildren(self, children):
        for child in children:
            try:
                if(count(child.get_children()) > 0):
                    self.hideChildren(child.get_children())
                else:
                    child.hide()
            except:
                child.hide()