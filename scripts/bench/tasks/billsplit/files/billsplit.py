def split_bill(amount_cents, n_people):
    """Split a bill total (in cents) evenly across n_people.

    Returns a list of n_people integers (cents each person owes).
    """
    if n_people <= 0:
        raise ValueError("n_people must be positive")
    share = amount_cents // n_people
    return [share for _ in range(n_people)]
