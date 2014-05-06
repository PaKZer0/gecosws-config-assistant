#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: local_file
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin

    if new_resource.delete_files.any?
      new_resource.delete_files.each do |value|
      makebackup = 1 if value.backup 
       if ::File.exists?(value.file)
         if ::File.file?(value.file)
           file value.file do
             backup makebackup
             action :delete
           end
         elsif ::File.directory?(value.file)
           directory value.file do
             recursive true
             action :delete
           end
         end
       end
      end
    end

    if new_resource.copy_files.any?
      new_resource.copy_files.each do |file|       
        if file.overwrite 
           grp_members = ::Etc.getgrnam(file.group).mem
           remote_file file.file_dest do
             source file.file_orig
             owner file.user
             mode file.mode
             group file.group
           end
         else
           grp_members = ::Etc.getgrnam(file.group).mem 
           remote_file file.file_dest do
              source file.file_orig
              owner file.user
              mode file.mode
              group file.group
              action :create_if_missing
           end
        end
      end
    end
    # TODO:
    # save current job ids (new_resource.job_ids) as "ok"

  rescue
    # TODO:
    # just save current job ids as "failed"
    # save_failed_job_ids
    raise
  end
end
