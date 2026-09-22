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
| Remanejamento algorítmico | remanejamentos + remanejamento_necessidades + remanejamento_rodadas + remanejamento_rodada_itens + remanejamento_reservas | processo operacional de redistribuição de agenda quando um profissional sai; modela estado, restrições e iterações do algoritmo, **não comportamento humano nem rodadas do MiroFish** |
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
Eventos reais normalizados: sessão, falta, atraso, pendência, resolução, mensagem, tarefa, desligamento/entrada de profissional, onboarding, cancelamento e glosa. Resultados intermediários do remanejador são classificados separadamente como estado/processo algorítmico, não como decisão humana observada.

### SimulationSeed
Pergunta + recorte temporal + unidades + coortes + fontes + arquétipos + cenário inicial + número de rodadas.

## Formação dos primeiros arquétipos

### Terapeuta
Fontes: profissionais, profissional_versoes, profissionais_historico, concilia_atendimentos, central_acompanhamentos, botconversa_message_log, tasks, grupos_terapeuticos.
Sinais: área, vínculo, carga, estabilidade, agenda, volume, presença, pendências, tempo de resolução, resposta a lembretes, participação em grupos.
Não usar nome/CPF/email como traço do agente.

### Gestor de unidade
Fontes: unidades, tasks, central_acompanhamentos, concilia_atendimentos e indicadores mensais.
Sinais: unidade, carga operacional, volume de exceções, resolução, distribuição de tarefas e pressão por prazo. O resultado do algoritmo de remanejamento não deve ser usado para inferir traços ou decisões do gestor.

### Responsável familiar
Fontes: crm_patients, crm_activity_log, patient_tracking_monthly, concilia_atendimentos, botconversa_message_log.
Sinais: jornada, frequência, faltas, contatos, continuidade e resposta a comunicações. Dados devem ser agregados/cohortizados.

### Operadora / pagador
Fontes: concilia_producao, concilia_faturamento, concilia_atendimentos.
Sinais: regras observadas, autorizações, glosas, pagamento e padrões por procedimento/plano. Preferir agregação institucional.

## Classificação semântica das fontes
Antes de alimentar agentes, cada fonte deve ser classificada como:
- **estado do mundo**: agenda, grupos, profissionais, carga, capacidade;
- **regra/restrição do mundo**: limites de grupo, compatibilidade e efeitos da composição;
- **evento real**: atendimento, falta, desligamento, entrada, pendência, resolução;
- **comportamento humano observado**: comunicação, resposta, conclusão de tarefa e decisão humana identificável;
- **processo algorítmico**: cálculos/iterações produzidos pelo sistema.

O módulo de remanejamento pertence principalmente a **processo algorítmico + estado/regras do mundo**. Seu contexto é a redistribuição da agenda quando um profissional deixa a clínica: o trabalho identifica quem sai/entra e a carga disponível; os pacientes são testados sucessivamente em grupos; cada inserção altera o estado do grupo (inclusive sua composição etária) e esse novo estado condiciona a próxima tentativa. O termo "rodada" nesse módulo é uma iteração desse processo de alocação, não uma rodada multiagente do MiroFish.

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
