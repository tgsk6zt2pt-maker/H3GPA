"""Read reported candidate lists without generating new predictions."""

import csv
from pathlib import Path


def load_candidates(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        required = {'rank', 'gene_id', 'go_context_reported', 'go_annotation'}
        if set(reader.fieldnames or []) != required:
            raise ValueError('Unexpected case-table columns')
        rows = list(reader)
    genes = set()
    for expected, row in enumerate(rows, 1):
        if int(row['rank']) != expected:
            raise ValueError('Ranks must be consecutive and start at one')
        if not row['gene_id'] or row['gene_id'] in genes:
            raise ValueError('Gene identifiers must be nonempty and unique')
        if row['go_context_reported'] not in {'yes', 'not_identified'}:
            raise ValueError('Unexpected annotation-context label')
        genes.add(row['gene_id'])
    return rows


def summarize_candidates(rows):
    return {
        'candidate_count': len(rows),
        'with_reported_go_context': sum(row['go_context_reported'] == 'yes' for row in rows),
        'without_reported_go_context': sum(row['go_context_reported'] == 'not_identified' for row in rows),
    }
