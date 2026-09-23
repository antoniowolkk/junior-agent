from rate_limiter import RateLimiter


def test_allows_within_limit():
    rl = RateLimiter(max_requests=3, window_seconds=60)
    assert rl.allow(0) is True
    assert rl.allow(0) is True
    assert rl.allow(0) is True


def test_new_limiter_is_empty():
    rl = RateLimiter(max_requests=5, window_seconds=60)
    assert rl.requests == []


if __name__ == "__main__":
    test_allows_within_limit()
    test_new_limiter_is_empty()
    print("all tests passed")
