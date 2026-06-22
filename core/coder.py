"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Coder Engine

Descrição: Fundação do sistema de autoevolução.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import subprocess
import sys
import shutil
import ast

from pathlib import Path
from datetime import datetime
from observability.logging.logger import (
    logger
)
from dataclasses import dataclass

class FileInspector:

    IGNORED_DIRS = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache"
    }

    def __init__(
        self,
        project_root="."
    ):

        self.project_root = Path(
            project_root
        ).resolve()

    def list_files(self):

        files = []

        for path in self.project_root.rglob("*"):

            if not path.is_file():
                continue

            if any(
                part in self.IGNORED_DIRS
                for part in path.parts
            ):
                continue

            files.append(
                str(
                    path.relative_to(
                        self.project_root
                    )
                )
            )

        return sorted(files)

    def read_file(
        self,
        relative_path: str
    ):

        file_path = (
            self.project_root /
            relative_path
        ).resolve()

        if not str(file_path).startswith(
            str(self.project_root)
        ):
            raise ValueError(
                "Acesso negado."
            )

        return file_path.read_text(
            encoding="utf-8"
        )

class SandboxManager:

    def __init__(
        self,
        sandbox_dir="sandbox"
    ):

        self.sandbox_dir = Path(
            sandbox_dir
        )

        self.sandbox_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def write_file(
        self,
        filename: str,
        content: str
    ):

        target = (
            self.sandbox_dir /
            filename
        )

        target.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        target.write_text(
            content,
            encoding="utf-8"
        )

        logger.info(
            f"Sandbox write: {target}"
        )

        return str(target)

    def create_copy(
        self,
        file_path: str
    ):

        source = Path(file_path)

        target = (
            self.sandbox_dir /
            file_path
        )

        target.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(
            source,
            target
        )

        logger.info(
            f"Sandbox copy: {source} -> {target}"
        )

        return str(target)

    def promote_copy(
        self,
        sandbox_file: str,
        target_file: str
    ):

        shutil.copy2(
            sandbox_file,
            target_file
        )

        logger.info(
            f"Sandbox promote: "
            f"{sandbox_file} -> {target_file}"
        )

    def remove_copy(
        self,
        sandbox_file: str
    ):

        sandbox_path = Path(
            sandbox_file
        )

        if sandbox_path.exists():

            sandbox_path.unlink()

            logger.info(
                f"Sandbox remove: "
                f"{sandbox_file}"
            )

