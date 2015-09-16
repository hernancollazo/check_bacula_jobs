# check_bacula_jobs

It's a simple shell script, to report Bacula jobs statuses on Nagios, from MySQL backend

### Installation

Since it is an active check, it is best used with NRPE. 

```sh
$ cd /tmp/
$ git clone [git-repo-url] check_bacula_jobs
$ cd check_bacula_jobs
$ cp check_bacula_jobs.py /usr/lib/nagios/plugins/check_bacula_jobs.py
$ cp check_bacula_jobs.cfg.dist /usr/lib/nagios/plugins/check_bacula_jobs.cfg
$ vim /usr/lib/nagios/plugins/check_bacula_jobs.cfg
```
And then, add to your NRPE config:

```sh
command[check_bacula_jobs]=/usr/lib/nagios/plugins/check_bacula_jobs.py
```
