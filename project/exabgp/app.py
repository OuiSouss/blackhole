"""
 This app for test with exabgp

It will be remove by other one after

"""
import os
from sys import stdout
from time import sleep
from flask import Flask, request, abort

app = Flask(__name__)
EXABGP_LOG = '/home/amelie/Documents/pdp-blackhole/project/exabgp/exabgp.log'
EXABGP_OUT = '/home/amelie/Documents/pdp-blackhole/project/exabgp/output.toto'


def read_output_file(output_file_path):
    """
    read_output_file Read output file just for version command

    """
    reader = open(output_file_path, 'r+')
    writer = open(EXABGP_OUT, 'w')
    if reader is None:
        return 'exabgp output file does not exists\n'
    lines = reader.readlines()
    number = 0
    response = ''
    for line in lines:
        if ('Responding to httpapi : exabgp' in line) and (number == 0):
            line = line.split(':')
            line = line[-1].strip(' ')
            response = line
            number += 1
    reader.truncate(0)
    reader.close()
    writer.close()
    return response


def is_exabgp_running():
    """
    is_exabgp_running check if exabgp is running

    :return: True if is running, False if not
    :rtype: boolean
    """

    exabgp_pid = os.getppid()
    try:
        os.kill(exabgp_pid, 0)
    except OSError:
        return False
    return True

@app.route('/', methods=['POST'])
def command():
    """
    command basic function to propose some command to exabgp

    """
    if not is_exabgp_running():
        abort(503, description='ExaBGP is not running')
    cmd = request.form['command']
    stdout.write('%s\n' % cmd)
    stdout.flush()
    sleep(1)
    response = ''
    if cmd == 'version':
        response = read_output_file(EXABGP_LOG)
    return response

if __name__ == '__main__':
    app.run()
