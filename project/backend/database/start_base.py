"""
MongoDB terminal mode
"""
import sys
import pprint
from funct_base import MongoDB

while 1:
    self = MongoDB('Route')
    selection = input('POST : add route, PATCH : update route,'\
                        'GET : get routes, PUT : update route V2 '\
                            'DEL : delete route, Q : quit\n')

    if selection == 'POST':
        ip = input('Enter ip\n')
        nexthop = input('Enter nexthop\n')
        commu = input('Enter community\n')
        post = {'ip': ip, 'next_hop': nexthop, 'communities': commu}
        self.add_route(post)
    elif selection == 'PATCH':
        ip = input('Enter ip\n')
        post = self.route.find_one({'ip': ip})
        post['is_activated'] = not post['is_activated']
        self.update_route(post)
    elif selection == 'GET':
        routes = self.get_all_routes()
        for route in routes:
            pprint.pprint(route)
    elif selection == 'PUT':
        ip = input('Enter ip\n')
        post = self.route.find_one({'ip': ip})
        new_communities = input('Enter new communities\n')
        new_ip = input('Enter new ip\n')
        new_next_hop = input('Enter new next_hop\n')
        new_activation = input('Enter new activation(boolean)\n')
        if new_activation == 'True' or new_activation == 'true':
            new_activation = True
        else:
            new_activation = False
        post['communities'] = new_communities
        post['ip'] = new_ip
        post['next_hop'] = new_next_hop
        post['is_activated'] = new_activation
        self.put_route(post)
    elif selection == 'DEL':
        ip = input('Enter ip\n')
        post = self.route.find_one({'ip': ip})
        self.delete_route(post)
    elif selection == 'Q':
        print('\nBye')
        sys.exit(1)
    else:
        print('\n INVALID SELECTION \n')
