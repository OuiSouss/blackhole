import sys
from funct_base import MongoDB


while(1):
    self = MongoDB('Route')
    selection = input('POST : add route, PATCH : update route, GET : get routes, DEL : delete route, Q : quit\n')

    if selection == 'POST':
        ip = input('Enter ip\n')
        nexthop = input('Enter nexthop\n')
        commu = input('Enter community\n')
        post = {'ip': ip, 'next_hop': nexthop, 'communities': commu}
        self.add_route(post)
    elif selection == 'PATCH':
        ip = input('Enter ip\n')
        post = {'ip': ip}
        self.update_route(post)    
    elif selection == 'GET':
        self.get_all_routes()
    elif selection == 'DEL':
        ip = input('Enter ip\n')
        post = {'ip': ip}
        self.delete_route(post)
    elif selection == 'Q':
        print('\nBye\n')
        sys.exit(1)
    else:
        print('\n INVALID SELECTION \n')
