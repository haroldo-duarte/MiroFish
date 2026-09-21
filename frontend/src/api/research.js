import request from './index'

export const researchApi = {
  listHypotheses(domain = 'toyt') {
    return request.get('/api/research/hypotheses', { params: { domain } })
  },
  getHypothesis(id) {
    return request.get(`/api/research/hypotheses/${id}`)
  },
  createHypothesis(payload) {
    return request.post('/api/research/hypotheses', payload)
  },
  listEvidence(domain = 'toyt') {
    return request.get('/api/research/evidence', { params: { domain } })
  },
  createEvidence(payload) {
    return request.post('/api/research/evidence', payload)
  },
  listExperiments(domain = 'toyt') {
    return request.get('/api/research/experiments', { params: { domain } })
  },
  createExperiment(payload) {
    return request.post('/api/research/experiments', payload)
  },
  listFindings(domain = 'toyt') {
    return request.get('/api/research/findings', { params: { domain } })
  },
  priorities(domain = 'toyt') {\n    return request.get('/api/research/priorities', { params: { domain } })\n  },\n  assessment(id) {
    return request.get(`/api/research/hypotheses/${id}/assessment`)
  },
  simulate(id, payload) {
    return request.post(`/api/research/hypotheses/${id}/simulate`, payload)
  }
}
