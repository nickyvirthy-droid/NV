Olá! Continuando desenvolvimento do projeto NV Runtime.

Versão atual concluída: v1.2.0-memory-core

## Visão Geral

NV Runtime é um runtime cognitivo modular desenvolvido em Python para servir como núcleo operacional da interface viva Nicky Virthy.

O objetivo do projeto é construir uma assistente operacional persistente capaz de:

* conversar com usuários;
* executar actions locais;
* acessar ferramentas do sistema;
* manter memória persistente;
* executar workflows;
* integrar serviços externos;
* operar de forma modular através de plugins.

---

# Estado Atual

Versão atual:

v1.2.0-memory-core

Branch principal:

master

Tags existentes:

* v1.0.0-foundation
* v1.1.0-actions
* v1.2.0-memory-core

Último commit relevante:

feat(memory): generic memory manager

---

# Arquitetura Atual

## Runtime

* RuntimeKernel
* RuntimeState
* RuntimeConfig
* ServiceContainer
* EventBus

## Providers

* ProviderManager
* LlamaCppProvider

Backend atual:

* llama.cpp server
* Porta: 8081
* Modelo:
  Qwen2.5-3B-Instruct-Q4_K_M

## Sessions

* SessionManager
* Session
* Histórico em memória

## Actions

* ActionRegistry
* ActionManager
* ActionContext
* ActionResolver

Actions implementadas:

* system_info
* datetime
* uptime

## Plugins

* PluginLoader
* Estrutura modular de actions

## Persistence

Banco:

MariaDB 12.2

Container Docker

Database:

nicky_db

Tabela principal:

nv_key_value

## Memory

ProfileMemory

MemoryManager

Operações disponíveis:

* set()
* get()
* exists()
* delete()

Persistência validada em MariaDB.

---

# Funcionalidades Implementadas

## Conversação

CLI funcional:

interfaces/cli/chat.py

## Memória

Nicky já consegue:

"Meu nome é Alex"

Salvar:

profile.user_name

Consultar:

"Qual meu nome?"

Resposta sem LLM.

## Actions

Perguntas operacionais executam localmente:

* informações do sistema
* versão do python
* hostname
* uptime
* data atual
* hora atual

Sem inferência do modelo.

## Persistência

Memória gravada em banco de dados.

Exemplo:

profile.user_name

profile.city

---

# Problemas Conhecidos

## Uptime

Action uptime retorna valor incorreto.

Exemplo observado:

20599 dias

Necessário revisar cálculo.

## Session Memory

Histórico ainda não é persistido.

Conversas são perdidas ao reiniciar.

## Resolver

Baseado apenas em regras estáticas.

Ainda não existe roteamento inteligente.

## Workflow Engine

Não iniciado.

## API REST

Não iniciada.

## Segurança

Não iniciada.

---

# Objetivo da Próxima Versão

Versão:

v1.2.1-memory-extraction

Objetivo:

Permitir que Nicky extraia memórias automaticamente durante a conversa.

Exemplo:

Usuário:

"Meu nome é Alex"

Salvar automaticamente:

profile.user_name

---

Usuário:

"Moro em Presidente Venceslau"

Salvar automaticamente:

profile.city

---

Usuário:

"Tenho uma impressora Bambu Lab A1"

Salvar automaticamente:

profile.printer

---

# Sugestões Técnicas

Implementar:

core/memory/extractors/

Estrutura sugerida:

* profile_extractor.py
* hardware_extractor.py
* location_extractor.py

Inicialmente usar regras simples.

Evitar LLM nesta etapa.

Persistir tudo através do MemoryManager.

---

# Regras de Compatibilidade

NÃO remover:

* RuntimeKernel
* ProviderManager
* ActionManager
* SessionManager
* MemoryManager

Manter compatibilidade com:

memory.profile.set_name()

Mesmo após introduzir sistema genérico.

Não alterar estrutura da tabela nv_key_value.

Novas funcionalidades devem ser incrementais.

Evitar breaking changes.

---

# Contexto Persistente

Infraestrutura atual do ambiente:

Servidor:

nicky-server

Sistema:

Ubuntu Server

CasaOS:

v0.4.15

LLM Local:

Qwen2.5-3B-Instruct-Q4_K_M

Backend:

llama.cpp server

Porta:

8081

Banco:

MariaDB Docker

Database:

nicky_db

Usuário conhecido:

Alex

Cidade conhecida:

Presidente Venceslau

---

# Próximo Passo Imediato

Implementar:

Automatic Memory Extraction

sem uso de LLM.

Primeiro objetivo:

Extrair automaticamente:

* nome
* cidade
* impressora
* servidor

e persistir via MemoryManager.
