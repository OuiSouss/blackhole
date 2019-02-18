# Projet de PDP : Routage vers trou noir piloté à distance

[![Build Status](https://travis-ci.org/OuiSouss/blackhole.svg?branch=master)](https://travis-ci.org/OuiSouss/blackhole)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=OuiSouss_blackhole&metric=alert_status)](https://sonarcloud.io/dashboard?id=OuiSouss_blackhole)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=OuiSouss_blackhole&metric=bugs)](https://sonarcloud.io/dashboard?id=OuiSouss_blackhole)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=OuiSouss_blackhole&metric=code_smells)](https://sonarcloud.io/dashboard?id=OuiSouss_blackhole)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=OuiSouss_blackhole&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=OuiSouss_blackhole)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=OuiSouss_blackhole&metric=coverage)](https://sonarcloud.io/dashboard?id=OuiSouss_blackhole)

## Objectif
L'objectif de ce projet est de développer un outil permettant à un administrateur réseau de définir à distance à partir d'un client Web, des routes menant vers des trous noirs pour dévier des attaques réseaux.
Ces routes seront envoyées à un serveur de route qui les diffusera auprès de tous les serveurs BGP du domaine.
Le logiciel devra être implémenté en Javascript et du côté serveur il devra piloter le logiciel ExaBGP écrit en Python.
L'application Web devra être de type RESTful et elle s'appuiera éventuellement sur un framework JS.
Elle devra supporter le routage vers trou noir par la destination, par la source et par la communauté BGP.

## Structure du dépôt

- [Project](./project) : Répertoire pour le code
  - [Frontend](./project/frontend) : Code du frontend
  - [README du projet](./project/README.md) : Informations pour configurer le projet
- [Reports](./reports) : Répertoire pour les fichiers latex


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
