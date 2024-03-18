# Autres exemples pour le même exercice

1. https://github.com/mkrtchian/foobartory
2. https://github.com/ThierryAbalea/foobartory
3. https://codesandbox.io/s/foobartory-i5yjf

# TODO

## Back

1. finir l'implémentation de l'énoncé
2. tests auto (unit, integration, leak, performance), code coverage
3. gestions des logs (faux temps en log context), est-ce qu'il faut open-telemetry ou un logger maison ?
4. documentation (code, archi): sphinx buildé sur Github pages
5. setup CQRS using Event Sourcing for better write performance and launch more games
   1. Is kafka have better throughput than other database ? Better for write store ?
   2. Create another microservice that build materialized view
   3. Add a route for requesting the materialized view to display graph in the frontend or do the route just return the raws events ? Utiliser GraphQL.
6. Est-ce que je peux optimiser une partie du code avec Numba ou Rust/pyo3/maturin ? Intégration maison possible ou impossible avec pdm ?
7. apprentissage par renforcement en donnant les règles comme AlphaZero (reinforcement learning)
8. use simpler trading ML methods: https://ml4trading.io/


## Front

Ma référence avec Next.js et FastAPI: https://github.com/nullchilly/NextChess/tree/main

1. Afficher la position en cours du jeu
2. Build static du site pour être déployable sur github pages ou sur un simple Nginx dans Kub ou utilisé le server par défaut de Node.js ?
3. Faire des graphes d'historique des données préssenties comme utile pour le trading
4. Influencer la partie depuis le front ?
   1. choix de la stratégie/modèle implémenté par le back ?
   2. on joue sur des paramètres simples du modèle ?
   3. donner des ordres simples pour piloter les robots avant de commencer la partie ou pendant la partie
   4. création de nouveaux modèles avec du code python éxécuté côté back ?

## Integration

1. docker-compose en local @xavier ✅
2. kind en local en repartant d'un script kind minimal et une charte minimale @xavier
3. HPA horizontal pour le back basé sur CPU @xavier
4. lier docker.com et github.com @thibaut ✅
5. pusher les images docker sur docker.com @xavier ✅
6. créer un compte sur https://labs.play-with-k8s.com/ @thibaut
7. déployer sur https://labs.play-with-k8s.com/ @xavier
8. utiliser open-telemetry: voir les logs et les traces quand CPU > 90%,
   est-ce qu'il faut Grafana pour faire l'aggrégation des logs, traces et metrics @xavier
   https://github.com/blueswen/fastapi-jaeger?tab=readme-ov-file
