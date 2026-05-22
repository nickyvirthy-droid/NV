# NV Working State

## Runtime
STATUS: funcionando

## API
STATUS: funcionando

Endpoints:
- /health
- /state
- /actions
- /chat
- /docs

## Action System
STATUS: funcionando

Ações:
- filesystem.create_folder

## Segurança
STATUS: parcialmente implementada

Proteções:
- sandbox workspace
- bloqueio de paths externos

## Problemas conhecidos

- LLM ainda altera nomes digitados incorretamente
- sem memória persistente
- sem autenticação
- sem permissões por usuário
