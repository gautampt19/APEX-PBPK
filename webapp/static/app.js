/* ══════════════════════════════════════════════════════════════════════════
   APEX-PBPK Dashboard — Client-Side Application Logic
   ══════════════════════════════════════════════════════════════════════════ */

// ── Mermaid Init ─────────────────────────────────────────────────────────
mermaid.initialize({
    startOnLoad: false,
    theme: 'dark',
    themeVariables: {
        primaryColor:       '#1a2744',
        primaryTextColor:   '#e2e8f0',
        primaryBorderColor: '#22d3ee',
        lineColor:          '#22d3ee',
        secondaryColor:     '#14b8a6',
        tertiaryColor:      '#0d1320',
        fontFamily:         'Inter, sans-serif',
        fontSize:           '13px',
    },
    flowchart: {
        curve: 'basis',
        padding: 20,
        htmlLabels: true,
        useMaxWidth: true,
    },
});

// ── State ────────────────────────────────────────────────────────────────
let currentFilename = null;
let currentPaperName = null;

// ── DOM References ───────────────────────────────────────────────────────
const uploadZone   = document.getElementById('upload-zone');
const fileInput    = document.getElementById('file-input');
const uploadedInfo = document.getElementById('uploaded-info');
const paperList    = document.getElementById('paper-list');
const runBtn       = document.getElementById('run-btn');
const logViewer    = document.getElementById('log-viewer');
const toggleLogBtn = document.getElementById('toggle-log-btn');
const spinner      = document.getElementById('spinner');
const statusText   = document.getElementById('status-text');
const progressBar  = document.getElementById('progress-bar');
const progressPct  = document.getElementById('progress-pct');
const lightbox     = document.getElementById('lightbox');
const lightboxImg  = document.getElementById('lightbox-img');
const modelBadge   = document.getElementById('model-badge');

// ── Tab Switching ────────────────────────────────────────────────────────
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    });
});

// ── Upload Logic ─────────────────────────────────────────────────────────
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('drag-over');
});
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));
uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('drag-over');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', () => {
    if (fileInput.files.length) handleFile(fileInput.files[0]);
});

async function handleFile(file) {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        alert('Please upload a PDF file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setStatus('Uploading...', 'running');

    try {
        const resp = await fetch('/api/upload', { method: 'POST', body: formData });
        const data = await resp.json();

        if (resp.ok) {
            currentFilename = data.filename;
            currentPaperName = data.paper_name;
            uploadedInfo.innerHTML = `
                <div class="uploaded-file">📄 ${data.filename}</div>
            `;
            runBtn.disabled = false;
            setStatus('PDF uploaded — ready to run', '');
            loadPaperList();

            // Check if results already exist
            loadResults(data.paper_name);
        } else {
            alert(data.error || 'Upload failed');
            setStatus('Upload failed', 'failed');
        }
    } catch (err) {
        alert('Upload error: ' + err.message);
        setStatus('Upload error', 'failed');
    }
}

// ── Paper List ───────────────────────────────────────────────────────────
async function loadPaperList() {
    try {
        const resp = await fetch('/api/papers');
        const data = await resp.json();
        paperList.innerHTML = '';
        data.papers.forEach(name => {
            const li = document.createElement('li');
            li.textContent = name;
            li.innerHTML = `📄 ${name}`;
            if (name === currentFilename) li.classList.add('active');
            li.addEventListener('click', () => {
                currentFilename = name;
                currentPaperName = name.replace('.pdf', '');
                uploadedInfo.innerHTML = `<div class="uploaded-file">📄 ${name}</div>`;
                runBtn.disabled = false;
                document.querySelectorAll('.paper-list li').forEach(l => l.classList.remove('active'));
                li.classList.add('active');
                loadResults(currentPaperName);
            });
            paperList.appendChild(li);
        });
    } catch (err) {
        console.error('Failed to load paper list:', err);
    }
}

// ── Run Pipeline ─────────────────────────────────────────────────────────
runBtn.addEventListener('click', async () => {
    if (!currentFilename) return;

    const model = document.getElementById('model-select').value;
    const useColpali = document.getElementById('use-colpali').checked;
    const topK = parseInt(document.getElementById('top-k').value) || 5;
    const backend = document.getElementById('backend-select').value;

    modelBadge.textContent = model;

    runBtn.disabled = true;
    logViewer.innerHTML = '';
    logViewer.classList.add('visible');
    setStatus('Starting pipeline...', 'running');
    setProgress(5);

    try {
        const resp = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                filename: currentFilename,
                use_colpali: useColpali,
                model: model,
                top_k: topK,
                backend: backend,
            }),
        });
        const data = await resp.json();

        if (!resp.ok) {
            setStatus('Failed to start: ' + (data.error || 'Unknown error'), 'failed');
            runBtn.disabled = false;
            return;
        }

        // Start SSE listener
        listenToJob(data.job_id);
    } catch (err) {
        setStatus('Error: ' + err.message, 'failed');
        runBtn.disabled = false;
    }
});

