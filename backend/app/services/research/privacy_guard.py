"""Fail-closed privacy boundary before Research Lab data reaches graph or agents."""
from typing import Any, Iterable
from .npc_adapter import NormalizedRecord

FORBIDDEN_KEYS = {
    "cpf", "email", "e_mail", "phone", "telefone", "celular", "mobile",
    "numero_cartao", "numero_do_cartao", "card_number", "cns",
    "nome_completo", "full_name", "patient_name", "professional_name",
    "nome_paciente", "nome_profissional", "address", "endereco",
    "password", "senha", "token", "access_token", "refresh_token",
    "api_key", "secret", "service_role_key",
}


class ResearchPrivacyError(ValueError):
    pass


class ResearchPrivacyGuard:
    @classmethod
    def _scan(cls, value: Any, path: str = "payload") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                normalized = str(key).strip().lower()
                child_path = f"{path}.{key}"
                if normalized in FORBIDDEN_KEYS:
                    raise ResearchPrivacyError(f"Forbidden direct identifier or secret at {child_path}")
                cls._scan(child, child_path)
        elif isinstance(value, (list, tuple)):
            for index, child in enumerate(value):
                cls._scan(child, f"{path}[{index}]")

    @classmethod
    def assert_safe_record(cls, record: NormalizedRecord) -> None:
        if record.pii_removed is not True:
            raise ResearchPrivacyError(
                f"Record {record.record_type!r} is not certified as PII-removed"
            )
        cls._scan(record.payload)

    @classmethod
    def assert_safe_records(cls, records: Iterable[NormalizedRecord]) -> None:
        for record in records:
            cls.assert_safe_record(record)
