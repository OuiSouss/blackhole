# Virtualisation avec Nemu

## Prérequis
- Installer Nemu : [Sous Debian](https://gitlab.com/v-a/nemu/wikis/tuto/install/debian)
- Installer Dynamips : [Github de Dynamips](https://github.com/GNS3/dynamips)
- Obtenir une image cisco 7200 : /net/stockage/dmagoni/ios/c7200-jk9s-mz.124-13b.image

Lors d'une première execution se référer à la dernière partie de ce fichier.

## Lancement Rapide
1. Executer le script [dyna.sh](./dyna.sh)
2. Lancer les VMs : `nemu -f bhre.py -i`
3. Dans les VM sauf **route-server** démarrer Bird : `mkdir /run/bird; bird`
4. Dans le **route-server**, démarrer ExaBGP : `systemctl start exabgp`

## Etapes de mise en route à la premiere exécution

1. Changer les variables au début du [script dyna.sh](./dyna.sh)
    - DYNA : Correspond au chemin du fichier executable de dynamips
    - CISCO_IMAGE : Correspond au chemin de l'image cisco 7200
    - IDLE_PC : S'obtient en lançant dynamips une première fois de la façon suivante

    ```bash
    dynamips -P 7200 c7200-jk9s-mz.124-13b.image
    # Faire un Ctrl-] + i pour obtenir les stats
    ```

    On obtient :

    ```text
    Please wait while gathering statistics...
    Done. Suggested idling PC:
    0x608724c0 (count=36)
    0x6077ab60 (count=44)
    0x6077b604 (count=27)
    0x6077b640 (count=30)
    0x60653a0c (count=70)
    0x60653a6c (count=64)
    0x60653ab4 (count=36)
    0x6077bf24 (count=40)
    0x6077c0d8 (count=74)
    ```
    Prendre le count le plus grand pour limiter l'usage du cpu.

2. Lancer le [script dyna](./dyna.sh)
    ```bash
    ./dyna.sh
    ```
3. Vérifier via un **htop** que des processus dynamips sont en cours. Pour se connecter aux routeurs, il suffit de lancer les commandes suivantes :
    ```bash
    # Pour le routeur R1
    telnet 127.0.0.1 2001
    # Pour le routeur R2
    telnet 127.0.0.1 2002
    ```
4. Lancer les machines virtuelles via Nemu :
    ```bash
    nemu -f bhre.py -i
    ```
5. Se connecter en mode **root** directement, c'est plus simple. **Login : root, password : root**
6. Dans chaque machine, il faut configurer les interfaces réseau. Pour cela, le dossier [interfaces](./interfaces) possède toutes les configurations. Il sufit de monter le dossier interfaces sur chaque VM puis de copier le fichier correspondant à la machine dans **/etc/network/**
    ```bash
    # Depuis le home de root
    mount -t 9p interfaces interfaces/
    cp interfaces/<fichier nom vm> /etc/network/interfaces
    /etc/init.d/networking restart
    ```
7. Vérifier la connectivité entre les paires de voisins
8. Activer l'IP forwarding sur le **border-router**.
9. Installer dans toutes les machines sauf le **route-server**, `bird`. Pour cela, la même procédure que le point 6 est à faire.
    ```bash
    # Depuis le home de root
    mount -t 9p bird bird/
    cp bird/<fichier nom vm> /etc/bird/bird.conf
    mkdir /run/bird; bird;
    ```
    On peut vérifier le bon fonctionnement de bird grâce à la commande `birdc sh proto`.
10. Installer ExaBGP sur le **route-server**
    ```bash
    apt install python-pip
    pip install exabgp==3.4.26
    ```
    **Il faut impérativement utiliser la version 3.4.26 d'ExaBGP et python 2**
11. Executer Exabgp en plaçant les fichiers dans la VM **route-server** comme suit :
    ```bash
    # Depuis le home de root
    mount -t 9p exabgp exabgp/
    cp exabgp/app.py /etc/exabgp/app.py
    cp exabgp/exabgp.conf /etc/exabgp/exabgp.conf
    cp exabgp/exabgp.service /etc/systemd/system/exabgp.service

    # Execution
    systemctl start exabgp
    ```
12. De la même façon, il est possible de récupérer tous le projet via le même style de commande sur le tag "project".