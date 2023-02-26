from rich.console import Console
from rich.table import Table
from rich.traceback import install
import configparser
import os
import random


class MathPerso:
    def __init__(self, nom_config: str = "config.cfg"):
        # Déclaration de variables
        self.nom_config = nom_config
        self.NOMBRE_MIN = 1
        self.NOMBRE_MAX = 10
        self.nb_questions = 10
        self.nom_joueur = "Joueur"
        self.operateur = 0
        self.nombre1 = 0
        self.nombre2 = 0
        self.score = 0
        self.operateur_str = ""
        self.reponse_calc = 0

        # Construction d'objet
        install()
        self.console = Console(force_terminal=True,color_system="auto",emoji=True)
        self.config = configparser.ConfigParser(comment_prefixes='#', allow_no_value=True)
        self.table = Table(show_header=True, header_style="bold magenta")
        self.table.add_column("opération", justify="center")
        self.table.add_column("Réponse joueur", justify="center")
        self.table.add_column("Bonne réponse", justify="center")
        self.table.add_column("Status", justify="center")

    def tirage_hasard(self):
        self.nombre1 = random.randint(self.NOMBRE_MIN, self.NOMBRE_MAX)
        self.nombre2 = random.randint(self.NOMBRE_MIN, self.NOMBRE_MAX)

        self.operateur = random.randint(0, 2)
        if self.operateur == 2 and self.nombre1 < self.nombre2:
            self.nombre1, self.nombre2 = self.nombre2, self.nombre1

        if self.operateur == 0:
            self.operateur_str = "+"
            self.reponse_calc = self.nombre1 + self.nombre2
        elif self.operateur == 1:
            self.operateur_str = "X"
            self.reponse_calc = self.nombre1 * self.nombre2
        elif self.operateur == 2:
            self.operateur_str = "-"
            self.reponse_calc = self.nombre1 - self.nombre2

    def poser_question(self):
        self.tirage_hasard()
        while True:
            reponse_str = input(f"Combien font {self.nombre1} {self.operateur_str} {self.nombre2} : ")
            try:
                reponse_int = int(reponse_str)
            except ValueError:
                print("Erreur : votre réponse n'est pas valide. Veuillez saisir un nombre ou un chiffre.")
            else:
                break

        if self.reponse_calc == reponse_int:
            print("[green]Bonne réponse[/green]")
            print()
            self.table.add_row(str(self.nombre1) + " " + self.operateur_str + " " + str(self.nombre2),
                               reponse_str, str(self.reponse_calc), "✅")
            return True
        print("[red]Mauvaise réponse[/red]")
        print(f"La bonne réponse est : {self.reponse_calc}")
        print()
        self.table.add_row(str(self.nombre1) + " " + self.operateur_str + " " + str(self.nombre2),
                           reponse_str, str(self.reponse_calc), "❌")
        return False

    def get_nom_joueur(self):
        return self.nom_joueur

    def set_non_joueur(self, nom: str):
        self.nom_joueur = nom

    def get_nb_question(self):
        return self.nb_questions

    def set_nb_question(self, nb_questions: int):
        self.nb_questions = nb_questions

    def get_score(self):
        return self.score

    def increase_score(self, increment: int = 1):
        try:
            self.score += int(increment)
            return True
        except ValueError:
            self.score += 1
            return False

    def afficher_score(self):
        clear_screen()
        self.affiche_tab()
        moyenne = int(self.nb_questions / 2)
        print(f"Votre score est de : {self.score}/{self.nb_questions}")
        if self.score == self.nb_questions:
            self.console.print(f"[green]Félicitation[/green] {self.nom_joueur} !! Vous avez trouvé toutes les réponses. :cake:")
        elif self.score == 0:
            self.console.print(f"Désolé {self.nom_joueur} !! Vous n'avez trouvé aucunes bonnes réponses.")
            self.console.print("Vous devriez réviser vos maths. :pile_of_poo:")
        elif self.score > moyenne:
            self.console.print(f"Pas mal {self.nom_joueur}, Vous êtes au-dessus de la moyenne. :smiley:")
        elif self.score < moyenne:
            self.console.print(f"Vous pouvez mieux faire {self.nom_joueur}, Vous êtes en dessous de la moyenne. :raccoon:")
        elif self.score == moyenne:
            self.console.print(f"Tout juste la moyenne {self.nom_joueur} :vampire:, vous pouvez mieux faire.")

        print()

    def load_config(self):
        try:
            with open(self.nom_config, "r") as file:
                self.config.read_file(file)
                self.nom_joueur = self.config.get("main", "nom", fallback="Joueur")
                self.NOMBRE_MAX = self.config.getint("main", "maxi", fallback=10)
                self.nb_questions = self.config.getint("main", "nb_questions", fallback=10)
            return True
        except (FileNotFoundError, configparser.NoSectionError, configparser.NoOptionError,
                configparser.MissingSectionHeaderError):
            print("Erreur de lecture du fichier, écriture des valeurs par défaut.")
            self.NOMBRE_MAX = 10
            self.nb_questions = 10
            self.nom_joueur = "Joueur"
            self.save_config()
            return False
        except ValueError:
            print("L'un des paramètres numériques est incorrecte. Utilisation des valeurs par défaut.")
            self.NOMBRE_MAX = 10
            self.nb_questions = 10
            self.save_config()
            return False

    def save_config(self):
        if os.path.exists(self.nom_config):
            os.remove(self.nom_config)
        try:
            with open(self.nom_config, "w") as file:
                if not self.config.has_section("main"):
                    self.config.add_section("main")
                self.config.set('main', "# Entrez ci-dessous le nom du joueur.")
                self.config.set("main", "nom", self.nom_joueur)
                self.config.set('main', "# Entrez ci-dessous le nombre maximal dans une opération.")
                self.config.set("main", "maxi", str(self.NOMBRE_MAX))
                self.config.set('main', "# Entrez ci-dessous le nombre d'opérations.")
                self.config.set("main", "nb_questions", str(self.nb_questions))
                self.config.write(file)
        except (FileNotFoundError, PermissionError):
            print("Erreur d'écriture du fichier")

    def affiche_tab(self):
        print()
        self.table.title = self.nom_joueur
        self.console.print(self.table)
        print()