class BackupManager:

    def __init__(
        self,
        backup_dir="backups"
    ):

        self.backup_dir = Path(
            backup_dir
        )

        self.backup_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def create_backup(
        self,
        file_path: str
    ):

        source = Path(
            file_path
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_name = (
            f"{source.name}.{timestamp}.bak"
        )

        destination = (
            self.backup_dir /
            backup_name
        )

        shutil.copy2(
            source,
            destination
        )

        logger.info(
            f"Backup criado: {destination}"
        )

        return str(destination)


class RollbackManager:

    def restore(
        self,
        backup_file: str,
        target_file: str
    ):

        shutil.copy2(
            backup_file,
            target_file
        )

        logger.warning(
            f"Rollback executado: "
            f"{backup_file} -> {target_file}"
        )

        return True

class ValidationEngine:

    DEFAULT_TESTS = [

        "tests/test_memory_manager.py",

        "tests/test_profile_memory.py",

        "tests/test_runtime_memory.py",

        "tests/test_resolver.py",
    ]

    def __init__(
        self,
        tests=None
    ):

        self.tests = (
            tests
            or self.DEFAULT_TESTS
        )

    def run_tests(self):

        results = []

        overall_success = True

        for test_file in self.tests:

            logger.info(
                f"Executando teste: {test_file}"
            )

            result = subprocess.run(
                [
                    sys.executable,
                    test_file
                ],
                capture_output=True,
                text=True
            )

            test_success = (
                result.returncode == 0
            )

            if not test_success:

                overall_success = False

            results.append(
                {
                    "file": test_file,
                    "success": test_success,
                    "return_code": (
                        result.returncode
                    ),
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            )

        return {
            "success": overall_success,
            "results": results
        }

class GitManager:

    def status(self):

        result = subprocess.run(
            [
                "git",
                "status",
                "--short"
            ],
            capture_output=True,
            text=True
        )

        return result.stdout

    def current_branch(self):

        result = subprocess.run(
            [
                "git",
                "rev-parse",
                "--abbrev-ref",
                "HEAD"
            ],
            capture_output=True,
            text=True
        )

        return result.stdout.strip()

    def add(
        self,
        files: list[str]
    ):

        result = subprocess.run(
            [
                "git",
                "add",
                *files
            ],
            capture_output=True,
            text=True
        )

        logger.info(
            f"Git add: {files}"
        )

        return {
            "success": (
                result.returncode == 0
            ),
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def log(
        self,
        limit: int = 10
    ):

        result = subprocess.run(
            [
                "git",
                "log",
                "--oneline",
                f"-{limit}"
            ],
            capture_output=True,
            text=True
        )

        return result.stdout

    def diff(self):

        result = subprocess.run(
            [
                "git",
                "diff"
            ],
            capture_output=True,
            text=True
        )

        return result.stdout

    def checkout(
        self,
        branch: str
    ):

        result = subprocess.run(
            [
                "git",
                "checkout",
                branch
            ],
            capture_output=True,
            text=True
        )

        logger.info(
            f"Git checkout: {branch}"
        )

        return {
            "success": (
                result.returncode == 0
            ),
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def fetch(self):

        result = subprocess.run(
            [
                "git",
                "fetch"
            ],
            capture_output=True,
            text=True
        )

        return {
            "success": (
                result.returncode == 0
            ),
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def pull(self):

        result = subprocess.run(
            [
                "git",
                "pull"
            ],
            capture_output=True,
            text=True
        )

        return {
            "success": (
                result.returncode == 0
            ),
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def push(self):

        result = subprocess.run(
            [
                "git",
                "push"
            ],
            capture_output=True,
            text=True
        )

        return {
            "success": (
                result.returncode == 0
            ),
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def commit(
        self,
        message: str,
        files: list[str] | None = None
    ):

        if files:

            self.add(files)

        result = subprocess.run(
            [
                "git",
                "commit",
                "-m",
                message
            ],
            capture_output=True,
            text=True,
            check=False
        )

        logger.info(
            f"Git commit: {message}"
        )

        return {
            "success": (
                result.returncode == 0
            ),
            "stdout": result.stdout,
            "stderr": result.stderr
        }

@dataclass
class CodePatch:
    file_path: str
    old_text: str
    new_text: str
    description: str = ""


class CodeAnalyzer:

    def analyze_file(self, file_path: str):

        source = Path(file_path).read_text(
            encoding="utf-8"
        )

        tree = ast.parse(source)

        imports = []
        classes = []
        functions = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                imports.extend(
                    alias.name
                    for alias in node.names
                )

            elif isinstance(
                node,
                ast.ImportFrom
            ):
                imports.append(
                    node.module
                )

            elif isinstance(
                node,
                ast.ClassDef
            ):
                classes.append(
                    node.name
                )

            elif isinstance(
                node,
                ast.FunctionDef
            ):
                functions.append(
                    node.name
                )

        return {
            "file": file_path,
            "lines": len(
                source.splitlines()
            ),
            "imports": sorted(
                set(imports)
            ),
            "classes": sorted(
                classes
            ),
            "functions": sorted(
                functions
            )
        }


class ValidationPipeline:

    def __init__(
        self,
        validator: ValidationEngine
    ):

        self.validator = validator

    def syntax_check(
        self,
        file_path: str
    ):

        if not file_path.endswith(".py"):

            return {
                "success": True,
                "skipped": True
            }

        try:

            source = Path(
                file_path
            ).read_text(
                encoding="utf-8"
            )

            ast.parse(source)

            return {
                "success": True
            }

        except Exception as exc:

            return {
                "success": False,
                "error": str(exc)
            }

    def validate(
        self,
        file_path: str
    ):

        syntax = self.syntax_check(
            file_path
        )

        if not syntax["success"]:

            return {
                "success": False,
                "stage": "syntax",
                "details": syntax
            }

        tests = (
            self.validator.run_tests()
        )

        if not tests["success"]:

            return {
                "success": False,
                "stage": "tests",
                "details": tests
            }

        return {
            "success": True
        }


class SafeApply:

    def __init__(
        self,
        sandbox_manager,
        backup_manager,
        rollback_manager,
        validator,
        git_manager
    ):

        self.sandbox = sandbox_manager
        self.backup = backup_manager
        self.rollback = rollback_manager
        self.validator = validator
        self.git = git_manager

    def apply_patch(
        self,
        patch: CodePatch,
        commit_message=None
    ):

        target_file = patch.file_path

        sandbox_file = (
            self.sandbox.create_copy(
                target_file
            )
        )

        sandbox_path = Path(
            sandbox_file
        )

        original = sandbox_path.read_text(
            encoding="utf-8"
        )

        if patch.old_text not in original:

            self.sandbox.remove_copy(
                sandbox_file
            )

            return {
                "success": False,
                "error": (
                    "Texto original "
                    "não encontrado."
                )
            }

        modified = original.replace(
            patch.old_text,
            patch.new_text
        )

        sandbox_path.write_text(
            modified,
            encoding="utf-8"
        )

        validation = (
            self.validator.validate(
                sandbox_file
            )
        )

        if not validation["success"]:

            self.sandbox.remove_copy(
                sandbox_file
            )

            return {
                "success": False,
                "validation": validation
            }

        backup_file = (
            self.backup.create_backup(
                target_file
            )
        )

        self.sandbox.promote_copy(
            sandbox_file,
            target_file
        )

        self.sandbox.remove_copy(
            sandbox_file
        )

        if commit_message:

            self.git.commit(
                commit_message,
                [target_file]
            )

        return {
            "success": True,
            "backup": backup_file
        }

class CoderEngine:

    def __init__(self):

        self.inspector = (
            FileInspector()
        )

        self.sandbox = (
            SandboxManager()
        )

        self.backup = (
            BackupManager()
        )

        self.rollback = (
            RollbackManager()
        )

        self.validator = (
            ValidationEngine()
        )

        self.git = (
            GitManager()
        )

        self.analyzer = (
            CodeAnalyzer()
        )

        self.pipeline = (
            ValidationPipeline(
                self.validator
            )
        )

        self.safe_apply = (
            SafeApply(
                self.sandbox,
                self.backup,
                self.rollback,
                self.pipeline,
                self.git
            )
        )
