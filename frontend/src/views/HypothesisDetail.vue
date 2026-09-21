<template>
  <main class="detail">
    <button class="back" @click="$router.push('/research')">← Mapa de Incertezas</button>
    <p v-if="error" class="box">{{ error }}</p>
    <template v-if="hypothesis">
      <header>
        <div>
          <p class="eyebrow">{{ label(hypothesis.category) }} · {{ hypothesis.hypothesis_id }}</p>
          <h1>{{ hypothesis.statement }}</h1>
        </div>
        <span class="state">{{ statusLabel(assessment?.status || hypothesis.status) }}</span>
      </header>

      <section class="assessment box">
        <h2>Avaliação epistemológica</h2>
        <div class="scores">
          <div><strong>{{ assessment?.support_score ?? '—' }}</strong><span>Suporte</span></div>
          <div><strong>{{ assessment?.contradiction_score ?? '—' }}</strong><span>Contradição</span></div>
          <div><strong>{{ assessment?.provenance?.real ?? 0 }}</strong><span>Evidência real</span></div>
          <div><strong>{{ assessment?.provenance?.simulation ?? 0 }}</strong><span>Simulação</span></div>
        </div>
        <p>{{ assessment?.note }}</p>
      </section>

      <section class="columns">
        <article class="box"><h2>Evidências</h2><div v-for="e in linkedEvidence" :key="e.evidence_id" class="item"><b>{{ e.title }}</b><p>{{ e.summary }}</p><small>{{ e.evidence_type }} · {{ e.direction }}</small></div><p v-if="!linkedEvidence.length">Nenhuma evidência vinculada.</p></article>
        <article class="box"><h2>Experimentos</h2><div v-for="e in linkedExperiments" :key="e.experiment_id" class="item"><b>{{ e.name }}</b><p>{{ e.method }}</p><small>{{ e.status }} · {{ e.metric || 'sem métrica definida' }}</small></div><p v-if="!linkedExperiments.length">Nenhum experimento vinculado.</p></article>
        <article class="box"><h2>Findings</h2><div v-for="f in linkedFindings" :key="f.finding_id" class="item"><b>{{ f.statement }}</b><small>{{ f.source_type }} · {{ f.direction }}</small></div><p v-if="!linkedFindings.length">Nenhum finding registrado.</p></article>
      </section>

      <section class="columns actions">
        <article class="box">
          <h2>Adicionar evidência</h2>
          <input v-model="evidenceDraft.title" placeholder="Título" />
          <select v-model="evidenceDraft.evidence_type"><option value="experiment">Experimento</option><option value="observational">Observacional</option><option value="literature">Literatura</option><option value="simulation">Simulação</option><option value="document">Documento</option></select>
          <select v-model="evidenceDraft.direction"><option value="supports">Apoia</option><option value="contradicts">Contradiz</option><option value="neutral">Neutra</option></select>
          <textarea v-model="evidenceDraft.summary" placeholder="O que esta evidência mostra?"></textarea>
          <button @click="addEvidence">Salvar evidência</button>
        </article>
        <article class="box">
          <h2>Planejar experimento</h2>
          <input v-model="experimentDraft.name" placeholder="Nome do experimento" />
          <textarea v-model="experimentDraft.method" placeholder="Método"></textarea>
          <input v-model="experimentDraft.metric" placeholder="Métrica principal" />
          <button @click="addExperiment">Salvar experimento</button>
        </article>
      </section>

      <section class="box simulate">
        <div><h2>Simular hipótese no MiroFish</h2><p>A simulação explora mecanismos e reações plausíveis. Ela gera sinal, não prova empírica.</p></div>
        <div class="simulation-form"><input v-model="projectId" placeholder="project_id com grafo Zep construído" /><button @click="simulate" :disabled="simulating">Criar simulação</button></div>
        <p v-if="simulationResult">Criada: <b>{{ simulationResult.simulation_id }}</b> · {{ simulationResult.status }}</p>
      </section>
    </template>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { researchApi } from '../api/research'
