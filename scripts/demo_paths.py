"""Illustrate direct and complementary three-hop paths on synthetic matrices."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from h3gpa.path_patterns import _third_order_bipartite, construct_x1e_x3e


def main():
    relation = np.array([[1, 0, 0], [1, 1, 0], [0, 1, 1]], dtype=np.float32)
    indirect = _third_order_bipartite(relation)
    assert indirect[0, 1] == 1
    assert np.all(indirect[relation > 0] == 0)
    target = np.ones((3, 3), dtype=np.float32)
    direct, third, _ = construct_x1e_x3e(target, relation, relation)
    assert direct.shape == third.shape == target.shape
    assert np.all(third[direct > 0] == 0)
    hidden_target = target.copy()
    hidden_target[0, 0] = 0
    masked_direct, masked_third, _ = construct_x1e_x3e(hidden_target, relation, relation)
    assert masked_direct[0, 0] == masked_third[0, 0] == 0
    print('Synthetic path, overlap and target-mask checks passed.')
    print('Direct path pattern:')
    print(direct)
    print('Complementary three-hop path pattern:')
    print(third)


if __name__ == '__main__':
    main()
