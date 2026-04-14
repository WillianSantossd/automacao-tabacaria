# Importando as funções de cada arquivo que você criou
from scraper import buscar_produto
from planilhas import salvar_dados
from banco import criar_banco, salvar_no_banco

def main():
    # 1. Pergunta o que o usuário quer buscar
    termo = input("Qual produto deseja buscar na Oasis Tabacaria? ")
    
    # 2. Prepara o Banco de Dados (Cria a tabela se não existir)
    criar_banco()
    
    # 3. Inicia o Robô (Scraper) para coletar os dados
    print("\n[ROBÔ] Iniciando coleta de dados... Aguarde.")
    dados = buscar_produto(termo)

    if dados:
        # 4. JUNÇÃO: Aqui os arquivos trabalham juntos com os mesmos dados
        
        # Salva no Banco de Dados (Para o sistema ter memória)
        salvar_no_banco(dados)
        
        # Salva na Planilha (Para você abrir e ler)
        salvar_dados(dados)
        
        print(f"\n[SUCESSO] Foram encontrados {len(dados)} itens.")
        print("Tudo foi salvo no Banco de Dados e na Planilha!")
    else:
        print("\n[AVISO] Nenhum item foi encontrado para essa busca.")

if __name__ == "__main__":
    main()