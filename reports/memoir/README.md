# Projet de PDP : Routage vers trou noir piloté à distance

## Objectif
L'objectif de ce projet est de développer un outil permettant à un administrateur réseau de définir à distance à partir d'un client Web, des routes menant vers des trous noirs pour dévier des attaques réseaux.
Ces routes seront envoyées à un serveur de route qui les diffusera auprès de tous les serveurs BGP du domaine.
Le logiciel devra être implémenté en Javascript et du côté serveur il devra piloter le logiciel ExaBGP écrit en Python.
L'application Web devra être de type RESTful et elle s'appuiera éventuellement sur un framework JS.
Elle devra supporter le routage vers trou noir par la destination, par la source et par la communauté BGP.

## Organisation
- [Trello](https://trello.com/invite/b/dZQteQPl/e0617eb1f7a6b316739c81d739760440/pdp-blackhole)

## Outils
- [ExaBGP](https://github.com/Exa-Networks/exabgp)
- [Nemu](https://gitlab.com/v-a/nemu)

## Lien utiles
- [PDF sur les blackholes](http://www.cisco.com/c/dam/en_us/about/security/intelligence/blackhole.pdf)
- [RTBH](http://packetlife.net/blog/2009/jul/6/remotely-triggered-black-hole-rtbh-routing/)
- [Cisco IPv6 RTFH](http://www.cisco.com/c/en/us/about/security-center/ipv6-remotely-triggered-black-hole.html)
- [supportforums.cisco.com](https://supportforums.cisco.com/discussion/12710041/bgp-remotely-triggered-black-hole-rtbh-routing)
- [Erco](https://erco.xyz/)
- [Projet de l'an dernier](https://services.emi.u-bordeaux.fr/projet/git/blackholepdp)
- [Tp pour Nemu](http://dept-info.labri.fr/~magoni/rvep/TD-RTBHR/)
