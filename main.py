"""Jeu Quoridor

Ce programme permet de joueur au jeu Quoridor.
"""

from api import appliquer_un_coup, créer_une_partie, récupérer_une_partie
from quoridor import (
    formater_le_jeu,
    interpréter_la_ligne_de_commande,
    sélectionner_un_coup,
)

# Mettre ici votre IDUL comme clé et votre Jeton comme secret.
JETONS = {
    "votre_idul": "votre_secret",
}


if __name__ == "__main__":
    args = interpréter_la_ligne_de_commande()
    secret = JETONS[args.idul]
    id_partie, état = créer_une_partie(args.idul, secret)
    while True:
        # Afficher la partie
        print(formater_le_jeu(état))
        # Demander au joueur de choisir son prochain coup
        coup, position = sélectionner_un_coup()
        try:
            # Envoyer le coup au serveur
            coup, position = appliquer_un_coup(
                id_partie,
                coup,
                position,
                args.idul,
                secret,
            )
        except StopIteration as erreur:
            # Si le jeu est terminé
            # Récupérer la partie finale
            id_partie, état = récupérer_une_partie(
                id_partie,
                args.idul,
                secret,
            )
            # Afficher la partie finale
            print(formater_le_jeu(état))
            # Afficher le gagnant
            print(f"Le gagnant est {erreur}")
            # Sortir de la boucle
            break

        # Récupérer la partie à jour
        id_partie, état = récupérer_une_partie(
            id_partie,
            args.idul,
            secret,
        )

