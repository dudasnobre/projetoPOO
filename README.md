# projetoPOO 
# 🏖️ Costa Bella — Sistema de Cadastro e Reservas

Este é um projeto web desenvolvido em Python utilizando o microframework **Flask** e o banco de dados **SQLite3**. O sistema gerencia a interface e a inteligência de negócios do restaurante à beira-mar chamado **Costa Bella**, oferecendo controle de acesso seguro para clientes e administradores.

---

## 📝 Funcionalidades do Sistema

* **Sistema de Autenticação Completo:** Telas responsivas de Cadastro e Login com validações de campos e mensagens dinâmicas (*flash messages*).
* **Controle de Níveis de Acesso (RBAC):** * **Usuário Comum:** Pode visualizar o cardápio e solicitar reservas de mesas.
  * **Administrador:** Possui privilégios exclusivos para acessar o painel de gerenciamento (`/reservas`) e visualizar todas as reservas efetuadas no banco de dados.
* **Mecanismo de Reserva Integrado:** Envio automático de dados estruturados (nome, telefone, data e quantidade de pessoas) para o banco de dados.
* **Persistência Local:** Banco de dados relacional leve (SQLite3) criado de forma automatizada na inicialização da aplicação.
* **Interface Dinâmica:** Front-end integrado com Jinja2, oferecendo suporte a rotas protegidas e troca de temas (Light/Dark mode).

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3 (Flask)
* **Frontend:** HTML5, CSS3 (Responsivo), FontAwesome
* **Banco de Dados:** SQLite3
* **Segurança:** Sessões criptografadas usando `app.secret_key` para prevenção de acessos indevidos.

---

## 🏗️ Estrutura Arquitetural (Mapeamento POO)

Embora o microframework Flask utilize rotas baseadas em funções no arquivo principal, os conceitos de **Programação Orientada a Objetos** e design de software estão aplicados implicitamente na estrutura de dados do projeto:

* **Abstração de Entidades:** Os dados manipulados pelo sistema representam objetos de entidades do mundo real (as tabelas `usuarios` e `reservas` mapeiam propriedades específicas que definem o estado de cada instância dessas entidades).
* **Encapsulamento e Estado com Dicionários de Linha (`sqlite3.Row`):** O uso do `conn.row_factory = sqlite3.Row` encapsula as tuplas do banco de dados em objetos de mapeamento baseados em chaves textuais, protegendo e organizando as propriedades de cada registro de usuário e reserva.
* **Gerenciamento de Estado Dinâmico:** O objeto global `session` do Flask funciona como um encapsulador do estado de login atual do cliente, isolando e retendo os atributos da sessão ativa do usuário.

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina. Você pode verificar executando:
```bash
python --version
