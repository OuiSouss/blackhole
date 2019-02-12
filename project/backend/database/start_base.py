from funct_base import insert, get, update, delete
import sys

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
