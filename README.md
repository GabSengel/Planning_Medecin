# Planification des Gardes Médicales

## Contexte du Projet

Ce projet vise à développer un outil pour l'organisation des gardes des médecins dans un service hospitalier. Il prend en compte divers critères comme les périodes de vacances, les disponibilités des médecins et le nombre maximal de gardes par médecin, pour optimiser la répartition des gardes et assurer une couverture efficace tout en respectant les contraintes individuelles.

## Objectifs

- *Gestion des périodes de vacances :* Chaque période est définie par son nom, un jour de début et une durée.
- *Gestion des disponibilités des médecins :* Chaque médecin a des jours spécifiques où il peut assurer des gardes.
- *Contraintes de planification :* Limiter le nombre maximal de gardes par médecin et assurer qu'un médecin ne travaille pas plus d'un jour pendant une période de vacances.

## Fonctionnalités

1. *Définition des Critères :*
   - Nombre total de jours pour la planification.
   - Détails et durée des périodes de vacances.
   - Disponibilités et contraintes pour chaque médecin.

2. *Création de Planning :*
   - Répartition équitable des gardes en tenant compte des disponibilités et des contraintes.

3. *Interface en Ligne de Commande :*
   - Commande pour créer un fichier de critères.
   - Commande pour visualiser les critères à partir d'un fichier JSON.
   - Commande pour générer un planning de gardes basé sur les critères définis.
   - Commande pour lancer l'application streamit 


## Technologies 

- *Python* : Langage de programmation principal pour le backend.
- *Pandas* : Bibliothèque pour la manipulation et l'analyse de données.
- *Pytest* : Framework de test pour Python, pour écrire et exécuter des tests.
- *Dataclasses* : Module pour simplifier la création de classes et d'instances.
- *Typer* : Bibliothèque pour créer des applications en ligne de commande.
- *Rich* : Bibliothèque pour le formatage de texte et affichages enrichis dans le terminal.
- *Json* : Module pour l'encodage et le décodage de données au format JSON.
- *Black* : Outil de formatage de code pour garantir un style cohérent.
- *Ruff* : Outil de vérification de code source pour améliorer la qualité du code.
- *Os* : Module pour interagir avec le système d'exploitation.
- *Streamlit* : Framework pour créer des applications web interactives.
- *Poetry* : Outil de gestion des dépendances et packaging pour Python.
- *Asciinema* : Outil pour enregistrer des sessions de terminal sous forme de vidéos ou de gifs.

### Installation des Dépendances

Utilisez poetry pour installer les dépendances nécessaires à partir du fichier pyproject.toml.

### Demonstration en ligne de commande 

Le fichier _main_.py sert d'interface en ligne de commande pour interagir avec le système. 
Les commandes disponibles sont :
- demo : Génère un fichier demonstration.json contenant les critères de planification.
- view [chemin] : Affiche les critères de planification à partir d'un fichier JSON spécifié.
- solve [chemin] : Génère le planning des gardes à partir des critères spécifiés dans le fichier JSON.
- appli : Lance l'application (interface graphique générant un planning suite à l'indication de critères)

## Démonstration

![Démonstration du projet](./img/demo.gif)

## Algorthime 

L'algorithme planifie un emploi du temps de gardes pour un groupe de médecins sur une période donnée, en tenant compte de leurs disponibilités et des périodes de vacances. 

1. *Initialisation* : L'algorithme commence par vérifier que le nombre de médecins est suffisant pour couvrir les plus longues périodes de vacances. Si ce n'est pas le cas, il renvoie une erreur.
2. *Planification quotidienne* : Pour chaque jour du planning (jusqu'au nombre total de jours spécifié), l'algorithme vérifie si c'est un jour de vacance et quel médecin est disponible et n'a pas encore atteint le nombre maximum de gardes qu'il peut faire.
3. *Affectation des gardes* :
- L'algorithme trie les médecins disponibles par le nombre de gardes déjà effectuées pour prioriser ceux qui en ont fait le moins.
- Il tente ensuite d'assigner un médecin à chaque jour. Si c'est un jour de vacance, il s'assure que le médecin n'a pas déjà été assigné à cette vacance. Si aucun médecin n'est disponible pour un jour donné, l'algorithme renvoie une erreur indiquant qu'il est impossible de compléter l'emploi du temps.
4. *Enregistrement* : Une fois un médecin assigné à un jour, son compteur de gardes est incrémenté, et l'information est enregistrée dans un tableau qui sera finalement retourné sous forme de DataFrame.

### Mise en garde 

 L'algorithme priorise les médecins ayant effectué le moins de gardes. Si cette logique aboutit à des situations où aucun médecin n'est disponible pour un jour spécifique, même si une autre répartition initiale des gardes aurait pu fonctionner, l'algorithme échouera.

## Utilisation de l'application 

Lancez l'application Streamlit :

streamlit run app.py

ou 

python -m planning_medecin appli

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

Si un tel emploi du temps existe, il faut également en expliciter un.
