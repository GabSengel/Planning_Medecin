# Planification des Gardes Médicales

## Contexte du Projet

Ce projet vise à développer un outil pour l'organisation des gardes des médecins dans un service hospitalier. Il prend en compte divers critères comme les périodes de vacances, les disponibilités des médecins et le nombre maximal de gardes par médecin, pour optimiser la répartition des gardes et assurer une couverture efficace tout en respectant les contraintes individuelles.

## Objectifs

- **Gestion des périodes de vacances :** Chaque période est définie par son nom, un jour de début et une durée.
- **Gestion des disponibilités des médecins :** Chaque médecin a des jours spécifiques où il peut assurer des gardes.
- **Contraintes de planification :** Limiter le nombre maximal de gardes par médecin et assurer qu'un médecin ne travaille pas plus d'un jour pendant une période de vacances.

## Fonctionnalités

1. **Définition des Critères :**
   - Nombre total de jours pour la planification.
   - Détails et durée des périodes de vacances.
   - Disponibilités et contraintes pour chaque médecin.

2. **Création de Planning :**
   - Répartition équitable des gardes en tenant compte des disponibilités et des contraintes.

3. **Interface en Ligne de Commande :**
   - Commandes pour créer un fichier de critères.
   - Commandes pour visualiser les critères à partir d'un fichier JSON.
   - Commandes pour générer un planning de gardes basé sur les critères définis.


## Technologies 

- Python pour le backend avec des bibliothèques comme Pandas pour la manipulation des données et Pytest pour les tests.
- Dataclasses pour la modélisation des données.
- Streamlit pour l'interface utilisateur graphique.
- Poetry pour la gestion des dépendances.
- Asciinema pour la création de démonstrations en gif.

### Installation des Dépendances

Utilisez `poetry` pour installer les dépendances nécessaires à partir du fichier `pyproject.toml`.

### Demonstration en ligne de commande 

Le fichier demo.py sert d'interface en ligne de commande pour interagir avec le système. 
Les commandes disponibles sont :
- `demo` : Génère un fichier demonstration.json contenant les critères de planification.
- `view [chemin]` : Affiche les critères de planification à partir d'un fichier JSON spécifié.
- `solve [chemin]` : Génère le planning des gardes à partir des critères spécifiés dans le fichier JSON.

## Démonstration

![Démonstration du projet](./img/demo.gif)

## Utilisation de l'application 

Lancez l'application Streamlit :

`streamlit run app.py`

## Auteurs 
Gabin SENGEL & Paul VIDAL 


## Sujet inital 

### Sujet 09

Un hopital doit organiser ses gardes.

Il y a $k$ périodes de vacances.
La $j$-ième période étant faite de $D_j$ jours consécutifs.

Il y a $n$ médecins dans l'hopital et le $i$-ème docteur a
un ensemble (pas juste un nombre) de jours $S_j$ où il peut assurer des gardes.

Déterminer si il existe un emploi du temps étant donnés

- un paramètre $c$ représentant le nombre maximal de jours de garde
  assignés à un même médecin,
- pour chaque période de vacance un médecin ne doit assurer au plus
  qu'un jour de garde.

Si un tel emploi du temps existe, il faut également en expliciter un.
