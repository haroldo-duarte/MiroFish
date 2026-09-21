<template>
  <main class="lab">
    <header class="hero">
      <div>
        <p class="eyebrow">TOYT · RESEARCH LAB</p>
        <h1>Mapa de Incertezas</h1>
        <p class="lead">O que sabemos, o que apenas suspeitamos e o que precisa ser testado antes de escalar o Toyt.</p>
      </div>
      <button class="primary" @click="showForm = !showForm">+ Nova hipótese</button>
    </header>

    <section v-if="showForm" class="panel form">
      <input v-model="draft.statement" placeholder="Ex.: Uma experiência visual mais atual aumenta a retenção." />
      <select v-model="draft.category">
        <option v-for="c in categories" :key="c" :value="c">{{ labels[c] }}</option>
      </select>
      <select v-model="draft.importance">
        <option value="high">Alta importância</option>
        <option value="medium">Média importância</option>
        <option value="low">Baixa importância</option>
      </select>
      <button class="primary" @click="createHypothesis" :disabled="saving">Salvar hipótese</button>
    </section>

    <section class="metrics">
      <article><strong>{{ hypotheses.length }}</strong><span>Hipóteses</span></article>
      <article><strong>{{ count('untested') }}</strong><span>Não testadas</span></article>
      <article><strong>{{ count('signal') }}</strong><span>Sinais</span></article>
      <article><strong>{{ count('supported') }}</strong><span>Com suporte</span></article>
      <article><strong>{{ evidence.length }}</strong><span>Evidências</span></article>
      <article><strong>{{ experiments.length }}</strong><span>Experimentos</span></article>
    </section>

    <nav class="filters">
      <button :class="{active: filter === 'all'}" @click="filter='all'">Todas</button>
      <button v-for="c in categories" :key="c" :class="{active: filter === c}" @click="filter=c">{{ labels[c] }}</button>
    </nav>

    <p v-if="error" class="error">{{ error }}</p>
    <section v-if="loading" class="empty">Carregando mapa de incertezas…</section>
    <section v-else-if="!filtered.length" class="empty">Nenhuma hipótese nesta categoria.</section>
    <section v-else class="grid">
      <article v-for="h in filtered" :key="h.hypothesis_id" class="card" @click="$router.push('/research/hypothesis/' + h.hypothesis_id)">
        <div class="card-top">
          <span class="category">{{ labels[h.category] || h.category }}</span>
          <span class="status" :data-status="h.status">{{ statusLabel(h.status) }}</span>
        </div>
        <h2>{{ h.statement }}</h2>
        <div class="meta">
          <span>Importância: {{ importanceLabel(h.importance) }}</span>
          <span>{{ h.evidence_ids?.length || 0 }} evidências</span>
          <span>{{ h.experiment_ids?.length || 0 }} experimentos</span>
          <span>{{ h.simulation_ids?.length || 0 }} simulações</span>
        </div>
      </article>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { researchApi } from '../api/research'

const hypotheses = ref([])
const evidence = ref([])
const experiments = ref([])
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const showForm = ref(false)
const filter = ref('all')
const categories = ['product','ux','clinical','behavior','market','pricing','distribution','economics']
const labels = { product:'Produto', ux:'UX / Interface', clinical:'Clínico', behavior:'Comportamento', market:'Mercado', pricing:'Pricing', distribution:'Distribuição', economics:'Economia da Saúde' }
const draft = reactive({ statement:'', category:'product', importance:'high', domain:'toyt' })

const filtered = computed(() => filter.value === 'all' ? hypotheses.value : hypotheses.value.filter(h => h.category === filter.value))
const count = status => hypotheses.value.filter(h => h.status === status).length
const statusLabel = s => ({untested:'Não testada',signal:'Sinal',supported:'Com suporte',contradicted:'Contradita',inconclusive:'Inconclusiva'}[s] || s)
const importanceLabel = s => ({high:'alta',medium:'média',low:'baixa'}[s] || s)

async function load() {
  loading.value = true; error.value = ''
  try {
    const [h,e,x] = await Promise.all([researchApi.listHypotheses(), researchApi.listEvidence(), researchApi.listExperiments()])
    hypotheses.value = h; evidence.value = e; experiments.value = x
  } catch (err) { error.value = err.message || 'Falha ao carregar Research Lab.' }
  finally { loading.value = false }
}
async function createHypothesis() {
  if (!draft.statement.trim()) return
  saving.value = true
  try {
    await researchApi.createHypothesis({...draft})
    draft.statement = ''; showForm.value = false; await load()
  } catch (err) { error.value = err.message }
  finally { saving.value = false }
}
onMounted(load)
</script>

<style scoped>
.lab{min-height:100vh;background:#f5f5f2;padding:48px;max-width:1500px;margin:auto}.hero{display:flex;justify-content:space-between;gap:32px;align-items:end;border-bottom:3px solid #111;padding-bottom:28px}.eyebrow{font-size:12px;font-weight:800;letter-spacing:.18em;margin-bottom:12px}.hero h1{font-size:48px;line-height:1}.lead{max-width:720px;margin-top:16px;color:#555;line-height:1.6}.primary{background:#111;color:#fff;border:0;padding:14px 20px;font-weight:700;cursor:pointer}.panel{background:#fff;border:1px solid #d8d8d2;padding:18px;margin-top:24px}.form{display:grid;grid-template-columns:1fr 180px 180px auto;gap:12px}.form input,.form select{border:1px solid #bbb;padding:12px;font:inherit}.metrics{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin:28px 0}.metrics article{background:#fff;border:1px solid #ddd;padding:18px}.metrics strong{display:block;font-size:30px}.metrics span{font-size:12px;color:#666}.filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px}.filters button{border:1px solid #bbb;background:transparent;padding:9px 12px;cursor:pointer}.filters .active{background:#111;color:#fff}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card{background:#fff;border:1px solid #d8d8d2;padding:22px;cursor:pointer;min-height:210px;display:flex;flex-direction:column}.card:hover{border-color:#111;transform:translateY(-2px)}.card-top{display:flex;justify-content:space-between;gap:12px}.category,.status{font-size:11px;text-transform:uppercase;font-weight:800;letter-spacing:.06em}.status[data-status="supported"]{text-decoration:underline 3px}.card h2{font-size:19px;line-height:1.45;margin:28px 0;flex:1}.meta{display:flex;gap:14px;flex-wrap:wrap;font-size:11px;color:#666;border-top:1px solid #eee;padding-top:14px}.empty,.error{padding:30px;background:#fff;border:1px solid #ddd}.error{border-color:#111}@media(max-width:1000px){.metrics{grid-template-columns:repeat(3,1fr)}.grid{grid-template-columns:repeat(2,1fr)}.form{grid-template-columns:1fr}.hero{align-items:start;flex-direction:column}}@media(max-width:650px){.lab{padding:24px}.grid{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}.hero h1{font-size:36px}}
</style>
