import sys
import os
from datetime import timedelta


rows, columns = None, None
results = tuple(os.popen('stty size', 'r').read().split())
if len(results):
    rows, columns = results
    rows, columns = int(rows), int(columns)


def info(message, *args):
    message = str(message)
    message = message.format(*args)
    message = '\r' + message
    if columns is not None:
        message += ''.join([' '] * (columns - len(message)))

    sys.stdout.write(message)
    sys.stdout.flush()

    line_break()


def line_break():
    sys.stdout.write('\n')
    sys.stdout.flush()


def progress(message_format, *args, **kwargs):
    if 'index' not in kwargs or 'count' not in kwargs:
        index = 1
        count = 1
    else:
        index = kwargs['index']
        count = kwargs['count']

    max_frequency = 10000
    body = count - count % max_frequency
    max_frequency = count / max_frequency
    if max_frequency != 0 and index % max_frequency > 0 and index < body:
        return

    percentage = 100.0 * index / count
    percentage = '{0:.2f}%'.format(min(100., percentage))

    message_format = message_format \
        .replace('{I}', str(index)) \
        .replace('{C}', str(count)) \
        .replace('{P}', percentage)

    message = '\r' + message_format.format(*args)
    if columns is not None:
        message += ''.join([' '] * (columns - len(message)))

    sys.stdout.write(message)
    sys.stdout.flush()


def delta(seconds):
    delta_string = str(timedelta(seconds=seconds))
    delta_string = delta_string.split('.')[0]

    return delta_string