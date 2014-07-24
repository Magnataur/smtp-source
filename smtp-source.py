#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement

import sys
import smtplib
import os
import threading
import Queue
import argparse
import logging


class Worker(threading.Thread):
    def __init__(self, work_queue, server, sender, to):
        super(Worker, self).__init__()

        self.smtpObj = smtplib.SMTP(server)
        self.receivers = to
        self.sender = sender
        self.queue = work_queue

    def __del__(self):
        if hasattr(self, 'smtpObj'):
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
            except IOError as e:
                logging.error('Unable to open mime -- {}'.format(e))
                continue

            try:
                self.smtpObj.sendmail(self.sender, self.receivers, mime)
            except smtplib.SMTPException as e:
                logging.error('Unable to send email -- {}'.format(e))
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

    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)-8s %(message)s',
                        datefmt='%H:%M:%S',
                        level=log_level)

    try:
        mimes = os.listdir(args.mimes)
    except OSError as e:
        logging.error('Unable to open mimes folder -- {}'.format(e))
        return -1
    else:
        logging.info('Got list of %s mimes' % len(mimes))

    queue = Queue.Queue()
    for filename in mimes:
        queue.put(os.path.join(args.mimes, filename))

    workers = []
    for n in xrange(args.workers):
        try:
            worker = Worker(queue, args.ip, args.sender, args.to)
        except:
            logging.error('Unable to start worker')
            continue
        else:
            workers.append(worker)
            worker.start()

    logging.info('All workers started')

    if workers:
        # Wait until queue is empty
        queue.join()
    else:
        logging.error('No workers found')
        return -1

    logging.info('Job done')
    return 0


if __name__ == '__main__':
    sys.exit(main())