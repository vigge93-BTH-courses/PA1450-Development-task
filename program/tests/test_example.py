from program.example import add, multiply


def test_add():
    # Given
    a = 2
    b = 3
    c = 0
    d = -2

    # When
    res1 = add(a, b)
    res2 = add(a, c)
    res3 = add(a, d)
    res4 = add(b, d)
    res5 = add(d, b)

    # Then
    assert res1 == 5
    assert res2 == 2
    assert res3 == 0
    assert res4 == 1
    assert res4 == res5


def test_multiply():
    # Given
    a = 1
    b = 4
    c = 2
    d = 0

    # When
    res1 = multiply(a, b)
    res2 = multiply(b, c)
    res3 = multiply(b, d)
    res4 = multiply(c, b)

    # Then
    assert res1 == b
    assert res2 == 8
    assert res3 == 0
    assert res4 == res2
