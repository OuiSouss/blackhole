
from funct_base import *
import sys

##while(1):
##    selection = raw_input('\nSelect C to connect, R to register, Q to quit\n')
##    if selection =='R':
##	register()
##    elif selection == 'C':
##    	login()
##    elif selection == 'Q':
##	print '\nBye bye\n'
##	sys.exit(1)
##    else:
##        print '\n INVALID SELECTION \n'
while(1):
    selection = input('\nSelect POST to insert, PUT to update,  GET to read, DEL to delete or Q to quit\n')

    if selection == 'POST':
        insert()
    elif selection == 'PUT':
        update()
    elif selection == 'GET':
        get()
    elif selection == 'DEL':
        delete()
    elif selection == 'Q':
        print ('\nBye\n')
        sys.exit(1)
    else:
        print ('\n INVALID SELECTION \n')
