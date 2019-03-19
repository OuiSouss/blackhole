"""
 This app for test with exabgp

It will be remove by other one after

"""

from sys import stdout
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def command():
    """
    command basic function to propose some command to exabgp

    """

    cmd = request.form['command']
    stdout.write('%s\n' % cmd)
    stdout.flush()
    return '%s\n' % cmd

if __name__ == '__main__':
    app.run()
