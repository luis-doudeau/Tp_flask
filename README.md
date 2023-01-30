# Tp_flask

## DOUDEAU Luis
## DE NARDI Lenny

0/ Placer vous à la racine du projet
1/ pip install -r requirement.txt
2/ cd tuto/
3/ flask run 
4/ Cliquez sur ctrl + le lien dans le terminal (127.0.0.1/5000)


# Fonctionalités Totalement Réalisées :

1/ Affichage paginé livres, détails (au click ou au survol)\
2/ Intégration Bootstrap ou autre lib de CSS\
3/ Edition/Suppression/Update Auteurs (modification se fait en double clickant sur la ligne du auteur)\
4/ Edition/Suppression/Update Livres  (modification se fait en double clickant sur la ligne du livre)\
5/ Recherche avancée dans les albums (par auteur, titre, prix, etc.). Bouton Filtre en vert. \
6/ commande d'import de données (loaddb). Dans le fichier commands.py\
7/ commande de création des tables (syncdb). Dans le fichiers commandes.py\


# Fonctionalités En partie Réalisées :

1/ Login (commandes newuser, password) avec limitation des pages d'édition aux utilisateurs authentifiés.\
Nous avons implémenté les méthodes : Classe LoginForm avec get_authenticated_user, Classe User, et méthodes newuser ainsi que passwd.

Nous avons enlevé les @login_required de notre fichiers views.py afin que vous puissiez tout de même consulter le module Admin.\
