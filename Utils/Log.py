import os
from datetime import datetime
import logging
import sys


class Log:

    filename = ''
    levels = 'INFO'
    file_pointer = None

    @staticmethod
    def create_from_cfg(config):
        module = 'Log.create'
        #logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        #logging.debug(os.getcwd())

        Log.filename = config['Log']['Filename']
        Log.levels = config['Log']['Level'].split(',')

        Log.create(config['Log']['Filename'], config['Log']['Level'])
        #Log.file_pointer = open(Log.filename, "w+")
        #Log.print('INFO', module, 'Logging levels: {}'.format(Log.levels))
        #Log.print('INFO', module, 'Current Working Directory: {}'.format(os.getcwd()))
        Log.print('INFO', module, 'Config Sections: {}'.format(config.sections()))

    @staticmethod
    def create(log_filename, levels_str):
        module = 'Log.create'
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        logging.debug(os.getcwd())

        Log.filename = log_filename
        Log.levels = levels_str.split(',')

        Log.file_pointer = open(Log.filename, "w+")
        Log.print('INFO', module, 'Logging levels: {}'.format(Log.levels))
        Log.print('INFO', module, 'Current Working Directory: {}'.format(os.getcwd()))


    @staticmethod
    def print(level, module, *msg):
        if level in Log.levels or level in ('ERR', 'ERROR', 'WARN', 'WARNING'):
            now = datetime.now()
            msg_out = '{} {} {}\n'.format(now, level, module)
            msg_out2 = ' '.join(map(str, msg))
            print(msg_out, msg_out2.strip(), '\n')
            print(msg_out, msg_out2.strip(), '\n', file=Log.file_pointer)
            Log.file_pointer.flush()

    @staticmethod
    def close():
        Log.file_pointer.close()


