"""Inspect reported candidate tables using species-specific case settings."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from h3gpa.case_data import load_candidates, summarize_candidates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--species', choices=['maize', 'rice'], required=True)
    args = parser.parse_args()
    config = json.loads((ROOT / 'configs' / (args.species + '.json')).read_text(encoding='utf-8'))
    rows = load_candidates(ROOT / config['case_table'])
    if len(rows) != config['top_k']:
        raise ValueError('Case size differs from the case configuration')
    print(json.dumps({
        'species': config['species'], 'trait_id': config['trait_id'],
        **summarize_candidates(rows),
    }, indent=2))
    for row in rows:
        print(row['rank'], row['gene_id'], row['go_annotation'] or '-')


if __name__ == '__main__':
    main()
