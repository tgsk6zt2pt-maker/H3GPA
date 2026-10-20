"""Selected direct and three-hop path operations from the local implementation."""

from __future__ import annotations

import numpy as np
from scipy import sparse


def _binary_sparse(value: np.ndarray) -> sparse.csr_matrix:
    """把任意正值关系矩阵转换为二值稀疏矩阵，供路径乘法使用。"""
    return sparse.csr_matrix((value > 0).astype(np.float32))


def _third_order_bipartite(value: np.ndarray) -> np.ndarray:
    """在二部关系中计算严格三跳邻居，并返回 0/1 关系矩阵。

    ``A A.T A`` 会同时包含经原路返回得到的直接边，因此最后排除原始一阶边，
    只保留与直接关系不重叠的三阶补充结构。
    """
    relation = _binary_sparse(value)
    three_hop = (relation @ (relation.T @ relation)).toarray() > 0
    return np.logical_and(three_hop, relation.toarray() == 0).astype(np.float32)


def construct_x1e_x3e(train_r14: np.ndarray, gene_mirna: np.ndarray, mirna_to_train: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict[str, np.ndarray]]:
    """由 Gene--miRNA 和 miRNA--TO 构造一阶与三阶 Gene--TO 证据。

    X1E = (R12_1 @ R24_1) elementwise R14_train
    X3E = (R12_3 @ R24_3) elementwise R14_train
    """
    r12_1, r24_1 = _binary_sparse(gene_mirna), _binary_sparse(mirna_to_train)
    r12_3 = _third_order_bipartite(gene_mirna)
    r24_3 = _third_order_bipartite(mirna_to_train)
    x1e = (((r12_1 @ r24_1).toarray() > 0).astype(np.float32) * train_r14.astype(np.float32))
    x3e = (((_binary_sparse(r12_3) @ _binary_sparse(r24_3)).toarray() > 0).astype(np.float32) * train_r14.astype(np.float32))
    # 三阶路径仍可能落到已有的一阶 Gene--TO 边，因此去除重叠位置以保留补充证据。
    x3e[x1e > 0] = 0.0
    return x1e, x3e, {"R12_3": r12_3, "R24_3": r24_3}
