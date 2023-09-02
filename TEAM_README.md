# UniversalConverterLatex 🚀

Un nouvelle manière de dessiner avec Latex.

Le site est accessible via http://localhost:8000/app/
Pour le moment, on peut convertir un fichier .tex contenu dans app/templates/app/test.tex en se rendant sur http://localhost:8000/app/latex


<details>
 <summary><strong>Table des matières</strong> (cliquer pour en savoir plus)</summary>

* [Installation et Usage](#-installation)
* [Latex, ça prend de la place](#-latex)
* [Explications de l'arborescence des fichiers](#-arborescence)
* [Petit tuto git](#-git)
</details>


## 💾 Installation et Usage

### Système Linux

Pour installer le docker sur votre machine :

```bash
make build
```
Pour le lancer :

```bash
make run
```

Pour le stopper :

```bash
make stop
```

Pour lancer un bash python (UTILE) :

```bash
make python
```

Pour migrer la base de données, c'est-à-dire enregistrer les ajouts fait dans app/models :

```bash
make db-migrate
```

Pour construire une nouvelle base de données avec les dernières structures migrées :

```bash
make db-update
```

Pour vous connecter à la base de données postgresql (il vous faut postgresql sur votre machine) :

```bash
make db-psql
```

Pour lancer les tests unitaires :

```bash
make test
```

Pour créer un profil administrateur, accessible à l'adresse http://localhost:8000/admin  :

```bash
make admin
```


### Docker

Quelques infos utiles si vous galérez avec docker :

Pour voir toutes les images docker présentes sur votre machine :
```
docker images
```

Certaines images anciennes, peuvent être inutiles et prendre de la place sur votre machine. Pour les retirer :

```
docker rmi <IMAGE ID>
```

De la même manière, pour voir tous les conteneurs installés sur votre machine :
```
docker ps -a
```

Pour en éliminer certains :

```
docker rm <CONTAINER ID>
```

Pour rentrer dans votre docker (UTILE) :

```
docker exec -it <CONTAINER ID de "universalconverterlatex_web_1"> bash
```

## 💾 Latex, ça prend de la place

Le docker installe tout latex (avec la commande RUN apt-get install -y texlive-full).
Cela prend BEAUCOUP DE TEMPS, car c'est un TRES GROS PACKAGE.
Si vous voulez éviter cela,  vous pouvez remplacer texlive-full (dans le Dockerfile) par un plus petit package, mais attention vous risquez de ne pas tout avoir. Voici la liste des packages à disposition, avec leur taille associée :

    texlive-base - 136 MB
    texlive-latex-recommended - 177 MB
    texlive - 240 MB
    texlive-latex-extra - 404 MB
    texlive-full - 4714 MB

## 💾 Arborescence des fichiers

    |--  .eggs : je sais pas, ça ne doit pas être important ;)
    |--  .nuxt : fichier de Baelish, pour le moment c'est pas lié
    |--  app : toute notre app est la dedans pour le moment !
            |-- migrations : dès qu'on valide les modifs faites sur la base de données avec 'make db-migrate', les fichiers vont là
            |-- static/app : pour le css, les polices, etc
            |-- templates/app : pour les pages web sous forme de templates et les fichier .tex
            |-- __init__.py : pour faire comprendre qu'on est dans package latex
            |-- admin : pour custom l'interface de l'admin
            |-- apps.py : pour la configuration de l'app
            |-- models.py : là ou l'on crée la base de données
            |-- test.py : là ou l'on place nos tests
            |-- urls.py : là ou l'on définit nos urls
            |-- views.py : là ou l'on définit nos vues
    |--  django_tex : bibliothèque qui permet de faire du .tex -> .pdf
    |--  public : ce n'est plus utile, car on place nos templates dans app/templates/app (plus propre)
    |--  Rapport-diteration : ...
    |--  templates : ici, c'est pour changer la tête de l'interface admin
    |--  test : ici, ce sont les tests de django_tex, on peut le remove
    |--  universalConverterLatexSite : ici, c'est un peu la carte d'identité de notre site avec les packages à installer, etc.
    Le reste est trivial.

## 💾 Petit tuto git

Les branches et le remisage
-----------

Les branches permettent de diviser l'espace de travail et ainsi mieux l'organiser. Une branche est simplement un ensemble de commits.

La commande suivante permet de voir les branches que vous possédez :
```
git branch
```

Vous pouvez vous déplacer sur n'importe quelle branche avec la commande suivante :
```
git checkout <nom_de_la_branche>
```


Lorsque vous créer une branche, vous aller tout simplement créer un endroit clôt avec pour base un ensemble de commits. Cet ensemble de commit est celui de la branche à partir de laquelle vous aller créer votre nouvelle branche !

Pour créer une branche :
```
git checkout -b <nom-de-votre-branche>
```


*************

Pour déplacer votre travail d'une branche à l'autre, vous pouvez utiliser le remisage !

Le principe de remisage est simple. Avec la commande ...
```
git stash
```
... vous allez sauvergarder votre travail et le retirer de la branche sur laquelle vous êtes !

Ce travail n'est pas perdu, il se situe sur une pile que vous pouvez observer avec la commande :
```
git stash list
```

Ensuite vous allez vous rendre sur la branche sur laquelle vous souhaitez travailler avec la commande :
```
git checkout <nom_de_la_branche>
```

Enfin, libérer votre travail de la pile avec une des deux commandes suivantes au choix :
```
git stash pop    => Retire votre travail de la pile et l'applique à la branche

git stash apply  => Ne retire pas votre travail de la pile et l'applique à la branche
```

*************

Il peut être aussi intéressant de récupérer les branches créées par vos collègues !
Pour cela, une commande :

```
git fetch
```

******************

Pour pusher une branche, rien de plus simple :
```
git push origin <nom-de-votre-branche>
```
En fait, lorsque vous êtes sur la branche master, on a l'équivalence suivante :
```
git push origin master
git push
```


Enfin, pour appliquer l'historique des commits d'une branche sur la votre, effectuez la commande suivante :

```
git rebase origin/<branche-sur-laquel-vous-voulez-vous-baser>
```

Les merge request
-----------

Sur gitlab, vous pouvez effectuer des merge request. Le principe est simple, vous allez tout simplement appliquer les changements apportés par la branche sur une autre branche, le plus souvent master :

```
Request to merge molecule-and-some-general-functions into master 
```

Ici, une personne veut merger la branche **molecule-and-some-general-functions** sur **master** par exemple.

Si il n'y a aucun conflits, on peut merger !
Pour cela, il suffit d'appuyer sur le bouton merge.
Certaines options sont présentes lors d'un merge :

 * remove source branch : pour enlever la branche qu'on merge, souvent c'est ce que l'on fait
 * squash commits : permet de réunir tout les commits en un seul, peut être utile si il y a plein de petits commits sur la branche !


Bonus : Cherry-pick
-----------

Commande simple et puissante, elle permet d'appliquer un commit, n'importe lequel, à la branche sur laquelle vous vous trouvez.

```
git cherry-pick <hash_du_commit_a_appliquer>
```