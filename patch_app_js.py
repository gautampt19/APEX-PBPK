import re

with open("webapp/static/app.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Fix addParamRow to attach listeners
target1 = """window.addParamRow = (btn, isStringValue) => {
    const tbody = btn.closest('.param-section').querySelector('tbody');
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td><input type="text" class="edit-key" placeholder="New key" /></td>
        <td><input type="text" class="edit-val" placeholder="Value" /></td>
        <td style="width:30px;"><button class="btn btn-secondary" style="padding:2px 6px; color:#ef4444;" onclick="this.closest('tr').remove(); saveUIToState();">✕</button></td>
    `;
    tbody.appendChild(tr);
};"""

replace1 = """window.addParamRow = (btn, isStringValue) => {
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
};"""
code = code.replace(target1, replace1)

# 2. Update renderCompartmentFlow to discover organs from all dicts
target2 = """async function renderCompartmentFlow(params) {
    const container = document.getElementById('compartment-diagram');
    const empty = document.getElementById('flow-empty');
    if (!params || !params.blood_flow_fraction || Object.keys(params.blood_flow_fraction).length === 0) {
        container.style.display = 'none'; empty.style.display = 'flex'; return;
    }
    empty.style.display = 'none'; container.style.display = 'flex';
    const bf = params.blood_flow_fraction;
    const organs = Object.keys(bf).filter(k => !k.startsWith('Human_') && k.trim() !== '');"""

replace2 = """async function renderCompartmentFlow(params) {
    const container = document.getElementById('compartment-diagram');
    const empty = document.getElementById('flow-empty');
    if (!params) {
        container.style.display = 'none'; empty.style.display = 'flex'; return;
    }
    
    // Discover organs from multiple parameter sections
    const bf = params.blood_flow_fraction || {};
    const vf = params.volume_fraction || {};
    const biochem = params.biochemical_parameters || {};
    
    let organSet = new Set();
    Object.keys(bf).forEach(k => organSet.add(k));
    Object.keys(vf).forEach(k => organSet.add(k));
    
    // Also try to find organs in partition coefficients (e.g., Liver:plasma or Liver_plasma)
    Object.keys(biochem).forEach(k => {
        if(k.includes(':plasma')) organSet.add(k.split(':plasma')[0].trim());
        if(k.includes('_plasma')) {
            const parts = k.split('_');
            if(parts.length > 1) {
                // e.g. TDCIPP_Liver_plasma -> we want Liver. Usually the organ is the word before _plasma
                const idx = parts.indexOf('plasma');
                if(idx > 0) organSet.add(parts[idx-1]);
            }
        }
    });
    
    const organs = Array.from(organSet).filter(k => !k.startsWith('Human_') && k.trim() !== '' && k.toLowerCase() !== 'plasma' && k.toLowerCase() !== 'blood');
    
    if (organs.length === 0) {
        container.style.display = 'none'; empty.style.display = 'flex'; return;
    }
    empty.style.display = 'none'; container.style.display = 'flex';"""
code = code.replace(target2, replace2)

# Update the organ loop to handle missing flow
target3 = """        const flow = bf[organ]; const sanitized = organ.replace(/[^a-zA-Z0-9]/g, '_');
        const kp = params.biochemical_parameters?.[`${organ}:plasma`] || '';
        const kpLabel = kp ? `\\nKp=${kp}` : '';"""

replace3 = """        const flow = bf[organ] !== undefined ? bf[organ] : "?"; 
        const sanitized = organ.replace(/[^a-zA-Z0-9]/g, '_');
        
        // Find partition coefficient (either Organ:plasma or Compound_Organ_plasma)
        let kp = '';
        for (const [k, v] of Object.entries(biochem)) {
            if (k === `${organ}:plasma` || k.includes(`${organ}_plasma`)) {
                kp = v; break;
            }
        }
        const kpLabel = kp ? `\\nKp=${kp}` : '';"""
code = code.replace(target3, replace3)


with open("webapp/static/app.js", "w", encoding="utf-8") as f:
    f.write(code)
