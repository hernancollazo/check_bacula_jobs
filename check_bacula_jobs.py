#!/usr/bin/python

###############################################################################
###
### check_bacula_jobs.py
###
### Report Bacula jobs statuses on Nagios from MySQL backend.
###
### You can use it as it is, for your own risk.
### Please report any bugs or comments to: hernan.collazo@gmail.com
###
###############################################################################
###
### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; either version 2 of the License, or
### (at your option) any later version.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###
###############################################################################

import ConfigParser
import os
import socket
import sys
import MySQLdb

script_path = os.path.dirname(os.path.abspath(__file__))
configFile = script_path + "/check_bacula_jobs.cfg"
cp = ConfigParser.ConfigParser()
cp.read(configFile)

mysqlhost = cp.get("database", "mysqlhost")
mysqluser = cp.get("database", "mysqluser")
mysqlpass = cp.get("database", "mysqlpass")
mysqldb = cp.get("database", "mysqldb")
history = cp.get("general", "history")

try:
    conn = MySQLdb.connect(host=mysqlhost,
                           user=mysqluser, passwd=mysqlpass, db=mysqldb)
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

cursor = conn.cursor()
cursor.execute("SELECT JobId, Name, StartTime, EndTime, Level, JobStatus, " +
               "JobFiles,JobBytes FROM Job WHERE Type='B' AND " +
               "RealEndTime >=  DATE_ADD(NOW(), INTERVAL -" + str(history) +
               " HOUR) ORDER BY JobId;")
rows = cursor.fetchall()
rowcount = cursor.rowcount

errorsCnt = 0
okCnt = 0
critHost = []

if rowcount < 1:
    print "[ERROR] No backups were found."
    sys.exit(3)

for row in rows:
    jobId = row[0]
    jobName = row[1]
    jobStarTime = row[2]
    jobLevel = row[4]
    jobStatus = row[5]
    if not jobStatus == "T":
        errorsCnt += 1
        critHost.append(jobName)
    else:
        okCnt += 1

cursor.close()
conn.close()

if errorsCnt == 0:
    print "[OK] " + str(okCnt) + " backups terminated normally."
    sys.exit(0)
else:
    print "[ERROR] Found problems in backups for hosts: " + str(critHost)
    sys.exit(2)
