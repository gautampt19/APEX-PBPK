/* ══════════════════════════════════════════════════════════════════════════
   APEX-PBPK Dashboard — Client-Side Application Logic (Editable)
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
    flowchart: { curve: 'basis', padding: 20, htmlLabels: true, useMaxWidth: true }
});

// ── State ────────────────────────────────────────────────────────────────
let currentFilename = null;
let currentPaperName = null;
let currentParams = null; // Holds the editable JSON parameters

// ── DOM References ───────────────────────────────────────────────────────
const uploadZone   = document.getElementById('upload-zone');
const fileInput    = document.getElementById('file-input');
const uploadedInfo = document.getElementById('uploaded-info');
const paperList    = document.getElementById('paper-list');
const extractBtn   = document.getElementById('extract-btn');
const generateBtn  = document.getElementById('generate-btn');
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
uploadZone.addEventListener('dragover', (e) => { e.preventDefault(); uploadZone.classList.add('drag-over'); });
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));
uploadZone.addEventListener('drop', (e) => {
    e.preventDefault(); uploadZone.classList.remove('drag-over');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', () => { if (fileInput.files.length) handleFile(fileInput.files[0]); });

let currentExtractedRecords = [];
let activeStudioSpecies = 'all';

function resetUI() {
    currentParams = null;
    currentExtractedRecords = [];
    if (generateBtn) generateBtn.style.display = 'none';
    extractBtn.disabled = false;
    
    const resultsContainer = document.getElementById('params-results-container');
    if (resultsContainer) resultsContainer.style.display = 'none';
    const emptyState = document.getElementById('params-empty');
    if (emptyState) emptyState.style.display = 'flex';
    
    const paramsContent = document.getElementById('params-content');
    if (paramsContent) {
        paramsContent.innerHTML = '';
        paramsContent.style.display = 'none';
    }
    
    logViewer.innerHTML = '<div class="term-line" style="color: var(--text-muted);">Ready to process scientific documents. Logs will stream here.</div>';
    setProgress(0);
    
    const countEl = document.getElementById('metric-params-count');
    if (countEl) countEl.textContent = '0';
    const compoundEl = document.getElementById('metric-compound');
    if (compoundEl) compoundEl.textContent = 'None Selected';
    const ontoEl = document.getElementById('metric-ontology-count');
    if (ontoEl) ontoEl.textContent = '0 Mapped';
}

async function handleFile(file) {
    if (!file.name.toLowerCase().endsWith('.pdf')) { alert('Please upload a PDF file.'); return; }
    resetUI();
    const formData = new FormData(); formData.append('file', file);
    setStatus('Uploading...', 'running');
    try {
        const resp = await fetch('/api/upload', { method: 'POST', body: formData });
        const data = await resp.json();
        if (resp.ok) {
            currentFilename = data.filename; currentPaperName = data.paper_name;
            uploadedInfo.innerHTML = `<div class="uploaded-file">📄 ${data.filename}</div>`;
            setStatus('PDF uploaded — ready to extract', '');
            
            loadResults(data.paper_name); // Check if results exist
        } else {
            alert(data.error || 'Upload failed'); setStatus('Upload failed', 'failed');
        }
    } catch (err) { alert('Upload error: ' + err.message); setStatus('Upload error', 'failed'); }
}

// ── Paper List ───────────────────────────────────────────────────────────
async function loadPaperList() {
    try {
        const resp = await fetch('/api/papers');
        const data = await resp.json();
        paperList.innerHTML = '';
        data.papers.forEach(name => {
            const li = document.createElement('li');
            li.innerHTML = `📄 ${name}`;
            if (name === currentFilename) li.classList.add('active');
            li.addEventListener('click', () => {
                currentFilename = name; currentPaperName = name.replace('.pdf', '');
                uploadedInfo.innerHTML = `<div class="uploaded-file">📄 ${name}</div>`;
                document.querySelectorAll('.paper-list li').forEach(l => l.classList.remove('active'));
                li.classList.add('active');
                resetUI();
                loadResults(currentPaperName);
            });
            paperList.appendChild(li);
        });
    } catch (err) { console.error('Failed to load paper list:', err); }
}

// ── Pipeline Runner ──────────────────────────────────────────────────────
async function runPipelineStep(stepName) {
    if (!currentFilename) return;
    const model = document.getElementById('model-select').value;
    const useColpali = document.getElementById('use-colpali').checked;
    const topK = parseInt(document.getElementById('top-k').value) || 5;
    const backend = document.getElementById('backend-select').value;
    modelBadge.textContent = model;
    
    extractBtn.disabled = true;
    generateBtn.disabled = true;
    logViewer.classList.add('visible');
    setStatus(`Starting ${stepName}...`, 'running');
    if (stepName === 'extract') setProgress(5);
    
    try {
        const resp = await fetch('/api/run', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: currentFilename, use_colpali: useColpali, model: model, top_k: topK, backend: backend, run_step: stepName }),
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.error || 'Unknown error');
        listenToJob(data.job_id, stepName);
    } catch (err) {
        setStatus('Error: ' + err.message, 'failed');
        extractBtn.disabled = false;
        if (currentParams) generateBtn.disabled = false;
    }
}

function _sourcePassBadge(sp) {
    const map = {
        'xml_table':          ['badge-green',  'XML Table'],
        'colpali_page':       ['badge-orange', 'Visual OCR'],
        'prose_pass':         ['badge-purple', 'Prose Text'],
        'pubchem_enrichment': ['badge-blue',   'PubChem'],
        'chembl_enrichment':  ['badge-pink',   'ChEMBL'],
        'autopk_table':       ['badge-cyan',   'AutoPK']
    };
    const [cls, label] = map[sp] || ['badge-gray', sp || 'Extraction'];
    return `<span class="modern-badge ${cls}">${label}</span>`;
}

function _safe(val) {
    return (val === null || val === undefined || val === '') ? '-' : val;
}

function listenToJob(jobId, stepName) {
    const es = new EventSource(`/api/status/${jobId}`);
    es.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setProgress(data.progress);
        if (data.current_step) setStatus(data.current_step, 'running');
        if (data.new_lines?.length) {
            data.new_lines.forEach(line => {
                const div = document.createElement('div');
                div.className = 'term-line';
                if (line.includes('✅')) div.classList.add('success');
                else if (line.includes('❌') || line.toLowerCase().includes('error')) div.classList.add('error');
                else if (line.startsWith('STEP:') || line.startsWith('[Auto-Routing]')) div.classList.add('step');
                else if (line.includes('[Table') || line.includes('[DB]') || line.includes('[PBPKO]')) div.classList.add('table');
                div.textContent = line;
                logViewer.appendChild(div);
            });
            logViewer.scrollTop = logViewer.scrollHeight;
        }
        if (data.status === 'completed' || data.status === 'failed') {
            es.close();
            spinner.classList.remove('active');
            extractBtn.disabled = false;
            
            if (data.status === 'completed') {
                setStatus(`${stepName === 'extract' ? 'Extraction' : 'Generation'} completed!`, 'completed');
                setProgress(100);
                loadResults(currentPaperName); // Reload data
            } else {
                setStatus(`${stepName} failed: ` + (data.error || ''), 'failed');
                if (currentParams) generateBtn.disabled = false;
            }
        }
    };
    es.onerror = () => { es.close(); setStatus('Connection lost', 'failed'); extractBtn.disabled = false; spinner.classList.remove('active'); };
}

extractBtn.addEventListener('click', () => { 
    logViewer.innerHTML = '<div class="term-line" style="color: var(--cyan);">[Engine] Initializing extraction pipeline...</div>'; 
    runPipelineStep('extract'); 
});

toggleLogBtn.addEventListener('click', () => {
    if (logViewer.style.display === 'none') {
        logViewer.style.display = 'block';
    } else {
        logViewer.innerHTML = '';
    }
});

generateBtn.addEventListener('click', async () => {
    try {
        setStatus('Saving parameters...', 'running');
        const resp = await fetch('/api/save-params', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paper_name: currentPaperName, parameters: currentParams })
        });
        if (!resp.ok) throw new Error("Failed to save parameters");
        runPipelineStep('generate');
    } catch (e) {
        alert(e);
        setStatus('Save failed', 'failed');
    }
});

// ── Load & Display Results ───────────────────────────────────────────────
async function loadResults(paperName) {
    try {
        const resp = await fetch(`/api/results/${paperName}`);
        if (!resp.ok) return;
        const data = await resp.json();
        currentParams = data.parameters || {};
        
        // Prefer rich Supabase DB records if present
        if (data.db_records && data.db_records.length > 0) {
            renderParametersTable(data.db_records);
        } else if (Object.keys(currentParams).length > 0) {
            // Fallback to legacy editable dictionary
            renderEditableParameters(currentParams);
        }
        
        renderCompartmentFlow(currentParams);
        renderColpaliPages(data.colpali_pages);
        renderRCode(data.r_code);
        renderReview(data.review || null);
        
    } catch (err) { console.error('Failed to load results:', err); }
}

function renderParametersTable(records) {
    currentExtractedRecords = records || [];
    const container = document.getElementById('params-results-container');
    const emptyState = document.getElementById('params-empty');
    
    if (!records || records.length === 0) {
        if (!currentParams || Object.keys(currentParams).length === 0) {
            if (container) container.style.display = 'none';
            if (emptyState) emptyState.style.display = 'flex';
            return;
        }
    }
    
    if (emptyState) emptyState.style.display = 'none';
    if (container) container.style.display = 'block';
    
    // Calculate and update metrics
    let foundCompound = '-';
    let ontologyCount = 0;
    records.forEach(r => {
        if (foundCompound === '-' && r.compound) foundCompound = r.compound;
        let pbpko = r.pbpko_term_id;
        if (!pbpko && r.canonical_name) {
            try {
                const parsed = JSON.parse(r.canonical_name);
                if (parsed.pbpko_id) pbpko = parsed.pbpko_id;
            } catch(e) {}
        }
        if (pbpko && pbpko !== '-') ontologyCount++;
    });
    
    const countEl = document.getElementById('metric-params-count');
    if (countEl) countEl.textContent = records.length;
    
    const compoundEl = document.getElementById('metric-compound');
    if (compoundEl) compoundEl.textContent = foundCompound;
    
    const ontoEl = document.getElementById('metric-ontology-count');
    if (ontoEl) ontoEl.textContent = `${ontologyCount} mapped`;
    
    populateMainTableRows(records);
}

function populateMainTableRows(records) {
    const tbody = document.getElementById('pbpk-table-body');
    if (!tbody) return;
    
    if (records.length === 0) {
        tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 40px; color: var(--text-muted);">No matching parameters found.</td></tr>`;
        return;
    }
    
    let html = '';
    records.forEach(p => {
        let canonName = p.parameter_normalized || '-';
        let pbpkoId = p.pbpko_term_id || '';
        
        if (p.canonical_name) {
            try {
                const parsed = JSON.parse(p.canonical_name);
                canonName = parsed.canonical_name || canonName;
                pbpkoId = parsed.pbpko_id || pbpkoId;
            } catch(e) {
                canonName = p.canonical_name;
            }
        }
        
        let pbpkoHtml = `<div class="onto-name">${canonName}</div>`;
        if (pbpkoId && pbpkoId !== '-') {
            const iri = `https://fair-pbk.wur.nl/vocabularies/parameter/${pbpkoId}`;
            pbpkoHtml += `<a class="onto-id-link" href="${iri}" target="_blank" title="View in FAIR-PBPK Ontology">${pbpkoId} ↗</a>`;
        }

        const rawParam = _safe(p.parameter_raw || p.parameter_name);
        const val = _safe(p.value);
        const dev = p.deviation_value ? `<span class="td-val-dev">±${p.deviation_value}</span>` : '';
        const unit = p.unit ? `<span class="unit-tag">${p.unit}</span>` : '-';
        const compound = p.compound ? `<span class="compound-tag">${p.compound}</span>` : '-';

        let speciesBadge = '-';
        if (p.species) {
            const sp = p.species.toLowerCase();
            if (sp.includes('human')) speciesBadge = `<span class="species-badge-human">Human</span>`;
            else if (sp.includes('rat')) speciesBadge = `<span class="species-badge-rat">Rat</span>`;
            else if (sp.includes('mouse')) speciesBadge = `<span class="species-badge-mouse">Mouse</span>`;
            else speciesBadge = `<span class="species-badge-default">${p.species}</span>`;
        }

        const routeForm = [p.route, p.formulation].filter(Boolean).join(' · ') || '-';
        const doseStr = p.dose_raw || (p.dose_value ? `${p.dose_value} ${p.dose_unit || ''}` : (p.dose ? `${p.dose}` : '-'));
        const cohort = _safe(p.cohort_or_condition);
        const sourceBadge = _sourcePassBadge(p.source_pass);

        html += `
            <tr>
                <td class="td-ontology">${pbpkoHtml}</td>
                <td style="color: #cbd5e1; font-weight: 500;">${rawParam}</td>
                <td><span class="td-val-box">${val}</span> ${dev}</td>
                <td>${unit}</td>
                <td>${compound}</td>
                <td>${speciesBadge}</td>
                <td style="color: var(--text-secondary);">${routeForm}</td>
                <td style="font-family: 'JetBrains Mono', monospace; color: #fbbf24;">${doseStr}</td>
                <td style="color: var(--text-muted); font-size: 0.78rem;">${cohort}</td>
                <td>${sourceBadge}</td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

window.filterParametersTable = () => {
    const query = (document.getElementById('param-search-input')?.value || '').toLowerCase();
    const filtered = currentExtractedRecords.filter(p => {
        const matchQuery = !query || 
            (p.parameter_raw && p.parameter_raw.toLowerCase().includes(query)) ||
            (p.parameter_name && p.parameter_name.toLowerCase().includes(query)) ||
            (p.parameter_normalized && p.parameter_normalized.toLowerCase().includes(query)) ||
            (p.canonical_name && p.canonical_name.toLowerCase().includes(query)) ||
            (p.pbpko_term_id && p.pbpko_term_id.toLowerCase().includes(query)) ||
            (p.compound && p.compound.toLowerCase().includes(query)) ||
            (p.cohort_or_condition && p.cohort_or_condition.toLowerCase().includes(query));
        
        const matchSpecies = activeStudioSpecies === 'all' || 
            (p.species && p.species.toLowerCase().includes(activeStudioSpecies));
        
        return matchQuery && matchSpecies;
    });
    populateMainTableRows(filtered);
};

window.setSpeciesFilter = (species, btn) => {
    activeStudioSpecies = species;
    document.querySelectorAll('.filter-chip').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    filterParametersTable();
};

window.exportParametersCSV = () => {
    if (!currentExtractedRecords || currentExtractedRecords.length === 0) return;
    const headers = ["Canonical_Name", "PBPKO_ID", "Parameter_Raw", "Value", "Deviation", "Unit", "Compound", "Species", "Route", "Formulation", "Dose", "Cohort", "Source_Pass"];
    const rows = currentExtractedRecords.map(p => {
        let pbpko = p.pbpko_term_id || '';
        let canon = p.parameter_normalized || '';
        if (p.canonical_name) {
            try {
                const parsed = JSON.parse(p.canonical_name);
                canon = parsed.canonical_name || canon;
                pbpko = parsed.pbpko_id || pbpko;
            } catch(e) { canon = p.canonical_name; }
        }
        return [
            `"${(canon || '').replace(/"/g, '""')}"`,
            `"${pbpko}"`,
            `"${(p.parameter_raw || p.parameter_name || '').replace(/"/g, '""')}"`,
            p.value !== null ? p.value : '',
            p.deviation_value !== null ? p.deviation_value : '',
            `"${p.unit || ''}"`,
            `"${p.compound || ''}"`,
            `"${p.species || ''}"`,
            `"${p.route || ''}"`,
            `"${p.formulation || ''}"`,
            `"${(p.dose_raw || p.dose_value || p.dose || '')}"`,
            `"${(p.cohort_or_condition || '').replace(/"/g, '""')}"`,
            `"${p.source_pass || ''}"`
        ].join(',');
    });
    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(','), ...rows].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `${currentPaperName || 'parameters'}_pbpk.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};

window.exportParametersJSON = () => {
    if (!currentExtractedRecords || currentExtractedRecords.length === 0) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(currentExtractedRecords, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `${currentPaperName || 'parameters'}_pbpk.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
};

// ── Editable Parameters UI ───────────────────────────────────────────────
function createEditableTable(sectionTitle, sectionObj, isStringValue=false) {
    if (!sectionObj) return '';
    let html = `
    <div class="param-section">
        <div class="param-section-title" style="display:flex; justify-content:space-between;">
            ${sectionTitle}
            <button class="btn btn-secondary" style="padding:2px 8px; font-size:11px;" onclick="addParamRow(this, ${isStringValue})">+ Add</button>
        </div>
        <table class="param-table editable-table">
            <thead><tr><th>Name/Organ</th><th>Value</th><th></th></tr></thead>
            <tbody>`;
            
    for (const [key, val] of Object.entries(sectionObj)) {
        html += `
            <tr>
                <td><input type="text" class="edit-key" value="${key}" /></td>
                <td><input type="text" class="edit-val" value="${val}" /></td>
                <td style="width:30px;"><button class="btn btn-secondary" style="padding:2px 6px; color:#ef4444;" onclick="this.closest('tr').remove(); saveUIToState();">✕</button></td>
            </tr>`;
    }
    html += `</tbody></table></div>`;
    return html;
}

window.addParamRow = (btn, isStringValue) => {
    const tbody = btn.closest('.param-section').querySelector('tbody');
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td><input type="text" class="edit-key" placeholder="New key" /></td>
        <td><input type="text" class="edit-val" placeholder="Value" /></td>
        <td style="width:30px;"><button class="btn btn-secondary" style="padding:2px 6px; color:#ef4444;" onclick="this.closest('tr').remove(); saveUIToState();">✕</button></td>
    `;
    tr.querySelectorAll('input').forEach(inp => {
        inp.addEventListener('input', () => saveUIToState());
    });
    tbody.appendChild(tr);
    saveUIToState();
};

window.saveUIToState = () => {
    if (!currentParams) currentParams = {};
    const sections = document.querySelectorAll('.param-section');
    
    sections.forEach(sec => {
        const title = sec.querySelector('.param-section-title').innerText;
        const rows = sec.querySelectorAll('tbody tr');
        const newObj = {};
        rows.forEach(r => {
            const k = r.querySelector('.edit-key').value.trim();
            let v = r.querySelector('.edit-val').value.trim();
            if (!k) return;
            if (!isNaN(v) && v !== '') v = Number(v);
            newObj[k] = v;
        });
        
        if (title.includes('Blood Flow')) currentParams.blood_flow_fraction = newObj;
        else if (title.includes('Volume')) currentParams.volume_fraction = newObj;
        else if (title.includes('Partition')) {
            if (!currentParams.biochemical_parameters) currentParams.biochemical_parameters = {};
            Object.keys(currentParams.biochemical_parameters).forEach(bk => {
                if(bk.includes('plasma') || bk.startsWith('Kp')) delete currentParams.biochemical_parameters[bk];
            });
            Object.assign(currentParams.biochemical_parameters, newObj);
        }
        else if (title.includes('Biochemical')) {
            if (!currentParams.biochemical_parameters) currentParams.biochemical_parameters = {};
            Object.keys(currentParams.biochemical_parameters).forEach(bk => {
                if(!(bk.includes('plasma') || bk.startsWith('Kp'))) delete currentParams.biochemical_parameters[bk];
            });
            Object.assign(currentParams.biochemical_parameters, newObj);
        }
        else if (title.includes('Equations')) currentParams.equations = newObj;
    });
    
    renderCompartmentFlow(currentParams);
};

function renderEditableParameters(params) {
    const container = document.getElementById('params-content');
    const empty = document.getElementById('params-empty');
    if (!params || Object.keys(params).length === 0) return;
    empty.style.display = 'none'; container.style.display = 'block';

    let html = '<div class="param-grid">';
    
    if(!params.blood_flow_fraction) params.blood_flow_fraction = {};
    if(!params.volume_fraction) params.volume_fraction = {};
    
    html += createEditableTable("�� Blood Flow Fractions", params.blood_flow_fraction);
    html += createEditableTable("📐 Volume Fractions", params.volume_fraction);
    html += '</div>';

    if (!params.biochemical_parameters) params.biochemical_parameters = {};
    const partitions = {}; const others = {};
    for (const [k, v] of Object.entries(params.biochemical_parameters)) {
        if (k.includes('plasma') || k.includes('blood') || k.startsWith('Kp')) partitions[k] = v;
        else others[k] = v;
    }
    
    html += createEditableTable("⚗️ Partition Coefficients", partitions);
    html += createEditableTable("🧪 Biochemical Parameters", others, true);
    html += createEditableTable("📝 Model Equations", params.equations || {}, true);

    container.innerHTML = html;
    
    container.querySelectorAll('input').forEach(inp => {
        inp.addEventListener('input', () => saveUIToState());
    });
}

// ── Render: Compartment Flow Diagram ─────────────────────────────────────
async function renderCompartmentFlow(params) {
    const container = document.getElementById('compartment-diagram');
    const empty = document.getElementById('flow-empty');
    
    if (!params) {
        container.style.display = 'none'; empty.style.display = 'flex'; return;
    }
    
    const bf = params.blood_flow_fraction || {};
    const vf = params.volume_fraction || {};
    const biochem = params.biochemical_parameters || {};
    
    let organSet = new Set();
    Object.keys(bf).forEach(k => organSet.add(k));
    Object.keys(vf).forEach(k => organSet.add(k));
    
    Object.keys(biochem).forEach(k => {
        if(k.includes(':plasma')) organSet.add(k.split(':plasma')[0].trim());
        if(k.includes('_plasma')) {
            const parts = k.split('_');
            if(parts.length > 1) {
                const idx = parts.indexOf('plasma');
                if(idx > 0) organSet.add(parts[idx-1]);
            }
        }
    });
    
    const organs = Array.from(organSet).filter(k => !k.startsWith('Human_') && k.trim() !== '' && k.toLowerCase() !== 'plasma' && k.toLowerCase() !== 'blood');
    
    if (organs.length === 0) {
        container.style.display = 'none'; empty.style.display = 'flex'; return;
    }
    
    empty.style.display = 'none'; container.style.display = 'flex';

    let mermaidCode = 'flowchart TD\n';
    mermaidCode += '    classDef organ fill:#1a2744,stroke:#22d3ee,stroke-width:2px,color:#e2e8f0\n';
    mermaidCode += '    classDef blood fill:#1a1428,stroke:#a78bfa,stroke-width:2px,color:#e2e8f0\n';
    mermaidCode += '    classDef gut fill:#142820,stroke:#34d399,stroke-width:2px,color:#e2e8f0\n';
    mermaidCode += '    BLOOD["🩸 Arterial Blood<br>Pool"]:::blood\n';
    mermaidCode += '    VENOUS["🫀 Venous Blood<br>Pool"]:::blood\n';

    const hasGut = organs.some(o => o.toLowerCase().includes('gut') || o.toLowerCase().includes('intestin'));

    organs.forEach(organ => {
        const flow = bf[organ] !== undefined ? bf[organ] : "?";
        const sanitized = organ.replace(/[^a-zA-Z0-9]/g, '_');
        
        let kp = '';
        for (const [k, v] of Object.entries(biochem)) {
            if (k === `${organ}:plasma` || k.includes(`${organ}_plasma`)) {
                kp = v; break;
            }
        }
        // Use HTML <br> instead of \\n to avoid mermaid syntax errors!
        const kpLabel = kp ? `<br>Kp=${kp}` : '';

        if (organ.toLowerCase().includes('liver')) {
            mermaidCode += `    ${sanitized}["🫁 ${organ}${kpLabel}"]:::organ\n`;
            mermaidCode += `    BLOOD -->|"Q=${flow}"| ${sanitized}\n`;
            if (hasGut) mermaidCode += `    ${sanitized} --> VENOUS\n`;
            else mermaidCode += `    ${sanitized} -->|"Portal + Hepatic"| VENOUS\n`;
        } else if (organ.toLowerCase().includes('gut') || organ.toLowerCase().includes('intestin')) {
            mermaidCode += `    ${sanitized}["🟢 ${organ}${kpLabel}"]:::gut\n`;
            mermaidCode += `    BLOOD -->|"Q=${flow}"| ${sanitized}\n`;
            mermaidCode += `    ${sanitized} -->|"Portal Vein"| Liver\n`;
        } else if (organ.toLowerCase().includes('lung')) {
            mermaidCode += `    ${sanitized}["🌬️ ${organ}${kpLabel}"]:::organ\n`;
            mermaidCode += `    VENOUS -->|"Q=${flow}"| ${sanitized}\n`;
            mermaidCode += `    ${sanitized} --> BLOOD\n`;
        } else {
            mermaidCode += `    ${sanitized}["${organ}${kpLabel}"]:::organ\n`;
            mermaidCode += `    BLOOD -->|"Q=${flow}"| ${sanitized}\n`;
            mermaidCode += `    ${sanitized} --> VENOUS\n`;
        }
    });

    const hasKabs = Object.keys(biochem).some(k => k.toLowerCase().includes('kabs'));
    if (hasKabs) {
        mermaidCode += '    DOSE["💊 Oral Dose"]:::gut\n';
        const gutNode = organs.find(o => o.toLowerCase().includes('gut') || o.toLowerCase().includes('intestin'));
        if (gutNode) mermaidCode += `    DOSE -->|"Kabs"| ${gutNode.replace(/[^a-zA-Z0-9]/g, '_')}\n`;
        else mermaidCode += '    DOSE -->|"Kabs"| Liver\n';
    }

    container.innerHTML = `<div class="mermaid">${mermaidCode}</div>`;
    try {
        container.removeAttribute('data-processed'); // force re-render
        await mermaid.run({ querySelector: '#compartment-diagram .mermaid' });
    } catch (e) {
        console.error("Mermaid error: ", e, "\\nGenerated Code:\\n", mermaidCode);
        container.innerHTML = `<div class="empty-state"><div class="empty-text">Diagram parsing error for edited values</div></div>`;
    }
}

// ── Render: ColPali Pages & R Code ───────────────────────────────────────
function renderColpaliPages(pages) {
    const gallery = document.getElementById('colpali-gallery');
    const empty = document.getElementById('colpali-empty');
    if (!pages || !pages.length) return;
    empty.style.display = 'none'; gallery.style.display = 'grid';
    gallery.innerHTML = pages.map(filename => {
        const pageNum = filename.match(/(\d+)/)?.[1] || '?';
        return `<div class="gallery-item" onclick="openLightbox('/api/colpali-pages/${filename}')">
                <img src="/api/colpali-pages/${filename}" alt="Page ${pageNum}" loading="lazy">
                <span class="page-label">Page ${parseInt(pageNum)}</span></div>`;
    }).join('');
}

function renderRCode(rCode) {
    const block = document.getElementById('rcode-block');
    const content = document.getElementById('rcode-content');
    const empty = document.getElementById('rcode-empty');
    if (!rCode) return;
    empty.style.display = 'none'; block.style.display = 'block';
    content.textContent = rCode;
}

// ── Lightbox & Helpers ───────────────────────────────────────────────────
function openLightbox(src) { lightboxImg.src = src; lightbox.classList.add('active'); }
lightbox.addEventListener('click', () => lightbox.classList.remove('active'));

function setStatus(text, state) {
    statusText.textContent = text; statusText.className = 'status-text' + (state ? ' ' + state : '');
    if (state === 'running') { spinner.classList.add('active'); progressBar.classList.add('active'); }
    else { spinner.classList.remove('active'); progressBar.classList.remove('active'); }
}
function setProgress(pct) { progressBar.style.width = pct + '%'; progressPct.textContent = pct + '%'; }
toggleLogBtn.addEventListener('click', () => logViewer.classList.toggle('visible'));
document.getElementById('model-select').addEventListener('change', (e) => modelBadge.textContent = e.target.value);



// ── Render: Model Review ──────────────────────────────────────────────────
function renderReview(review) {
    const container = document.getElementById('review-content');
    const empty = document.getElementById('review-empty');
    if (!review) { container.style.display = 'none'; empty.style.display = 'flex'; return; }

    empty.style.display = 'none'; container.style.display = 'block';

    const statusColors = { PASS: '#10b981', PASS_WITH_WARNINGS: '#f59e0b', FAIL: '#ef4444', ERROR: '#8b5cf6' };
    const statusIcons  = { PASS: '✅', PASS_WITH_WARNINGS: '⚠️', FAIL: '❌', ERROR: '💥' };
    const checkIcons   = { OK: '✅', WARNING: '⚠️', ERROR: '❌' };
    const checkColors  = { OK: '#10b981', WARNING: '#f59e0b', ERROR: '#ef4444' };

    const status = review.overall_status || 'UNKNOWN';
    const color  = statusColors[status] || '#64748b';
    const icon   = statusIcons[status] || '❓';

    let html = `
    <div class="review-panel">
        <div class="review-header" style="border-left:4px solid ${color}; padding:12px 16px; margin-bottom:20px; background:rgba(255,255,255,0.03); border-radius:0 8px 8px 0;">
            <div style="font-size:1.1rem; font-weight:700; color:${color};">${icon} ${status}</div>
            <div style="color:var(--text-muted); margin-top:4px;">${review.summary || ''}</div>
        </div>

        <div class="review-checks" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap:12px; margin-bottom:20px;">`;

    (review.checks || []).forEach(chk => {
        const c = checkColors[chk.status] || '#64748b';
        const ci = checkIcons[chk.status] || '❓';
        html += `
            <div class="review-check" style="background:var(--surface-2); border:1px solid ${c}33; border-radius:8px; padding:12px;">
                <div style="font-weight:600; color:${c}; margin-bottom:6px; font-size:0.8rem; letter-spacing:0.05em;">${ci} ${chk.category || ''}</div>
                <div style="font-size:0.85rem; color:var(--text-muted);">${chk.message || ''}</div>
            </div>`;
    });
    html += '</div>';

    if (review.critical_issues?.length) {
        html += `<div style="background:rgba(239,68,68,0.1); border:1px solid #ef4444; border-radius:8px; padding:14px; margin-bottom:16px;">
            <div style="font-weight:700; color:#ef4444; margin-bottom:8px;">🚨 Critical Issues</div>
            <ul style="margin:0; padding-left:18px; color:var(--text-muted);">
                ${review.critical_issues.map(i => `<li style="margin-bottom:4px;">${i}</li>`).join('')}
            </ul></div>`;
    }

    if (review.recommendations?.length) {
        html += `<div style="background:rgba(16,185,129,0.08); border:1px solid #10b981; border-radius:8px; padding:14px;">
            <div style="font-weight:700; color:#10b981; margin-bottom:8px;">💡 Recommendations</div>
            <ul style="margin:0; padding-left:18px; color:var(--text-muted);">
                ${review.recommendations.map(r => `<li style="margin-bottom:4px;">${r}</li>`).join('')}
            </ul></div>`;
    }

    html += '</div>';
    container.innerHTML = html;
}

// ══════════════════════════════════════════════════════════════════════════════
// Compartment Flow Builder (Cytoscape.js)
// ══════════════════════════════════════════════════════════════════════════════

let flowMode = 'view'; // 'view' | 'edit'

window.setFlowMode = function(mode) {
    flowMode = mode;
    document.getElementById('flow-view-pane').style.display = mode === 'view' ? 'block' : 'none';
    document.getElementById('flow-edit-pane').style.display = mode === 'edit' ? 'block' : 'none';
    document.getElementById('flow-view-btn').classList.toggle('active', mode === 'view');
    document.getElementById('flow-edit-btn').classList.toggle('active', mode === 'edit');
    if (mode === 'edit') {
        cyBuilder.init();
        cyBuilder.loadFromParams();
    }
};

const cyBuilder = {
    cy: null,
    connectMode: false,
    connectSource: null,
    popover: null,

    // ── Cytoscape style sheet ────────────────────────────────────────────────
    _style: [
        { selector: 'node[type="organ"]', style: {
            'shape': 'round-rectangle', 'width': 'label', 'height': 'label',
            'padding': '14px', 'background-color': '#1a2744',
            'border-color': '#22d3ee', 'border-width': 2,
            'color': '#e2e8f0', 'font-size': 11, 'font-family': 'Inter, sans-serif',
            'text-valign': 'center', 'text-halign': 'center',
            'label': 'data(label)', 'text-wrap': 'wrap', 'text-max-width': '120px',
            'cursor': 'pointer',
        }},
        { selector: 'node[type="blood"]', style: {
            'shape': 'ellipse', 'width': 'label', 'height': 'label', 'padding': '14px',
            'background-color': '#1a1428', 'border-color': '#a78bfa', 'border-width': 2,
            'color': '#e2e8f0', 'font-size': 11, 'label': 'data(label)',
            'text-valign': 'center', 'text-halign': 'center', 'cursor': 'pointer',
        }},
        { selector: 'node:selected', style: { 'border-color': '#fbbf24', 'border-width': 3 }},
        { selector: 'edge', style: {
            'curve-style': 'bezier', 'target-arrow-shape': 'triangle',
            'target-arrow-color': '#22d3ee', 'line-color': '#22d3ee',
            'width': 1.5, 'label': 'data(label)',
            'font-size': 9, 'color': '#94a3b8',
            'text-background-color': '#0a0f1a', 'text-background-opacity': 1,
            'text-background-padding': '3px', 'cursor': 'pointer',
        }},
        { selector: 'edge:selected', style: { 'line-color': '#fbbf24', 'target-arrow-color': '#fbbf24' }},
    ],

    // ── Init ─────────────────────────────────────────────────────────────────
    init() {
        if (this.cy) return;
        this.cy = cytoscape({
            container: document.getElementById('cy-canvas'),
            style: this._style,
            elements: [],
            layout: { name: 'grid' },
            userZoomingEnabled: true,
            userPanningEnabled: true,
            boxSelectionEnabled: true,
        });
        // Click on node → edit popover
        this.cy.on('tap', 'node', (evt) => {
            if (this.connectMode) {
                this._handleConnectClick(evt.target);
            } else {
                this._showNodePopover(evt.target, evt.renderedPosition);
            }
        });
        // Click on edge → edit label
        this.cy.on('tap', 'edge', (evt) => {
            if (!this.connectMode) this._showEdgePopover(evt.target, evt.renderedPosition);
        });
        // Click canvas → close popover
        this.cy.on('tap', (evt) => {
            if (evt.target === this.cy) this._closePopover();
        });
    },

    // ── Load from currentParams ───────────────────────────────────────────────
    loadFromParams() {
        if (!this.cy) this.init();
        this.cy.elements().remove();
        const bf = (currentParams && currentParams.blood_flow_fraction) ? currentParams.blood_flow_fraction : {};
        const vf = (currentParams && currentParams.volume_fraction)     ? currentParams.volume_fraction     : {};
        const biochem = (currentParams && currentParams.biochemical_parameters) ? currentParams.biochemical_parameters : {};

        // Always add blood nodes
        this.cy.add([
            { data: { id: 'ARTERIAL', label: '🩸 Arterial Blood', type: 'blood' } },
            { data: { id: 'VENOUS',   label: '🫀 Venous Blood',   type: 'blood' } },
        ]);

        const organs = Object.keys(bf).filter(k => !k.startsWith('Human_'));
        if (organs.length === 0 && Object.keys(vf).length > 0) {
            Object.keys(vf).filter(k => !k.startsWith('Human_') && k.toLowerCase() !== 'plasma').forEach(o => organs.includes(o) || organs.push(o));
        }

        organs.forEach(organ => {
            const q = bf[organ] !== undefined ? bf[organ] : '?';
            const v = vf[organ] !== undefined ? vf[organ] : '?';
            let kp = '';
            for (const [k, val] of Object.entries(biochem)) {
                if (k === `${organ}:plasma` || k.includes(`${organ}_plasma`)) { kp = val; break; }
            }
            const label = `${organ}\nQ=${q} V=${v}${kp ? '\nKp=' + kp : ''}`;
            this.cy.add({ data: { id: organ, label, organName: organ, q, v, kp, type: 'organ' } });
        });

        organs.forEach(organ => {
            const q = bf[organ] !== undefined ? bf[organ] : '?';
            if (organ.toLowerCase().includes('lung')) {
                this._addEdge('VENOUS', organ, `Q=${q}`);
                this._addEdge(organ, 'ARTERIAL', '');
            } else if (organ.toLowerCase().includes('gut') || organ.toLowerCase().includes('intestin')) {
                this._addEdge('ARTERIAL', organ, `Q=${q}`);
                const liver = organs.find(o => o.toLowerCase().includes('liver'));
                this._addEdge(organ, liver || 'VENOUS', 'Portal');
            } else if (organ.toLowerCase().includes('liver')) {
                this._addEdge('ARTERIAL', organ, `Q=${q}`);
                this._addEdge(organ, 'VENOUS', 'Hepatic');
            } else {
                this._addEdge('ARTERIAL', organ, `Q=${q}`);
                this._addEdge(organ, 'VENOUS', '');
            }
        });

        this.autoLayout();
    },

    _addEdge(src, tgt, label) {
        if (!this.cy.getElementById(src).length || !this.cy.getElementById(tgt).length) return;
        const id = `e_${src}_${tgt}`;
        if (!this.cy.getElementById(id).length) {
            this.cy.add({ data: { id, source: src, target: tgt, label } });
        }
    },

    // ── Add Nodes ────────────────────────────────────────────────────────────
    addOrganNode() {
        const name = prompt('Organ name (e.g. Liver, Kidney, Fat):');
        if (!name || !name.trim()) return;
        const id = name.trim().replace(/[^a-zA-Z0-9]/g, '_');
        const q  = prompt('Blood flow fraction Q (e.g. 0.174):', '0.0') || '0.0';
        const v  = prompt('Volume fraction V (e.g. 0.036):', '0.0') || '0.0';
        const kp = prompt('Partition coefficient Kp (leave blank if unknown):', '') || '';
        const label = `${name.trim()}\nQ=${q} V=${v}${kp ? '\nKp=' + kp : ''}`;
        this.cy.add({ data: { id, label, organName: name.trim(), q, v, kp, type: 'organ' } });
        this.cy.getElementById(id).position({ x: 200 + Math.random() * 300, y: 200 + Math.random() * 200 });
    },

    addBloodNodes() {
        if (!this.cy.getElementById('ARTERIAL').length)
            this.cy.add({ data: { id: 'ARTERIAL', label: '🩸 Arterial Blood', type: 'blood' } });
        if (!this.cy.getElementById('VENOUS').length)
            this.cy.add({ data: { id: 'VENOUS', label: '🫀 Venous Blood', type: 'blood' } });
        this.autoLayout();
    },

    // ── Connect Mode ─────────────────────────────────────────────────────────
    toggleConnectMode() {
        this.connectMode = !this.connectMode;
        this.connectSource = null;
        const btn = document.getElementById('connect-btn');
        const hint = document.getElementById('flow-connect-hint');
        if (this.connectMode) {
            btn.classList.add('active');
            hint.textContent = '← Click source node, then target node to draw an arrow';
        } else {
            btn.classList.remove('active');
            hint.textContent = '';
        }
    },

    _handleConnectClick(node) {
        if (!this.connectSource) {
            this.connectSource = node;
            node.style('border-color', '#fbbf24');
            document.getElementById('flow-connect-hint').textContent = '✓ Source selected — now click the target node';
        } else {
            const label = prompt('Edge label (e.g. Q=0.17, Portal Vein — or leave blank):', '') || '';
            this._addEdge(this.connectSource.id(), node.id(), label);
            this.connectSource.style('border-color', this.connectSource.data('type') === 'blood' ? '#a78bfa' : '#22d3ee');
            this.connectSource = null;
            this.toggleConnectMode();
        }
    },

    // ── Delete Selected ──────────────────────────────────────────────────────
    deleteSelected() {
        const selected = this.cy.$(':selected');
        if (!selected.length) { alert('Select a node or edge first (click to select)'); return; }
        if (confirm(`Delete ${selected.length} selected element(s)?`)) selected.remove();
    },

    // ── Auto Layout ──────────────────────────────────────────────────────────
    autoLayout() {
        if (!this.cy) return;
        // Manual hierarchical: ARTERIAL top, organs middle, VENOUS bottom
        const w = document.getElementById('cy-canvas').offsetWidth || 800;
        const organs = this.cy.nodes('[type="organ"]');
        const spacing = Math.max(130, Math.min(200, (w - 100) / Math.max(organs.length, 1)));
        const startX = (w - spacing * (organs.length - 1)) / 2;

        this.cy.getElementById('ARTERIAL').position({ x: w / 2, y: 60 });
        organs.forEach((n, i) => n.position({ x: startX + i * spacing, y: 250 }));
        this.cy.getElementById('VENOUS').position({ x: w / 2, y: 440 });
        this.cy.fit(this.cy.elements(), 30);
    },

    // ── Apply to Parameters ──────────────────────────────────────────────────
    async applyToParams() {
        if (!this.cy) return;
        if (!currentParams) currentParams = {};
        if (!currentParams.blood_flow_fraction) currentParams.blood_flow_fraction = {};
        if (!currentParams.volume_fraction) currentParams.volume_fraction = {};
        if (!currentParams.biochemical_parameters) currentParams.biochemical_parameters = {};

        // Clear existing (non-Human_) organ entries
        ['blood_flow_fraction', 'volume_fraction'].forEach(key => {
            Object.keys(currentParams[key]).forEach(k => { if (!k.startsWith('Human_')) delete currentParams[key][k]; });
        });

        this.cy.nodes('[type="organ"]').forEach(node => {
            const d = node.data();
            const organ = d.organName || d.id;
            const q = parseFloat(d.q);
            const v = parseFloat(d.v);
            const kp = parseFloat(d.kp);
            if (!isNaN(q)) currentParams.blood_flow_fraction[organ] = q;
            if (!isNaN(v)) currentParams.volume_fraction[organ]     = v;
            if (!isNaN(kp) && kp > 0) currentParams.biochemical_parameters[`${organ}:plasma`] = kp;
        });

        // Rebuild param tables to reflect changes
        renderEditableParameters(currentParams);
        renderCompartmentFlow(currentParams);

        // Save to server
        try {
            const resp = await fetch('/api/save-params', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ paper_name: currentPaperName, parameters: currentParams })
            });
            if (resp.ok) {
                const hint = document.getElementById('flow-connect-hint');
                hint.textContent = '✅ Parameters saved!';
                hint.style.color = '#10b981';
                setTimeout(() => { hint.textContent = ''; hint.style.color = ''; }, 3000);
            }
        } catch(e) { console.error('Save failed:', e); }
    },

    // ── Node Popover ─────────────────────────────────────────────────────────
    _showNodePopover(node, pos) {
        this._closePopover();
        const d = node.data();
        const isBlood = d.type === 'blood';
        const div = document.createElement('div');
        div.className = 'node-popover';
        div.style.left = (pos.x + 20) + 'px';
        div.style.top  = (pos.y + 20) + 'px';
        div.innerHTML = `
            <h4>${isBlood ? d.label : '✏️ Edit ' + (d.organName || d.id)}</h4>
            ${!isBlood ? `
            <label>Organ Name</label><input id="pop-name" value="${d.organName || d.id}">
            <label>Blood Flow Fraction (Q)</label><input id="pop-q" type="number" step="0.001" value="${d.q || 0}">
            <label>Volume Fraction (V)</label><input id="pop-v" type="number" step="0.001" value="${d.v || 0}">
            <label>Partition Coef. Kp (0 = none)</label><input id="pop-kp" type="number" step="0.01" value="${d.kp || 0}">
            <div class="pop-btns">
                <button class="pop-btn pop-save" onclick="cyBuilder._saveNodeEdit('${node.id()}')">💾 Save</button>
                <button class="pop-btn pop-del" onclick="cyBuilder._deleteNode('${node.id()}')">🗑️ Delete</button>
                <button class="pop-btn pop-cancel" onclick="cyBuilder._closePopover()">✕</button>
            </div>` : `<div class="pop-btns"><button class="pop-btn pop-cancel" onclick="cyBuilder._closePopover()">✕ Close</button></div>`}
        `;
        document.body.appendChild(div);
        this.popover = div;
    },

    _showEdgePopover(edge, pos) {
        this._closePopover();
        const div = document.createElement('div');
        div.className = 'node-popover';
        div.style.left = (pos.x + 20) + 'px';
        div.style.top  = (pos.y + 20) + 'px';
        div.innerHTML = `
            <h4>✏️ Edit Connection</h4>
            <label>Label (e.g. Q=0.17)</label>
            <input id="pop-edge-label" value="${edge.data('label') || ''}">
            <div class="pop-btns">
                <button class="pop-btn pop-save" onclick="cyBuilder._saveEdgeEdit('${edge.id()}')">💾 Save</button>
                <button class="pop-btn pop-del" onclick="cyBuilder._deleteEdge('${edge.id()}')">🗑️ Delete</button>
                <button class="pop-btn pop-cancel" onclick="cyBuilder._closePopover()">✕</button>
            </div>
        `;
        document.body.appendChild(div);
        this.popover = div;
    },

    _saveNodeEdit(nodeId) {
        const node = this.cy.getElementById(nodeId);
        const name = document.getElementById('pop-name')?.value.trim() || node.data('organName');
        const q    = document.getElementById('pop-q')?.value  || '0';
        const v    = document.getElementById('pop-v')?.value  || '0';
        const kp   = document.getElementById('pop-kp')?.value || '0';
        const label = `${name}\nQ=${q} V=${v}${parseFloat(kp) > 0 ? '\nKp=' + kp : ''}`;
        node.data({ organName: name, q, v, kp, label });
        this._closePopover();
    },

    _deleteNode(nodeId) {
        if (confirm('Delete this node and all its connections?')) {
            this.cy.getElementById(nodeId).remove();
            this._closePopover();
        }
    },

    _saveEdgeEdit(edgeId) {
        const label = document.getElementById('pop-edge-label')?.value || '';
        this.cy.getElementById(edgeId).data('label', label);
        this._closePopover();
    },

    _deleteEdge(edgeId) {
        this.cy.getElementById(edgeId).remove();
        this._closePopover();
    },

    _closePopover() {
        if (this.popover) { this.popover.remove(); this.popover = null; }
    },
};
