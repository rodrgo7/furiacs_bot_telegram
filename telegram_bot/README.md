# Bot do Telegram do FURIA CS

Um bot do Telegram para os fãs do FURIA CS, fornecendo notícias, recursos da comunidade e informações sobre a equipe.

## Recursos
- Últimas notícias do FURIA CS de várias fontes
- Bate-papo da comunidade com filtragem de mensagens
- Informações sobre a lista de equipes
- Atualizações do ranking da equipe
- Destaques das partidas (em breve)
- Links de mídia social

## Estrutura do projeto
```
telegram_bot/
├── config/
│ ├─── menus.py # Configurações do menu do bot
│ └─── settings.py # Configurações do ambiente e do bot
├─── banco de dados/
│ ├─── models.py # Modelos de banco de dados
│ └─── operations.py # Operações do banco de dados
├─── serviços/
│ └── news_service.py # Serviço de busca de notícias
├─── utils/
│ ├─── word_filter.py # Sistema de filtragem de mensagens
│ ├─── bads_word.py # Lista de palavras ofensivas
│ └─── encryption.py # Utilitários de criptografia
├── main.py # Aplicativo principal do bot
├─── requirements.txt # Dependências do Python
.env # Variáveis de ambiente (não estão no repositório)
```

## Configuração
1. Clonar o repositório:
```bash
git clone [repository-url]
cd telegram_bot
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` com as seguintes variáveis:
```env
API_ID=seu_telegrama_api_id
API_HASH=seu_telegrama_api_hash
BOT_TOKEN=seu_token_de_bot
DB_HOST=seu_hospedeiro_do_banco_de_dados
DB_USER=seu_usuário_do_banco_de_dados
DB_PASSWORD=sua_senha_de_banco_de_dados
DB_NAME=nome_do_seu_banco_de_dados
GNEWS_API_KEY=sua_chave_de_api_de_notícias
```

4. Configure o banco de dados MySQL:
```sql
CREATE DATABASE your_database_name;
CREATE USER 'your_database_user'@'localhost' IDENTIFIED BY 'your_database_password';
CONCEDER TODOS OS PRIVILÉGIOS EM SEU NOME_DO_BANCO_DE_DADOS.* PARA 'SEU USUÁRIO_DO_BANCO_DE_DADOS'@'localhost';
LIBERAR PRIVILÉGIOS;
```

5. Execute o bot:
```bash
python main.py
```

## Recursos em detalhes

### Serviço de notícias
- Obtém as últimas notícias do FURIA CS:
  - API do GNews
  - HLTV
  - Dust2

### Bate-papo da comunidade
- Bate-papo em tempo real para os fãs do FURIA
- Filtragem de mensagens para conteúdo ofensivo
- Limitação da taxa de mensagens
- Histórico de bate-papo

### Banco de dados
- Banco de dados MySQL para armazenamento de mensagens
- Gerenciamento de dados do usuário
- Rastreamento do histórico de mensagens

### Segurança
- Proteção de variáveis de ambiente
- Criptografia de mensagens
- Sistema de filtragem de palavras


## Agradecimentos
- FURIA Esports
- API do bot do Telegram
- Oliveiradev