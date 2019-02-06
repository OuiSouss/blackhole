
from funct_base import *
import sys

while(1):
    selection = raw_input('\nSelect C to connect, R to register, Q to quit\n')
    if selection =='R':
	register()
    elif selection == 'C':
    	login()
    elif selection == 'Q':
	print '\nBye bye\n'
	sys.exit(1)
    else:
        print '\n INVALID SELECTION \n'
