"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Security Exceptions

Descrição: Exceções da Security Layer.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""


class SecurityError(Exception):
    pass


class PolicyViolation(SecurityError):
    pass


class PermissionDenied(SecurityError):
    pass


class ScopeViolation(SecurityError):
    pass


class ApprovalRequired(SecurityError):
    pass


class SecurityConfigurationError(SecurityError):
    pass
