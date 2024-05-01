import pandas as pd
from typing import List, Set, Dict
from dataclasses import dataclass

@dataclass
class PeriodeVacance:
    """
    Classe représentant une période de vacances avec un nom, un jour de début, et une durée.

    ## Attributes:
        nom (str): Le nom de la période de vacances.
        debut (int): Le jour de début de la période de vacances, généralement exprimé en tant que numéro de jour dans l'année.
        duree (int): La durée de la période de vacances, exprimée en nombre de jours.

    ## Raises:
        ValueError: Si la durée de la période est inférieure à zéro ou est infinie, indiquant que la durée n'est pas valide.
        ValueError: Si le jour de début est inférieur à zéro ou est infini, indiquant que le jour de début n'est pas valide.
        TypeError: Si le jour de début ou la durée n'est pas de type int.

    ## Example:
        >>> vacance = PeriodeVacance("Noel", 25, 5)
        >>> print(vacance.nom, vacance.debut, vacance.duree)
        Noel 25 5
    """
    nom: str
    debut: int
    duree: int

    def __post_init__(self):
        """ "Verifie la validité de la durée"""
        if self.duree < 0 or self.duree == float("inf"):
            raise ValueError(f"La durée de la période {self} n'est pas valide")
        """Verifie la validité de début"""
        if self.debut < 0 or self.debut == float("inf"):
            raise ValueError(f"Le jours de debut de la période {self} n'est pas valide")


@dataclass
class Medecin:
    """
    Classe représentant un médecin avec un identifiant unique et un ensemble de jours où il est disponible pour les gardes.

    ## Attributes:
        id (str): Identifiant unique du médecin, qui doit être une chaîne de caractères.
        disponibilites (Set[int]): Ensemble des jours où le médecin est disponible, exprimés en jours de l'année.

    ## Raises:
        ValueError: Si 'id' n'est pas une chaîne de caractères.
        ValueError: Si 'disponibilites' n'est pas un ensemble (set).
        ValueError: Si 'disponibilites' contient des éléments qui ne sont pas des entiers.
        ValueError: Si 'disponibilites' est vide.
        ValueError: Si 'disponibilites' contient des valeurs négatives.

    ## Example:
        >>> medecin = Medecin("Dr.Cardio", {1, 2, 3})
        >>> print(medecin.id)
        Dr.Cardio
        >>> print(medecin.disponibilites)
        {1, 2, 3}
    """
    id: str
    disponibilites: Set[int]

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise ValueError(f"L'ID du médecin doit être une chaîne de caractères, reçu: {type(self.id)}")
        if not isinstance(self.disponibilites, set):
            raise ValueError(f"Les disponibilités doivent être de type set, reçu: {type(self.disponibilites).__name__}")
        if not all(isinstance(jour, int) for jour in self.disponibilites):
            raise ValueError("Toutes les valeurs dans les disponibilités doivent être des entiers.")
        if not self.disponibilites:
            raise ValueError(f"Le medecin {self} doit avoir au moins un jour de disponibilité")
        if any(jour < 0 for jour in self.disponibilites):
            raise ValueError(f"Le medecin {self} ne peut pas avoir de valeurs négatives dans les disponibilités")