function listenToJob(jobId) {
    const es = new EventSource(`/api/status/${jobId}`);

    es.onmessage = (event) => {
        const data = JSON.parse(event.data);

        // Update progress
        setProgress(data.progress);
        if (data.current_step) {
            setStatus(data.current_step, 'running');
        }

        // Append new log lines
        if (data.new_lines && data.new_lines.length) {
            data.new_lines.forEach(line => {
                const div = document.createElement('div');
                div.className = 'log-line';
                if (line.includes('✅')) div.classList.add('success');
                else if (line.includes('❌')) div.classList.add('error');
                else if (line.startsWith('STEP:')) div.classList.add('step');
                div.textContent = line;
                logViewer.appendChild(div);
            });
            logViewer.scrollTop = logViewer.scrollHeight;
        }

        // Check completion
        if (data.status === 'completed') {
            es.close();
            setStatus('Pipeline completed!', 'completed');
            setProgress(100);
            runBtn.disabled = false;
            spinner.classList.remove('active');
            loadResults(currentPaperName);
        } else if (data.status === 'failed') {
            es.close();
            setStatus('Pipeline failed: ' + (data.error || ''), 'failed');
            runBtn.disabled = false;
            spinner.classList.remove('active');
        }
    };

    es.onerror = () => {
        es.close();
        setStatus('Connection lost', 'failed');
        runBtn.disabled = false;
        spinner.classList.remove('active');
    };

    spinner.classList.add('active');
}

// ── Load & Display Results ───────────────────────────────────────────────
async function loadResults(paperName) {
    try {
        const resp = await fetch(`/api/results/${paperName}`);
        if (!resp.ok) return;
        const data = await resp.json();

        renderParameters(data.parameters);
        renderCompartmentFlow(data.parameters);
        renderColpaliPages(data.colpali_pages);
        renderRCode(data.r_code);
    } catch (err) {
        console.error('Failed to load results:', err);
    }
}

