const fs = require('fs');

const params = JSON.parse(fs.readFileSync('pipeline_output/s12249-023-02680-y_params.json', 'utf8'));

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

console.log(mermaidCode);
