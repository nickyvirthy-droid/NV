# ==============================================================================
# OMEGA DRAKON • SYSTEMS
# ------------------------------------------------------------------------------
# Projeto: NV (Ecossistema de Automação Modular)
# Módulo: tests.test_logger
# Versão: 1.8.0
# Autor: Alex Projeti
# Descrição: Ficheiro de testes unitários para validação do formato JSON e da
#            estrutura de telemetria do sistema de logs estruturados.
# ------------------------------------------------------------------------------
# "Tecnologia que respira."
# ==============================================================================

import logging
import json
import io
import unittest
from datetime import datetime
from core.logger import setup_logger

class TestJSONLogger(unittest.TestCase):
    """Conjunto de testes para garantir a conformidade do formato JSON dos logs."""

    def setUp(self):
        """Configura um stream de captura em memória antes de cada teste."""
        self.stream = io.StringIO()
        # Cria um logger isolado apontando para o nosso stream em memória
        self.logger = logging.getLogger("TEST_NV_LOG")
        self.logger.setLevel(logging.INFO)
        
        # Importa o formatador dinamicamente para garantir o vínculo
        from core.logger import JSONFormatter
        self.handler = logging.StreamHandler(self.stream)
        self.handler.setFormatter(JSONFormatter())
        self.logger.addHandler(self.handler)

    def tearDown(self):
        """Limpa os handlers após a execução do teste."""
        self.logger.removeHandler(self.handler)
        self.handler.close()

    def test_log_output_is_valid_json(self):
        """Garante que a saída do logger seja um JSON válido e contenha os campos obrigatórios."""
        mensagem_teste = "Inicializando módulo de teste."
        self.logger.info(mensagem_teste)
        
        # Recupera a string gerada e faz o parse para dicionário
        output = self.stream.getvalue().strip()
        log_data = json.loads(output)
        
        # Validação dos campos estruturais exigidos pelo core
        self.assertEqual(log_data["level"], "INFO")
        self.assertEqual(log_data["message"], mensagem_teste)
        self.assertIn("timestamp", log_data)
        self.assertIn("module", log_data)
        self.assertIn("function", log_data)

    def test_log_with_extra_context_data(self):
        """Garante que metadados passados no argumento 'extra_data' sejam injetados corretamente."""
        self.logger.warning(
            "Falha temporária de conexão.", 
            extra={"extra_data": {"ip": "127.0.0.1", "tentativa": 3}}
        )
        
        output = self.stream.getvalue().strip()
        log_data = json.loads(output)
        
        # Validação do payload customizado
        self.assertEqual(log_data["level"], "WARNING")
        self.assertEqual(log_data["extra"]["ip"], "127.0.0.1")
        self.assertEqual(log_data["extra"]["tentativa"], 3)

    def test_log_exception_capture(self):
        """Garante que exceções sejam tratadas e adicionadas ao bloco 'exception' do JSON."""
        try:
            1 / 0
        except ZeroDivisionError:
            self.logger.error("Erro matemático detetado.", exc_info=True)
            
        output = self.stream.getvalue().strip()
        log_data = json.loads(output)
        
        self.assertEqual(log_data["level"], "ERROR")
        self.assertIn("exception", log_data)
        self.assertIn("ZeroDivisionError", log_data["exception"])

if __name__ == "__main__":
    unittest.main()
