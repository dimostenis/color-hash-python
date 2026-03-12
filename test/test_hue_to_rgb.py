"""
Unit tests for hue_to_rgb.

The function is piecewise linear over [0, 1]:
  branch 1  t in [0,   1/6):  p + (q-p) * 6t
  branch 2  t in [1/6, 1/2):  q
  branch 3  t in [1/2, 2/3):  p + (q-p) * (2/3 - t) * 6
  branch 4  t in [2/3, 1  ]:  p

Values of t outside [0, 1] are normalized by adding or subtracting 1
before the piecewise evaluation.

We use p=0, q=1 in most cases so that the expected output equals the
"blend factor" directly (0 to 1), making arithmetic easier to follow.
"""

from __future__ import annotations

import pytest

from colorhash.colorhash import hue_to_rgb

P = 0.0
Q = 1.0


class TestBranch1:
    """t in [0, 1/6)  →  p + (q-p) * 6 * t"""

    def test_t_zero(self):
        # 6 * 0 = 0
        assert hue_to_rgb(P, Q, 0.0) == pytest.approx(0.0)

    def test_t_midpoint(self):
        # t = 1/12  →  6 * (1/12) = 0.5
        assert hue_to_rgb(P, Q, 1 / 12) == pytest.approx(0.5)

    def test_t_just_below_one_sixth(self):
        # t approaching 1/6 from the left  →  6*(1/6 - ε) ≈ 1
        eps = 1e-9
        assert hue_to_rgb(P, Q, 1 / 6 - eps) == pytest.approx(1.0, abs=1e-6)

    def test_arbitrary_pq(self):
        # p=0.2, q=0.8, t=1/12  →  0.2 + 0.6*0.5 = 0.5
        assert hue_to_rgb(0.2, 0.8, 1 / 12) == pytest.approx(0.5)


class TestBranch2:
    """t in [1/6, 1/2)  →  q"""

    def test_t_one_sixth(self):
        assert hue_to_rgb(P, Q, 1 / 6) == pytest.approx(Q)

    def test_t_one_third(self):
        assert hue_to_rgb(P, Q, 1 / 3) == pytest.approx(Q)

    def test_t_just_below_one_half(self):
        eps = 1e-9
        assert hue_to_rgb(P, Q, 1 / 2 - eps) == pytest.approx(Q)

    def test_arbitrary_pq(self):
        assert hue_to_rgb(0.1, 0.7, 1 / 3) == pytest.approx(0.7)


class TestBranch3:
    """t in [1/2, 2/3)  →  p + (q-p) * (2/3 - t) * 6"""

    def test_t_one_half(self):
        # (2/3 - 1/2) * 6 = (1/6) * 6 = 1  →  q
        assert hue_to_rgb(P, Q, 1 / 2) == pytest.approx(1.0)

    def test_t_midpoint(self):
        # t = 7/12  →  (2/3 - 7/12) * 6 = (1/12) * 6 = 0.5
        assert hue_to_rgb(P, Q, 7 / 12) == pytest.approx(0.5)

    def test_t_just_below_two_thirds(self):
        eps = 1e-9
        assert hue_to_rgb(P, Q, 2 / 3 - eps) == pytest.approx(0.0, abs=1e-6)

    def test_arbitrary_pq(self):
        # p=0.2, q=0.8  →  0.2 + 0.6*(2/3-7/12)*6 = 0.2 + 0.6*0.5 = 0.5
        assert hue_to_rgb(0.2, 0.8, 7 / 12) == pytest.approx(0.5)


class TestBranch4:
    """t in [2/3, 1]  →  p"""

    def test_t_two_thirds(self):
        assert hue_to_rgb(P, Q, 2 / 3) == pytest.approx(P)

    def test_t_five_sixths(self):
        assert hue_to_rgb(P, Q, 5 / 6) == pytest.approx(P)

    def test_t_one(self):
        # t=1.0 is NOT > 1, so no adjustment; falls through to branch 4
        assert hue_to_rgb(P, Q, 1.0) == pytest.approx(P)

    def test_arbitrary_pq(self):
        assert hue_to_rgb(0.3, 0.9, 5 / 6) == pytest.approx(0.3)


class TestNormalization:
    """t outside [0, 1] is shifted by ±1 before evaluation."""

    def test_negative_t_shifted_up(self):
        # t = -1/12  →  normalized to 11/12  →  branch 4  →  p
        assert hue_to_rgb(P, Q, -1 / 12) == pytest.approx(hue_to_rgb(P, Q, 11 / 12))

    def test_negative_t_lands_in_branch1(self):
        # t = -11/12  →  normalized to 1/12  →  branch 1:  6*(1/12) = 0.5
        assert hue_to_rgb(P, Q, -11 / 12) == pytest.approx(0.5)

    def test_t_just_above_one_shifted_down(self):
        # t = 13/12  →  normalized to 1/12  →  branch 1:  6*(1/12) = 0.5
        assert hue_to_rgb(P, Q, 13 / 12) == pytest.approx(hue_to_rgb(P, Q, 1 / 12))

    def test_t_just_above_one_lands_in_branch2(self):
        # t = 1 + 1/3  →  normalized to 1/3  →  branch 2  →  q
        assert hue_to_rgb(P, Q, 1 + 1 / 3) == pytest.approx(Q)

    def test_normalized_result_matches_in_range_result(self):
        # Round-trip: applying normalization must give the same result as
        # calling with the already-in-range value.
        for t_in_range in [
            0.0,
            1 / 12,
            1 / 6,
            1 / 4,
            1 / 3,
            1 / 2,
            7 / 12,
            2 / 3,
            3 / 4,
            5 / 6,
        ]:
            assert hue_to_rgb(P, Q, t_in_range - 1) == pytest.approx(
                hue_to_rgb(P, Q, t_in_range),
                abs=1e-9,
            ), f"Failed for t={t_in_range}"
            assert hue_to_rgb(P, Q, t_in_range + 1) == pytest.approx(
                hue_to_rgb(P, Q, t_in_range),
                abs=1e-9,
            ), f"Failed for t={t_in_range}"


class TestPEqualsQ:
    """When p == q (zero saturation), all branches must return p."""

    @pytest.mark.parametrize(
        "t",
        [0.0, 1 / 12, 1 / 6, 1 / 3, 1 / 2, 7 / 12, 2 / 3, 5 / 6, 1.0, -1 / 12, 13 / 12],
    )
    def test_returns_p_for_any_t(self, t: float):
        val = 0.6
        assert hue_to_rgb(val, val, t) == pytest.approx(val)


class TestContinuity:
    """The function should be continuous at each branch boundary."""

    @pytest.mark.parametrize(
        "boundary",
        [1 / 6, 1 / 2, 2 / 3],
    )
    def test_continuous_at_boundary(self, boundary: float):
        eps = 1e-7
        left = hue_to_rgb(P, Q, boundary - eps)
        right = hue_to_rgb(P, Q, boundary)
        assert left == pytest.approx(right, abs=1e-5)
