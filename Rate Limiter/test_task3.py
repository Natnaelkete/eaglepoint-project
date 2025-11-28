"""
Test suite for Task 3: Rate Limiter
"""

import unittest
import time
from task3_rate_limiter import RateLimiter


class TestRateLimiter(unittest.TestCase):
    """Test cases for the rate limiter."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.limiter = RateLimiter(max_requests=5, window_seconds=60)
    
    def test_basic_allowed(self):
        """Test that requests are allowed within limit."""
        user_id = "user1"
        
        for i in range(5):
            allowed, info = self.limiter.is_allowed(user_id)
            self.assertTrue(allowed, f"Request {i+1} should be allowed")
            self.assertEqual(info["current_requests"], i + 1)
    
    def test_rate_limit_exceeded(self):
        """Test that requests are blocked when limit exceeded."""
        user_id = "user2"
        
        # Make 5 allowed requests
        for _ in range(5):
            allowed, _ = self.limiter.is_allowed(user_id)
            self.assertTrue(allowed)
        
        # 6th request should be blocked
        allowed, info = self.limiter.is_allowed(user_id)
        self.assertFalse(allowed)
        self.assertEqual(info["current_requests"], 5)
        self.assertIn("Rate limit exceeded", info["message"])
    
    def test_multiple_users(self):
        """Test that rate limiting works per user."""
        user1 = "alice"
        user2 = "bob"
        
        # Both users should be able to make 5 requests
        for _ in range(5):
            allowed1, _ = self.limiter.is_allowed(user1)
            allowed2, _ = self.limiter.is_allowed(user2)
            self.assertTrue(allowed1)
            self.assertTrue(allowed2)
        
        # Both should be blocked on 6th request
        allowed1, _ = self.limiter.is_allowed(user1)
        allowed2, _ = self.limiter.is_allowed(user2)
        self.assertFalse(allowed1)
        self.assertFalse(allowed2)
    
    def test_time_window_reset(self):
        """Test that rate limit resets after time window."""
        user_id = "user3"
        current_time = time.time()
        
        # Make 5 requests
        for _ in range(5):
            allowed, _ = self.limiter.is_allowed(user_id, current_time)
            self.assertTrue(allowed)
        
        # 6th request should be blocked
        allowed, _ = self.limiter.is_allowed(user_id, current_time)
        self.assertFalse(allowed)
        
        # After window expires, should be allowed again
        future_time = current_time + 61  # 61 seconds later
        allowed, info = self.limiter.is_allowed(user_id, future_time)
        self.assertTrue(allowed)
        self.assertEqual(info["current_requests"], 1)
    
    def test_get_status(self):
        """Test get_status method."""
        user_id = "user4"
        
        # Make 3 requests
        for _ in range(3):
            self.limiter.is_allowed(user_id)
        
        status = self.limiter.get_status(user_id)
        self.assertEqual(status["current_requests"], 3)
        self.assertEqual(status["remaining_requests"], 2)
        self.assertTrue(status["is_allowed"])
    
    def test_reset_user(self):
        """Test reset_user method."""
        user_id = "user5"
        
        # Make 5 requests
        for _ in range(5):
            self.limiter.is_allowed(user_id)
        
        # Should be blocked
        allowed, _ = self.limiter.is_allowed(user_id)
        self.assertFalse(allowed)
        
        # Reset user
        self.limiter.reset_user(user_id)
        
        # Should be allowed again
        allowed, info = self.limiter.is_allowed(user_id)
        self.assertTrue(allowed)
        self.assertEqual(info["current_requests"], 1)
    
    def test_reset_all(self):
        """Test reset_all method."""
        user1 = "user6"
        user2 = "user7"
        
        # Make requests for both users
        for _ in range(5):
            self.limiter.is_allowed(user1)
            self.limiter.is_allowed(user2)
        
        # Reset all
        self.limiter.reset_all()
        
        # Both should be allowed again
        allowed1, _ = self.limiter.is_allowed(user1)
        allowed2, _ = self.limiter.is_allowed(user2)
        self.assertTrue(allowed1)
        self.assertTrue(allowed2)
    
    def test_custom_limits(self):
        """Test with custom rate limits."""
        custom_limiter = RateLimiter(max_requests=3, window_seconds=30)
        user_id = "user8"
        
        # Should allow 3 requests
        for i in range(3):
            allowed, _ = custom_limiter.is_allowed(user_id)
            self.assertTrue(allowed)
        
        # 4th should be blocked
        allowed, _ = custom_limiter.is_allowed(user_id)
        self.assertFalse(allowed)
    
    def test_invalid_initialization(self):
        """Test that invalid initialization raises errors."""
        with self.assertRaises(ValueError):
            RateLimiter(max_requests=0)
        
        with self.assertRaises(ValueError):
            RateLimiter(window_seconds=0)
        
        with self.assertRaises(ValueError):
            RateLimiter(max_requests=-1)


if __name__ == "__main__":
    unittest.main()

