async function refreshHealth() {
  const r = await fetch('/api/health');
  const d = await r.json();
  document.getElementById('health').textContent =
    `API OK • ${d.vector_chunks} chunks • Groq ${d.groq_configured ? 'on' : 'off'} • Tavily ${d.tavily_configured ? 'on' : 'off'}`;
}
refreshHealth();

async function uploadPdf() {
  const file = document.getElementById('pdf').files[0];
  const out = document.getElementById('uploadResult');
  if (!file) { out.textContent = 'Choose a PDF first.'; return; }
  const form = new FormData();
  form.append('file', file);
  out.textContent = 'Indexing...';
  const r = await fetch('/api/documents/upload', { method: 'POST', body: form });
  const d = await r.json();
  out.textContent = r.ok ? `Indexed ${d.chunks} chunks.` : (d.detail || 'Upload failed.');
  refreshHealth();
}

async function research() {
  const query = document.getElementById('query').value.trim();
  const useWeb = document.getElementById('web').checked;
  if (!query) return;

  const card = document.getElementById('answerCard');
  card.classList.remove('hidden');
  document.getElementById('answer').textContent = 'Researching...';
  document.getElementById('sources').innerHTML = '';

  const r = await fetch('/api/research', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query, use_web: useWeb, top_k: 5})
  });
  const d = await r.json();
  if (!r.ok) {
    document.getElementById('answer').textContent = d.detail || 'Research failed.';
    return;
  }

  document.getElementById('route').textContent = `Route: ${d.route}`;
  document.getElementById('answer').textContent = d.answer;
  document.getElementById('metrics').textContent = JSON.stringify(d.metrics, null, 2);

  const box = document.getElementById('sources');
  for (const s of d.sources) {
    const div = document.createElement('div');
    div.className = 'source';
    div.innerHTML = `<strong>[${s.id}] ${escapeHtml(s.title)}</strong>
      <div class="muted">${escapeHtml(s.source_type)}${s.page ? ` • page ${s.page}` : ''}${s.score != null ? ` • score ${s.score}` : ''}</div>
      ${s.url ? `<a href="${escapeAttr(s.url)}" target="_blank" rel="noopener">Open source</a>` : ''}
      <div>${escapeHtml(s.snippet)}</div>`;
    box.appendChild(div);
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}
function escapeAttr(s) { return escapeHtml(s); }