// ── Render: Parameters ───────────────────────────────────────────────────
function renderParameters(params) {
    const container = document.getElementById('params-content');
    const empty = document.getElementById('params-empty');
    if (!params) return;

    empty.style.display = 'none';
    container.style.display = 'block';

    let html = '';

    // Blood Flow + Volume in a grid
    html += '<div class="param-grid">';

    // Blood Flow Fractions
    if (params.blood_flow_fraction && Object.keys(params.blood_flow_fraction).length) {
        html += `<div class="param-section">
            <div class="param-section-title">🩸 Blood Flow Fractions</div>
            <table class="param-table"><thead><tr>
                <th>Organ</th><th>Fraction of Q<sub>c</sub></th>
            </tr></thead><tbody>`;
        for (const [organ, val] of Object.entries(params.blood_flow_fraction)) {
            html += `<tr>
                <td class="param-name">${organ}</td>
                <td class="param-value">${val}</td>
            </tr>`;
        }
        html += '</tbody></table></div>';
    }

    // Volume Fractions
    if (params.volume_fraction && Object.keys(params.volume_fraction).length) {
        html += `<div class="param-section">
            <div class="param-section-title">📐 Volume Fractions</div>
            <table class="param-table"><thead><tr>
                <th>Organ</th><th>Fraction of BW</th>
            </tr></thead><tbody>`;
        for (const [organ, val] of Object.entries(params.volume_fraction)) {
            html += `<tr>
                <td class="param-name">${organ}</td>
                <td class="param-value">${val}</td>
            </tr>`;
        }
        html += '</tbody></table></div>';
    }

    html += '</div>';  // close param-grid

    // Biochemical Parameters
    if (params.biochemical_parameters && Object.keys(params.biochemical_parameters).length) {
        // Separate partition coefficients from other params
        const partitions = {};
        const others = {};
        for (const [k, v] of Object.entries(params.biochemical_parameters)) {
            if (k.includes('plasma') || k.includes('blood') || k.startsWith('Kp')) {
                partitions[k] = v;
            } else {
                others[k] = v;
            }
        }

        if (Object.keys(partitions).length) {
            html += `<div class="param-section">
                <div class="param-section-title">⚗️ Partition Coefficients</div>
                <table class="param-table"><thead><tr>
                    <th>Parameter</th><th>Value</th>
                </tr></thead><tbody>`;
            for (const [k, v] of Object.entries(partitions)) {
                html += `<tr>
                    <td class="param-name">${k}</td>
                    <td class="param-value">${v}</td>
                </tr>`;
            }
            html += '</tbody></table></div>';
        }

        if (Object.keys(others).length) {
            html += `<div class="param-section">
                <div class="param-section-title">🧪 Biochemical Parameters</div>
                <table class="param-table"><thead><tr>
                    <th>Parameter</th><th>Value</th>
                </tr></thead><tbody>`;
            for (const [k, v] of Object.entries(others)) {
                html += `<tr>
                    <td class="param-name">${k}</td>
                    <td class="param-value">${typeof v === 'number' ? v : `"${v}"`}</td>
                </tr>`;
            }
            html += '</tbody></table></div>';
        }
    }

    // Equations
    if (params.equations && Object.keys(params.equations).length) {
        html += `<div class="param-section">
            <div class="param-section-title">📝 Model Equations</div>`;
        for (const [name, formula] of Object.entries(params.equations)) {
            html += `<div class="equation-card">
                <div class="equation-name">${name}</div>
                <div class="equation-formula">${formula}</div>
            </div>`;
        }
        html += '</div>';
    }

    container.innerHTML = html;
}

// ── Render: Compartment Flow Diagram ─────────────────────────────────────
async function renderCompartmentFlow(params) {
    const container = document.getElementById('compartment-diagram');
    const empty = document.getElementById('flow-empty');
    if (!params || !params.blood_flow_fraction) return;

    empty.style.display = 'none';
    container.style.display = 'flex';

    // Filter to unique organ names (remove Human_ prefixed duplicates for diagram)
    const bf = params.blood_flow_fraction;
    const organs = Object.keys(bf).filter(k => !k.startsWith('Human_'));

    // Build Mermaid flowchart
    let mermaidCode = 'flowchart TD\n';

    // Style definitions
    mermaidCode += '    classDef organ fill:#1a2744,stroke:#22d3ee,stroke-width:2px,color:#e2e8f0\n';
    mermaidCode += '    classDef blood fill:#1a1428,stroke:#a78bfa,stroke-width:2px,color:#e2e8f0\n';
    mermaidCode += '    classDef gut fill:#142820,stroke:#34d399,stroke-width:2px,color:#e2e8f0\n';

    // Central nodes
    mermaidCode += '    BLOOD["🩸 Arterial Blood\\nPool"]:::blood\n';
    mermaidCode += '    VENOUS["🫀 Venous Blood\\nPool"]:::blood\n';

    // Determine if gut/GI exists
    const hasGut = organs.some(o => o.toLowerCase().includes('gut') || o.toLowerCase().includes('intestin'));

    // Add organ nodes and connections
    organs.forEach(organ => {
        const flow = bf[organ];
        const sanitized = organ.replace(/[^a-zA-Z0-9]/g, '_');
        const kp = params.biochemical_parameters?.[`${organ}:plasma`] || '';
        const kpLabel = kp ? `\\nKp=${kp}` : '';

        if (organ.toLowerCase() === 'liver') {
            mermaidCode += `    ${sanitized}["🫁 ${organ}${kpLabel}"]:::organ\n`;
            mermaidCode += `    BLOOD -->|"Q=${flow}"| ${sanitized}\n`;

            if (hasGut) {
                mermaidCode += `    ${sanitized} --> VENOUS\n`;
            } else {
                mermaidCode += `    ${sanitized} -->|"Portal + Hepatic"| VENOUS\n`;
            }
        } else if (organ.toLowerCase().includes('gut') || organ.toLowerCase().includes('intestin')) {
            mermaidCode += `    ${sanitized}["🟢 ${organ}${kpLabel}"]:::gut\n`;
            mermaidCode += `    BLOOD -->|"Q=${flow}"| ${sanitized}\n`;
            mermaidCode += `    ${sanitized} -->|"Portal Vein"| Liver\n`;
        } else if (organ.toLowerCase() === 'lung') {
            mermaidCode += `    ${sanitized}["��️ ${organ}${kpLabel}"]:::organ\n`;
            mermaidCode += `    VENOUS -->|"Q=${flow}"| ${sanitized}\n`;
            mermaidCode += `    ${sanitized} --> BLOOD\n`;
        } else {
            mermaidCode += `    ${sanitized}["${organ}${kpLabel}"]:::organ\n`;
            mermaidCode += `    BLOOD -->|"Q=${flow}"| ${sanitized}\n`;
            mermaidCode += `    ${sanitized} --> VENOUS\n`;
        }
    });

    // Add dose compartment if Kabs exists
    const biochem = params.biochemical_parameters || {};
    const hasKabs = Object.keys(biochem).some(k => k.toLowerCase().includes('kabs'));
    if (hasKabs) {
        mermaidCode += '    DOSE["💊 Oral Dose"]:::gut\n';
        const gutNode = organs.find(o => o.toLowerCase().includes('gut') || o.toLowerCase().includes('intestin'));
        if (gutNode) {
            mermaidCode += `    DOSE -->|"Kabs"| ${gutNode.replace(/[^a-zA-Z0-9]/g, '_')}\n`;
        } else {
            mermaidCode += '    DOSE -->|"Kabs"| Liver\n';
        }
    }

    // Render with Mermaid
    container.innerHTML = `<div class="mermaid">${mermaidCode}</div>`;

    try {
        await mermaid.run({ querySelector: '#compartment-diagram .mermaid' });
    } catch (e) {
        console.error('Mermaid rendering error:', e);
        container.innerHTML = `<div class="empty-state"><div class="empty-icon">⚠️</div><div class="empty-text">Diagram rendering error. Check console.</div></div>`;
    }
}

