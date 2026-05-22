# NV Architecture

## Core Runtime

Responsável por:
- startup
- lifecycle
- capabilities
- event orchestration

## Event Bus

Fluxo assíncrono de eventos internos.

Eventos atuais:
- USER_MESSAGE_RECEIVED
- ACTION_REQUESTED
- ACTION_COMPLETED
- SYSTEM_HEALTH_CHECK

## Action System

Pipeline:
LLM -> Parser -> ActionService -> Executor -> Action

## Workspace Security

Todas ações filesystem devem operar dentro:

/home/alex/NV/workspaces/alex

Exceção:
- modo administrador

## Interfaces

Atuais:
- FastAPI

Futuras:
- Telegram
- WebSocket
- CLI
- PWA

## LLM Layer

Atualmente:
- llama.cpp
- Ollama compatível

Futuro:
- múltiplos providers
- router
- memory
- planning
