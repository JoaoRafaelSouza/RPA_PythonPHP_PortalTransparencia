#!/bin/bash

echo "🧼 LIMPEZA INTERATIVA DOCKER"
echo "-----------------------------"

read -p "Deseja limpar containers parados? (s/N): " res
[[ "$res" == "s" || "$res" == "S" ]] && docker container prune -f

read -p "Deseja limpar imagens não utilizadas? (s/N): " res
[[ "$res" == "s" || "$res" == "S" ]] && docker image prune -a -f

read -p "Deseja limpar volumes não utilizados? (s/N): " res
[[ "$res" == "s" || "$res" == "S" ]] && docker volume prune -f

read -p "Deseja limpar redes não utilizadas? (s/N): " res
[[ "$res" == "s" || "$res" == "S" ]] && docker network prune -f

read -p "Deseja limpar cache de build? (s/N): " res
[[ "$res" == "s" || "$res" == "S" ]] && docker builder prune -f

echo "✅ Limpeza concluída."
docker system df