// ── Render: ColPali Pages ────────────────────────────────────────────────
function renderColpaliPages(pages) {
    const gallery = document.getElementById('colpali-gallery');
    const empty = document.getElementById('colpali-empty');
    if (!pages || !pages.length) return;

    empty.style.display = 'none';
    gallery.style.display = 'grid';

    gallery.innerHTML = pages.map(filename => {
        const pageNum = filename.match(/(\d+)/)?.[1] || '?';
        return `
            <div class="gallery-item" onclick="openLightbox('/api/colpali-pages/${filename}')">
                <img src="/api/colpali-pages/${filename}" alt="Page ${pageNum}" loading="lazy">
                <span class="page-label">Page ${parseInt(pageNum)}</span>
            </div>
        `;
    }).join('');
}

// ── Render: R Code ───────────────────────────────────────────────────────
function renderRCode(rCode) {
    const block = document.getElementById('rcode-block');
    const content = document.getElementById('rcode-content');
    const empty = document.getElementById('rcode-empty');
    if (!rCode) return;

    empty.style.display = 'none';
    block.style.display = 'block';
    content.textContent = rCode;
}

// ── Lightbox ─────────────────────────────────────────────────────────────
function openLightbox(src) {
    lightboxImg.src = src;
    lightbox.classList.add('active');
}
lightbox.addEventListener('click', () => lightbox.classList.remove('active'));

// ── Helpers ──────────────────────────────────────────────────────────────
function setStatus(text, state) {
    statusText.textContent = text;
    statusText.className = 'status-text' + (state ? ' ' + state : '');
    if (state === 'running') {
        spinner.classList.add('active');
        progressBar.classList.add('active');
    } else {
        spinner.classList.remove('active');
        progressBar.classList.remove('active');
    }
}

function setProgress(pct) {
    progressBar.style.width = pct + '%';
    progressPct.textContent = pct + '%';
}

toggleLogBtn.addEventListener('click', () => {
    logViewer.classList.toggle('visible');
});

// ── Model badge sync ─────────────────────────────────────────────────────
document.getElementById('model-select').addEventListener('change', (e) => {
    modelBadge.textContent = e.target.value;
});

// ── Init ─────────────────────────────────────────────────────────────────
loadPaperList();
