from pymongo import MongoClient
import datetime

client = MongoClient('localhost:27017')
global dbr
global dbi
dbr = client.Route
dbi = client.Security

def insert():
    try:
        routeId = input('Enter Id :')
        routeNetwork = input('Enter Network :')
        routeMask = input('Enter Mask :')
        routeNextHop = input('Enter NextHop :')
        routeCommunity = input('Enter Community:')
        
        dbr.Route.insert_one(
            {
                "id": routeId,
                "network": routeNetwork,
                "mask": routeMask,
                "nexthop": routeNextHop,
                "community": routeCommunity,
                "enabled": 1,
     #           "created":datetime.now(),
     #           "modified":datetime.now(),
        })
        print ('\nInserted data successfully\n')
    
    except Exception as e:
        print (str(e))

def read():
    try:
        routesCol = dbr.Route.find()
        print ('\n All data from Route Database \n')
        for route in routesCol:
            print (route)

    except Exception as e:
        print (str(e))

def activate():
    try:
        criteria = input('\nEnter id to update\n')
        routeNetwork = input('\nEnter network to update\n')

        dbr.Route.update_one(
            {"id": criteria},
            {
                "$set": {
      #              "modified":datetime.now(),
                    "enabled":0
                }
            }
        )
        print ("\nRecord updated successfully\n")   
    
    except Exception as e:
        print (str(e))

def desactivate():
    try:
        criteria = input('\nEnter id to update\n')
        qrouteNetwork = input('\nEnter network to update\n')

        dbr.Route.update_one(
            {"id": criteria},
            {
                "$set": {
       #             "modified":datetime.now(),
                    "enabled":1
                }
            }
        )
        print ("\nRecord updated successfully\n")
    
    except Exception as e:
        print (str(e))

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
        criteria = input('\nEnter id to delete\n')
        dbr.Route.delete_many({"id": criteria})
        print ('\nDeletion successful\n')
    except Exception as e:
        print (str(e))

def register():
    try:
        userId = input('Enter Id :')
        userUsername = input('Enter Username :')
        userPassword = input('Enter Password :')
        userEmail = input('Enter Email :')
        
        dbi.Security.insert_one(
            {
                "id": userId,
                "username":userUsername,
                "password":userPassword,
                "email":userEmail,
     #           "created":datetime.now(),
     #           "modified":datetime.now(),
        })
        print ('\nRegistered successfully\n')
    
    except Exception as e:
        print (str(e))

def connect():
    while(1):
        selection = input('\nSelect POST to insert, PUT to update, to read, DELETE to delete, DECO to disconnect\n')
        if selection == 'POST':
            insert()
        elif selection == 'PUT':
            update()
        elif selection == 'GET':
           	read()
        elif selection == 'DELETE':
           	delete()
        elif selection == 'DECO':
            print ('\nBye\n')
            break
        else:
            print ('\n INVALID SELECTION \n')

def login():
    try:
        usersCol = dbi.Security.find()
        #userId = raw_input('Enter Id :')
        userUsername = input('Enter Username :')
        userPassword = input('Enter Password :')
        for users in usersCol:
            if users == userUsername:
                if users.password == userPassword:
                    connect()
                else:
                    print ('\nBad password\n')
            else:
                print ('\nBad username\n')

    except Exception as e:
        print (str(e))
