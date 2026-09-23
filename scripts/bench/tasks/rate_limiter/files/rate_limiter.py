class RateLimiter:
    """Sliding-window rate limiter: at most max_requests per window_seconds."""

    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []

    def allow(self, now):
        """Call with the current timestamp (seconds). Returns True if the
        request is allowed, False if the caller is over the limit."""
        self.requests = [t for t in self.requests if now - t > self.window_seconds]
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
