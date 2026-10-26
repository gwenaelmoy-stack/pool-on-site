# Site Pool-On

Site statique de [pool-on.com](https://www.pool-on.com), en anglais (racine) et en français (`/fr/`).

## Contenu du dépôt

- `site/` : le site publié, tel quel (HTML, `site.css`, `assets/`). C'est le dossier à servir.
- `source/` : le générateur des pages.
  - `build.py` produit les pages anglaises.
  - `i18n.py` produit les pages françaises à partir de `fr.py` (les traductions) et ajoute le bouton EN/FR.
  - Pour régénérer après une modification : `sh source/make.sh`.

## Langue

Un navigateur réglé en français est envoyé vers `/fr/`, les autres restent en anglais. Le choix fait avec le bouton EN/FR est mémorisé dans le navigateur.

## Mise en ligne (Cloudflare Pages)

- Commande de build : aucune.
- Dossier de sortie : `site`.
- `site/_headers` ajoute les en-têtes de sécurité et empêche l'indexation de l'adresse de test `*.pages.dev`.

## Reste à faire avant la bascule de pool-on.com

- Retirer le bandeau « Maquette de travail » et compléter les éléments marqués en jaune.
- Brancher le formulaire de contact.
- Remplacer la vidéo YouTube de l'accueil par le fichier vidéo hébergé sur le site.
