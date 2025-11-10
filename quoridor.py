"""Module Quoridor

Functions:
    * interpréter_la_ligne_de_commande - Génère un interpréteur de commande.
    * formater_entête - Formater la représentation graphique du damier.
    * formater_le_damier - Formater la représentation graphique de la légende.
    * formater_le_jeu - Formater la représentation graphique d'un jeu.
    * sélectionner_un_coup - Demander le prochain coup à jouer au joueur.
"""

import argparse


def interpréter_la_ligne_de_commande():
    """Génère un interpréteur de commande.

    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
                   Cette objet aura l'attribut «idul» représentant l'idul du joueur.
    """
    parser = argparse.ArgumentParser()

    # Complétez le code ici
    # vous pourriez aussi avoir à ajouter des arguments dans ArgumentParser(...)
    parser.add_argument("idul", type=str, help="L'idul du joueur.")

    return parser.parse_args()


def formater_entête(joueurs):
    """Formater la représentation graphique de la légende.

    Args:
        joueurs (list): Liste de dictionnaires représentant les joueurs.

    Returns:
        str: Chaîne de caractères représentant la légende.
    """
    resultat = "Légende:\n"
    i=1
    liste = []
    for joueur in joueurs:
        liste.append(joueur["nom"])
                       
    for joueur in joueurs:
        if len(liste[0]) > len(liste[1]):
            if i == 1:
                ch = "   " + str(i) + "=" + joueur["nom"] + ",    murs=" + " ".join("|"*joueur["murs"]) + "\n"
                resultat += ch
            else:
                a = len("   " + str(i) + "=" + liste[0] + ",") - len("   " + str(i) + "=" + liste[1] + ",") 
                resultat += "   " + str(i) + "=" + joueur["nom"] + "," + " "*(4 + a) +  "murs=" + " ".join("|"*joueur["murs"]) + "\n"
                
        else:
            if i == 1:
                b = len("   " + str(i) + "=" + liste[1] + ",") - len("   " + str(i) + "=" + liste[0] + ",") 
                ch = "   " + str(i) + "=" + joueur["nom"] + "," + " "*(4 + b) +   "murs=" + " ".join("|"*joueur["murs"]) + "\n"
                resultat += ch
            else:
                resultat += "   " + str(i) + "=" + joueur["nom"] + ",    murs=" + " ".join("|"*joueur["murs"]) + "\n"
            
        i+=1
    print(resultat)


