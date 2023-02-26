import os
import sys

from rich import print

from fonctions import clear_screen
from mathperso import MathPerso


def main():
    clear_screen()
    jeu = MathPerso()
    jeu.load_config()
    print(f"Bonjour {jeu.get_nom_joueur()} et bienvenu dans la version 1.00 du jeu de math.")
    print()
    for i in range(jeu.get_nb_question()):
        print(f"Question {i + 1}/{jeu.get_nb_question()} :")
        if jeu.poser_question():
            jeu.increase_score()
    jeu.afficher_score()
    if os.name == 'nt':
        print("Appuyez sur une Entrée pour mettre fin au programme.")
        sys.stdin.read(1)


if __name__ == "__main__":
    main()
