from playwright.sync_api import Page, expect


def test_login_campos_obrigatorios_vazios(page: Page, base_url: str):
    """
    Cenário 2A (Caso Negativo - Campos Obrigatórios Vazios):
    - Ação inicial: Acessar a página de login (/login).
    - Etapas: Clicar diretamente no botão 'Entrar' sem preencher email e senha.
    - Resultado observável: O sistema bloqueia o envio no cliente e exibe o alerta 'Preencha todos os campos'.
    """
    page.goto(f"{base_url}/login")

    expect(page.get_by_role("heading", name="Login")).to_be_visible()

    page.get_by_role("button", name="Entrar").click()

    alerta_erro = page.locator(".alert-error")
    expect(alerta_erro).to_be_visible()
    expect(alerta_erro).to_contain_text("Preencha todos os campos")


def test_login_credenciais_invalidas(page: Page, base_url: str):
    """
    Cenário 2B (Caso Negativo - Credenciais Inválidas na API):
    - Ação inicial: Acessar a página de login (/login).
    - Etapas: Informar um email e senha fictícios não cadastrados e clicar em 'Entrar'.
    - Resultado observável: A API rejeita a autenticação e a interface exibe mensagem de erro sem redirecionar.
    """
    page.goto(f"{base_url}/login")

    page.get_by_label("Email").fill("usuario.inexistente.teste@exemplo.com")
    page.get_by_label("Senha").fill("SenhaInvalida123")
    page.get_by_role("button", name="Entrar").click()

    alerta_erro = page.locator(".alert-error")
    expect(alerta_erro).to_be_visible(timeout=10000)
    expect(page).to_have_url(f"{base_url}/login")


def test_sugestao_borda_e_falha_servidor(page: Page, base_url: str):
    """
    Cenário 2C (Caso de Borda e Resiliência - Espaços em Branco e Erro 500 da API):
    - Ação inicial: Acessar a página de recomendação (/sugestao).
    - Etapas: Preencher apenas espaços em branco (verificando botão desabilitado) e depois simular falha 500 da API ao buscar.
    - Resultado observável: O botão permanece bloqueado para entrada vazia e, diante de falha no servidor, a interface exibe alerta amigável sem quebrar.
    """
    page.goto(f"{base_url}/sugestao")

    campo_descricao = page.get_by_placeholder(
        "Ex: quero algo na beira do mar, tranquilo, bom pra família..."
    )
    botao_buscar = page.get_by_role("button", name="Buscar passeios")

    # 1. Valor de borda: apenas espaços em branco não deve habilitar o envio
    campo_descricao.fill("     ")
    expect(botao_buscar).to_be_disabled()

    # 2. Simulação de falha na API (HTTP 500) para verificar resiliência da interface
    page.route("**/api/**", lambda route: route.fulfill(status=500, body="Internal Server Error"))

    campo_descricao.fill("passeio de jangada em maceio")
    expect(botao_buscar).to_be_enabled()
    botao_buscar.click()

    mensagem_erro = page.locator(".sp-mensagem-semresultado")
    expect(mensagem_erro).to_be_visible(timeout=10000)
    expect(mensagem_erro).to_contain_text("Ops! Não consegui me conectar ao servidor. Tente novamente.")



def test_cadastro_senhas_nao_coincidem(page: Page, base_url: str, output_path):
    """
    Cenário 2D (Caso Negativo - Senhas Diferentes no Cadastro):
    - Ação inicial: Acessar a página de cadastro (/cadastro).
    - Etapas: Preencher os campos obrigatórios com dados válidos,
      exceto a confirmação de senha, que será diferente da senha original.
    - Resultado observável: O sistema bloqueia o cadastro e exibe
      o alerta 'As senhas não coincidem'.
    """
    page.goto(f"{base_url}/cadastro")

    page.locator('input[name="firstName"]').fill("Usuario")
    page.locator('input[name="lastName"]').fill("Teste")
    page.locator('input[name="email"]').fill("usuario.teste@example.com")
    page.locator('input[type="tel"]').fill("+5582999999999")
    page.locator('input[name="senha"]').fill("SenhaTeste123")
    page.locator('input[name="confirmarSenha"]').fill("SenhaDiferente123")

    page.locator("button.submit-btn").click()

    alerta_erro = page.locator(".alert.alert-error")

    expect(alerta_erro).to_be_visible()
    expect(alerta_erro).to_contain_text("As senhas não coincidem")

    page.evaluate("window.scrollTo(0, 0)")

    page.screenshot(
        path=f"{output_path}/cadastro-senhas-diferentes.png",
        full_page=True
    )
