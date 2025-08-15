import unittest
import math
from src.f0z_algebra.stabilizer import PyZeroMath

class TestF0ZAlgebra(unittest.TestCase):
    """
    Unit tests for the core F0Z-Algebra components.
    This suite validates the behavior of the stabilization functions.
    """

    @classmethod
    def setUpClass(cls):
        """Set up a single instance of the math module for all tests."""
        print("\n--- Starting F0Z-Algebra Test Suite ---")
        cls.math = PyZeroMath()
        cls.epsilon = 1e-8

    def test_stabilize_positive_large_number(self):
        """Tests that a large positive number remains unchanged."""
        self.assertEqual(self.math.f0z_stabilize(100.0, self.epsilon), 100.0)

    def test_stabilize_negative_large_number(self):
        """Tests that a large negative number remains unchanged."""
        self.assertEqual(self.math.f0z_stabilize(-100.0, self.epsilon), -100.0)

    def test_stabilize_positive_small_number(self):
        """
        CRITICAL TEST: Tests that a small positive number is stabilized to +epsilon.
        This prevents underflow and division by a near-zero positive number.
        """
        self.assertEqual(self.math.f0z_stabilize(1e-10, self.epsilon), self.epsilon)

    def test_stabilize_negative_small_number(self):
        """
        CRITICAL TEST: Tests that a small negative number is stabilized to -epsilon.
        This prevents underflow and division by a near-zero negative number.
        """
        self.assertEqual(self.math.f0z_stabilize(-1e-10, self.epsilon), -self.epsilon)

    def test_stabilize_exact_zero(self):
        """
        CRITICAL TEST: Tests that an exact zero is stabilized to +epsilon.
        This is the core of preventing division-by-zero errors.
        """
        self.assertEqual(self.math.f0z_stabilize(0.0, self.epsilon), self.epsilon)

    def test_stabilize_at_epsilon_boundary(self):
        """Tests that a number exactly at the epsilon boundary is not changed."""
        self.assertEqual(self.math.f0z_stabilize(self.epsilon, self.epsilon), self.epsilon)
        self.assertEqual(self.math.f0z_stabilize(-self.epsilon, self.epsilon), -self.epsilon)
    
    def test_f0z_optimizer_decision_below_threshold(self):
        """Tests that the optimizer correctly decides to proceed when cost is low."""
        from src.f0z_algebra.stabilizer import F0ZOptimizer
        optimizer = F0ZOptimizer(self.math)
        self.assertTrue(optimizer.decide(cost=0.1, threshold=0.3))

    def test_f0z_optimizer_decision_above_threshold(self):
        """Tests that the optimizer correctly decides to reject when cost is high."""
        from src.f0z_algebra.stabilizer import F0ZOptimizer
        optimizer = F0ZOptimizer(self.math)
        self.assertFalse(optimizer.decide(cost=0.5, threshold=0.3))

    def test_f0z_optimizer_decision_near_zero_cost(self):
        """
        CRITICAL TEST: Tests that the optimizer can make a decision even with a
        classically problematic near-zero cost, thanks to stabilization.
        """
        from src.f0z_algebra.stabilizer import F0ZOptimizer
        optimizer = F0ZOptimizer(self.math)
        # Without stabilization, this could be a floating point issue.
        # With F0Z, it's a clear decision.
        self.assertTrue(optimizer.decide(cost=1e-12, threshold=0.3))


if __name__ == '__main__':
    unittest.main()