const route=useRoute(), hypothesis=ref(null), assessment=ref(null), evidence=ref([]), experiments=ref([]), findings=ref([]), error=ref('')
const projectId=ref(''), simulating=ref(false), simulationResult=ref(null)
const evidenceDraft=ref({title:'',evidence_type:'observational',direction:'supports',summary:''})
const experimentDraft=ref({name:'',method:'',metric:''})
const linkedEvidence=computed(()=>evidence.value.filter(e=>e.hypothesis_ids?.includes(route.params.hypothesisId)))
const linkedExperiments=computed(()=>experiments.value.filter(e=>e.hypothesis_ids?.includes(route.params.hypothesisId)))
const linkedFindings=computed(()=>findings.value.filter(f=>f.hypothesis_id===route.params.hypothesisId))
const labels={product:'Produto',ux:'UX / Interface',clinical:'Clínico',behavior:'Comportamento',market:'Mercado',pricing:'Pricing',distribution:'Distribuição',economics:'Economia da Saúde'}
const label=s=>labels[s]||s
const statusLabel=s=>({untested:'Não testada',signal:'Sinal',supported:'Com suporte',contradicted:'Contradita',inconclusive:'Inconclusiva'}[s]||s)
async function load(){try{const id=route.params.hypothesisId; const [h,a,e,x,f]=await Promise.all([researchApi.getHypothesis(id),researchApi.assessment(id),researchApi.listEvidence(),researchApi.listExperiments(),researchApi.listFindings()]);hypothesis.value=h;assessment.value=a;evidence.value=e;experiments.value=x;findings.value=f}catch(err){error.value=err.message}}
async function addEvidence(){try{await researchApi.createEvidence({...evidenceDraft.value,hypothesis_ids:[route.params.hypothesisId],domain:'toyt'});evidenceDraft.value={title:'',evidence_type:'observational',direction:'supports',summary:''};await load()}catch(err){error.value=err.message}}
async function addExperiment(){try{await researchApi.createExperiment({...experimentDraft.value,hypothesis_ids:[route.params.hypothesisId],domain:'toyt'});experimentDraft.value={name:'',method:'',metric:''};await load()}catch(err){error.value=err.message}}
async function simulate(){if(!projectId.value.trim())return;simulating.value=true;try{simulationResult.value=await researchApi.simulate(route.params.hypothesisId,{project_id:projectId.value.trim()});await load()}catch(err){error.value=err.message}finally{simulating.value=false}}
onMounted(load)
</script>

<style scoped>
.detail{min-height:100vh;background:#f5f5f2;padding:42px;max-width:1400px;margin:auto}.back{border:0;background:transparent;font-weight:700;cursor:pointer;margin-bottom:28px}header{display:flex;justify-content:space-between;gap:30px;border-bottom:3px solid #111;padding-bottom:28px}h1{font-size:38px;max-width:950px;line-height:1.2}.eyebrow{font-size:11px;font-weight:800;letter-spacing:.1em;margin-bottom:12px}.state{border:2px solid #111;padding:10px 14px;height:max-content;font-weight:800}.box{background:#fff;border:1px solid #d7d7d1;padding:22px;margin-top:18px}.box h2{font-size:15px;text-transform:uppercase;letter-spacing:.06em;margin-bottom:18px}.scores{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}.scores div{border-right:1px solid #ddd}.scores strong{font-size:28px;display:block}.scores span,small{font-size:11px;color:#666}.columns{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.item{border-top:1px solid #eee;padding:14px 0}.item p{margin:8px 0;color:#444;line-height:1.5}.simulate{display:grid;grid-template-columns:1fr 1fr;gap:24px}.simulate p{color:#555;margin-top:8px}.simulation-form{display:flex;gap:8px}.simulation-form input{flex:1;padding:12px;border:1px solid #aaa}.actions input,.actions select,.actions textarea{width:100%;padding:11px;border:1px solid #bbb;margin:6px 0;font:inherit}.actions textarea{min-height:90px}.actions button{background:#111;color:#fff;border:0;padding:11px 16px;font-weight:700;cursor:pointer}.simulation-form button{background:#111;color:#fff;border:0;padding:12px 18px;font-weight:700}.box>p{color:#666}@media(max-width:900px){.columns{grid-template-columns:1fr}.simulate{grid-template-columns:1fr}.scores{grid-template-columns:repeat(2,1fr)}.detail{padding:24px}header{flex-direction:column}}
</style>
