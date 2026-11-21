# Testes End-to-End (E2E) — Sistema GTur

Repositório dedicado à automação de testes End-to-End (E2E) do sistema web **GTur**, desenvolvido como atividade prática da disciplina de **Qualidade de Software (QDSW-2026-2)** no Instituto Federal de Alagoas (IFAL – Campus Maceió).

**Integrantes da Equipe:**
- Roberto dos Santos Silva Junior
- Annanda Lopes Jacobs
- Rosilene da Silva Santos

---

## 1. Ferramenta e Versões Utilizadas

- **Linguagem:** Python `3.14.0`
- **Framework de Testes:** `pytest` `9.2.0`
- **Ferramenta de Automação E2E:** `pytest-playwright` `0.10.0` (com motor `playwright` e navegador Chromium)
- **Relatórios e Evidências:** `pytest-html` `4.2.0`

---

## 2. Pré-requisitos e Configuração

### Sistema-Alvo (`GTur`)
Para executar os testes localmente, o ambiente do **GTur** precisa estar ativo:
1. **Banco de Dados PostgreSQL** em execução com o banco `gtur_db` configurado, contendo passeios cadastrados e o arquivo de embeddings atualizado (`python gerar_embeddings.py`).
2. **Backend (Django REST Framework)** rodando em `http://127.0.0.1:8000` (`python manage.py runserver`).
3. **Frontend (React + Vite)** rodando em `http://localhost:5173` (`npm run dev`).

### Ambiente de Testes (`gtur-testes-e2e`)
1. Clone este repositório e acesse a pasta do projeto:
   ```bash
   git clone https://github.com/RobertoSants/gtur-testes-e2e.git
   cd gtur-testes-e2e
   ```
2. Crie e ative o ambiente virtual Python:
   ```powershell
   python -m venv venv
   venv\Scripts\Activate
   ```
3. Instale as dependências e o navegador Chromium do Playwright:
   ```powershell
   pip install -r requirements.txt
   playwright install chromium
   ```
4. *(Opcional)* Caso utilize uma porta diferente da padrão, copie `.env.example` para `.env` e ajuste a variável `BASE_URL=http://localhost:5173`.

---

## 3. Comandos para Execução e Evidências

Com o backend e o frontend do GTur ativos, execute um dos comandos abaixo na raiz deste repositório:

- **Execução padrão (modo segundo plano, gera capturas de tela e relatório HTML):**
  ```powershell
  pytest
  ```
- **Execução visual (abre o navegador Chromium na tela para acompanhar o percurso):**
  ```powershell
  pytest --headed
  ```
- **Execução com gravação de vídeo:**
  ```powershell
  pytest --video on
  ```

Os artefatos gerados (capturas de tela de cada cenário, vídeos e o relatório consolidado `relatorio.html`) ficam salvos automaticamente na pasta `evidencias/`.

---

## 4. Resumo dos Cenários Automatizados

- **Sistema-alvo:** Aplicação Web GTur (`http://localhost:5173`) integrada à API Django REST (`http://127.0.0.1:8000`).

### Cenário 1 — Fluxo Principal (`tests/test_fluxo_principal.py`)
- **Caso de teste:** `test_buscar_e_abrir_detalhes_passeio_sugerido`
- **Ação inicial:** Acessar a página de recomendação inteligente de passeios (`/sugestao`).
- **Etapas:** Preencher o campo de descrição com o perfil desejado (*"quero algo na beira do mar, tranquilo, bom pra família"*), acionar o botão **Buscar passeios**, aguardar o processamento da recomendação, localizar o primeiro card sugerido e clicar em **Ver detalhes**.
- **Resultado observável esperado:** O sistema exibe a mensagem de confirmação com a contagem de passeios encontrados, renderiza o card do passeio compatível e redireciona para a página de detalhes (`/passeios/:id`) exibindo o título do passeio selecionado.

