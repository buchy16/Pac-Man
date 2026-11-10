à traduire :

https://pyinstaller.org/en/stable/usage.html

https://pyinstaller.org/en/v6.4.0/runtime-information.html 

---

### Arborescence OK

Avoir les dossiers `modules/` et `assets/` en dehors de `src/` est une bonne pratique d'architecture logicielle.

- `src/` 
  contient uniquement le code source du jeu. 
- `assets/`
  contient les ressources graphiques.
- `modules/`
  contient les dépendances locales sous forme de roues (`.whl`). 

=> Structure propre, à priori facile à packager.

