# Planning de Développement Back-End — Pac-Man (7 Jours)

**Cadence de travail :** 7h à 11h par jour  
**Volume global estimé :** 18h30 (fluide) à 33h30 (avec blocages)  
**Temps disponible total :** 49h à 77h  

---

## 1. Diagramme de Gantt (Vue Synthétique)

```text
Tâches / Modules          | J1 | J2 | J3 | J4 | J5 | J6 | J7 |
-----------------------------------------------------------------
1. Engine (Fin & Tests)   |████|    |    |    |    |    |    |
2. Level (Code & Tests)   |████|    |    |    |    |    |    |
3. Pacman (Code & Tests)  |    |████|    |    |    |    |    |
4. Ghosts (Logique & IA)  |    |████|████|    |    |    |    |
5. Ghosts (Tests)         |    |    |████|    |    |    |    |
6. Game (Orchestration)   |    |    |    |████|    |    |    |
7. Game (Tests unitaires) |    |    |    |    |████|    |    |
8. Tests d'intégration    |    |    |    |    |    |████|    |
9. Buffer & Raccord IHM   |    |    |    |    |    |    |████|
```

---

## 2. Découpage Quotidien & Livrables

### Jour 1 : Finalisation Engine & Classe Level
* **Engine :** Validation finale de `is_valid_position` et cas limites de sortie de grille.
* **Level :** Implémentation du tableau d'objets, de `consume_object(y, x)` et de la `@property remaining_objects`.
* **Tests :** Écriture et validation des suites de tests unitaires pour `Engine` et `Level`.
* **Temps estimé :** 5h30 à 7h00

### Jour 2 : Classe Pacman & Début des Ghosts
* **Pacman :** Gestion de l'état (position $x, y$, directions actuelle/souhaitée, réinitialisation).
* **Ghosts :** Structure de base de la classe `Ghost`, gestion des états (Normal / Frightened).
* **Tests :** Tests unitaires complets de la classe `Pacman`.
* **Temps estimé :** 4h00 à 6h00

### Jour 3 : Intelligence Artificielle des 2 Fantômes
* **Ghosts (IA) :** Algorithmes de choix de trajectoire pour les 2 fantômes distincts (traqueur et aléatoire/embusqué).
* **Tests :** Tests unitaires validant les déplacements, la réaction aux murs et le changement d'état des fantômes.
* **Temps estimé :** 3h00 à 6h00

### Jour 4 : Orchestrateur Game
* **Game :** Structure globale et implémentation des sous-fonctions :
  * `pacman_update(direction)`
  * `_handle_consumption()`
  * `ghost_update()`
  * `update(direction)` (1 tick logique)
* **Temps estimé :** 3h00 à 5h00

### Jour 5 : Tests Unitaires de Game
* **Règles du jeu :** Validation complète du score, des collisions Pac-Man/Fantômes, de la perte de vies et des conditions de fin de partie (Victoire / Défaite).
* **Tests :** Écriture de la suite de tests pour la classe `Game`.
* **Temps estimé :** 3h00 à 5h00

### Jour 6 : Tests d'Intégration & Recette
* **Simulations :** Exécution de parties complètes simulées en console/script sans IHM Pygame.
* **Debug :** Résolution des cas limites (*edge cases*) et nettoyage du code.
* **Temps estimé :** 2h00 à 4h00

### Jour 7 : Marge de Sécurité & Raccordement Binôme
* **Buffer :** Absorption des retards éventuels accumulés pendant la semaine.
* **Synchronisation :** Connexion du moteur `Game` avec l'interface Pygame développée par le binôme.
* **Temps estimé :** Journée de marge / Raccordement final

---

## 3. Récapitulatif du Budget Temps

| Module / Étape | Estimation Basse | Estimation Haute (avec blocages) |
| :--- | :---: | :---: |
| **Engine** (Fin + Tests) | 1h30 | 3h00 |
| **Level** (Code + Tests) | 2h00 | 4h00 |
| **Pacman** (Code + Tests) | 2h00 | 3h30 |
| **2 Ghosts** (Code + Tests) | 5h00 | 8h00 |
| **Game** (Code + Tests) | 4h00 | 7h00 |
| **Integration & Debug Global** | 4h00 | 8h00 |
| **TOTAL** | **18h30** | **33h30** |