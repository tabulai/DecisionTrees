# State of Decision Tree Algorithms: June 2026

A literature-review repo on decision tree algorithms: classical top-down
induction, split criteria, pruning, oblique and model trees, scalable tree
construction, random forests, boosted decision trees, optimal sparse trees,
streaming trees, survival trees, causal trees, quantile forests, and isolation
forests.

Version: 0.2

## Read the Report

- Interactive report: [index.html](index.html)
- Source research brief: [deep-research-report.md](deep-research-report.md)
- Reference audit summary: [reference_audit_june_2026.md](reference_audit_june_2026.md)
- Reference manifest: [references/manifest.csv](references/manifest.csv)
- BibTeX bibliography: [references/bibliography.bib](references/bibliography.bib)
- Demo notebooks: [notebooks](notebooks)

## Repository Contents

- `index.html` - generated static HTML report for GitHub Pages or local reading
- `deep-research-report.md` - source literature review
- `references/manifest.csv` - curated reference manifest with 105 decision-tree algorithm sources
- `references/manifest.json` - JSON form of the same reference manifest
- `references/bibliography.bib` - BibTeX bibliography keyed to the report
- `references/README.md` - notes on the reference audit and citation keys
- `reference_audit_june_2026.md` - topic counts and scope notes for the literature audit
- `notebooks/01_classical_cart_pruning.ipynb` - CART and pruning demo
- `notebooks/02_ensembles_random_forest_boosting.ipynb` - tree ensemble demo
- `notebooks/03_split_criteria_id3_cart.ipynb` - split criteria from scratch
- `notebooks/04_hoeffding_tree_stream_demo.ipynb` - streaming tree split decisions
- `scripts/build_report.py` - rebuilds `index.html` from the source report
- `requirements.txt` - Python dependencies for notebooks and report generation

## Rebuilding Generated Artifacts

From a fresh checkout:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build_report.py
```

To run the notebooks:

```sh
jupyter lab notebooks
```

The notebooks use synthetic datasets so they can run without downloading data.

## Citation

If you use this work, please cite it as:

Tunguz, B. (2026). *State of Decision Tree Algorithms: June 2026*. GitHub.
https://github.com/tabulai/DecisionTrees

BibTeX:

```bibtex
@misc{tunguz2026decisiontrees,
  author = {Tunguz, Bojan},
  title = {State of Decision Tree Algorithms: June 2026},
  year = {2026},
  howpublished = {\url{https://github.com/tabulai/DecisionTrees}},
  note = {Literature review and demo notebooks}
}
```

## License

This repository is licensed under the Creative Commons Attribution 4.0
International License (CC BY 4.0).

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
