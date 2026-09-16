"""Input discovery and the external input-data contract.

The external contract is identical to ``tb-hyy``: the ATLAS open-data
``GamGam`` ROOT directory is read from ``$TB_HYY_INPUTS`` when that variable is
set, and the expected layout underneath it is ``MC/`` and ``data/``.  ROOT
inputs are never copied into the submission directory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .common import sha256_of

#: Physics grouping of every accepted sample.
SAMPLE_ROLES: dict[str, dict[str, Any]] = {
    "ttH": {"role": "signal_top", "kind": "mc", "label": "ttH (H->yy)"},
    "tH": {"role": "signal_top", "kind": "mc", "label": "tH (H->yy)"},
    "ggH": {"role": "resonant_higgs", "kind": "mc", "label": "ggH (H->yy)"},
    "VBF": {"role": "resonant_higgs", "kind": "mc", "label": "VBF (H->yy)"},
    "WH": {"role": "resonant_higgs", "kind": "mc", "label": "WH (H->yy)"},
    "ZH": {"role": "resonant_higgs", "kind": "mc", "label": "ZH (H->yy)"},
    "ggZH": {"role": "resonant_higgs", "kind": "mc", "label": "ggZH (H->yy)"},
    "data": {"role": "observed_data", "kind": "data", "label": "observed GamGam data"},
}

EXCLUSION_STATEMENT = (
    "This run processes ONLY nominal Higgs H->gamma gamma signal MC "
    "(ggH, VBF, WH, ZH, ggZH, ttH, tH) and observed GamGam data. "
    "Sherpa yy / prompt-diphoton continuum MC and every other non-Higgs MC "
    "sample (ttbar, single top, V+jets, ...) are explicitly EXCLUDED: they are "
    "neither opened nor read. The continuum background is instead modelled "
    "data-driven, from the NTI diphoton control sample (BDT training and "
    "categorization control estimates) and from the observed TI data sidebands "
    "(statistical workspace)."
)


def resolve_inputs(cfg: Mapping[str, Any]) -> dict[str, Any]:
    """Locate every requested sample file and build the input-data contract."""
    inputs_cfg = cfg["inputs"]
    root = Path(inputs_cfg["resolved_root"])
    mc_dir = root / inputs_cfg["mc_subdir"]
    data_dir = root / inputs_cfg["data_subdir"]
    suffix = inputs_cfg["file_suffix"]

    missing: list[str] = []
    samples: list[dict[str, Any]] = []

    for name in inputs_cfg["mc_samples"]:
        path = mc_dir / f"{name}{suffix}"
        if not path.exists():
            missing.append(str(path))
            continue
        samples.append(
            {
                "sample": name,
                **SAMPLE_ROLES[name],
                "path": str(path),
                "tree": inputs_cfg["tree"],
                **sha256_of(path),
            }
        )

    for name in inputs_cfg["data_samples"]:
        path = data_dir / f"{name}{suffix}"
        if not path.exists():
            missing.append(str(path))
            continue
        samples.append(
            {
                "sample": name,
                **SAMPLE_ROLES[name],
                "path": str(path),
                "tree": inputs_cfg["tree"],
                **sha256_of(path),
            }
        )

    present_dirs = {
        "MC": sorted(p.name for p in mc_dir.glob("*.root")) if mc_dir.is_dir() else [],
        "data": sorted(p.name for p in data_dir.glob("*.root")) if data_dir.is_dir() else [],
    }
    requested = set(inputs_cfg["mc_samples"]) | set(inputs_cfg["data_samples"])
    seen_files = {f"{n}{suffix}" for n in requested}
    not_read = sorted(
        [f"MC/{n}" for n in present_dirs["MC"] if n not in seen_files]
        + [f"data/{n}" for n in present_dirs["data"] if n not in seen_files]
    )

    contract = {
        "contract_name": "tb-hyy GamGam open-data input contract",
        "environment_variable": inputs_cfg["env_var"],
        "environment_variable_value": inputs_cfg.get("env_var_value"),
        "resolved_from_environment": inputs_cfg.get("resolved_from_env", False),
        "input_root": str(root),
        "expected_layout": {"MC": str(mc_dir), "data": str(data_dir)},
        "layout_present": {"MC": mc_dir.is_dir(), "data": data_dir.is_dir()},
        "tree_name": inputs_cfg["tree"],
        "tree_format": "ROOT RNTuple (read with uproot)",
        "inputs_copied_into_submission": False,
        "inputs_read_in_place": True,
        "scope": {
            "nominal_higgs_signal_mc_only": True,
            "observed_data_included": True,
            "sherpa_yy_excluded": True,
            "prompt_diphoton_continuum_mc_excluded": True,
            "other_non_higgs_mc_excluded": True,
            "statement": EXCLUSION_STATEMENT,
        },
        "requested_mc_samples": list(inputs_cfg["mc_samples"]),
        "requested_data_samples": list(inputs_cfg["data_samples"]),
        "excluded_sample_classes": list(inputs_cfg["excluded_samples"]),
        "files_present_in_input_root": present_dirs,
        "files_present_but_not_read": not_read,
        "resolved_samples": samples,
        "missing_files": missing,
    }
    return contract
