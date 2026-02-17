# FilMatch 🎬

FilMatch é um **sistema de recomendação de filmes inteligente**, que combina **perfil do usuário** e **inteligência artificial** para sugerir filmes de forma personalizada.  
O projeto inclui **sistema de login e cadastro**, **feedback do usuário**, e um recomendador que aprende com as preferências individuais.

---

## Funcionalidades principais

- Cadastro e login seguro de usuários
- Perfil de usuário com preferências de gêneros
- Recomendação de filmes baseada em inteligência artificial
- Sistema de feedback para melhorar futuras recomendações
- Interface web simples e intuitiva, feita com **Flask**, **HTML**, **CSS**, **Python** e **JavaScript**
- Banco de dados SQLite para armazenar usuários e suas preferências

---

## Pré-requisitos

- Python 3.10+  
- Git (opcional, para clonar o projeto)  

---

## Passo 1: Clonar o projeto

bash
git clone https://github.com/GUiAlvezzzzzz/FilMatch.git
cd FilMatch

## Passo 2: Criar e ativar o ambiente virtual

Windows:
    python -m venv venv
    .\venv\Scripts\activate

Linux/MacOS:
    python3 -m venv venv
    source venv/bin/activate

## Passo 3: Instalar dependências

pip install -r requirements.txt ou pip install flask requests


## Passo 4: Rodar o projeto localmente

python app.py

O Flask vai iniciar o servidor local (normalmente em http://127.0.0.1:5000)

Abra o navegador e acesse http://127.0.0.1:5000 para ver a página de login/cadastro


Estrutura do projeto (resumida):

FilMatch/
│
├─ app.py               # Arquivo principal do Flask, gerencia rotas, login e recomendador
├─ db.py                # Conexão e criação do banco SQLite
├─ static/
│   ├─ login.css         # Estilo da página de login
│   └─ login_script.js   # Script de login e registro com fetch
├─ templates/
│   └─ login.html        # Página de login e cadastro
└─ database/
    └─ app.db            # Banco de dados SQLite (após criar)



Observações importantes:

O sistema mantém o usuário logado enquanto a sessão estiver ativa no servidor local.

Todos os scripts de front-end (JS e CSS) estão em static/, e o HTML em templates/.

O recomendador utiliza perfil de usuário e inteligência artificial para sugerir filmes personalizados.

O feedback dado pelos usuários ajuda a melhorar futuras recomendações.



Autor

Guilherme Alves – Desenvolvedor do FilMatch 🎬
GitHub: GUiAlvezzzzzz
