import os
import sys
import hashlib
from collections import defaultdict

def calcular_hash(arquivo, bloco=262144):
    """Calcula SHA-256 de um arquivo"""
    sha256 = hashlib.sha256()
    
    try:
        with open(arquivo, "rb") as f:
            chunk = f.read(bloco)
            while chunk:
                sha256.update(chunk)
                chunk = f.read(bloco)
        return sha256.hexdigest()
    except Exception as e:
        raise Exception(f"Erro ao calcular hash: {e}")

# ============================================================
# pega a pasta via parâmetro ou pergunta ao usuário
# ============================================================
if len(sys.argv) > 1:
    PASTA = sys.argv[1]
else:
    PASTA = input("Digite o caminho da pasta: ").strip()

# Remove aspas
PASTA = PASTA.strip('"\'').strip()

# Validação
if not os.path.isdir(PASTA):
    print(f"Pasta inválida: {PASTA}")
    sys.exit(1)

print(f"\nEscaneando: {PASTA}\n")

# ============================================================
# 1. Agrupar por tamanho
# ============================================================
arquivos_por_tamanho = defaultdict(list)
contador_total = 0

for raiz, _, arquivos in os.walk(PASTA):
    for nome in arquivos:
        contador_total += 1
        caminho = os.path.join(raiz, nome)
        
        try:
            tamanho = os.path.getsize(caminho)
            arquivos_por_tamanho[tamanho].append(caminho)
        except Exception as e:
            print(f"Erro ao acessar {caminho}: {e}")

print(f"Total de arquivos encontrados: {contador_total}")

# ============================================================
# 2. Hash apenas dos candidatos
# ============================================================
arquivos_por_hash = defaultdict(list)
candidatos = sum(1 for lista in arquivos_por_tamanho.values() if len(lista) > 1)
print(f"Candidatos a duplicados (mesmo tamanho): {sum(len(lista) for lista in arquivos_por_tamanho.values() if len(lista) > 1)}")
print("Calculando hashes...\n")

for tamanho, lista in arquivos_por_tamanho.items():
    if len(lista) < 2:
        continue
    
    for caminho in lista:
        try:
            h = calcular_hash(caminho)
            arquivos_por_hash[h].append(caminho)
        except Exception as e:
            print(f"Erro ao processar {caminho}: {e}")

# ============================================================
# 3. Mostrar duplicados
# ============================================================
encontrou = False

for h, lista in sorted(arquivos_por_hash.items(), key=lambda x: len(x[1]), reverse=True):
    if len(lista) > 1:
        encontrou = True
        print("=" * 80)
        print(f"HASH: {h}")
        print(f"Duplicados encontrados: {len(lista)}")
        print(f"Tamanho: {os.path.getsize(lista[0]):,} bytes\n")
        
        for arq in sorted(lista):
            print(f"  • {arq}")
        print()

if not encontrou:
    print("Nenhum arquivo duplicado encontrado.")