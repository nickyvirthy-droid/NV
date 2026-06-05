# Changelog

## v1.2.0-memory-core

Data: 03/06/2026

### Adicionado

#### Database

* DatabaseManager
* Connection Layer
* Migration System
* Repository Pattern

#### Persistence

* KeyValueRepository
* MariaDB Integration

#### Memory

* ProfileMemory
* MemoryManager
* Generic set/get API

#### Actions

* DatetimeAction
* UptimeAction
* SystemInfoAction

#### Runtime

* Registro de database no kernel
* Registro de memory no kernel

#### CLI

* Consulta de nome persistido
* Integração com actions locais

### Corrigido

* Integração ActionManager + RuntimeKernel
* Registro automático de actions
* Persistência de perfil

### Validado

* Persistência em MariaDB
* Consulta de memória
* Actions locais
* Integração Runtime → Database → Memory

---

## Próxima Versão

v1.2.1-memory-extraction

Objetivos:

* Extração automática de memória
* Persistência automática de fatos
* Expansão do ProfileMemory
* Preparação para memória conversacional
