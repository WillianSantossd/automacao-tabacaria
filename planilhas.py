import pandas as pd
import os
from datetime import datetime

# Nome do arquivo único por execução
agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
ARQUIVO = f"busca_{agora}.xlsx"

def salvar_dados(dados):
    df_final = pd.DataFrame(dados)

    try:
        # Usando xlsxwriter para formatar colunas
        writer = pd.ExcelWriter(ARQUIVO, engine='xlsxwriter')
        df_final.to_excel(writer, index=False, sheet_name='Produtos')

        workbook  = writer.book
        worksheet = writer.sheets['Produtos']

        # Formato para deixar o cabeçalho em negrito
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})

        for i, col in enumerate(df_final.columns):
            # Acha o tamanho do maior texto na coluna
            max_len = df_final[col].astype(str).str.len().max()
            max_len = max(max_len, len(col)) + 4 # Espaço extra
            
            # Limita a largura máxima para não ficar exagerado nos links
            if max_len > 70: max_len = 70
            
            worksheet.set_column(i, i, max_len)
            # Reaplica o título com formato negrito
            worksheet.write(0, i, col, header_format)

        writer.close()
        print(f"\n[SUCESSO] Planilha organizada: {ARQUIVO}")

    except Exception as e:
        print(f"[ERRO] Falha ao formatar, salvando modo simples: {e}")
        df_final.to_excel(ARQUIVO, index=False)