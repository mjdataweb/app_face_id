# Flask Facial Recognition Web Service

## Description

Ce projet est un service web de reconnaissance faciale développé avec Flask. Les utilisateurs peuvent télécharger des images pour les comparer à une image de référence afin de déterminer si elles appartiennent à la même personne. Le service utilise les bibliothèques `face_recognition` et `opencv-python` pour la détection et la comparaison des visages.

## Auteurs

-  Marcel MISSIHOUN
- Othmane SENNIA
- Grégory HERY


## Fonctionnalités

- Téléchargement d'images pour la reconnaissance faciale.
- Comparaison d'une image de référence avec une image cible pour vérifier une correspondance.
- Sauvegarde des images traitées dans un répertoire désigné.
- Interface web conviviale pour l'utilisateur.

## Prérequis

Assurez-vous que Python est installé sur votre système (Python 3.7 ou supérieur recommandé). Installez les dépendances nécessaires à l'aide du fichier `requirements.txt` :

```bash
pip install -r requirements.txt
