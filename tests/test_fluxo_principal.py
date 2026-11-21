import re
from playwright.sync_api import Page, expect


def test_buscar_sugestao_passeio_fluxo_principal(page: Page, base_url: str):
    """
    Cenário 1 (Fluxo Principal):
    - Ação inicial: Acessar a página de recomendação (/sugestao).
    - Etapas: Preencher o campo de descrição da experiência e clicar em 'Buscar passeios'.
    - Resultado observável: O sistema exibe a mensagem de confirmação e renderiza ao menos um card de passeio sugerido.
    """
    page.goto(f"{base_url}/sugestao")

    # Verifica se a página carregou corretamente
    expect(
        page.get_by_role("heading", name="Qual experiência você procura?")
    ).to_be_visible()

    # Preenche a descrição usando o placeholder real do SugestaoPage.jsx
    campo_descricao = page.get_by_placeholder(
        "Ex: quero algo na beira do mar, tranquilo, bom pra família..."
    )
    campo_descricao.fill("quero algo na beira do mar, tranquilo, bom pra família")

    # Clica no botão de busca
    botao_buscar = page.get_by_role("button", name="Buscar passeios")
    expect(botao_buscar).to_be_enabled()
    botao_buscar.click()

    # Aguarda e verifica o resultado observável na tela (timeout maior para carregamento inicial do modelo NLP)
    mensagem_resultado = page.locator(".sp-mensagem-resultado")
    expect(mensagem_resultado).to_be_visible(timeout=30000)
    expect(mensagem_resultado).to_contain_text(
        re.compile(r"Encontrei [1-9]\d* passeios? que combinam com o que você procura!")
    )

    # Verifica se pelo menos um card de passeio foi renderizado com o botão 'Ver detalhes'
    primeiro_card = page.locator(".sp-card").first
    expect(primeiro_card).to_be_visible()
    expect(primeiro_card.get_by_role("button", name="Ver detalhes")).to_be_visible()