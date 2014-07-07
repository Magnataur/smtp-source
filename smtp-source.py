#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement

import sys
import smtplib
import os
import threading
import Queue
import argparse


class Worker(threading.Thread):
    def __init__(self, work_queue, server, sender, to):
        super(Worker, self).__init__()

        self.smtpObj = smtplib.SMTP(server)
        self.receivers = to
        self.sender = sender
        self.queue = work_queue

    def __del__(self):
        self.smtpObj.close()

    def run(self):
        while True:
            try:
                f_name = self.queue.get_nowait()
            except Queue.Empty:
                break

            self.queue.task_done()
            try:
                with open(f_name, 'rb') as fp:
                    mime = fp.read()
            except IOError:
                print('Error: unable to open: %s' % f_name)
                continue

            try:
                self.smtpObj.sendmail(self.sender, self.receivers, mime)
            except smtplib.SMTPException:
                print('Error: unable to send email')
                continue

        return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mimes', default='./', help='path to mimes folder')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')
    parser.add_argument('-w', '--workers', type=int, default=5, help='number of worker processes')
    parser.add_argument('-i', '--ip', default='127.0.0.1', help='smtp server ip address')
    parser.add_argument('-s', '--sender', default='test@mail', help='mail sender')
    parser.add_argument('-t', '--to', nargs='*', default=['yoda@klms'], help='mail receiver')

    args = parser.parse_args()

    try:
        mimes = os.listdir(args.mimes)
    except OSError:
        print('Unable to open mimes folder - %s' % args.mimes)
        return -1

    if args.verbose:
        print('Got %s mimes' % len(mimes))

    queue = Queue.Queue()
    for filename in mimes:
        queue.put(filename)

    for n in xrange(args.workers):
        worker = Worker(queue, args.ip, args.sender, args.to)
        worker.start()

    # Wait until queue is empty
    queue.join()


if __name__ == '__main__':
    sys.exit(main())