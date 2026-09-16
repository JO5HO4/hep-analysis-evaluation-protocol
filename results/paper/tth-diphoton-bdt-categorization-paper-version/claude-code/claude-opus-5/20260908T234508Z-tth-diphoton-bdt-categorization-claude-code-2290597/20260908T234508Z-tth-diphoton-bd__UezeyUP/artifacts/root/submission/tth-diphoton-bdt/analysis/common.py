"""Shared helpers: configuration loading, results layout and JSON writing."""

from __future__ import annotations

import json
import math
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import yaml

PACKAGE_ROOT = Path(__file__).resolve().parent
SUBMISSION_ROOT = PACKAGE_ROOT.parent
DEFAULT_CONFIG = SUBMISSION_ROOT / "config" / "config.yaml"


def load_config(path: str | os.PathLike[str] | None = None) -> dict[str, Any]:
    cfg_path = Path(path) if path else DEFAULT_CONFIG
    with open(cfg_path, "r", encoding="utf-8") as handle:
        cfg = yaml.safe_load(handle)
    cfg["_config_path"] = str(cfg_path)
    return cfg


def resolve_runtime(cfg: Mapping[str, Any]) -> dict[str, Any]:
    """Apply environment overrides and return the fully resolved settings."""
    resolved = json.loads(json.dumps({k: v for k, v in cfg.items() if k != "_config_path"}))
    resolved["_config_path"] = cfg.get("_config_path")

    env_var = cfg["inputs"]["env_var"]
    input_root = os.environ.get(env_var) or cfg["inputs"]["default_root"]
    resolved["inputs"]["resolved_root"] = str(input_root)
    resolved["inputs"]["resolved_from_env"] = bool(os.environ.get(env_var))
    resolved["inputs"]["env_var_value"] = os.environ.get(env_var)

    cap_env = cfg["run"]["max_selected_per_sample_env"]
    cap_raw = os.environ.get(cap_env)
    cap: int | None = None
    if cap_raw is not None and str(cap_raw).strip() != "":
        cap = int(cap_raw)
        if cap <= 0:
            cap = None
    resolved["run"]["max_selected_per_sample"] = cap
    resolved["run"]["max_selected_per_sample_source"] = (
        f"environment:{cap_env}" if cap is not None else "unset (uncapped)"
    )
    resolved["run"]["row_cap_policy"] = (
        "uncapped by default; TTH_MAX_SELECTED_PER_SAMPLE limits selected rows "
        "per sample only when explicitly set for development throttling"
    )

    results_dir = os.environ.get("TTH_RESULTS_DIR") or cfg["run"]["results_dir"]
    resolved["run"]["results_dir"] = str(results_dir)
    return resolved


@dataclass(frozen=True)
class Paths:
    root: Path

    def __post_init__(self) -> None:
        for sub in (
            "",
            "plots",
            "model",
            "optimization",
            "inference",
            "categorization",
            "categorization/plots",
            "categorization/histograms",
            "fit",
            "fit/FIT1",
            "fit/FIT1/plots",
        ):
            (self.root / sub).mkdir(parents=True, exist_ok=True)

    def __call__(self, *parts: str) -> Path:
        return self.root.joinpath(*parts)


class _NpEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:  # noqa: D102
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            value = float(o)
            return value if math.isfinite(value) else None
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, Path):
            return str(o)
        if isinstance(o, set):
            return sorted(o)
        return super().default(o)


def _sanitize(obj: Any) -> Any:
    if isinstance(obj, float):
        return obj if math.isfinite(obj) else None
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize(v) for v in obj]
    return obj


def write_json(path: str | os.PathLike[str], payload: Any) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(_sanitize(payload), handle, indent=2, sort_keys=False, cls=_NpEncoder)
        handle.write("\n")
    return out


def write_yaml(path: str | os.PathLike[str], payload: Any) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        yaml.safe_dump(
            json.loads(json.dumps(_sanitize(payload), cls=_NpEncoder)),
            handle,
            sort_keys=False,
            default_flow_style=False,
        )
    return out


def sha256_of(path: str | os.PathLike[str], max_bytes: int = 8 * 1024 * 1024) -> dict[str, Any]:
    """Cheap fingerprint of a (possibly large) input file."""
    import hashlib

    p = Path(path)
    size = p.stat().st_size
    digest = hashlib.sha256()
    with open(p, "rb") as handle:
        digest.update(handle.read(max_bytes))
    return {
        "path": str(p),
        "size_bytes": size,
        "sha256_first_bytes": digest.hexdigest(),
        "hashed_bytes": min(size, max_bytes),
    }


def environment_record() -> dict[str, Any]:
    import platform
    import sys

    versions: dict[str, str] = {}
    for module in ("numpy", "pandas", "sklearn", "uproot", "awkward", "matplotlib", "scipy", "yaml"):
        try:
            versions[module] = __import__(module).__version__
        except Exception:  # pragma: no cover - defensive
            versions[module] = "unavailable"
    try:
        import ROOT

        versions["ROOT"] = ROOT.gROOT.GetVersion()
    except Exception:  # pragma: no cover
        versions["ROOT"] = "unavailable"

    return {
        "python": sys.version,
        "platform": platform.platform(),
        "packages": versions,
        "threading": {
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
            "note": "single-threaded numeric backends are forced by run_analysis.py "
            "for bit-level reproducibility",
        },
    }


def git_describe(path: str | os.PathLike[str]) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:  # pragma: no cover
        pass
    return None


def safe_div(num: float, den: float, default: float = float("nan")) -> float:
    return float(num) / float(den) if den not in (0, 0.0) else default
