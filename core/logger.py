# ==============================================================================
# OMEGA DRAKON • SYSTEMS
# ------------------------------------------------------------------------------
# Projeto: NV (Ecossistema de Automação Modular)
# Módulo: core.logger
# Versão: 1.8.0
# Autor: Alex Projeti
# Descrição: Sistema central de logging estruturado em JSON para telemetria,
#            auditoria de comandos e rastreamento de execução de plugins.
# ------------------------------------------------------------------------------
# "Tecnologia que respira."
# ==============================================================================

import logging
import json
import sys
from datetime import datetime, timezone  # Atualizado para incluir timezone
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    """Formatador personalizado para converter logs em estruturas JSON legíveis por máquina."""
    def format(self, record: logging.LogRecord) -> str:
        log_payload: Dict[str, Any] = {
            # CORREÇÃO: Substituído datetime.utcnow() pelo padrão moderno e seguro do Python 3.12+
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        
        if hasattr(record, "extra_data"):
            log_payload["extra"] = record.extra_data
            
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_payload, ensure_ascii=False)

def setup_logger(name: str = "NV_CORE", level: int = logging.INFO) -> logging.Logger:
    """Configura o logger padrão do ecossistema NV."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(level)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(JSONFormatter())
        logger.addHandler(console_handler)
        
    return logger

nv_logger = setup_logger()
