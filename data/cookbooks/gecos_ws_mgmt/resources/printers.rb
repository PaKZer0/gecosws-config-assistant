#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: printers
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

actions :setup

attribute :printers_list, :kind_of => Array
attribute :job_ids, :kind_of => Array
