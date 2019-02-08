from pymongo import MongoClient
from datetime import *
import pprint
#from urllib import request, parse
#import json

uri = 'mongodb://Bidule45:Truc45@ds127115.mlab.com:27115/route_base'

client = MongoClient(uri)
global dbr
dbr = client.route_base
print(dbr.collection_names(include_system_collections=False))

def insert():
    try:
        routeNetwork = input('Enter Network :')
        routeMask = input('Enter Mask :')
        routeNextHop = input('Enter NextHop :')
        routeCommunity = input('Enter Community:')
        
        dbr.Route.insert_one(
            {
                "network":routeNetwork,
                "mask":routeMask,
                "nexthop":routeNextHop,
                "community":routeCommunity,
                "enabled":1,
                "created":datetime.utcnow(),
                "modified":datetime.utcnow(),
                "last_activation":datetime.utcnow()
        })
        print ('\nInserted data successfully\n')
    
    except Exception as e:
        print (e)

def read():
    try:
        routesCol = dbr.Route.find()
        print ('\n All data from Route Database \n')
        for route in routesCol:
            pprint.pprint(route)

    except Exception as e:
        print (e)

def read_one():
    try:
        routeNetwork = input('Enter Network :')
        route = dbr.Route.find_one({"network":routeNetwork})
        print ('\n Data from Route Database \n')
        pprint.pprint(route)

    except Exception as e:
        print (e)

def get():
    while(1):
        selection = input('\nSelect RALL to read all data, RONE to read one or Q to quit\n')

        if selection == 'RALL':
            read()
        elif selection == 'RONE':
            read_one()
        elif selection == 'Q':
            print('\nExiting Read option\n')
            break
        else:
            print ('\n INVALID SELECTION \n')

    
def activate():
    try:
        routeNetwork = input('\nEnter network to update\n')

        dbr.Route.update_one(
            {"network": routeNetwork},
            {
                "$set": {
                    "modified":datetime.utcnow(),
                    "last_activation":datetime.utcnow(),
                    "enabled":1
                }
            }
        )
        print ('\nRecord updated successfully\n')    
    
    except Exception as e:
        print (e)

def desactivate():
    try:
        routeNetwork = input('\nEnter network to update\n')

        dbr.Route.update_one(
            {"network": routeNetwork},
            {
                "$set": {
                    "modified":datetime.utcnow(),
                    "enabled":0
                }
            }
        )
        print ('\nRecord updated successfully\n')    
    
    except Exception as e:
        print (e)

def update():
    selection = input('\nSelect ACT to activate, DESACT to desactivate\n')
    
    if selection == 'ACT':
        activate()
    elif selection == 'DESACT':
        desactivate()
    else:
        print ('\n INVALID SELECTION \n')


def delete():
    try:
        routeNetwork = input('\nEnter network to delete\n')
        dbr.Route.delete_many({"network": routeNetwork})
        print ('\nDeletion successful\n') 
    except Exception as e:
        print (e)

##def register():
##    try:
##        userId = raw_input('Enter Id :')
##        userUsername = raw_input('Enter Username :')
##        userPassword = raw_input('Enter Password :')
##        userEmail = raw_input('Enter Email :')
##        
##        dbi.Security.insert_one(
##            {
##                "id": userId,
##                "username":userUsername,
##                "password":userPassword,
##                "email":userEmail,
##     #           "created":datetime.now(),
##     #           "modified":datetime.now(),
##        })
##        print '\nRegistered successfully\n'
##    
##    except Exception, e:
##        print str(e)
##
##def connect():
##	while(1):
##        	selection = raw_input('\nSelect POST to insert, PUT to update,  GET to read, DELETE to delete, DECO to disconnect\n')
##
##    		if selection == 'POST':
##        		insert()
##    		elif selection == 'PUT':
##       			update()
##    		elif selection == 'GET':
##        		read()
##    		elif selection == 'DELETE':
##        		delete()
##    		elif selection == 'DECO':
##			print '\nBye\n'
##			break
##    		else:
##        		print '\n INVALID SELECTION \n'
##
##def login():
##    try:
##        usersCol = dbi.Security.find()
##         #userId = raw_input('Enter Id :')
##	userUsername = raw_input('Enter Username :')
##	userPassword = raw_input('Enter Password :')
##        for users in usersCol:
##            if users == userUsername:
##		if users.password == userPassword:
##			connect()
##		else:
##			print '\nBad password\n'
##	    else:
##			print '\nBad username\n'
##
##    except Exception, e:
##        print str(e)
##
