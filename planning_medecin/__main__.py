import json
import os
from typer import Typer
from rich.console import Console
from rich.table import Table
from planning_medecin.lib_hp import Medecin, PeriodeVacance, trouver_emploi_du_temps

app = Typer()
console = Console()


def get_data():
    """Récupère les données nécessaires pour la génération du planning."""
    medecins = [
        Medecin("Dr. MACHECOURT", {1, 2, 3, 4, 8, 9}),
        Medecin("Dr. SENGEL", {1, 2, 4, 5, 6, 7, 10}),
        Medecin("Dr. THEODORE", {2, 3, 5, 6, 7, 8}),
        Medecin("Dr. LECH", {3, 4, 6, 9, 10}),
        Medecin("Dr. VIDAL", {1, 5, 7, 8, 9, 10}),
    ]
    vacances = [PeriodeVacance("Noel", 3, 2), PeriodeVacance("Ete", 8, 2)]
    return medecins, vacances


@app.command()
def demo():
    """Génère un fichier demonstration.json contenant les critères."""
    medecins, vacances = get_data()
    data = {
        "medecins": [
            {"id": med.id, "disponibilites": list(med.disponibilites)}
            for med in medecins
        ],
        "vacances": [
            {"nom": vac.nom, "debut": vac.debut, "duree": vac.duree} for vac in vacances
        ],
    }
    with open("demonstration.json", "w") as file:
        json.dump(data, file, indent=2)


@app.command()
def view(chemin: str):
    """Visualise les critères à partir d'un fichier JSON."""
    with open(chemin, "r") as file:
        data = json.load(file)
    medecins = data["medecins"]
    vacances = data["vacances"]
    display_criteria(medecins, vacances, 10, 3)


@app.command()
def solve(chemin: str):
    """Résout le planning des gardes à partir d'un fichier JSON."""
    with open(chemin, "r") as file:
        data = json.load(file)
    medecins = [
        Medecin(med["id"], set(med["disponibilites"])) for med in data["medecins"]
    ]
    vacances = [
        PeriodeVacance(vac["nom"], vac["debut"], vac["duree"])
        for vac in data["vacances"]
    ]
    emploi_du_temps_df = trouver_emploi_du_temps(medecins, vacances, 10, 3)
    display_planning(emploi_du_temps_df)


@app.command()
def appli():
    """Lance l'application Streamlit."""
    os.system("streamlit run planning_medecin/app.py")

def display_criteria(medecins, vacances, nb_jours, max_gardes):
    """Affiche les critères de planification dans une table formatée."""
    table = Table(title="Critères de la Planification des Gardes")
    table.add_column("Type", justify="right", style="cyan", no_wrap=True)
    table.add_column("Détails", style="magenta")
    medecin_details = "\n".join(
        [f"{med['id']}: {sorted(med['disponibilites'])}" for med in medecins]
    )
    table.add_row("Médecins", medecin_details)
    vacances_details = "\n".join(
        [
            f"{vac['nom']}: Jour début {vac['debut']}, Durée {vac['duree']} jours"
            for vac in vacances
        ]
    )
    table.add_row("Vacances", vacances_details)
    table.add_row("Nombre total de jours", str(nb_jours))
    table.add_row("Max gardes par médecin", str(max_gardes))
    console.print(table)


def display_planning(emploi_du_temps_df):
    """Affiche le planning des gardes dans une table formatée."""
    table = Table(title="Planning des Gardes")
    columns = ["Jour"] + list(emploi_du_temps_df.columns)
    for col in columns:
        table.add_column(col)
    for index, row in emploi_du_temps_df.iterrows():
        table.add_row(index, *[str(val) for val in row.values])
    console.print(table)


if __name__ == "__main__":
    app()
