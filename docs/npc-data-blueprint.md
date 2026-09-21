# NPC / Neuropsicocentro → MiroFish: Data Blueprint

## Status
Levantamento read-only do Supabase gerenciado pelo Lovable do projeto Neuropsicocentro. Esta especificação **não conecta** o runtime do MiroFish ao Supabase e não copia PII. Ela define de onde virá cada sinal para construir mundo, agentes, relações, memória e cenários.

## Princípio de modelagem
O MiroFish não deve transformar uma pessoa real em personagem identificável. Dados individuais alimentam agregações/coortes e arquétipos sintéticos. Toda característica derivada precisa carregar provenance. Dados observados e resultados simulados permanecem separados.

## Fontes prioritárias encontradas

| Camada | Fonte | Uso no MiroFish |
|---|---|---|
| Sessões/agenda | concilia_atendimentos | presença, horários, área, unidade, profissional, paciente, procedimento, autorização, faltas, linha verde, confirmação |
| Produção | concilia_producao | volume, procedimento, plano, unidade, aprovação/glosa |
| Movimentação | concilia_movimentacao | eventos operacionais e dinâmica temporal |
| Jornada longitudinal | patient_tracking_monthly | permanência/atividade mensal de pacientes |
| Absenteísmo | mv_absenteismo_mensal | padrões agregados de faltas por unidade/área/vínculo |
| Atendimento mensal | mv_atendimentos_mensal | volume e pacientes por unidade/status |
| Terapias | mv_terapias_paciente_quinzena | intensidade/mix terapêutico por paciente e área |
| Unidade atual | mv_paciente_unidade_atual | vínculo operacional paciente-unidade |
| Retiradas/faltas | mv_retiradas_base | faltas, motivos, elegibilidade e penalização |
| Grupos | grupos_terapeuticos + grupos_pacientes | estrutura de grupos, lotação, área, profissional, sala, dia/horário e participantes |
| Profissionais | profissionais + profissional_versoes + profissionais_historico | perfil profissional, vínculo, carga, área, certificações e mudanças históricas |
| Unidades | unidades | contexto físico/operacional e horários |
| Pendências | central_acompanhamentos + central_notas + central_resumo_semanal_log | prazo, tipo, status, resolução e intervenções |
| Comunicação automatizada | botconversa_message_log + botconversa_advertencias | envio, entrega, erro, tipo e relação com atendimentos |
| Comunicação interna | channels + channel_members + messages + direct_messages | rede e padrões de comunicação; conteúdo textual exige política específica |
| Trabalho | tasks + task_comments | atribuição, prioridade, prazo, conclusão e colaboração |
| Remanejamento | remanejamentos + remanejamento_necessidades + remanejamento_rodadas + remanejamento_rodada_itens + remanejamento_reservas | decisões operacionais em rodadas, conflitos, reservas, responsáveis |
| CRM | crm_patients + crm_activity_log | jornada de entrada, contatos, onboarding, cancelamento |
| Cadastro | controle_cadastral | completude cadastral e fricções de processo |
| Financeiro | concilia_faturamento | pagamentos/glosas/valor; usar preferencialmente agregado |

## Objetos canônicos

### WorldContext
Unidades, horários, regras, áreas, procedimentos, planos, capacidade, grupos e calendário.

### SyntheticAgentProfile
- role
- cohort
- organization_context
- goals
- incentives
- constraints
- behavioral_signals
- communication_signals
- workload_signals
- relationship_edges
- memory_summary
- provenance[]

### RelationshipEdge
Relações agregadas derivadas de grupo, unidade, tarefas, comunicação e fluxo operacional. Evitar expor nomes/IDs reais ao motor quando não necessários.

### ObservedEvent
Eventos reais normalizados: sessão, falta, atraso, pendência, resolução, mensagem, tarefa, remanejamento, onboarding, cancelamento, glosa.

### SimulationSeed
Pergunta + recorte temporal + unidades + coortes + fontes + arquétipos + cenário inicial + número de rodadas.

## Formação dos primeiros arquétipos

### Terapeuta
Fontes: profissionais, profissional_versoes, profissionais_historico, concilia_atendimentos, central_acompanhamentos, botconversa_message_log, tasks, grupos_terapeuticos.
Sinais: área, vínculo, carga, estabilidade, agenda, volume, presença, pendências, tempo de resolução, resposta a lembretes, participação em grupos.
Não usar nome/CPF/email como traço do agente.

### Gestor de unidade
Fontes: unidades, tasks, central_acompanhamentos, remanejamentos, concilia_atendimentos, indicadores mensais.
Sinais: unidade, carga operacional, volume de exceções, resolução, distribuição de tarefas, remanejamentos e pressão por prazo.

### Responsável familiar
Fontes: crm_patients, crm_activity_log, patient_tracking_monthly, concilia_atendimentos, botconversa_message_log.
Sinais: jornada, frequência, faltas, contatos, continuidade e resposta a comunicações. Dados devem ser agregados/cohortizados.

### Operadora / pagador
Fontes: concilia_producao, concilia_faturamento, concilia_atendimentos.
Sinais: regras observadas, autorizações, glosas, pagamento e padrões por procedimento/plano. Preferir agregação institucional.

## Memória
A memória do agente deve ser composta de eventos normalizados e resumos agregados, não de dumps de linhas. Cada item deve conter source_table, source_key pseudonimizada, observed_at e extraction_version.

## Rodadas
1. Snapshot real do período selecionado.
2. Construção dos arquétipos/coortes.
3. Construção de relações.
4. Seed do cenário.
5. Rodada N: ações/interações.
6. Persistência de memória sintética da rodada.
7. Próxima rodada.
8. ReportAgent.
9. Finding marcado como synthetic/simulation.
10. Reavaliação epistemológica sem promover simulação a prova empírica.

## Estratégia de atualização
Fase 1: snapshot read-only para exploração e calibração.
Fase 2: adapter Supabase incremental por updated_at/imported_at/data.
Fase 3: atualização quase em tempo real somente para fontes em que isso gere valor. O Knowledge Graph recebe upserts idempotentes com watermark por fonte.

## Segurança
- conexão server-side; nunca service-role no frontend;
- princípio do menor privilégio e preferencialmente views/RPCs read-only;
- pseudonimização antes de enviar dados ao motor;
- excluir credenciais, CPF, telefone, cartão e outros identificadores diretos;
- conteúdo de mensagens deve ter governança própria antes de ser usado;
- provenance obrigatório;
- logs de ingestão e versão de transformação.

## Próxima conexão
Implementar NPCSupabaseAdapter contra views/RPCs read-only dedicadas. O adapter deve produzir os objetos canônicos acima e manter watermarks. Esta branch deixa o contrato e o catálogo prontos sem armazenar credenciais.
