#!/usr/bin/env python3
"""Quick test of the interactive parameter editor from run_pipeline.py.
Uses the existing params JSON so we don't need to wait for OCR + LLM."""

import json
import os
import sys

params_json = "pipeline_output/s12249-023-02680-y_params.json"

if not os.path.exists(params_json):
    print(f"❌ {params_json} not found. Run the extraction step first.")
    sys.exit(1)

with open(params_json, "r", encoding="utf-8") as f:
    params = json.load(f)

def _save_params():
    with open(params_json, "w", encoding="utf-8") as f:
        json.dump(params, f, indent=4)

def _display_params():
    print(f"\n{'='*60}")
    print(f"  EXTRACTED PARAMETERS — REVIEW & EDIT")
    print(f"{'='*60}")

    bf = params.get("blood_flow_fraction", {})
    vf = params.get("volume_fraction", {})
    compartments = sorted(set(list(bf.keys()) + list(vf.keys())))
    print(f"\n📦 Compartments detected ({len(compartments)}):")
    print(f"   {', '.join(compartments)}")

    if bf:
        print(f"\n🩸 Blood Flow Fractions (fraction of cardiac output):")
        for organ, val in sorted(bf.items()):
            print(f"   {organ:<20s} {val}")

    if vf:
        print(f"\n📐 Volume Fractions (fraction of body weight):")
        for organ, val in sorted(vf.items()):
            print(f"   {organ:<20s} {val}")

    biochem = params.get("biochemical_parameters", {})
    if biochem:
        print(f"\n⚗️  Biochemical Parameters ({len(biochem)}):")
        kps = {k: v for k, v in biochem.items() if "plasma" in k.lower() or "partition" in k.lower() or k.startswith("Kp")}
        other = {k: v for k, v in biochem.items() if k not in kps}
        if kps:
            print(f"   ── Partition Coefficients ──")
            for k, v in sorted(kps.items()):
                print(f"   {k:<30s} {v}")
        if other:
            print(f"   ── Other ──")
            for k, v in sorted(other.items()):
                print(f"   {k:<30s} {v}")

    equations = params.get("equations", {})
    if equations:
        print(f"\n📝 Equations ({len(equations)}):")
        for name, eq in equations.items():
            eq_display = eq if len(eq) < 80 else eq[:77] + "..."
            print(f"   {name:<30s} {eq_display}")

def _try_numeric(val_str):
    try:
        f = float(val_str)
        return int(f) if f == int(f) else f
    except ValueError:
        return val_str

def _pick_section():
    sections = [
        ("blood_flow_fraction",    "Blood Flow Fractions"),
        ("volume_fraction",        "Volume Fractions"),
        ("biochemical_parameters", "Biochemical Parameters"),
        ("equations",              "Equations"),
    ]
    print("\n   Which section?")
    for i, (_, label) in enumerate(sections, 1):
        print(f"   {i}) {label}")
    try:
        choice = input("   Section number: ").strip()
        idx = int(choice) - 1
        if 0 <= idx < len(sections):
            return sections[idx][0]
    except (ValueError, EOFError):
        pass
    print("   ⚠️  Invalid section.")
    return None

def _edit_param():
    section_key = _pick_section()
    if not section_key:
        return
    section = params.get(section_key, {})
    if not section:
        print(f"   Section is empty. Use 'add' to add parameters first.")
        return
    print(f"\n   Current keys: {', '.join(section.keys())}")
    try:
        key = input("   Parameter name to edit: ").strip()
    except EOFError:
        return
    if key not in section:
        print(f"   ⚠️  '{key}' not found in this section.")
        return
    print(f"   Current value: {section[key]}")
    try:
        new_val = input(f"   New value: ").strip()
    except EOFError:
        return
    if not new_val:
        print("   ⚠️  Empty input — value unchanged.")
        return
    section[key] = _try_numeric(new_val)
    params[section_key] = section
    _save_params()
    print(f"   ✅ {key} → {section[key]}")

def _add_param():
    section_key = _pick_section()
    if not section_key:
        return
    if section_key not in params:
        params[section_key] = {}
    try:
        key = input("   New parameter name: ").strip()
    except EOFError:
        return
    if not key:
        print("   ⚠️  Empty name — cancelled.")
        return
    if key in params[section_key]:
        print(f"   ⚠️  '{key}' already exists (value: {params[section_key][key]}). Use 'edit' to change it.")
        return
    try:
        val = input(f"   Value for '{key}': ").strip()
    except EOFError:
        return
    if not val:
        print("   ⚠️  Empty value — cancelled.")
        return
    params[section_key][key] = _try_numeric(val)
    _save_params()
    print(f"   ✅ Added {key} = {params[section_key][key]}")

def _delete_param():
    section_key = _pick_section()
    if not section_key:
        return
    section = params.get(section_key, {})
    if not section:
        print(f"   Section is empty.")
        return
    print(f"\n   Current keys: {', '.join(section.keys())}")
    try:
        key = input("   Parameter name to delete: ").strip()
    except EOFError:
        return
    if key not in section:
        print(f"   ⚠️  '{key}' not found.")
        return
    del section[key]
    params[section_key] = section
    _save_params()
    print(f"   🗑️  Deleted '{key}'")

def _add_compartment():
    try:
        name = input("   New compartment name (e.g., Spleen): ").strip()
    except EOFError:
        return
    if not name:
        print("   ⚠️  Empty name — cancelled.")
        return
    try:
        bf_val = input(f"   Blood flow fraction for {name} (or press Enter to skip): ").strip()
    except EOFError:
        bf_val = ""
    if bf_val:
        if "blood_flow_fraction" not in params:
            params["blood_flow_fraction"] = {}
        params["blood_flow_fraction"][name] = _try_numeric(bf_val)
    try:
        vf_val = input(f"   Volume fraction for {name} (or press Enter to skip): ").strip()
    except EOFError:
        vf_val = ""
    if vf_val:
        if "volume_fraction" not in params:
            params["volume_fraction"] = {}
        params["volume_fraction"][name] = _try_numeric(vf_val)
    try:
        kp_val = input(f"   {name}:plasma partition coefficient (or press Enter to skip): ").strip()
    except EOFError:
        kp_val = ""
    if kp_val:
        if "biochemical_parameters" not in params:
            params["biochemical_parameters"] = {}
        params["biochemical_parameters"][f"{name}:plasma"] = _try_numeric(kp_val)
    _save_params()
    print(f"   ✅ Compartment '{name}' added.")


# ── Interactive loop ──
_display_params()

MENU = """
┌────────────────────────────────────────┐
│  [v] View parameters                   │
│  [e] Edit a parameter value            │
│  [a] Add a parameter                   │
│  [d] Delete a parameter                │
│  [c] Add a new compartment             │
│  [ENTER] ✅ Continue to R generation   │
│  [q] ❌ Abort pipeline                 │
└────────────────────────────────────────┘"""

while True:
    print(MENU)
    try:
        choice = input("▶ Choice: ").strip().lower()
    except EOFError:
        choice = ""

    if choice == "" or choice == "enter":
        print("\n  ✅ Parameters approved. Continuing to R model generation...")
        break
    elif choice == "q":
        print("❌ Pipeline aborted by user.")
        sys.exit(0)
    elif choice == "v":
        _display_params()
    elif choice == "e":
        _edit_param()
    elif choice == "a":
        _add_param()
    elif choice == "d":
        _delete_param()
    elif choice == "c":
        _add_compartment()
    else:
        print(f"   ⚠️  Unknown option '{choice}'")

print("\n🎉 Editor test complete! JSON saved to:", params_json)
