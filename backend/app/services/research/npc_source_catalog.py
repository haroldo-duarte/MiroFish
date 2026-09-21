"""NPC/Neuropsicocentro source catalog for Research Lab.

This module contains no credentials and performs no database access.
It is the source-of-truth mapping used by the future Supabase adapter.
"""

NPC_SOURCE_CATALOG = {
    "sessions": {
        "sources": ["concilia_atendimentos", "mv_atendimentos_mensal"],
        "purpose": ["attendance", "schedule", "workload", "unit", "procedure", "exceptions"],
        "sensitivity": "pseudonymize",
    },
    "professionals": {
        "sources": ["profissionais", "profissional_versoes", "profissionais_historico"],
        "purpose": ["role", "area", "employment", "workload", "skills", "history"],
        "sensitivity": "aggregate_or_pseudonymize",
    },
    "groups": {
        "sources": ["grupos_terapeuticos", "grupos_pacientes"],
        "purpose": ["capacity", "relationships", "schedule", "group_structure"],
        "sensitivity": "pseudonymize",
    },
    "pending_work": {
        "sources": ["central_acompanhamentos", "central_notas", "central_resumo_semanal_log"],
        "purpose": ["deadlines", "resolution_behavior", "operational_pressure"],
        "sensitivity": "pseudonymize",
    },
    "communications": {
        "sources": ["botconversa_message_log", "botconversa_advertencias", "channels", "channel_members", "messages", "direct_messages"],
        "purpose": ["communication_network", "delivery", "response_patterns"],
        "sensitivity": "restricted_content",
    },
    "tasks": {
        "sources": ["tasks", "task_comments"],
        "purpose": ["assignment", "priority", "deadline", "completion", "collaboration"],
        "sensitivity": "pseudonymize",
    },
    "remanejamento": {
        "sources": ["remanejamentos", "remanejamento_necessidades", "remanejamento_rodadas", "remanejamento_rodada_itens", "remanejamento_reservas"],
        "purpose": ["operational_decisions", "conflicts", "capacity_matching", "round_history"],
        "sensitivity": "pseudonymize",
    },
    "patient_journey": {
        "sources": ["patient_tracking_monthly", "mv_terapias_paciente_quinzena", "mv_paciente_unidade_atual", "mv_retiradas_base"],
        "purpose": ["continuity", "therapy_mix", "unit_link", "absence_patterns"],
        "sensitivity": "aggregate_or_pseudonymize",
    },
    "crm": {
        "sources": ["crm_patients", "crm_activity_log"],
        "purpose": ["lead_journey", "onboarding", "contact", "cancellation"],
        "sensitivity": "aggregate_or_pseudonymize",
    },
    "payer": {
        "sources": ["concilia_producao", "concilia_faturamento"],
        "purpose": ["authorization", "glosa", "payment", "economics"],
        "sensitivity": "aggregate",
    },
}

NPC_ARCHETYPE_RECIPES = {
    "therapist": ["professionals", "sessions", "groups", "pending_work", "communications", "tasks"],
    "unit_manager": ["sessions", "pending_work", "tasks", "remanejamento"],
    "family_caregiver": ["patient_journey", "crm", "communications", "sessions"],
    "payer": ["payer", "sessions"],
}

DIRECT_IDENTIFIERS_TO_EXCLUDE = {
    "cpf", "email", "phone", "telefone", "numero_cartao", "cns", "nome_completo"
}
