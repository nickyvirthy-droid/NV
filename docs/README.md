# NV Runtime

Interface Viva: Nicky Virthy

## Descrição

NV Runtime é um runtime cognitivo modular desenvolvido para servir como núcleo operacional da assistente Nicky Virthy.

O sistema combina:

* Runtime modular
* Providers LLM
* Actions locais
* Memória persistente
* Sistema de plugins
* Workflows
* Integrações externas

---

## Stack Atual

### Linguagem

Python 3.12

### Banco

MariaDB

### LLM

Qwen2.5-3B-Instruct-Q4_K_M

### Backend LLM

llama.cpp server

### Sistema Operacional

Ubuntu Server

---

## Estrutura

core/

* runtime
* actions
* sessions
* events
* registry
* memory
* database
* state

llm/

* providers
* prompts
* system

plugins/

* actions

interfaces/

* cli

---

## Funcionalidades

### Conversação

CLI operacional.

### Actions

* system_info
* datetime
* uptime

### Memória

Persistência via MariaDB.

### Providers

Integração com llama.cpp.

---

## Roadmap

### v1.2.1

Automatic Memory Extraction

### v1.3.0

REST API

### v1.4.0

Workflow Engine

### v1.5.0

Tool Runtime

### v2.0.0

Cognitive Runtime
