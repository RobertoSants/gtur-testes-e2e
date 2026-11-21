import re
from playwright.sync_api import Page, expect


def test_buscar_e_abrir_detalhes_passeio_sugerido(page: Page, base_url: str):
    """
    Cenário 1 (Fluxo Principal Completo):
    - Ação inicial: Acessar a página de recomendação (/sugestao).
    - Etapas: Descrever o perfil do passeio, acionar 'Buscar passeios', verificar o card sugerido e clicar em 'Ver detalhes'.
    - Resultado observável: O sistema exibe os passeios compatíveis e navega para a página de detalhes (/passeios/:id) exibindo o passeio selecionado.
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

    # Aguarda e verifica o resultado observável na tela
    mensagem_resultado = page.locator(".sp-mensagem-resultado")
    expect(mensagem_resultado).to_be_visible(timeout=30000)
    expect(mensagem_resultado).to_contain_text(
        re.compile(r"Encontrei [1-9]\d* passeios? que combinam com o que você procura!")
    )

    # Verifica se pelo menos um card de passeio foi renderizado com o botão 'Ver detalhes'
    primeiro_card = page.locator(".sp-card").first
    expect(primeiro_card).to_be_visible()

    # Captura o nome do passeio sugerido antes de navegar para os detalhes
    nome_passeio = primeiro_card.locator(".sp-card-nome").inner_text().strip()

    # Completa o percurso clicando em 'Ver detalhes'
    primeiro_card.get_by_role("button", name="Ver detalhes").click()

    # Verifica o redirecionamento para a rota de detalhes e a exibição do passeio escolhido
    expect(page).to_have_url(re.compile(r".*/passeios/\d+$"), timeout=10000)
    expect(page.get_by_text(nome_passeio).first).to_be_visible(timeout=10000)