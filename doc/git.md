#### ToC
ToDo

*[Back to top](<#toc>)*


---

Nouvelle branche

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
git switch my_new_branch
```

+ ou bien, **créer et basculer** en 1 seule commande :
```bash
# commande historique (`checkout` sert à la fois à changer de branche et à restaurer des fichiers)
git checkout -b new_branch
# ou bien syntaxe moderne, `switch` est dédié uniquement à la navigation entre les branches
git switch -c new_branch
```
*[Back to top](<#toc>)*

---

AVANT une pull request, mettre à jour la branche locale avec `main`
pour s'assurer que la branche n'est pas obsolète et qu'il n'y a pas de conflits non résolus :
```bash
# ne pas oublier ce push, sinon le pull main ne passera pas...
git push # pour `git push origin my_branch`

# pour recup du main en local
git switch main
git pull origin main # fusionne les modifs du `main` distant vers le `main` local

# pour fusion -EN LOCAL- du main mis à jour dans my_branch
git switch my_branch
git merge main  # ctrl + X (Merge made by the 'ort' strategy)
```
=> vérifier que ca n'a rien cassé, re-puh :
```bash
git push origin my_branch
```
et *enfin* let's go pour la pull request :D
*[Back to top](<#toc>)*

---

Faire une Pull Request
*Le passage par une Pull Request (PR) est la bonne méthode : cela évite d'altérer `main` directement et force la revue de code.*

Après avoir poussé la branche `my_branch` sur GitHub, le reste se passe principalement sur l'interface web de GitHub

1. Compare & pull request
 + **Compare & pull request** si le push est très récent
Sinon :
 + **« Pull requests »** / **« New pull request »**
 + Vérifier la comparaison des branches en haut : `base: main` $\leftarrow$ `compare: my_branch`.

2. Renseigner la demande
* **Titre** : concis et explicite (ex. : `feat: ajout du module de my_branch`).
* **Description** : résumé précis des modifications apportées, logique retenue, ce qui doit être testé...
* **Reviewers** : sur le panneau latéral à droite, cliquer sur la roue crantée à côté de *Reviewers* et sélectionner le compte GitHub des collègues.

3. Valider
 + **Create pull request**

... ENSUITE ...

1. les collègues
+ recevront une notification,
+ pourront inspecter les différences (*diff*) dans l'onglet **« Files changed »**,
+ commenter des lignes précises,
+ et enfin cliquer sur **« Review changes »** pour valider (*Approve*) ou demander des ajustements.

2. Fusionner
Une fois approuvée, 
+ **« Merge pull request »** / **« Confirm merge »**

... ne pas oublier :

3. En local pour soi
Une fois le merge validé sur GitHub, mettre à jour le dépôt local :
```bash
git switch main
git pull origin main
```
=> et c'est reparti pour une nouvelle branche :D
```bash
git switch -c new_branch
# `-c` garantit qu'on repart directement de la version la plus à jour de `main`
```
*[Back to top](<#toc>)*

---


Supprimer EN LOCAL une branche supprimée depuis GITHUB
**1. revenir au `main`**
On ne peut pas supprimer la branche sur laquelle on se trouve :
```bash
git switch main
git pull origin main # récupère le merge fait sur GitHub
```

**2. Supprimer la branche locale**
L'option `-d` vérifie d'abord que les commits ont bien été intégrés :
```bash
git branch -d my_branch # supprime la branche locale
```
*Si Git refuse car la branche n'est pas totalement fusionnée, forcer la suppression avec `git branch -D sonNom`*.

**3. Nettoyer les références distantes fantômes**
Après suppression de la branche locale, le Git local garde en mémoire la référence distante obsolète, il faut synchroniser le dépôt local avec l'état réel de GitHub et purger ces références mortes :
```bash
git fetch --prune # cf élaguer ;)
```
**4. Vérifier que l'espace est propre**
```bash
git branch -a
# puis `q` pour reprendre la main
```
`sonNom` et `origin/sonNOM` doivent avoir totalement disparu.
*[Back to top](<#toc>)*

---

PB pour changer de branche, par ex `git switch main` provoque cette erreur :
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

---

Identifier les dépôts distants liés à un projet local :
```bash
# à la racine du dépôt :
git remote -v

# doit afficher
origin git@framagit.org:utilisateur/projet.git (fetch)  # lecture
origin git@framagit.org:utilisateur/projet.git (push)   # écriture
```
*[Back to top](<#toc>)*

---

---


# Pull request V2

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

*[Back to top](<#toc>)*



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

=> *à tester pour la correction de p'tits bugs à la fin ?*

*[Back to top](<#toc>)*