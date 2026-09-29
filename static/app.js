const input = document.getElementById('imageInput');
const dropzone = document.getElementById('dropzone');
const previewImage = document.getElementById('previewImage');
const emptyState = document.getElementById('emptyState');
const previewState = document.getElementById('previewState');
const analyzeBtn = document.getElementById('analyzeBtn');
const errorText = document.getElementById('errorText');
const loader = document.getElementById('loader');
const resultEmpty = document.getElementById('resultEmpty');
const resultContent = document.getElementById('resultContent');

let selectedFile = null;

function setError(message = '') {
  errorText.textContent = message;
  errorText.classList.toggle('hidden', !message);
}

function setFile(file) {
  if (!file) return;
  const allowed = ['image/jpeg', 'image/png', 'image/webp'];
  if (!allowed.includes(file.type)) {
    setError('Use a JPG, PNG or WEBP image.');
    return;
  }
  if (file.size > 8 * 1024 * 1024) {
    setError('Image is too large. Maximum size is 8 MB.');
    return;
  }

  setError('');
  selectedFile = file;
  const url = URL.createObjectURL(file);
  previewImage.src = url;
  emptyState.classList.add('hidden');
  previewState.classList.remove('hidden');
  analyzeBtn.disabled = false;
}

input.addEventListener('change', () => setFile(input.files[0]));

dropzone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropzone.classList.add('dragover');
});
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropzone.classList.remove('dragover');
  setFile(e.dataTransfer.files[0]);
});

function populate(data) {
  const p = data.prediction;
  const n = data.nutrition;
  document.getElementById('foodName').textContent = n.food_name || p.label;
  document.getElementById('confidence').textContent = `${p.confidence}%`;
  document.getElementById('confidenceBar').style.width = `${Math.min(100, Math.max(0, p.confidence))}%`;
  document.getElementById('calories').textContent = Math.round(Number(n.calories_kcal || 0));
  document.getElementById('servingEstimate').textContent = `Serving estimate: ${n.serving_estimate || '—'}`;

  const macros = n.macros_g || {};
  document.getElementById('protein').textContent = Number(macros.protein || 0).toFixed(1);
  document.getElementById('carbs').textContent = Number(macros.carbs || 0).toFixed(1);
  document.getElementById('fat').textContent = Number(macros.fat || 0).toFixed(1);
  document.getElementById('fiber').textContent = Number(macros.fiber || 0).toFixed(1);

  const ingredients = document.getElementById('ingredients');
  ingredients.innerHTML = '';
  (n.ingredients || []).forEach(item => {
    const span = document.createElement('span');
    span.className = 'chip';
    span.textContent = item;
    ingredients.appendChild(span);
  });
  document.getElementById('ingredientCount').textContent = (n.ingredients || []).length;

  const micros = document.getElementById('micros');
  micros.innerHTML = '';
  (n.micros || []).forEach(item => {
    const row = document.createElement('div');
    row.className = 'micro-item';
    row.innerHTML = `<span>${escapeHtml(item.name || '')}</span><strong>${escapeHtml(item.amount || '')}</strong>`;
    micros.appendChild(row);
  });

  document.getElementById('confidenceNote').textContent = n.confidence_note || 'Nutrition values are estimates based on the visible serving.';

  const predictions = document.getElementById('topPredictions');
  predictions.innerHTML = '';
  (p.top_predictions || []).forEach(item => {
    const row = document.createElement('div');
    row.className = 'pred-row';
    row.innerHTML = `<span>${escapeHtml(item.label)}</span><strong>${item.confidence}%</strong>`;
    predictions.appendChild(row);
  });
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

analyzeBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  setError('');
  analyzeBtn.disabled = true;
  analyzeBtn.querySelector('span:first-child').textContent = 'Analyzing…';
  loader.classList.remove('hidden');

  const formData = new FormData();
  formData.append('image', selectedFile);

  try {
    const response = await fetch('/predict', { method: 'POST', body: formData });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Analysis failed.');

    populate(data);
    resultEmpty.classList.add('hidden');
    resultContent.classList.remove('hidden');
    document.getElementById('resultCard').scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    setError(err.message || 'Something went wrong.');
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.querySelector('span:first-child').textContent = 'Analyze my food';
    loader.classList.add('hidden');
  }
});
