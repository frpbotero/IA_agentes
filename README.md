# 🧠 OpenAI Text Generation Experiments

Este repositório contém experimentos e estudos práticos com a API de **Chat Completions da OpenAI**, utilizando o modelo `gpt-3.5-turbo`.

## 📁 Conteúdo

- [`1-generate_text.ipynb`](1-generate_text.ipynb):  
  Notebook principal contendo chamadas à API da OpenAI para geração de respostas com histórico de conversa, parâmetros como temperatura e max_tokens, e manipulação básica do retorno.

## 🚀 Tecnologias Utilizadas

- Python 3.12
- OpenAI Python SDK (`openai`)
- Jupyter Notebooks
- Ambiente virtual com `venv`

## ✅ Pré-requisitos

1. Python 3.12 instalado
2. Clonar este repositório:
   ```bash
   git clone https://github.com/frpbotero/openapi-app.git
   cd openapi-app
   ```
3. Criar e ativar o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate    # Windows
   ```
4. Instalar dependências:
   ```bash
     pip install openai jupyter
5. Criar um arquivo .env com sua chave da OpenAI:
  ```bash
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
  ```

💡 Objetivos do Projeto
Praticar o uso da API de chat da OpenAI

Entender os parâmetros de geração de texto como temperature, max_tokens e history

Explorar fluxos básicos de construção de assistentes e interfaces LLM com Python

📌 Observações
Este projeto é educacional e será expandido futuramente com outros testes e integrações (ex: LangChain, agentes, etc).
