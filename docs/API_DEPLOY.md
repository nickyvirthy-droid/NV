API_DEPLOY
Projeto: Nicky Virthy (NV)

Documento Oficial de Implantação da API Layer
Versão: v1.11.0
Data: Agosto/2026


Porta Oficial
API Layer REST: 7001
Bind padrão: 0.0.0.0 (ou 127.0.0.1 se quiser apenas local)

Acesso local:  http://127.0.0.1:7001
Acesso rede:   http://192.168.0.250:7001
Acesso remoto: http://100.77.67.53:7001  (Tailscale)

Health público:
GET /health


Arquivos entregues
- nv-api.service          → unit systemd
- nv-api.env.example      → variáveis de ambiente
- interfaces/api/server.py (já com CORS + Rate Limit)


Instalação (servidor)

1. Garantir que o venv e o código estejam em /home/alex/NV

2. Configurar ambiente
   cp nv-api.env.example /home/alex/NV/.env
   # editar NV_API_KEY, NV_CORS_ORIGINS, etc.

3. Instalar o serviço
   sudo cp nv-api.service /etc/systemd/system/nv-api.service
   sudo systemctl daemon-reload
   sudo systemctl enable nv-api
   sudo systemctl start nv-api

4. Verificar
   sudo systemctl status nv-api
   curl -s http://127.0.0.1:7001/health | jq
   journalctl -u nv-api -f


Comandos úteis
sudo systemctl start nv-api
sudo systemctl stop nv-api
sudo systemctl restart nv-api
sudo systemctl status nv-api
journalctl -u nv-api -n 100 --no-pager


Relação com nicky.service
- nicky.service (porta 7000): processo principal (Telegram + orquestração)
- nv-api.service (porta 7001): API REST dedicada

Podem rodar em paralelo.
Se no futuro a API for incorporada ao main.py, o unit nv-api pode ser desativado.


Segurança recomendada em produção
- Definir NV_API_KEY forte
- Definir NV_CORS_ORIGINS com domínios reais (não usar *)
- Manter NV_RATE_LIMIT_ENABLED=true
- Preferir acesso via Tailscale em vez de exposição pública direta
- Firewall: liberar 7001 apenas na interface necessária


OMEGA DRAKON • SYSTEMS
Tecnologia que respira.