def jours_de_gardes(vacances: List[PeriodeVacance], nb_jours: int) -> Dict[int, str]:
    """
    Crée un dictionnaire indiquant les jours qui sont des jours de vacances, associés au nom de la période de vacance.

    ## Parameters:
        vacances (List[PeriodeVacance]): Liste des périodes de vacances, chacune avec un nom, un jour de début et une durée.
        nb_jours (int): Le nombre total de jours considérés pour l'analyse, ce nombre doit être positif.

    ## Raises:
        ValueError: Si la liste des périodes de vacances est vide.
        ValueError: Si le nombre de jours est inférieur ou égal à zéro ou est infini.

    ## Returns:
        Dict[int, str]: Un dictionnaire où chaque clé est un numéro de jour et chaque valeur est le nom de la période de vacance correspondante pour ce jour, ou une chaîne vide si ce n'est pas un jour de vacance.

    ## Example:
        >>> vacances = [PeriodeVacance("Noel", 5, 2), PeriodeVacance("Ete", 9, 3)]
        >>> nb_jours = 15
        >>> jours_vacances = jours_de_gardes(vacances, nb_jours)
        >>> print(jours_vacances)
        {1: '', 2: '', 3: '', 4: '', 5: 'Noel', 6: 'Noel', 7: '', 8: '', 9: 'Ete', 10: 'Ete', 11: 'Ete', 12: '', 13: '', 14: '', 15: ''}
    """
    if not vacances:
        raise ValueError("La liste des périodes de vacances ne peut pas être vide.")
    
    if nb_jours <= 0 or nb_jours == float("inf"):
        raise ValueError(f"Le nombre de jours doit être un entier positif, reçu: {nb_jours}")

    jdg = {i + 1: "" for i in range(nb_jours)}
    for vacance in vacances:
        for i in range(vacance.debut, vacance.debut + vacance.duree):
            jdg[i] = vacance.nom
    return jdg


def dispo_medecin(medecins: List[Medecin], nb_jours :int) -> Dict[int, List[int]]:
    """
    Crée un dictionnaire associant chaque jour aux identifiants des médecins disponibles ce jour-là.

    ## Parameters:
        medecins (List[Medecin]): Liste des médecins avec leurs jours de disponibilité. Chaque médecin doit avoir un identifiant unique et un ensemble de jours où ils sont disponibles.
        nb_jours (int): Le nombre total de jours considérés pour l'analyse, ce nombre doit être positif.

    ## Raises:
        TypeError: Si 'medecins' est None, indiquant que l'argument attendu n'est pas une liste.
        ValueError: Si 'medecins' est une liste vide, indiquant qu'aucun médecin n'est disponible pour être planifié.

    ## Returns:
        Dict[int, List[int]]: Un dictionnaire où chaque clé est un jour (représenté par un entier) et chaque valeur est une liste d'identifiants de médecins disponibles ce jour. Cela permet d'identifier rapidement quels médecins sont disponibles à chaque jour donné.

    ## Example:
        >>> medecins = [Medecin("Dr. VIDAL", {1, 3, 5}), Medecin("Dr. SENGEL", {2, 3})]
        >>> disponibilites = dispo_medecin(medecins)
        >>> print(disponibilites)
        {1: ["Dr. VIDAL"], 2: ["Dr. SENGEL"], 3: ["Dr. VIDAL", "Dr. SENGEL"], 5: ["Dr. VIDAL"]}
    """
    if medecins is None:
        raise TypeError("La liste des médecins doit être de type List[Medecin], reçu None")
    if not medecins:
        raise ValueError("La liste des médecins ne peut pas être vide.")

    dispo_med = {j : [] for j in range(1, nb_jours + 1)}
    for medecin in medecins:
        for jour in medecin.disponibilites:
            if jour not in dispo_med:
                dispo_med[jour] = []
            dispo_med[jour].append(medecin.id)
    return dispo_med


