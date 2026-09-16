"""tth-diphoton-bdt: top-associated H -> gamma gamma BDT categorization pipeline."""

from .top_categorization import (  # noqa: F401
    BDT_FEATURES,
    CATEGORY_ORDER,
    assign_top_category,
    build_jet_features,
    invariant_mass,
    optimize_bdt_boundaries,
    stable_partition,
)

__version__ = "1.0.0"
