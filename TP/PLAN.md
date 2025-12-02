# Plan de test - TP Corentin Echivard Lizaso

## Tests Unitaires

1. Fonction de conversion depuis le binaire

   - Pourquoi ?
     - Pour s'assurer que la conversion fonctionne sans fautes
   - Comment ?
     - Vérification avec un cas normal
     - Vérification avec un cas défectueux
       - Pas le bon format de donnée reçu
       - Mauvaise données en sortie de conversions.
       - Données contradictoire (annonce de cinq triangle alors qu'il n'y en a que trois)

2. Fonction de conversion vers le binaire

   - Pourquoi ?
     - Pour s'assurer que la conversion fonctionne sans fautes
   - Comment ?
     - Vérification avec un cas normal
     - Vérification avec un cas défectueux
       - Données vide en entrée - Erreur attendue
       - Données NULL - Erreur attendue
       - Mauvais format de donnée en entrée - Erreur attendue

3. Triangularisation

   - Pourquoi ?
     - Pour s'assurer que la triangularisation fonctionne sans fautes
   - Comment ?
     - Cas normal
     - Cas où l'identifiant n'est pas bon et qu'il retourne bien la bonne erreur
     - Mauvais format du PointSetID - Erreur attendue
     - Mauvais format de la réponse API - Erreur attendue

4. Création des triangles à la fin de l'algo

   - Pourquoi ?
     - Pour s'assurer que la création des triangles fonctionne sans fautes
   - Comment ?
     - Vérifier avec un ensemble de points et une triangulation valide que la structure `Triangles` (contenant les points et les indices des triangles) est correctement créée.
     - Tester avec un ensemble de points vide.
     - Tester avec un ensemble de points ne permettant pas de former un triangle (ex: 2 points).

5. Test API
   - Pourquoi ?
     - Pour tester tout les retours possible de l'API
   - Comment ?
     - **Cas nominal ("Happy path")** : 
        * PointSetID valide. 
            * Mocker le `PointSetManager` pour qu'il retourne un PointSet valide. 
            * Le test doit vérifier que le statut de la réponse est `200 OK` et qu'il ait les bonnes données.
     - **Cas d'erreurs** :
       - PointSetID non trouvé : 
            * Mocker le `PointSetManager` pour qu'il retourne un PointSet invalide. 
            * Le test doit vérifier que le statut de la réponse est `404 Not Found` et qu'il retourne une erreur 404. 
            * L'API du `Triangulator` doit répercuter cette erreur
       - `PointSetManager` indisponible :
            * L'API doit retourner une erreur serveur (par exemple, un statut 503 Service Unavailable).
       - PointSetID malformé dans la requête du client (ex: pas un UUID). 
            * L'API doit retourner une erreur client (400 Bad Request).
       - Données du PointSet reçues du `PointSetManager` invalides. 
            * L'API doit retourner une erreur serveur (500 Internal Server Error).
       - Utiliser une méthode HTTP non autorisée :
            * L'API doit retourner une erreur 405 Method Not Allowed.

## Tests de performances

1. Temps de traitement de la conversion depuis le binaire

   - Pourquoi ?
     - Mesurer l'efficacité de la conversion des données binaires en objets PointSet.
   - Comment ?
     - Générer des PointSet binaires de différentes tailles
     - Exécuter la fonction de conversion et mesurer le temps moyen et l'écart-type.

2. Temps de traitement de la conversion vers le binaire
   - Pourquoi ?
     - Mesurer l'efficacité de la conversion des objets Triangles en format binaire.
   - Comment ?
     - Créer des objets Triangles de différentes tailles
     - exécuter la fonction de conversion et mesurer le temps moyen et l'écart-type.

3. Temps de traitement de la triangularisation
   - Pourquoi ?
     - Évaluer la performance de l'algorithme de triangulation.
   - Comment ?
     - Mesurer le temps d'exécution de l'algorithme sur des ensembles de points de tailles différentes
     - Tester des points différents :
       - Points distribués uniformément de manière aléatoire.
       - Points formant des motifs spécifiques (ex: alignés, en cercle, en grille).

## Test d'intégration

1. Entre la conversion depuis le binaire et l'algorithme de triangularisation

   - Pourquoi ?
     - S'assurer que la structure de données généré par la conversion depuis le binaire est correctement interprétée par l'algorithme de triangulation.
   - Comment ?
     - Créer un PointSet binaire valide.
     - Appeler la fonction de conversion pour obtenir un objet PointSet en mémoire.
     - Passer cet objet directement à la fonction de triangulation.
     - Vérifier que la triangulation s'exécute sans erreur et que le résultat est conforme à ce qui est attendu pour les points donnés.

2. Entre la sortie de l'aglo et la création des objets triangles
   - Pourquoi ?
     - Valider que les indices de triangles générés par l'algorithme sont correctement utilisés pour construire les Triangles finale.
   - Comment ?
     - Utiliser un ensemble de points connu et le résultat attendu de la triangulation.
     - Appeler la fonction qui créer les Triangles à partir des deux éléments.
     - Vérifier que l'objet Triangles créé contient bien les points d'origine et que les indices des triangles sont corrects.

3. Entre les objets triangles et la conversion vers le binaire
   - Pourquoi ?
     - Garantir que les Triangles est correctement converti en format binaire.
   - Comment ?
     - Créer un objet Triangles complet.
     - Le passer à la fonction de conversion vers le binaire.
     - Vérifier que le flux binaire généré est correct :
       - Le nombre de points et leurs coordonnées.
       - Le nombre de triangles et les indices de leurs sommets sont corrects.
       - L'ensemble peut être relu par la fonction de conversion **depuis** le binaire.
