#!/usr/bin/env python

import ConfigParser
import sys, os, os.path, re, glob
import datetime, time, subprocess, shlex
from distutils.spawn import find_executable

import argparse


#Sample configuration file
config_example = """

[website]
project1 = /home/webs/Projects/Wordpress/
project2 = /home/webs/Projects/Wordpress/

[database_backup_path]
path = /data

[backup_policy]
rotate = 7 
""" 


#Delete files 
def delete_old_files(directory, site):
  r_latest = r"latest"
  f_del = r""+site+""
  #print site
  for f in os.listdir(directory):
    if re.search(r_latest, f):
      continue
    if re.search(f_del, f):
      print os.path.join(directory, f)
      os.remove(os.path.join(directory, f))


# Check rotation #dirty way  

def check_rotation():

  config = ConfigParser.ConfigParser()
  config.read('/etc/wordpress_backup.ini')

  rotation_number = config.get('backup_policy', 'rotate')
  storage_path = config.get('database_backup_path', 'path')
  backup_sites = config.items('website')
  for (site_item, site_path ) in backup_sites:
    rotation_file_count = len(glob.glob1(storage_path,site_item+"*"))
    if( int(rotation_number) <= int(rotation_file_count)):
      delete_old_files(storage_path, site_item) 
      print " Cleansing rotation files for .. " + site_item 
    print "Rotaion under limit skip... " + site_item
  
 

# check basic requirement 

init_app = ['git', 'wp', 'rsync', 'php'] 

def init_check():
  for app_init in init_app:
    app_check = find_executable(app_init)

    if app_check:
      print "App " + app_init +" Founded On " + os.path.abspath(app_check) 
      check_flag = True
    else:
      print "App " + app_init + " Not found please install before"
      check_flag = False
  if check_flag:
    write_config_init()


def is_exec(fpath):
  return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

  
def write_config_init():
  with open('/etc/wordpress_backup.ini', 'a+') as config_file:
    config_file.write(config_example)



# read configuration file 

config = ConfigParser.ConfigParser()
config.read('/etc/wordpress_backup.ini')

def get_ctime_from_file(file):
  stat = os.stat(file)
  return datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d-%H-%M")



def wordpress_backup(site='default'):
  config = ConfigParser.ConfigParser()
  config.read('/etc/wordpress_backup.ini')

  backup_sites = config.items('website')
  output = config.items('database_backup_path')
  time_backup = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') 
  
  if site == 'default':
    for ( site_item, site_path ) in backup_sites:
      print site_path + " " + time_backup
      latest_backup_file = config.get('database_backup_path','path') + '/' + site_item + '_' + 'latest.sql'

      if os.path.exists(latest_backup_file):
        ctime_str = get_ctime_from_file(latest_backup_file)
        next_backup_file = config.get('database_backup_path','path') + '/' + site_item + '_' + ctime_str +'.sql'
        os.rename(latest_backup_file, next_backup_file)
        backup_cmd = 'wp --allow-root db export '+ latest_backup_file 
        backup_ = shlex.split(backup_cmd)
        process = subprocess.Popen( backup_, cwd=site_path)
        process.wait()
      else:
        backup_cmd = 'wp --allow-root db export '+ latest_backup_file 
        backup_ = shlex.split(backup_cmd)
        process = subprocess.Popen( backup_, cwd=site_path) 
        process.wait()
      backup_ftimestamp = os.stat(latest_backup_file)
  else:
    flag_ = False 
    for ( site_item, site_path ) in backup_sites:
      if site_item == site:
        latest_backup_file = config.get('database_backup_path','path') + '/' + site_item + '_' + 'latest.sql'
        if os.path.exists(latest_backup_file):
          ctime_str = get_ctime_from_file(latest_backup_file)
          next_backup_file = config.get('database_backup_path','path') + '/' + site_item + '_' + ctime_str +'.sql'
          os.rename(latest_backup_file, next_backup_file)
          backup_cmd = 'wp --allow-root db export '+ latest_backup_file 
          backup_ = shlex.split(backup_cmd)
          process = subprocess.Popen( backup_, cwd=site_path)
          process.wait()
          flag_ = True
          break
        else:
          backup_cmd = 'wp --allow-root db export '+ latest_backup_file
          backup_ = shlex.split(backup_cmd)
          process = subprocess.Popen( backup_, cwd=site_path)
          process.wait()
          flag_ = True
          break
    if not flag_ :
      print "Not found site: " + site +" you want in config file ( /etc/wordpress_backup.ini )"

# Restore 

def wordpress_restore(site='default'):
  config = ConfigParser.ConfigParser()
  config.read('/etc/wordpress_backup.ini')

  backup_sites = config.items('website')
  output = config.items('database_backup_path')

  if site == 'default':
    for ( site_item, site_path ) in backup_sites:
      print " Restore "+ site_path  
      latest_backup_file = config.get('database_backup_path','path') + '/' + site_item + '_' + 'latest.sql'

      if os.path.exists(latest_backup_file):
        restore_cmd = 'wp --allow-root db import '+ latest_backup_file
        restore_ = shlex.split(restore_cmd)
        process = subprocess.Popen( restore_, cwd=site_path)
        process.wait()
    print "Restore All sites - DONE "
  else:
    flag_ = False
    for ( site_item, site_path ) in backup_sites:
      if site_item == site:
        latest_backup_file = config.get('database_backup_path','path') + '/' + site_item + '_' + 'latest.sql'
        if os.path.exists(latest_backup_file):
          restore_cmd = 'wp --allow-root db import '+ latest_backup_file
          restore_ = shlex.split(restore_cmd)
          process = subprocess.Popen( restore_, cwd=site_path)
          process.wait()
          flag_ = True
          break
    if not flag_ : 
      print "Can't restore site named: "+ site +" Please set it up in config file ( /etc/wordpress_backup.ini )"


# List wordpress site in Config file

def wordpress_list():
  config = ConfigParser.ConfigParser()
  config.read('/etc/wordpress_backup.ini')
  backup_sites = config.items('website')
  print " === Backup list ===" 
  print ""
  for ( site_item, site_path ) in backup_sites:
    print "Backup named  '" + site_item + "'  and wordpress site at  " + site_path
 
     


#for section in config.sections():
#  print section 


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description = "Wordpress Backup script")
  parser.add_argument('--clean', help="Check file roration and cleansing", action='store_true')
  parser.add_argument('--backup', help='Backup { wordpress_site }')  
  parser.add_argument('--backup_all', help='Backup ALL wordpress site', action='store_true')
  parser.add_argument('--restore', help='Restore wordpress specify site')
  parser.add_argument('--restore_all' , help='Restore ALL wordpress', action='store_true')
  parser.add_argument('--list_site', help='List site in config file (/etc/wordpress_backup.ini)', action='store_true')
  args = parser.parse_args()

  if args.backup_all:
     wordpress_backup()
  if args.backup is not None:
     wordpress_backup(args.backup) 
  if args.list_site:
     wordpress_list()
  if args.restore_all:
     wordpress_restore()
  if args.restore is not None:
     wordpress_restore(args.restore)
  if args.clean:
     check_rotation()
  if not os.path.exists('/etc/wordpress_backup.ini'):
     init_check()

  if not len(sys.argv) > 1:
     print "run with -h or --help for details"
