# Action Protocol

Formato padrão:

ACTION: action_name
PARAM: value

Exemplo:

ACTION: filesystem.create_folder
PATH: projeto_python

## Regras

- não corrigir nomes automaticamente
- preservar input do usuário
- não inferir paths absolutos
- actions devem ser explícitas
