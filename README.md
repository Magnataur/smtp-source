smtp-source
===========

Simple tool for sending emails stored as files in local folder. Usage:

/usr/bin/python2.7 smtp-source.py -h
usage: smtp-source.py [-h] [-m MIMES] [-v] [-w WORKERS] [-i IP] [-s SENDER]
                      [-t [TO [TO ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -m MIMES, --mimes MIMES
                        path to mimes folder
  -v, --verbose         enable verbose output
  -w WORKERS, --workers WORKERS
                        number of worker processes
  -i IP, --ip IP        smtp server ip address
  -s SENDER, --sender SENDER
                        mail sender
  -t [TO [TO ...]], --to [TO [TO ...]]
                        mail receiver

Process finished with exit code 0

Example:

/usr/bin/python2.7 smtp-source.py -m ./path/to/mimes -w 10 -i 192.168.1.2 -s test@mail.ru -t hello@yandex.ru