def trouver_emploi_du_temps(
    medecins: List[Medecin],
    vacances: List[PeriodeVacance],
    nb_jours: int,
    max_gardes: int
) -> pd.DataFrame:
    """
    Planifie l'emploi du temps des gardes pour les médecins sur une période donnée, en prenant en compte leurs disponibilités et les périodes de vacances spécifiées.

    ## Parameters:
        medecins (List[Medecin]): Liste des médecins avec leurs identifiants et disponibilités.
        vacances (List[PeriodeVacance]): Liste des périodes de vacances, avec un nom, un jour de début, et une durée pour chaque période.
        max_gardes (int): Le nombre maximum de gardes qu'un médecin peut avoir pendant la période spécifiée.
        nb_jours (int): Le nombre total de jours sur lesquels l'emploi du temps est planifié.

    ## Raises :
        ValueError: Si la durée de la plus grande période de vacances est supérieure au nombre de médecins.
        ValueError: Si il existe un jour sans médecin disponible (soit aucun médecin n'est disponible ce jour, soit les médecins disponibles ce jour ont atteint le nombre maximal de gardes)

    ## Returns:
        pd.DataFrame: Un DataFrame où les lignes représentent les jours et les colonnes les médecins, avec des marquages indiquant les jours où chaque médecin est en garde.

    ## Example:
        >>> medecins = medecins = [
    Medecin("Dr. MACHECOURT", {1, 2, 3, 4, 8, 9}),
    Medecin("Dr. SENGEL", {1, 2, 4, 5, 6, 7, 10}),
    Medecin("Dr. THEODORE", {2, 3, 5, 6, 7, 8}),
    Medecin("Dr. LECH", {3, 4, 6, 9, 10}),
    Medecin("Dr. VIDAL", {1, 5, 7, 8, 9, 10}),
    ]
        >>> vacances = [PeriodeVacance("Noel", 3, 2), PeriodeVacance("Ete", 8, 2)]
        >>> max_gardes = 3
        >>> nb_jours = 10
        >>> emploi_du_temps_df = trouver_emploi_du_temps(medecins, vacances, 2, 6)
        >>> print(emploi_du_temps_df)
                        Dr. MACHECOURT Dr. SENGEL Dr. THEODORE Dr. LECH Dr. VIDAL
        Jour 1                   X          -            -        -         -
        Jour 2                   -          X            -        -         -
        Jour 3 Noel              -          -            X        -         -
        Jour 4 Noel              -          -            -        X         -
        Jour 5                   -          -            -        -         X
        Jour 6                   -          X            -        -         -
        Jour 7                   -          -            X        -         -
        Jour 8 Ete               X          -            -        -         -
        Jour 9 Ete               -          -            -        X         -
        Jour 10                  -          -            -        -         X
    """
    duree_max_vac = max(v.duree for v in vacances) if vacances else 0
    if len(medecins) < duree_max_vac:
        raise ValueError(f"Nombre de médecins insuffisant pour couvrir la plus longue période de vacances de {duree_max_vac} jours.")

    jours_garde = jours_de_gardes(vacances, nb_jours)
    dispo_medecins = dispo_medecin(medecins, nb_jours)
    emploi_du_temps = {med.id: ["-"] * (nb_jours) for med in medecins}
    gardes_vacance = {med.id: {v.nom: False for v in vacances} for med in medecins}
    gardes_count = {med.id: 0 for med in medecins}

    for jour in range(1, nb_jours + 1):
        vacance_nom = jours_garde[jour]
        medecins_jour = [
            (med_id, gardes_count[med_id])
            for med_id in dispo_medecins.get(jour, [])
            if gardes_count[med_id] < max_gardes
        ]
        medecins_jour.sort(key=lambda x: x[1]) 

        if not medecins_jour:
            raise ValueError(f"Aucun médecin disponible pour le jour {jour}, impossible de compléter l'emploi du temps.")

        for med_id, _ in medecins_jour:
            if all(emploi_du_temps[m][jour - 1] == "-" for m in emploi_du_temps):
                if vacance_nom:
                    if not gardes_vacance[med_id][vacance_nom]:
                        gardes_vacance[med_id][vacance_nom] = True
                        emploi_du_temps[med_id][jour-1] = "X"
                        gardes_count[med_id] += 1
                        break
                    else :
                        raise ValueError(f"Les médecins disponibles pour {vacance_nom} ont déjà réalisé leur jour de garde et des jours sont encore sans médecins.")
                else:
                    emploi_du_temps[med_id][jour-1] = "X"
                    gardes_count[med_id] += 1
                    break

    index_labels = [f"Jour {j} {jours_garde[j]}" if jours_garde[j] else f"Jour {j}" for j in range(1, nb_jours + 1)]
    df = pd.DataFrame(emploi_du_temps, index=index_labels)
    return df
