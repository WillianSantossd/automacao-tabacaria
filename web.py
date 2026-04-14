import argparse
import html
import os
import webbrowser
from banco import listar_produtos

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Consultas - Oasis Tabacaria</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f4f4f8; color: #222; margin: 0; padding: 24px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 10px 24px rgba(0,0,0,.08); }}
        h1 {{ margin-top: 0; }}
        .meta {{ margin-bottom: 20px; color: #555; }}
        .filtro {{ margin: 16px 0; }}
        .filtro input {{ width: 320px; padding: 10px 12px; border: 1px solid #ccc; border-radius: 6px; }}
        .filtro button {{ padding: 10px 16px; background: #0078d7; border: none; color: white; border-radius: 6px; cursor: pointer; }}
        .filtro button:hover {{ background: #005ea6; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
        th, td {{ padding: 12px 10px; border: 1px solid #e0e0e0; text-align: left; vertical-align: top; }}
        th {{ background: #0078d7; color: #fff; }}
        tr:nth-child(even) {{ background: #fafafa; }}
        a {{ color: #0078d7; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .empty {{ padding: 24px; color: #555; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Consultas de Produtos</h1>
        <div class="meta">Total de registros: {total}. Filtro aplicado: <strong>{filtro_display}</strong></div>
        <table>
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>Marca</th>
                    <th>Valor</th>
                    <th>Disponibilidade</th>
                    <th>Data</th>
                    <th>Link</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
</body>
</html>
'''


def gerar_html(produtos, filtro):
    filtro_display = filtro if filtro else 'Nenhum'
    filtro_html = html.escape(filtro)

    if produtos:
        linhas = []
        for item in produtos:
            linhas.append(
                '<tr>'
                f'<td>{html.escape(item["PRODUTO"])}</td>'
                f'<td>{html.escape(item["MARCA"])}</td>'
                f'<td>{html.escape(item["VALOR"])}</td>'
                f'<td>{html.escape(item["DISPONIBILIDADE"])}</td>'
                f'<td>{html.escape(item["DATA"])}</td>'
                f'<td><a href="{html.escape(item["LINK"])}" target="_blank">Abrir</a></td>'
                '</tr>'
            )
        table_rows = '\n'.join(linhas)
    else:
        table_rows = '<tr><td colspan="6" class="empty">Nenhum registro encontrado.</td></tr>'

    return HTML_TEMPLATE.format(
        total=len(produtos),
        filtro_display=html.escape(filtro_display),
        filtro_html=filtro_html,
        table_rows=table_rows,
    )


def salvar_arquivo(html_text, nome_arquivo='consultas.html'):
    caminho = os.path.abspath(nome_arquivo)
    with open(caminho, 'w', encoding='utf-8') as arquivo:
        arquivo.write(html_text)
    return caminho


def main():
    parser = argparse.ArgumentParser(description='Gerar página de consultas de produtos do banco.')
    parser.add_argument('-q', '--query', default='', help='Filtrar por nome ou marca')
    parser.add_argument('-o', '--open', action='store_true', help='Abrir a página gerada no navegador')
    args = parser.parse_args()

    produtos = listar_produtos(args.query)
    html_text = gerar_html(produtos, args.query)
    caminho = salvar_arquivo(html_text)

    print(f'Página gerada em: {caminho}')

    if args.open:
        webbrowser.open('file://' + caminho)


if __name__ == '__main__':
    main()
