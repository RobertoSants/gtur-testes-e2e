from playwright.sync_api import Page, expect


def test_login_campos_obrigatorios_vazios(page: Page, base_url: str):
    """
    Cenário 2A (Caso Negativo - Campos Obrigatórios Vazios):
    - Ação inicial: Acessar a página de login (/login).
    - Etapas: Clicar diretamente no botão 'Entrar' sem preencher email e senha.
    - Resultado observável: O sistema bloqueia o envio e exibe o alerta 'Preencha todos os campos'.
    """
    page.goto(f"{base_url}/login")

    expect(page.get_by_role("heading", name="Login")).to_be_visible()

    page.get_by_role("button", name="Entrar").click()

    alerta_erro = page.locator(".alert-error")
    expect(alerta_erro).to_be_visible()
    expect(alerta_erro).to_contain_text("Preencha todos os campos")


def test_login_credenciais_invalidas(page: Page, base_url: str):
    """
    Cenário 2B (Caso Negativo - Credenciais Inválidas):
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