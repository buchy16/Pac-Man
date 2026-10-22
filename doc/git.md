#### Table of Contents

[BRANCHES](<#branches>)

+ [APRES suppression d'une branche depuis GITHUB](<#apres-suppression-dune-branche-depuis-github>)
+ [Mettre à jour les branches locales avec `main`](<#mettre-à-jour-les-branches-locales-avec-main>)
+ [Erreur git switch](<#pb-pour-changer-de-branche>)

[PULL REQUEST](<#pull-request>)

[Issues](<#issues>)

*[Back to top](<#table-of-contents>)*

---

# Branches

+ Mettre à jour le `main` AVANT de créer une branche :
```bash
git switch main
git pull
```

+ créer une nouvelle branche :
```bash
git branch <my_new_branch>
```
+ basculer sur une branche existante :
```bash
git switch my_branch
```

+ ou bien, **créer et basculer** en 1 seule commande :
```bash
git switch -c my_new_branch
```

## APRES suppression d'une branche depuis GITHUB
Il faut la supprimer en local :

```bash
git switch main
git pull origin main # récupère le merge fait sur GitHub
git branch -d my_branch # supprime la branche locale

# le Git local garde en mémoire la référence distante obsolète
git fetch --prune # purger ces références mortes

# Vérifier que l'espace est propre 
git branch -a
# my_branch` et `origin/my_branch` doivent avoir totalement disparu.
```

## Mettre à jour les branches locales avec `main`

Au préalable, s'assurer d'avoir un répertoire de travail propre : `commit` ou `stash` tous les changements.

Puis mettre à jour `main` en local :
```bash
git switch main
git pull origin main # récupère toutes les nouveautés de `main` depuis Github
# donc les merges ainsi que les commits directs des binômes
```

puis pour chaque branche `my_branch` à mettre à jour en local :
```bash
git switch my_branch
git merge main
```
=> Ainsi, toutes les branches vont fusionner exactement la même version :)

(*en cas de conflit : les résoudre, puis `git add <fichiers>` et `git commit`*)

Si la branche existe aussi sur GitHub :
```bash
git push
```

*[Back to top](<#table-of-contents>)*

## PB pour changer de branche

par ex `git switch main` provoque cette erreur :
```bash
error: Your local changes to the following files would be overwritten by checkout:
[liste_des_fichiers]
Please commit your changes or stash them before you switch branches.
Aborting
```
=> signifie que des modifs (non commitées) sur les fichiers listés seraient écrasées par leur version présente sur `main`.

Pour VOIR ces modifs :
```bash
git diff main
```
+ rouge = code actuellement sur la branche main, mais supprimé ou modifié depuis le dernier commit.
+ vert = code en local, qui écraserait main si on force le passage

#### SOLUCE 1
```bash
# Garder ces modifications car elle ont du sens sur cette branche :
git add fichier1 fichier2
git commit -m "blabla"

# et plus tard si besoin :
git push
```

#### SOLUCE 2
```bash
# Mettre ces modifications de côté temporairement :
git stash
#  ou bien pour inclure les nouveaux fichiers non suivis :
git stash -u

# et pour les récupérer plus tard, sur une branche `quelconque` :
git switch quelconque
git stash pop
```

#### SOLUCE 3
```bash
# Supprimer définitive ces modifications, bonnes pour la poubelle :
git restore fichier1 fichier2
```

Dans les 3 cas, `git switch main` ne devrait plus poser de souci :D

*[Back to top](<#table-of-contents>)*

# Pull request

## Création

Passer par une Pull Request (PR) est une bonne pratique :
+ évite d'altérer `main` directement,
+ force la revue de code.

=> A faire depuis la page d'accueil du dépôt GitHub.

#### Compare 
+ Vérifier la comparaison des branches (en haut : `base : main` <- `compare : my_branch`).

#### Renseigner la demande
+ **Titre** : concis et explicite (par ex `feat : ajout du module X`).
+ **Description** : résumé précis des modifications apportées, logique retenue, ce qui doit être testé... (si usage des [issues](<#issues>), ajouter un mot-clé de fermeture, par ex `Fixes #34`).
+ **Reviewers** : sélectionner les collègues dans le panneau latéral à droite.

#### Créer la PR
+ `Create pull request`.

## Résolution

+ inspecter les différences (*diff*) dans l'onglet `Files changed`,
+ commenter des lignes précises,
+ `Review changes` pour valider ou demander des ajustements.

## Conflits (snifff...)
Si le bouton de fusion est bloqué à cause de modifications concurrentes :
```bash
# Récupérer les nouveautés de `main` en local
git fetch
git merge origin/main

# Résoudre les conflits dans l'éditeur de code

# Pousser les modifications pour mettre à jour la PR et débloquer la situation
git push
```

## Fusion et nettoyage
Une fois la PR approuvée et sans conflits :
+ `Merge pull request` et `Confirm merge`,
+ pour supprimer la branche distante et garder le dépôt propre, `Delete branch`.

+ [synchroniser en local](<#apres-suppression-dune-branche-depuis-github>)

*[Back to top](<#table-of-contents>)*

# et d'autres trucs...

## Issues

### Fonctionnement

#### Tickets (*Issues*)
Sur GitHub, l'onglet Issues sert à lister les tâches, les bugs à corriger ou les nouvelles fonctionnalités.
=> Chaque ticket créé reçoit automatiquement un numéro unique d'identification (par ex: `#12`).

#### Lien avec Pull Request
On ouvre une Pull Request pour le code qui règle le problème précis du ticket.
=> En incluant le mot exact `Closes #12` dans le champ de description de cette PR, GitHub crée instantanément un lien cliquable entre la PR et le ticket.

#### Automatisation à la fusion
Le ticket reste ouvert tant que la PR est en phase de revue, puis au moment du `Merge pull request` GitHub détecte le mot-clé et passe automatiquement le statut du ticket de *Open* à *Closed*.

### Intérêt

* **Traçabilité :** N'importe quel collègue qui consulte le ticket à l'avenir verra exactement quel bloc de code a résolu le problème.
* **Propreté :** Personne n'oublie de fermer les tâches terminées. Le tableau de bord du projet reste à jour sans aucun effort administratif manuel.

*[Back to top](<#table-of-contents>)*