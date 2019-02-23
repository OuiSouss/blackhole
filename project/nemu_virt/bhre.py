'''
Black Hole Routing Experiment
'''

InitNemu(session='blackholerouting',\
	     workspace='/home/amelie/Documents/pdp-blackhole/project/nemu_virt/',\
		 hdcopy=True)

VHostConf('debian', display='sdl', vga='std', enable_kvm=None, localtime=None, k='fr', m='4G', cpu='kvm64')

VHost('attacker', conf='debian',
	hds=[VFs('/home/amelie/Documents/pdp-blackhole/project/nemu_virt/blackholing/fs/debian8.img',\
			 'cow', tag='attacker.img')],
	nics=[
	VNic(hw='0a:0a:0a:00:01:01'),
	VNic(hw='0a:0a:0a:00:01:02'),
	VNic(hw='0c:0c:0c:00:01:01')])

VHost('border-router', conf='debian',
	hds=[VFs('/home/amelie/Documents/pdp-blackhole/project/nemu_virt/blackholing/fs/debian8.img',\
			 'cow', tag='ce-bgp.img')],
	nics=[
	VNic(hw='0a:0a:0a:00:02:01'),
	VNic(hw='0a:0a:0a:00:02:02'),
	VNic(hw='0c:0c:0c:00:02:02')])

VHost('route-server', conf='debian',
	hds=[VFs('/home/amelie/Documents/pdp-blackhole/project/nemu_virt/blackholing/fs/debian8.img',\
			 'cow', tag='route-server.img')],
	nics=[
	VNic(hw='0a:0a:0a:00:03:01'),
	VNic(hw='0c:0c:0c:00:03:03')])

VHost('target', conf='debian',
	hds=[VFs('/home/amelie/Documents/pdp-blackhole/project/nemu_virt/blackholing/fs/debian8.img',\
			 'cow', tag='web-server.img')],
	nics=[
	VNic(hw='0a:0a:0a:00:04:01'),
	VNic(hw='0c:0c:0c:00:04:04')])

VHost('client', conf='debian',
	hds=[VFs('/home/amelie/Documents/pdp-blackhole/project/nemu_virt/blackholing/fs/debian8.img',\
			 'cow', tag='client.img')],
	nics=[
	VNic(hw='0a:0a:0a:00:05:01'),
	VNic(hw='0a:0a:0a:00:05:02'),
	VNic(hw='0c:0c:0c:00:05:05')])


'''
VRouter('box', nics=[VNic(), VNic()], services=[Service('ipforward'), Service('ifup', '1:192.168.0.1'), Service('gateway', 0),
	Service('masquerade', ipsrc='192.168.0.0/24'),
	Service('dnsmasq', domain='local', net='192.168.0.0/24', start='192.168.0.10', end='192.168.0.20', ifaces=[1])],
	enable_kvm=None, localtime=None, k='fr', display='sdl', vga='std')
'''

VSwitch('sw1', niface=3)
SetIface("sw1:0", proto='udp', port=11001, lport=11002)
SetIface("sw1:1", proto='udp', port=11003, lport=11004)
SetIface("sw1:2", proto='udp', port=10002, lport=10003)

VSwitch('sw2', niface=3)
SetIface("sw2:0", proto='udp', port=11005, lport=11006)
SetIface("sw2:1", proto='udp', port=11007, lport=11008)
SetIface("sw2:2", proto='udp', port=10004, lport=10005)

VSwitch('sw3', niface=4)
SetIface("sw3:0", proto='udp', port=11009, lport=11010)
SetIface("sw3:1", proto='udp', port=11011, lport=11012)

SetIface("sw3:2", proto='udp', port=10006, lport=10007)
SetIface("sw3:3", proto='udp', port=10008, lport=10009)

VSwitch('sw4', niface=2)
SetIface("sw4:0", proto='udp', port=11013, lport=11014)
SetIface("sw4:1", proto='udp', port=11015, lport=11016)

Link(client='attacker:0', core='sw1:0')
Link(client='attacker:1', core='sw2:1')
Link(client='client:0', core='sw2:0')
Link(client='client:1', core='sw1:1')

Link(client='border-router:0', core='sw3:0')
Link(client='route-server:0', core='sw3:1')
Link(client='target:0', core='sw4:0')
Link(client='border-router:1', core='sw4:1')

VSlirp('slirp1', net='192.168.1.0/24')
Link(client='attacker:2', core='slirp1')

VSlirp('slirp2', net='192.168.2.0/24')
Link(client='border-router:2', core='slirp2')

VSlirp('slirp3', net='192.168.3.0/24')
Link(client='route-server:1', core='slirp3')

VSlirp('slirp4', net='192.168.4.0/24')
Link(client='target:1', core='slirp4')

VSlirp('slirp5', net='192.168.5.0/24')
Link(client='client:2', core='slirp5')

