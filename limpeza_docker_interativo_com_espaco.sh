#!/bin/bash

echo "🧼 LIMPEZA INTERATIVA DOCKER COM RELATÓRIO DE ESPAÇO"
echo "-----------------------------------------------------"

# Obtém o uso de espaço antes da limpeza
espaco_antes=$(docker system df --format "{{.Size}}" | grep total | awk '{print $1}')
echo "📦 Espaço ocupado ANTES da limpeza: $(docker system df | grep 'Total space used' | awk '{print $4, $5}')"

# Etapas interativas
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

echo ""
echo "📊 Verificando espaço após limpeza..."

# Obtém o uso de espaço depois da limpeza
espaco_depois=$(docker system df | grep 'Total space used' | awk '{print $4, $5}')
echo "📦 Espaço ocupado DEPOIS da limpeza: $espaco_depois"

# Converte para bytes para cálculo (usando docker system df de forma customizada)
espaco_antes_bytes=$(docker system df --format "{{.Size}}" | grep total | sed 's/[^0-9.]//g')
espaco_depois_bytes=$(docker system df --format "{{.Size}}" | grep total | sed 's/[^0-9.]//g')

# Cálculo simples da diferença (estimado)
echo "✅ Estimativa de espaço liberado: aproximadamente $(echo "$espaco_antes_bytes - $espaco_depois_bytes" | bc) GB"

echo "✅ Limpeza concluída!"