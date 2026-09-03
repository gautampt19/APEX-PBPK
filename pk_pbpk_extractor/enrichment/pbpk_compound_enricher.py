"""
pk_pbpk_extractor/enrichment/pbpk_compound_enricher.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PBPK-specific compound parameter enrichment.

Queries scientific databases (PubChem, ChEMBL, DrugBank cross-refs)
to retrieve fundamental physicochemical constants and clearance mechanisms
required for PBPK modeling equations (e.g., Rodgers-Rowland / Poulin-Theil Kp,
Peff, ion trapping, CLu).
"""

from __future__ import annotations
import json
import logging
import os
import re
import subprocess
import tempfile
from typing import Dict, List, Optional, Tuple, Any

logger = logging.getLogger(__name__)

# Base path for scientific agent skills
SCIENCE_SKILLS_DIR = os.path.expanduser("~/.gemini/config/plugins/science/skills")
PUBCHEM_DIR = os.path.join(SCIENCE_SKILLS_DIR, "pubchem_database")
CHEMBL_DIR = os.path.join(SCIENCE_SKILLS_DIR, "chembl_database")


def _run_skill_script(skill_dir: str, script_name: str, args: List[str]) -> Optional[dict]:
    """Execute a scientific agent skill script via uv run."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        out_path = tmp.name

    cmd = ["uv", "run", f"scripts/{script_name}"] + args + ["--output", out_path]
    try:
        res = subprocess.run(
            cmd,
            cwd=skill_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if res.returncode == 0 and os.path.exists(out_path):
            with open(out_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        else:
            logger.warning("Skill script failed (%s): %s", script_name, res.stderr)
            return None
    except Exception as e:
        logger.warning("Error running skill %s: %s", script_name, e)
        return None
    finally:
        if os.path.exists(out_path):
            try:
                os.remove(out_path)
            except Exception:
                pass


def _extract_fup_from_text(text: str) -> Optional[float]:
    """Extract unbound fraction (fup) from protein binding text description (e.g., '97% bound' -> 0.03)."""
    m = re.search(r"(\d+(?:\.\d+)?)\s*%\s*(?:bound|binding)", text, re.IGNORECASE)
    if m:
        pct_bound = float(m.group(1))
        if 0 <= pct_bound <= 100:
            return round((100.0 - pct_bound) / 100.0, 4)
    return None


def resolve_compound_name(paper_title: str, text_context: str = "") -> Optional[str]:
    """
    Heuristic extraction of target drug name from paper title or text context.
    Matches standard pharmaceutical drug suffixes or common compounds.
    """
    # Common PBPK model drug pattern (e.g. Midazolam, Theophylline, Chlorpyrifos, Itraconazole)
    drug_suffix_re = re.compile(
        r"([A-Z][a-z]{3,20}(?:am|in|ol|one|ide|ine|ate|ib|ab|ole|cin|vir|il|an))"
    )
    # Check title first
    matches = drug_suffix_re.findall(paper_title)
    # Exclude common scientific non-drug words
    blacklist = {
        "Administration", "Absorption", "Application", "Evaluation",
        "Determination", "Distribution", "Elimination", "Inhibition",
        "Investigation", "Pharmacokinetic", "Physiologically", "Validation",
        "Formulation", "Dissolution", "Prediction", "Simulation", "Metabolism",
        "Concentration", "Interaction", "Disposition", "Characterization",
        "Human", "Plasma", "Tissue", "Model", "Equation", "Section", "Table"
    }
    candidates = [m for m in matches if m not in blacklist]
    if candidates:
        return candidates[0]

    # Check context text
    if text_context:
        matches = drug_suffix_re.findall(text_context[:2000])
        candidates = [m for m in matches if m not in blacklist]
        if candidates:
            return candidates[0]

    return None


def enrich_pbpk_properties(
    compound_name: str,
    paper_id: str = "unknown"
) -> Tuple[List[tuple], Dict[str, Any]]:
    """
    Enriches PBPK modeling parameters for a compound using PubChem, ChEMBL, and DrugBank cross-refs.

    Returns:
        (param_records, compound_meta)
        where param_records is a list of 13-tuples ready for DB/harmonizer.
    """
    records = []
    compound_meta = {
        "compound_name": compound_name,
        "pubchem_cid": None,
        "chembl_id": None,
        "drugbank_id": None,
        "smiles": None,
        "molecular_weight": None,
        "logp": None,
        "tpsa": None,
        "mechanisms": [],
    }

    if not compound_name:
        return records, compound_meta

    print(f"[PBPK Skill Enrichment] Querying PubChem & ChEMBL for drug: '{compound_name}'.")

    # ── 1. PubChem: Resolution & Properties ──────────────────────
    cid = None
    if os.path.exists(PUBCHEM_DIR):
        res = _run_skill_script(PUBCHEM_DIR, "pubchem_api.py", ["resolve", "--name", compound_name])
        if res:
            try:
                cids = res.get("identifiers", {}).get("IdentifierList", {}).get("CID", [])
                if cids:
                    cid = cids[0]
                    compound_meta["pubchem_cid"] = cid
                    print(f"    ✓ PubChem CID: {cid}")

                # SMILES from resolve
                p_res = res.get("properties", {}).get("PropertyTable", {}).get("Properties", [])
                if p_res:
                    compound_meta["smiles"] = p_res[0].get("ConnectivitySMILES") or p_res[0].get("SMILES")
            except Exception:
                pass

        if cid:
            # Fetch physical properties (MW, XLogP, TPSA, HBD, HBA)
            props_data = _run_skill_script(PUBCHEM_DIR, "pubchem_api.py", ["properties", "--cid", str(cid)])
            if props_data:
                try:
                    p_list = props_data.get("PropertyTable", {}).get("Properties", [])
                    if p_list:
                        p = p_list[0]
                        # Molecular Weight (g/mol)
                        if "MolecularWeight" in p:
                            mw = float(p["MolecularWeight"])
                            compound_meta["molecular_weight"] = mw
                            records.append((
                                paper_id, "PubChem_CID_" + str(cid),
                                "human", "pure_compound", "IV", 0.0,
                                "Molecular Weight", "molecular weight",
                                mw, None, "mean", "g/mol", "pubchem_enrichment"
                            ))

                        # LogP (XLogP)
                        if "XLogP" in p and p["XLogP"] is not None:
                            logp = float(p["XLogP"])
                            compound_meta["logp"] = logp
                            records.append((
                                paper_id, "PubChem_CID_" + str(cid),
                                "human", "pure_compound", "IV", 0.0,
                                "LogP", "octanol water partition coefficient",
                                logp, None, "mean", "dimensionless", "pubchem_enrichment"
                            ))

                        # TPSA (Topological Polar Surface Area, A^2)
                        if "TPSA" in p and p["TPSA"] is not None:
                            tpsa = float(p["TPSA"])
                            compound_meta["tpsa"] = tpsa
                            records.append((
                                paper_id, "PubChem_CID_" + str(cid),
                                "human", "pure_compound", "IV", 0.0,
                                "TPSA", "polar surface area",
                                tpsa, None, "mean", "A^2", "pubchem_enrichment"
                            ))

                        # HBD (Hydrogen Bond Donors)
                        if "HBondDonorCount" in p and p["HBondDonorCount"] is not None:
                            hbd = float(p["HBondDonorCount"])
                            records.append((
                                paper_id, "PubChem_CID_" + str(cid),
                                "human", "pure_compound", "IV", 0.0,
                                "HBD", "hydrogen bond donor count",
                                hbd, None, "mean", "count", "pubchem_enrichment"
                            ))

                        # HBA (Hydrogen Bond Acceptors)
                        if "HBondAcceptorCount" in p and p["HBondAcceptorCount"] is not None:
                            hba = float(p["HBondAcceptorCount"])
                            records.append((
                                paper_id, "PubChem_CID_" + str(cid),
                                "human", "pure_compound", "IV", 0.0,
                                "HBA", "hydrogen bond acceptor count",
                                hba, None, "mean", "count", "pubchem_enrichment"
                            ))
                except Exception as e:
                    logger.warning("Error parsing PubChem properties: %s", e)

            # Check DrugBank & Registry Xrefs
            xrefs = _run_skill_script(PUBCHEM_DIR, "pubchem_api.py", ["xrefs", "--cid", str(cid), "--type", "RegistryID"])
            if xrefs:
                try:
                    reg_ids = xrefs.get("InformationList", {}).get("Information", [{}])[0].get("RegistryID", [])
                    for rid in reg_ids:
                        if rid.startswith("DB") and len(rid) == 7:  # e.g. DB00683
                            compound_meta["drugbank_id"] = rid
                            print(f"    ✓ DrugBank Accession: {rid}")
                            break
                except Exception:
                    pass

            # Fetch Pharmacology (Protein binding / fup from DrugBank/FDA labels)
            pharm_data = _run_skill_script(PUBCHEM_DIR, "pubchem_api.py", ["pharmacology", "--cid", str(cid)])
            if pharm_data:
                try:
                    def _search_sections(sec):
                        if isinstance(sec, dict):
                            h = sec.get("TOCHeading", "")
                            if h == "Protein Binding":
                                for info in sec.get("Information", []):
                                    val_str = info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                    fup = _extract_fup_from_text(val_str)
                                    if fup is not None:
                                        records.append((
                                            paper_id, "PubChem_DrugBank_CID_" + str(cid),
                                            "human", "pure_compound", "IV", 0.0,
                                            "fup", "fraction unbound plasma",
                                            fup, None, "mean", "fraction", "pubchem_enrichment"
                                        ))
                                        print(f"    ✓ Protein Binding Derived fup: {fup}")
                                        break
                            for k, v in sec.items():
                                if k == "Section":
                                    _search_sections(v)
                        elif isinstance(sec, list):
                            for s in sec:
                                _search_sections(s)

                    _search_sections(pharm_data.get("Record", {}).get("Section", []))
                except Exception as e:
                    logger.warning("Error parsing PubChem pharmacology: %s", e)

    # ── 2. ChEMBL: Molecule & Mechanism of Action ─────────────────
    if os.path.exists(CHEMBL_DIR):
        chembl_data = _run_skill_script(CHEMBL_DIR, "chembl_api.py", ["molecule", "--search", compound_name, "--limit", "1"])
        if chembl_data:
            try:
                mols = chembl_data.get("molecules", [])
                if mols:
                    mol = mols[0]
                    chembl_id = mol.get("molecule_chembl_id")
                    compound_meta["chembl_id"] = chembl_id
                    print(f"    ✓ ChEMBL ID: {chembl_id}")

                    # SMILES from ChEMBL if not in PubChem
                    if not compound_meta["smiles"]:
                        compound_meta["smiles"] = mol.get("molecule_structures", {}).get("canonical_smiles")

                    # ALogP if PubChem didn't have XLogP
                    mprops = mol.get("molecule_properties", {})
                    if compound_meta["logp"] is None and "alogp" in mprops and mprops["alogp"] is not None:
                        alogp = float(mprops["alogp"])
                        compound_meta["logp"] = alogp
                        records.append((
                            paper_id, chembl_id,
                            "human", "pure_compound", "IV", 0.0,
                            "ALogP", "octanol water partition coefficient",
                            alogp, None, "mean", "dimensionless", "chembl_enrichment"
                        ))

                    # Mechanisms & Metabolic Enzymes
                    if chembl_id:
                        mech_data = _run_skill_script(
                            CHEMBL_DIR, "chembl_api.py",
                            ["mechanism", "--filter", f"molecule_chembl_id={chembl_id}", "--limit", "5"]
                        )
                        if mech_data:
                            mechs = mech_data.get("mechanisms", [])
                            for m in mechs:
                                moa = m.get("mechanism_of_action")
                                if moa:
                                    compound_meta["mechanisms"].append(moa)
                            if compound_meta["mechanisms"]:
                                print(f"    ✓ ChEMBL Mechanism: {compound_meta['mechanisms'][0][:60]}...")
            except Exception as e:
                logger.warning("Error parsing ChEMBL properties: %s", e)

    print(f"  [PBPK Skill Enrichment] Generated {len(records)} enriched PBPK parameter records.")
    return records, compound_meta