def formater_le_damier(joueurs, murs):
    """Formater la représentation graphique du damier.

    Args:
        joueurs (list): Liste de dictionnaires représentant les joueurs.
        murs (dict): Dictionnaire représentant l'emplacement des murs.

    Returns:
        str: Chaîne de caractères représentant le damier.
    """
    
    NB = 9                     # dimension du plateau
    CELLW = 3                  # largeur d'une case (pour centrer un symbole)
    DOT = '.'                  # ce qui est dessiné dans une case vide

    # ---- 1) canevas modifiable (liste de lignes, chaque ligne = liste de caractères)
    lines = []

    # Bordure supérieure (esthétique)
    inner_width = 2 + (CELLW + 1) * NB + 1  # | + ( " xxx" * NB ) + |  (approx)
    top_border = " " * 2 + "-" * (inner_width - 1)
    lines.append(list(top_border))

    # Une ligne "cases" et une ligne "interstice" entre chaque rangée
    def row_line(label):
        # ex: "9 | .   .   .   ... |"
        left = f"{label} "
        core = ["|"]
        for _ in range(NB):
            core.append(" ")
            core.append(DOT.center(CELLW))
        core.append(" ")
        core.append("|")
        return list(left + "".join(core))

    def gap_line():
        # interstice pour murs horizontaux, même largeur que row_line (sans le label)
        left = "  "
        core = ["|", " " * ((CELLW + 1) * NB + 1), "|"]
        return list(left + "".join(core))

    for r in range(NB, 0, -1):
        lines.append(row_line(r))
        if r > 1:
            lines.append(gap_line())

    # ---- 2) indices du bas
    bottom_border = " -|" + "-" * ((CELLW + 1) * NB + 1)
    numbers_line = "   " + "   ".join(str(i) for i in range(1, NB + 1))
    lines.append(list(bottom_border))
    lines.append(list(numbers_line))

    # ---- 3) utilitaires pour trouver les index dans le canevas
    # ligne de cases pour la rangée r :
    def line_index_for_row(r):
        # top_border = 0, puis rangée 9 = 1, interstice, rangée 8 = 3, ...
        return 1 + 2 * (NB - r)

    # première colonne de la case c dans une "row_line"
    def char_index_for_col(c):
        # "  | xxx xxx ... xxx |"
        return 4 + (c - 1) * (CELLW + 1)  # 2 (label) + 1 (espace) + 1 (|) = 4

    # ---- 4) placer les joueurs (1, 2, …)
    for idx, j in enumerate(joueurs, start=1):
        r, c = j["position"]
        if 1 <= r <= NB and 1 <= c <= NB:
            li = line_index_for_row(r)
            ci = char_index_for_col(c)
            txt = str(idx).center(CELLW)
            for k, ch in enumerate(txt):
                lines[li][ci + k] = ch

    # ---- 5) dessiner les murs
    # horizontaux : sur la ligne d'interstice au-dessous de la rangée r
    for r, c in murs.get("horizontaux", []):
        if 1 <= r <= NB - 1 and 1 <= c <= NB - 1:
            inter_line = line_index_for_row(r) + 1  # ligne interstice
            start_ci = char_index_for_col(c)
            span = (CELLW + 1) * 2 - 1              # couvre 2 “cases” et l'espace
            for dx in range(span):
                lines[inter_line][start_ci + dx] = "-"

    # verticaux : une “barre” qui traverse la row r et l’interstice au-dessus
    for r, c in murs.get("verticaux", []):
        if 1 <= r <= NB - 1 and 1 <= c <= NB:
            row_li = line_index_for_row(r)
            gap_li = row_li - 1                     # interstice au-dessus
            ci = char_index_for_col(c) - 1          # position entre deux cases
            lines[row_li][ci] = "|"
            lines[gap_li][ci] = "|"

    # ---- 6) retour chaîne
    return "\n".join("".join(L) for L in lines)


def formater_le_jeu(état):
    """Formater la représentation graphique d'un jeu.

    Doit faire usage des fonctions formater_entête et formater_le_damier.

    Args:
        état (dict): Dictionnaire représentant l'état du jeu.

    Returns:
        str: Chaîne de caractères représentant le jeu.
    """
    message = ""
    message += formater_entête(état["joueurs"]) + "\n"
        # Damier (utilise ta fonction précédente)
    message += formater_le_damier(état["joueurs"], état["murs"]) + "\n"

    return message


def sélectionner_un_coup():
    """Sélectionner un coup

    Returns:
        tuple: Un tuple composé d'un type de coup et de la position.
               Le type de coup est une chaîne de caractères.
               La position est une liste de 2 entiers [x, y].
    Examples:
        Quel coup voulez-vous jouer? ('D', 'MH', 'MV') : D
        Donnez la position du coup à jouer ('x, y') : 2, 6
    """
    coup = input("Quel coup voulez-vous jouer? ('D', 'MH', 'MV') : ")
    position = input("Donnez la position du coup à jouer ('x, y') : ")
    k =0
    for i in position:
        if i == ' ':
            position = position[0:k] + position[k + 1:len(position)]
        k+=1
    while coup not in ['D', 'MH', 'MV']:
        coup = input("Quel coup voulez-vous jouer? ('D', 'MH', 'MV') : ")
    while position[0] not in ['0','1','2','3','4','5','6','7','8'] or position[2] not in ['0','1','2','3','4','5','6','7','8'] or position[1] != ',' or len(position) != 3:
        position = input("Donnez la position du coup à jouer ('x, y') : ")
    
    return coup, [int(position[0]), int(position[2])]
    
    
