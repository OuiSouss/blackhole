'''
Black Hole Routing Experiment
'''

# Define a session for InitNemu
# Be careful to don't have a directory with the same name
SESSION = 'blackhole'

# Define a workspace for InitNemu
# We set it with our local directory nemu_virt
WORKSPACE = '.'

# Define where the debian image is located
# On cremi, is on /net/stockage/amerisi/bhre/blackholerouting/fs/debian8.img
DEBIAN_IMAGE = 'blackholerouting/fs/debian8.img'

InitNemu(session=SESSION, workspace=WORKSPACE, hdcopy=True)

VHostConf('debian', display='sdl', vga='std', enable_kvm=None, localtime=None,
		  k='fr', m='4G', cpu='kvm64')

VHost('attacker', conf='debian',
	  hds=[VFs(DEBIAN_IMAGE, 'cow', tag='attacker.img')],
	  nics=[
		  VNic(hw='0a:0a:0a:00:01:01'),
		  VNic(hw='0a:0a:0a:00:01:02'),
		  VNic(hw='0c:0c:0c:00:01:01')])

VHost('route-web-server', conf='debian',
	  hds=[VFs(DEBIAN_IMAGE, 'cow', tag='route-web-server.img')],
	  nics=[
		  VNic(hw='0a:0a:0a:00:03:01'),
		  VNic(hw='0c:0c:0c:00:03:03')])

VHost('client', conf='debian',
	hds=[VFs(DEBIAN_IMAGE, 'cow', tag='client.img')],
	nics=[
		VNic(hw='0a:0a:0a:00:05:01'),
		VNic(hw='0a:0a:0a:00:05:02'),
		VNic(hw='0c:0c:0c:00:05:05')])

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

Link(client='attacker:0', core='sw2:0')
Link(client='attacker:1', core='sw1:1')
Link(client='client:0', core='sw1:0')
Link(client='client:1', core='sw2:1')

Link(client='route-web-server:0', core='sw3:0')

VSlirp('slirp1', net='192.168.1.0/24')
Link(client='attacker:2', core='slirp1')

VSlirp('slirp2', net='192.168.3.0/24')
Link(client='route-web-server:1', core='slirp2')

VSlirp('slirp3', net='192.168.5.0/24')
Link(client='client:2', core='slirp3')

StartNemu()