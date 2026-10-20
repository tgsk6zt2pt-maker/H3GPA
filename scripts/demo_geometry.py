"""CPU-only illustration with synthetic vectors."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

import torch

from h3gpa.hyperbolic_ops import (
    expmap0,
    logmap0,
    mobius_add,
    poincare_distance,
    squash_tangent,
)


def main():
    curvature = 0.1
    attributes = torch.tensor([[0.1, 0.2, -0.1]], dtype=torch.float64)
    context = torch.tensor([[0.05, -0.1, 0.15]], dtype=torch.float64)
    tangent = squash_tangent(attributes)
    point = expmap0(tangent, curvature)
    other = expmap0(squash_tangent(context), curvature)
    recovered = logmap0(point, curvature)
    fused = mobius_add(point, other, curvature)
    assert torch.allclose(recovered, tangent, atol=1e-8)
    assert torch.all(curvature * fused.square().sum(dim=-1) < 1)
    assert torch.allclose(
        poincare_distance(point, other, curvature),
        poincare_distance(other, point, curvature),
        atol=1e-8,
    )
    zero = torch.zeros_like(point)
    assert torch.allclose(logmap0(expmap0(zero, curvature), curvature), zero)
    assert torch.allclose(mobius_add(point, zero, curvature), point, atol=1e-8)
    assert torch.allclose(poincare_distance(point, point, curvature), torch.zeros(1, dtype=point.dtype), atol=1e-8)
    print("Mapping round trip, ball boundary, distance and identity checks passed.")
    print("Synthetic example distance:", poincare_distance(point, other, curvature).item())


if __name__ == "__main__":
    main()
