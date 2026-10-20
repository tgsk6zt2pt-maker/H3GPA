# H3GPA

This repository accompanies the manuscript:

**H3GPA: Plant Genome-Phenome Association Prediction Using Hyperbolic Multiview Representation and Higher-Order Heterogeneous Relation Learning**

## Current release

This pre-acceptance release contains selected method components and the candidate
lists reported in the two manuscript case studies. Further code and data will
be added upon acceptance.

## Contents

```text
H3GPA/
|-- README.md
|-- requirements.txt
|-- configs/
|   |-- maize.json
|   `-- rice.json
|-- src/h3gpa/
|   |-- __init__.py
|   |-- hyperbolic_ops.py
|   |-- path_patterns.py
|   `-- case_data.py
|-- scripts/
|   |-- demo_geometry.py
|   |-- demo_paths.py
|   `-- inspect_cases.py
`-- data/case_studies/
    |-- README.md
    |-- maize_TO0000316_top12.csv
    `-- rice_TO0000456_top12.csv
```

The case-study files contain 12 ranked candidates each:

- Maize: TO:0000316, photosynthetic capacity.
- Rice: TO:0000456, spikelet number.

GO annotations provide functional context only. They are not experimental
confirmation of the predicted associations or an independent validation dataset;
GO-derived features are also used by the model. No prediction scores or new
annotations have been generated for this release.

## Selected code and examples

The released components cover Poincare-ball operations, direct and complementary
three-hop path processing, and candidate-table loading and summaries. The
geometry and path functions are extracted from the local implementation;
candidate-table utilities and demonstration scripts are release helpers.

The `configs` files contain selected settings for inspecting the maize and rice
cases and the geometry illustration. The scripts demonstrate these components;
they do not run the full paper experiments.

Use Python 3.9 or later with PyTorch installed. This example uses only small
synthetic vectors on the CPU, not biological training data.

```bash
pip install -r requirements.txt
python scripts/demo_geometry.py
python scripts/demo_paths.py
python scripts/inspect_cases.py --species maize
python scripts/inspect_cases.py --species rice
```

The path example verifies indirect links, overlap removal and target masking
using small synthetic matrices. The case-inspection script reads the reported
candidate lists without generating new model predictions.

## Data and code availability

The case-study candidate tables and selected method components are included
at this stage. The full implementation, experimental configurations, reproduction
instructions, and processed data that can be redistributed will be released upon
acceptance of the manuscript. Source links and preprocessing instructions will
be provided for data that cannot be redistributed.

## Repository

https://github.com/tgsk6zt2pt-maker/H3GPA
