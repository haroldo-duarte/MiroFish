from app.models.research_hierarchy import ResearchDomain, Study, ResearchQuestion
from app.models.hypothesis import Hypothesis


def test_research_hierarchy_links_domain_study_question_hypothesis():
    domain = ResearchDomain(name="NPC", slug="npc")
    study = Study(domain_id=domain.domain_id, title="Pendências")
    question = ResearchQuestion(study_id=study.study_id, question="Qual estratégia reduz perda de prazo?")
    hypothesis = Hypothesis(
        statement="Lembretes melhoram resolução",
        category="behavior",
        domain="npc",
        study_id=study.study_id,
        question_id=question.question_id,
    )
    assert study.domain_id == domain.domain_id
    assert question.study_id == study.study_id
    assert hypothesis.study_id == study.study_id
    assert hypothesis.question_id == question.question_id
