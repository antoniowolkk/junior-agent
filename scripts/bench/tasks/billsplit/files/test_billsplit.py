from billsplit import split_bill


def test_even_split():
    assert split_bill(1000, 4) == [250, 250, 250, 250]


def test_two_way():
    assert split_bill(2000, 2) == [1000, 1000]


if __name__ == "__main__":
    test_even_split()
    test_two_way()
    print("all tests passed")
