
## ✅ Funcionalidades do Projeto (Checklist)

Abaixo listamos os Requisitos Funcionais (RF) planejados e o status atual de implementação neste protótipo:

- [x] **RF001 — Cadastro de Escola Particular**
  - *Implementação:* Modelo de dados `Escola` criado e populado via script de migração (20 escolas de exemplo). Gerenciamento via Django Admin.

- [x] **RF002 — Autenticação/Autorização**
  - *Implementação:* Utiliza o sistema de autenticação nativo do Django (`django.contrib.auth`) e painel administrativo.

- [x] **RF003 — Upload de documentos e vinculação ao checklist**
  - *Implementação:* Página de upload dedicada, suporte a tipos de documentos (AVCB, Alvarás, etc.), campo "Outros" dinâmico e validação de datas de vencimento (data específica ou ano).

- [ ] **RF004 — OCR para leitura automática de vencimentos e classificação**
  - *Status:* Não implementado.

- [ ] **RF005 — Sistema de avisos (envio e histórico)**
  - *Status:* Parcialmente atendido pela página "Arquivos a Vencer", que lista visualmente os documentos críticos. Envio de e-mails não implementado.

- [ ] **RF006 — Agenda de inscrições/renovações e relatórios**
  - *Status:* Não implementado.

- [ ] **RF007 — Geração automática de Termo de Homologação (PDF)**
  - *Status:* Não implementado.

- [ ] **RF008 — Integração / envio ao Departamento Jurídico**
  - *Status:* Não implementado.

- [ ] **RF009 — Gestão de docentes**
  - *Status:* Não implementado.

- [x] **RF010 — Painel administrativo (visão geral)**
  - *Implementação:* Dashboard na página inicial com uploads recentes e página "Arquivos a Vencer" filtrando documentos vencidos ou a vencer em 3 meses.

- [x] **RF011 — Logs e trilha de auditoria**
  - *Implementação:* Registro imutável de quem enviou (`responsavel_upload`) e quando (`data_hora_envio`) no modelo `Documento`.

- [ ] **RF012 — Importação/Exportação de dados (CSV/Excel)**
  - *Status:* Não implementado.

- [ ] **RF013 — Permissões de acesso e despersonalização de dados**
  - *Status:* Não implementado.

- [x] **RF014 — Upload seguro e armazenamento de arquivos**
  - *Implementação:* Uploads processados pelo Django, renomeação segura e restrição de edição após o envio (arquivos imutáveis).

-----

# 📘 Manual de Instalação e Execução: Projeto Demo (Django)

Bem-vindo\! Este guia foi criado para ajudar você a instalar, configurar e rodar o projeto **demo** em sua máquina, mesmo que você nunca tenha programado antes.

Este projeto utiliza **Python** e o framework **Django**.

-----

## 📋 Pré-requisitos

Antes de começar, você precisa ter duas coisas instaladas no seu computador:

