# Virtualisation avec Nemu

## Prérequis
- Installer Nemu : [Sous Debian](https://gitlab.com/v-a/nemu/wikis/tuto/install/debian)
- Installer Dynamips : [Github de Dynamips](https://github.com/GNS3/dynamips)
- Obtenir une image cisco 7200 : /net/stockage/dmagoni/ios/c7200-jk9s-mz.124-13b.image

## Etapes de mise en route

1. Changer les variables au début du [script dyna](./dyna.sh)
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