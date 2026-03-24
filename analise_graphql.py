import requests
import csv
from collections import defaultdict

def gerar_relatorio_arquitetura(github_token):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {github_token}"}
    
    query = """
    query($cursor: String) {
      search(query: "repo:langchain-ai/langchain is:pr is:merged merged:>=2025-01-01", type: ISSUE, first: 100, after: $cursor) {
        issueCount
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          ... on PullRequest {
            title
            url
            mergedAt
            additions
            deletions
            labels(first: 10) {
              nodes {
                name
              }
            }
          }
        }
      }
    }
    """
    
    cursor = None
    tem_proxima_pagina = True
    pagina_atual = 1
    
    # Estruturas para armazenar os dados agregados
    impacto_por_tag = defaultdict(lambda: {'adicoes': 0, 'delecoes': 0, 'quantidade_prs': 0})
    lista_todos_prs = []

    print("Iniciando extração completa de PRs. Isso pode levar 1 ou 2 minutos...")

    while tem_proxima_pagina:
        print(f"Buscando página {pagina_atual}...")
        response = requests.post(url, json={'query': query, 'variables': {"cursor": cursor}}, headers=headers)
        
        if response.status_code != 200:
            print(f"Erro na requisição: {response.status_code}")
            break
            
        dados = response.json().get('data', {}).get('search', {})
        prs = dados.get('nodes', [])
        
        for pr in prs:
            if pr:
                titulo = pr.get('title')
                url_pr = pr.get('url')
                data_merge = pr.get('mergedAt')[:10] # Pegando só a data (YYYY-MM-DD)
                adicoes = pr.get('additions', 0)
                delecoes = pr.get('deletions', 0)
                tags = [label['name'] for label in pr.get('labels', {}).get('nodes', [])]
                
                lista_todos_prs.append({
                    'titulo': titulo,
                    'url': url_pr,
                    'data': data_merge,
                    'adicoes': adicoes,
                    'delecoes': delecoes,
                    'tags': ", ".join(tags)
                })
                
                # Agregando dados pelas tags
                if not tags:
                    tags = ['sem_tag']
                
                for tag in tags:
                    impacto_por_tag[tag]['adicoes'] += adicoes
                    impacto_por_tag[tag]['delecoes'] += delecoes
                    impacto_por_tag[tag]['quantidade_prs'] += 1

        page_info = dados.get('pageInfo', {})
        tem_proxima_pagina = page_info.get('hasNextPage', False)
        cursor = page_info.get('endCursor')
        pagina_atual += 1

    # --- PROCESSAMENTO DOS DADOS PARA O TERMINAL ---
    
    print("\n" + "="*50)
    print("📊 RESULTADOS DA ANÁLISE ARQUITETURAL")
    print("="*50 + "\n")

    # 1. Tags que mais removeram código (Onde está a prova da modularização)
    tags_ordenadas_por_delecao = sorted(impacto_por_tag.items(), key=lambda x: x[1]['delecoes'], reverse=True)
    
    print("🏆 TOP 10 TAGS QUE MAIS REMOVERAM CÓDIGO:")
    for tag, stats in tags_ordenadas_por_delecao[:10]:
        saldo = stats['adicoes'] - stats['delecoes']
        print(f"Tag: {tag.ljust(25)} | PRs: {str(stats['quantidade_prs']).ljust(4)} | Deleções: -{str(stats['delecoes']).ljust(6)} | Adições: +{str(stats['adicoes']).ljust(6)} | Saldo: {saldo}")

    # 2. Os Maiores PRs (Os "Eventos Canônicos" da refatoração)
    prs_ordenados_por_delecao = sorted(lista_todos_prs, key=lambda x: x['delecoes'], reverse=True)
    
    print("\n🔥 TOP 5 PRs COM MAIOR DELEÇÃO ABSOLUTA:")
    for pr in prs_ordenados_por_delecao[:5]:
        print(f"- {pr['titulo']}")
        print(f"  Deleções: -{pr['delecoes']} | Data: {pr['data']}")
        print(f"  Tags: {pr['tags']}")
        print(f"  URL: {pr['url']}\n")

    # --- EXPORTAÇÃO PARA CSV ---
    nome_arquivo = 'relatorio_arquitetura_langchain.csv'
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['titulo', 'url', 'data', 'adicoes', 'delecoes', 'tags'])
        writer.writeheader()
        writer.writerows(lista_todos_prs)
    
    print(f"✅ Arquivo '{nome_arquivo}' gerado com sucesso com {len(lista_todos_prs)} PRs detalhados!")

MEU_TOKEN = "######" 
gerar_relatorio_arquitetura(MEU_TOKEN)