### Cenário 2 — Casos Negativos, Borda e Resiliência (`tests/test_caso_negativo.py`)
- **2A — Campos obrigatórios vazios (`test_login_campos_obrigatorios_vazios`):**
  - **Ação inicial:** Acessar a página de autenticação (`/login`).
  - **Etapas:** Acionar diretamente o botão **Entrar** sem preencher e-mail e senha.
  - **Resultado observável esperado:** O formulário bloqueia a requisição no cliente e exibe o alerta *"Preencha todos os campos"*.
- **2B — Credenciais inválidas na API (`test_login_credenciais_invalidas`):**
  - **Ação inicial:** Acessar a página de autenticação (`/login`).
  - **Etapas:** Preencher e-mail e senha fictícios não cadastrados e acionar **Entrar**.
  - **Resultado observável esperado:** A API rejeita a autenticação e a interface exibe a mensagem de erro mantendo o usuário na rota `/login`.
- **2C — Valor de borda e resiliência de rede (`test_sugestao_borda_e_falha_servidor`):**
  - **Ação inicial:** Acessar a página de recomendação (`/sugestao`).
  - **Etapas:** Inserir apenas espaços em branco no campo de busca (verificando o bloqueio do botão) e, em seguida, interceptar a chamada à API simulando erro interno `HTTP 500` ao submeter uma busca válida.
  - **Resultado observável esperado:** O botão **Buscar passeios** permanece desabilitado para entrada composta apenas por espaços e, diante da falha simulada no servidor, a interface exibe a mensagem amigável *"Ops! Não consegui me conectar ao servidor. Tente novamente."* sem quebra visual.

---

## 5. Delimitação de Escopo

- **O que o percurso testado exercita:** A integração de ponta a ponta entre a interface web (React/Vite), a comunicação HTTP via Axios, os endpoints da API REST (Django), a consulta ao banco de dados relacional (PostgreSQL) e o motor de recomendação semântica baseado em embeddings (`embeddings.json`).
- **O que fica fora do escopo (não permite concluir):**
  - **Persistência de escrita no banco:** Os cenários validam fluxos de consulta, recomendação e rejeição de login inválido, não comprovando operações de gravação ou alteração definitiva (como criação de reservas, cadastro de usuários ou persistência de favoritos após recarregamento da página).
  - **Serviços externos e ações críticas:** Não são testados envio de e-mails reais, recuperação de senha, meios de pagamento ou exclusão de registros.

---

## 6. Reflexão sobre Dificuldades, Limitações e Conclusões

- **Dificuldades e limitações encontradas:**
  1. **Orquestração de ambiente e massa de dados:** Como um teste E2E depende do sistema completo ativo, foi necessário garantir a execução simultânea de três serviços (PostgreSQL, Django e Vite) e a existência de passeios previamente cadastrados com descrições realistas.
  2. **Sincronização do motor NLP:** Inicialmente, a busca em `/sugestao` retornou zero resultados porque o arquivo `embeddings.json` estava desatualizado em relação aos registros do banco local. Foi necessário executar o script `gerar_embeddings.py` para sincronizar os vetores de busca e ajustar o tempo limite de espera (`timeout`) para acomodar o carregamento inicial do modelo NLP na primeira requisição.
  3. **Interceptação de rotas de rede:** Na simulação de falha `HTTP 500`, foi preciso mapear o padrão exato das requisições para a API (`/api/**`) para garantir que o Playwright interceptasse a chamada antes de atingir o backend local.
- **Conclusões do grupo:** Os testes E2E demonstraram alto valor para validar jornadas críticas sob a perspectiva real do usuário e verificar como a interface reage a falhas de rede e entradas inválidas. Contudo, evidenciaram maior custo de preparação de ambiente e maior sensibilidade a dados externos em comparação aos testes de unidade e integração já existentes no GTur, reforçando que testes E2E devem ser aplicados de forma seletiva nos fluxos principais da aplicação.