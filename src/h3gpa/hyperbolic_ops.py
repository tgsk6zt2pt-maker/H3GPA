"""Selected Poincare-ball geometry operations.

Function bodies extracted unchanged from the local hyperbolic-operations module.
Only these seven functions are included; no training or model modules are released.
"""

import math

import torch


def artanh(value: torch.Tensor) -> torch.Tensor:
    """数值稳定的反双曲正切函数，供指数映射、对数映射和距离计算调用。"""
    value = value.clamp(-1.0 + 1e-7, 1.0 - 1e-7)
    return 0.5 * (torch.log1p(value) - torch.log1p(-value))


def project_ball(value: torch.Tensor, curvature: float) -> torch.Tensor:
    """把越界点投影回曲率为 ``curvature`` 的庞加莱球内部。"""
    maximum = (1.0 - 1e-5) / math.sqrt(curvature)
    norm = torch.linalg.vector_norm(value, dim=-1, keepdim=True).clamp_min(1e-8)
    return value * torch.clamp(maximum / norm, max=1.0)


def squash_tangent(value: torch.Tensor, radius: float = 1.0) -> torch.Tensor:
    """平滑限制切空间向量范数，防止高维输入映射到球边界附近。"""
    if radius <= 0:
        raise ValueError("radius must be positive")
    norm = torch.linalg.vector_norm(value, dim=-1, keepdim=True)
    return value * (radius / (radius + norm)).to(dtype=value.dtype)


def expmap0(value: torch.Tensor, curvature: float) -> torch.Tensor:
    """原点指数映射：把欧氏切空间向量映射为庞加莱球中的点。"""
    root = math.sqrt(curvature)
    norm = torch.linalg.vector_norm(value, dim=-1, keepdim=True).clamp_min(1e-8)
    mapped = torch.tanh(root * norm) * value / (root * norm)
    return project_ball(mapped, curvature)


def logmap0(value: torch.Tensor, curvature: float) -> torch.Tensor:
    """原点对数映射：把庞加莱球中的点映回欧氏切空间进行线性运算。"""
    root = math.sqrt(curvature)
    value = project_ball(value, curvature)
    norm = torch.linalg.vector_norm(value, dim=-1, keepdim=True).clamp_min(1e-8)
    return artanh(root * norm) * value / (root * norm)


def mobius_add(left: torch.Tensor, right: torch.Tensor, curvature: float) -> torch.Tensor:
    """Möbius 加法：在庞加莱球内融合两个双曲表示。"""
    left_sq = torch.sum(left * left, dim=-1, keepdim=True)
    right_sq = torch.sum(right * right, dim=-1, keepdim=True)
    inner = torch.sum(left * right, dim=-1, keepdim=True)
    numerator = (1.0 + 2.0 * curvature * inner + curvature * right_sq) * left
    numerator = numerator + (1.0 - curvature * left_sq) * right
    denominator = 1.0 + 2.0 * curvature * inner + curvature * curvature * left_sq * right_sq
    return project_ball(numerator / denominator.clamp_min(1e-8), curvature)


def poincare_distance(left: torch.Tensor, right: torch.Tensor, curvature: float) -> torch.Tensor:
    """计算两个庞加莱球点之间的双曲距离。"""
    delta = mobius_add(-left, right, curvature)
    norm = torch.linalg.vector_norm(delta, dim=-1).clamp_max((1.0 - 1e-7) / math.sqrt(curvature))
    return 2.0 * artanh(math.sqrt(curvature) * norm) / math.sqrt(curvature)
