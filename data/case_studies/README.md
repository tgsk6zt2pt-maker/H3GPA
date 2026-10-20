# Case-study candidate tables

These CSV files reproduce the two Top-12 candidate tables in the current
manuscript. They are reported ranking outputs, not model input data or a
standalone dataset for evaluating predictive performance.

| File | Species | Trait ID | Trait name |
| --- | --- | --- | --- |
| maize_TO0000316_top12.csv | Maize | TO:0000316 | Photosynthetic capacity |
| rice_TO0000456_top12.csv | Rice | TO:0000456 | Spikelet number |

## Columns

- `rank`: position in the reported candidate list, from 1 to 12.
- `gene_id`: gene identifier as reported in the manuscript.
- `go_context_reported`: `yes` corresponds to the manuscript check mark;
  `not_identified` corresponds to the question mark. These are reported annotation
  context labels, not independently validated positive or negative associations.
- `go_annotation`: GO identifiers from the manuscript table; multiple terms are
  separated by semicolons. An empty field indicates that no terms were reported.

Known associations were excluded from the reported rankings, as described in the
manuscript. Prediction scores, complete ranking matrices, sequences, expression
profiles, and training labels are not included. The files were checked against
the manuscript tables; no new predictions or GO annotation lookups were run.

GO-derived features are also part of the model inputs, so these annotations must
not be interpreted as independent biological validation. Missing annotation
context is not confirmation that a candidate association is absent.
