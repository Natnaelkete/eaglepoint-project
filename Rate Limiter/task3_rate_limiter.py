import time
from collections import defaultdict, deque
from threading import Lock
from typing import Dict, Tuple, Optional


class RateLimiter:
    """
    A rate limiter that tracks requests per user within a time window.
    
    Features:
    - Configurable request limit and time window
    - Per-user tracking
    - Automatic cleanup of expired entries
    - Thread-safe operations
    
    Example:
        >>> limiter = RateLimiter(max_requests=5, window_seconds=60)
        >>> if limiter.is_allowed("user123"):
        ...     # Process request
        ...     pass
        ... else:
        ...     # Rate limit exceeded
        ...     pass
    """
    
    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        """
        Initialize the rate limiter.
        
        Args:
            max_requests (int): Maximum number of requests allowed per window
            window_seconds (int): Time window in seconds
        """
        if max_requests <= 0:
            raise ValueError("max_requests must be positive")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
        
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        
        # Store request timestamps per user: {user_id: deque([timestamp1, timestamp2, ...])}
        self._requests: Dict[str, deque] = defaultdict(lambda: deque())
        
        # Lock for thread safety
        self._lock = Lock()
    
    def is_allowed(self, user_id: str, current_time: Optional[float] = None) -> Tuple[bool, Dict[str, any]]:
        """
        Check if a request is allowed for the given user.
        
        Args:
            user_id (str): The user identifier
            current_time (float, optional): Current timestamp (for testing). 
                                          If None, uses time.time()
        
        Returns:
            tuple: (is_allowed: bool, info: dict)
                - is_allowed: True if request is allowed, False if rate limited
                - info: Dictionary with details about the rate limit status
        """
        if current_time is None:
            current_time = time.time()
        
        with self._lock:
            # Get or create deque for this user
            user_requests = self._requests[user_id]
            
            # Remove expired timestamps (older than window_seconds)
            cutoff_time = current_time - self.window_seconds
            while user_requests and user_requests[0] < cutoff_time:
                user_requests.popleft()
            
            # Check if limit exceeded
            request_count = len(user_requests)
            
            if request_count >= self.max_requests:
                # Rate limit exceeded
                oldest_request = user_requests[0]
                time_until_reset = self.window_seconds - (current_time - oldest_request)
                
                return False, {
                    "allowed": False,
                    "user_id": user_id,
                    "current_requests": request_count,
                    "max_requests": self.max_requests,
                    "window_seconds": self.window_seconds,
                    "time_until_reset": round(time_until_reset, 2),
                    "message": f"Rate limit exceeded. Try again in {time_until_reset:.1f} seconds."
                }
            else:
                # Allow request - add current timestamp
                user_requests.append(current_time)
                
                return True, {
                    "allowed": True,
                    "user_id": user_id,
                    "current_requests": request_count + 1,
                    "max_requests": self.max_requests,
                    "window_seconds": self.window_seconds,
                    "remaining_requests": self.max_requests - (request_count + 1),
                    "message": "Request allowed"
                }
    
    def get_status(self, user_id: str, current_time: Optional[float] = None) -> Dict[str, any]:
        """
        Get current rate limit status for a user without making a request.
        
        Args:
            user_id (str): The user identifier
            current_time (float, optional): Current timestamp (for testing)
        
        Returns:
            dict: Status information about the user's rate limit
        """
        if current_time is None:
            current_time = time.time()
        
        with self._lock:
            user_requests = self._requests[user_id]
            
            # Remove expired timestamps
            cutoff_time = current_time - self.window_seconds
            while user_requests and user_requests[0] < cutoff_time:
                user_requests.popleft()
            
            request_count = len(user_requests)
            
            if user_requests:
                oldest_request = user_requests[0]
                time_until_reset = max(0, self.window_seconds - (current_time - oldest_request))
            else:
                time_until_reset = 0
            
            return {
                "user_id": user_id,
                "current_requests": request_count,
                "max_requests": self.max_requests,
                "window_seconds": self.window_seconds,
                "remaining_requests": self.max_requests - request_count,
                "time_until_reset": round(time_until_reset, 2),
                "is_allowed": request_count < self.max_requests
            }
    
    def reset_user(self, user_id: str):
        """
        Reset rate limit for a specific user (clear their request history).
        
        Args:
            user_id (str): The user identifier to reset
        """
        with self._lock:
            if user_id in self._requests:
                del self._requests[user_id]
    
    def reset_all(self):
        """Reset rate limit for all users."""
        with self._lock:
            self._requests.clear()


def main():
    """Example usage of the rate limiter."""
    print("=" * 60)
    print("Rate Limiter - Example")
    print("=" * 60)
    
    # Create rate limiter: 5 requests per 60 seconds
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    
    user_id = "user123"
    
    print(f"\nTesting rate limiter for user: {user_id}")
    print(f"Limit: {limiter.max_requests} requests per {limiter.window_seconds} seconds\n")
    
    # Simulate multiple requests
    print("Simulating 7 requests:")
    print("-" * 60)
    
    for i in range(7):
        allowed, info = limiter.is_allowed(user_id)
        
        status = "[ALLOWED]" if allowed else "[BLOCKED]"
        print(f"Request {i+1}: {status}")
        print(f"  Current requests: {info['current_requests']}/{info['max_requests']}")
        
        if allowed:
            print(f"  Remaining: {info['remaining_requests']}")
        else:
            print(f"  Time until reset: {info['time_until_reset']:.1f}s")
        
        print()
    
    # Show status
    print("-" * 60)
    print("Current status:")
    status = limiter.get_status(user_id)
    print(f"  User: {status['user_id']}")
    print(f"  Requests: {status['current_requests']}/{status['max_requests']}")
    print(f"  Remaining: {status['remaining_requests']}")
    print(f"  Allowed: {status['is_allowed']}")
    
    # Test with multiple users
    print("\n" + "=" * 60)
    print("Testing with multiple users:")
    print("=" * 60)
    
    users = ["alice", "bob", "charlie"]
    
    for user in users:
        print(f"\nUser: {user}")
        for i in range(3):
            allowed, info = limiter.is_allowed(user)
            print(f"  Request {i+1}: {'[OK]' if allowed else '[BLOCKED]'} "
                  f"({info['current_requests']}/{info['max_requests']})")
    
    # Show status for all users
    print("\n" + "-" * 60)
    print("Status for all users:")
    for user in users:
        status = limiter.get_status(user)
        print(f"  {user}: {status['current_requests']}/{status['max_requests']} "
              f"(remaining: {status['remaining_requests']})")


if __name__ == "__main__":
    main()

