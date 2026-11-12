à traduire :

https://pyinstaller.org/en/stable/usage.html

https://pyinstaller.org/en/v6.4.0/runtime-information.html 

---

OUILLE OUILLE OUILLE conflits...

git switch Packaging 
 Pacman_GIT git:(Packaging) git merge main      
Auto-merging src/__main__.py
CONFLICT (content): Merge conflict in src/__main__.py
Auto-merging src/game/entities/ghost.py
Auto-merging src/game/entities/ghost_manager.py
Auto-merging src/game/entities/player.py
Auto-merging src/game/game.py
CONFLICT (content): Merge conflict in src/game/game.py
Auto-merging src/game/gums/pacgum_manager.py
Auto-merging src/game/gums/super_pacgum.py
Auto-merging src/menu/main_menu.py
Auto-merging src/utils/sprites.py
CONFLICT (content): Merge conflict in src/utils/sprites.py
Auto-merging src/utils/utils.py
CONFLICT (content): Merge conflict in src/utils/utils.py
Automatic merge failed; fix conflicts and then commit the result.

---

### Arborescence OK

Dossiers `modules/` et `assets/` en dehors de `src/` : OK, bonne architecture

- `src/` 
  contient uniquement le code source du jeu. 
- `assets/`
  contient les ressources graphiques.
- `modules/`
  contient les dépendances locales `.whl`.

=> Structure propre, à priori facile à packager...
... MAIS des problèmes de chemin peuvent se produire avec PyInstaller, à cause de l'arborescence du projet qui change quand le script Python est transformé en exécutable (*gelé/frozen*).


## `--onedir` vs `--onefile`

Avec **PyInstaller**, les modes `--onefile` et `--onedir` définissent la façon dont le programme et ses dépendances (bibliothèques, fichiers DLL, etc.) sont empaquetés dans le dossier `dist/`.

=> il faut choisir entre performances et commodité de distribution :

* **`--onedir`** (par défaut)
	PyInstaller regroupe l'appli et ses dépendances dans un dossier pour un démarrage rapide
	-`/+\` Démarrage instantané car les fichiers sont déjà décompressés ;
	-`/+\` Moins de soucis avec les antivirus, car les fichiers sont visibles et plus facilement validés par les systèmes de sécurité ;
	-`/+\` Mises à jour plus faciles, on peut modifier un petit composant sans tout re-faire ;
	-`/-\` Pour le partager, il faut généralement le zipper ou créer un vrai programme d'installation.

* **`--onefile`** (pas forcément plus simple)
	PyInstaller compresse tout (script, interpréteur Python, bibliothèques...) dans **1 seul fichier exécutable** autonome qui doit se décompresser à chaque lancement
	-`/+\` Très facile à partager, propre et rapide à distribuer ;
	-`/-\` Lancement plus lent (doit décompresser tout à chaque démarrage) ;
	-`/-\` Faux positifs antivirus ;
	-`/-\` Plus difficile à déboguer si des fichiers de données manquent.


Pour Itch.io, il est conseillé est d'utiliser `--onedir`, puis de zipper le dossier obtenu avant de l'uploader :
- Les joueurs d'Itch.io sont frileux face aux fichiers `.exe` uniques et inconnus... qu'ils ne peuvent pas explorer.
- Les mises à jour sont ultra-légères, Itch ne téléchargera QUE les fichiers modifiés (vs l'intégralité de l'exécutable avec `--onefile`).
- Les dossiers des fichiers externes (sprites, musiques, polices...) peuvent rester visiblement stockés à côté de l'exécutable, plus simple à gérer dans le code Python... *à condition de l'avoir anticipé :P*.


## `sys._MEIPASS` 

Quel que soit le mode choisi, une variable `sys._MEIPASS` est créée par PyInstaller dès que le script est *gelé*.

```text
dist/PacMan/
├── PacMan.exe          ← sys.executable
└── _internal/          ← sys._MEIPASS (dépendances ET fichiers de données)
    ├── data/
    └── ...
```

- mode `--onedir` :
	`sys._MEIPASS` pointe simplement vers le sous-dossier `_internal` de l'application généré par PyInstaller

- mode `--onefile` :
	`sys._MEIPASS` pointe vers un dossier temporaire caché (créé dynamiquement dans le système et supprimé automatiquement à la fermeture du programme).


## `get_resource_path()`

Pour éviter les problèmes de chemins d'accès, puisque l'emplacement des fichiers change selon que le script tourne en mode développement ou une fois gelé, la solution standard consiste à calculer dynamiquement le chemin absolu du dossier racine de l'application au moment de l'exécution.

1. un fichier dédié pour ne plus calculer le chemin depuis un sous-dossier :

```Python
# par ex `paths.py`
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent # si placé à la racine du projet
```

2. une fonction qui détecte si l'appli tourne depuis le script .py d'origine ou depuis l'exécutable généré par PyInstaller :
```python
import sys
from pathlib import Path
from paths import ROOT_DIR
 
    
def get_resource_path(relative_path: str) -> Path:
    """Chemin d'une ressource, en dev comme dans le build PyInstaller.
    ARG: nom du fichier recherché
    RETURN: objet issu du module `pathlib`
    """
    if getattr(sys, "frozen", False):
        # En mode figé, sys._MEIPASS pointe vers dist/PacMan/_internal
        base_path = Path(getattr(sys, "_MEIPASS"))
    else:
        # En dev, Ancrage absolu :D
        base_path = ROOT_DIR
    return base_path / relative_path
```

3. cette fonction appliquée à tous les fichiers externes
```python
# À ÉVITER (plantera une fois packagé) :
# image_path = "data/image.png"

#  À FAIRE
image_path = get_resource_path("data/image.png")
```

`/!\` ne pas oublier d'inclure les dossiers de ressources lors du build