1.  **Python** (Versão 3.8 ou superior):
      * [Baixar Python para Windows](https://www.python.org/downloads/windows/) (⚠️ **Importante:** Na instalação, marque a caixinha **"Add Python to PATH"**).
      * Linux: Geralmente já vem instalado. Se não, use `sudo apt install python3 python3-venv`.
2.  **Git** (Opcional, mas recomendado):
      * [Baixar Git](https://www.google.com/search?q=https://git-scm.com/downloads).

-----

## 🚀 Passo a Passo da Instalação

### 1\. Baixar o Código

Você tem duas opções:

  * **Opção A (Com Git):** Abra o terminal e digite:
    ```bash
    git clone https://github.com/YesAlcazar/lpfatec.git
    ```
  * **Opção B (Sem Git):** Vá até a página do repositório, clique no botão verde **\<\> Code** e escolha **Download ZIP**. Depois, extraia a pasta no seu computador.

### 2\. Entrar na Pasta do Projeto

Abra o seu Terminal (CMD ou PowerShell no Windows, Terminal no Linux/Mac) e navegue até a pasta do projeto.

```bash
cd lpfatec
cd demo
```

*(Nota: Certifique-se de estar na pasta onde existe o arquivo `manage.py`)*.

### 3\. Criar um Ambiente Virtual

Para não misturar as instalações do projeto com o seu computador, criamos uma "caixa isolada" chamada ambiente virtual.

  * **No Windows:**
    ```bash
    python -m venv venv
    ```
  * **No Linux/Mac:**
    ```bash
    python3 -m venv venv
    ```

### 4\. Ativar o Ambiente Virtual

Agora precisamos entrar nessa "caixa".

  * **No Windows:**
    ```bash
    venv\Scripts\activate
    ```
    *(Se aparecer `(venv)` no começo da linha do terminal, funcionou\!)*
  * **No Linux/Mac:**
    ```bash
    source venv/bin/activate
    ```

### 5\. Instalar o Django e Dependências

Agora que o ambiente está ativo, vamos instalar o Django e o que mais for necessário.

```bash
pip install django
```

*(Se houver um arquivo `requirements.txt` no projeto, use: `pip install -r requirements.txt`)*

### 6\. Configurar o Banco de Dados Inicial

O Django precisa criar algumas tabelas básicas para funcionar. Rode o comando:

```bash
python manage.py migrate
```

### 7\. Rodar o Servidor Localmente

Para testar se tudo funcionou apenas no seu computador:

```bash
python manage.py runserver
```

Abra seu navegador e acesse: `http://127.0.0.1:8000`. Se vir um foguete ou a página do projeto, parabéns\! 🎉

Para parar o servidor, volte ao terminal e aperte `Ctrl + C`.

-----

## 🌐 Como Expor na Rede (Wi-Fi)

Se você quer que **outras pessoas na mesma rede Wi-Fi** (pelo celular ou outro PC) acessem o seu sistema, siga os passos abaixo.

### 1\. Descobrir seu IP Local

Você precisa saber qual é o endereço do seu computador na rede.

  * **No Windows:** Digite `ipconfig` no terminal. Procure por **Endereço IPv4** (Geralmente algo como `192.168.0.X` ou `192.168.1.X`).
  * **No Linux:** Digite `ip a` ou `hostname -I`.

### 2\. Configurar o Django para Aceitar Conexões Externas

O Django, por segurança, bloqueia acessos externos. Precisamos liberar.

1.  Abra o arquivo `demo/settings.py` (dentro da pasta do código).
2.  Procure a linha `ALLOWED_HOSTS = []`.
3.  Mude para:
    ```python
    ALLOWED_HOSTS = ['*']
    ```
    *(O asterisco significa "permitir tudo". Em produção real, colocaríamos apenas o domínio/IP específico, mas para testes locais isso serve).*

### 3\. Rodar o Servidor para a Rede

Agora, rode o comando especificando que o servidor deve ouvir "todo mundo" (`0.0.0.0`):

```bash
python manage.py runserver 0.0.0.0:8000
```

### 4\. Acessar de Outro Dispositivo

No celular ou outro computador conectado na **mesma Wi-Fi**, abra o navegador e digite o IP que você achou no passo 1, seguido da porta 8000.

Exemplo: `http://192.168.0.15:8000`

-----

## ❓ FAQ (Perguntas Frequentes)

### 1\. O comando `python` não é reconhecido no Windows.

**R:** Provavelmente o Python não foi adicionado ao "PATH" durante a instalação. Tente usar o comando `py` em vez de `python`. Se não funcionar, reinstale o Python marcando a opção **"Add Python to environment variables"**.

### 2\. Aparece um erro `DisallowedHost` na tela.

**R:** Você esqueceu de configurar o `ALLOWED_HOSTS = ['*']` no arquivo `settings.py`. Veja a seção "Como Expor na Rede" acima.

### 3\. O terminal diz que a porta 8000 já está em uso.

**R:** Você provavelmente já tem outro servidor rodando. Tente rodar em outra porta, por exemplo, a 8080:
`python manage.py runserver 8080`

### 4\. Como faço para sair do ambiente virtual?

**R:** Basta digitar o comando `deactivate` no terminal.

### 5\. Tentei acessar pelo celular mas não carrega (Time out).

**R:** Provavelmente o **Firewall do Windows** está bloqueando a conexão.

  * Ao rodar o comando `runserver` pela primeira vez, o Windows costuma perguntar se permite o acesso. Clique em "Permitir" (marque redes privadas).
  * Se não apareceu, tente desativar o firewall temporariamente para testar.

### 6\. O CSS/Design não carregou quando acessei pelo celular.

**R:** Isso acontece porque o modo `DEBUG` do Django serve arquivos estáticos de forma simples. Certifique-se de que `DEBUG = True` está no `settings.py`. Se já estiver, verifique se o celular está acessando via `http` e não `https`.