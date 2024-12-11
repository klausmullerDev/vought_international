Vought International - Sistema de Gestão de Super-Heróis e Missões

Bem-vindo ao sistema de gestão de super-heróis da Vought International, uma plataforma para gerenciar heróis, vilões, crimes, missões, e batalhas de forma interativa. Este sistema foi projetado com uma interface moderna e intuitiva, utilizando Python, Flask, Bootstrap e SQLite para proporcionar uma experiência completa.

Funcionalidades Principais

Gestão de Heróis:
Visualizar a lista completa de heróis.
Adicionar, editar e excluir heróis.
Filtrar heróis por nome, status (Ativo, Inativo, Banido) ou popularidade.
Atualização automática de status com base na popularidade.
Gerenciamento de Missões:
Adicionar novas missões com heróis designados.
Editar ou excluir missões existentes.
Executar missões e determinar o sucesso ou fracasso com base na força dos heróis e na dificuldade.
Filtrar missões por dificuldade, status (Pendente, Concluída, Falhada) ou outros critérios.
Registro de Crimes:
Adicionar e gerenciar crimes associados a heróis.
Ajustar automaticamente a popularidade do herói com base na severidade dos crimes.
Esconder ou desocultar crimes confidenciais.
Filtrar crimes por severidade, nome ou herói envolvido.
Simulador de Batalhas:
Simular batalhas entre heróis e vilões ou entre heróis.
Log detalhado da batalha com jogadas e resultados dinâmicos.
Atualização de força e popularidade dos participantes com base no resultado.
Registro de Batalhas:
Histórico completo das batalhas simuladas, incluindo heróis, vilões e vencedores.
Tecnologias Utilizadas

Backend:
Python 3.10
Flask (Framework web)
SQLAlchemy (ORM para banco de dados)
SQLite (Banco de dados)
Frontend:
Bootstrap 5.3 (Estilização)
HTML5/CSS3 (Interface)
JavaScript (Funcionalidades dinâmicas)
Outros:
Werkzeug (Autenticação e rotas seguras)
Jinja2 (Renderização de templates)
Estrutura do Projeto

Vought-International/
├── app/
│   ├── static/                # Arquivos estáticos (CSS, imagens, etc.)
│   │   ├── style.css          # Estilização personalizada
│   │   ├── vought_logo.jpg    # Logo da empresa
│   ├── templates/             # Templates HTML
│   │   ├── base.html          # Template base para herança
│   │   ├── index.html         # Página inicial
│   │   ├── heroes.html        # Página de heróis
│   │   ├── crimes.html        # Página de crimes
│   │   ├── missions.html      # Página de missões
│   │   ├── battle.html        # Simulador de batalhas
│   │   ├── battle_log.html    # Registro de batalhas
│   ├── __init__.py            # Inicialização do Flask
│   ├── models.py              # Modelos de dados
│   ├── routes.py              # Rotas do sistema
│   ├── database.py            # Configuração do banco de dados
├── instance/
│   ├── vought_db              # Banco de dados SQLite
├── tests/                     # Testes do sistema
├── README.md                  # Documentação do projeto
└── .gitignore                 # Arquivos ignorados pelo Git
Requisitos

Certifique-se de ter os seguintes softwares instalados:

Python: 3.10 ou superior
Pipenv ou venv: Para gerenciar dependências
SQLite: Incluído na maioria das distribuições Python
Instalação

Clone o repositório:
git clone https://github.com/seu-usuario/vought-international.git
cd vought-international
Crie um ambiente virtual:
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
Instale as dependências:
pip install -r requirements.txt
Configure o banco de dados:
python
>>> from app.database import init_db
>>> init_db()
Inicie o servidor:
flask run
Acesse no navegador:
http://127.0.0.1:5000
Testes

Execute os testes automatizados para verificar a integridade do sistema:
pytest tests/
Estilo de Código

Certifique-se de que o código segue os padrões do PEP 8. Utilize o flake8 para verificar:

flake8 app/
Melhorias Futuras

Adicionar autenticação para diferentes níveis de acesso (admin, operador, visitante).
Exportar relatórios de missões, crimes e batalhas em PDF.
Implementar notificações em tempo real para novos crimes ou mudanças no status das missões.
Adicionar um dashboard com gráficos de desempenho dos heróis.
Integração com APIs externas para gerar cenários dinâmicos de batalhas.
Integrantes do Projeto

Klaus Müller Marques
Júlio Masumi Kondo
Rafael Neris Carvalho
