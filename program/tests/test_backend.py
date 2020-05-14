from backend import file_reader


def test_file_reader():
    # Given
    a = "data.csv"
    b = "random.csv"
    c = "rolig.csv"
    d = "data.img"

    # When
    res1 = backend.file_reader(a)
    res2 = backend.file_reader(b)
    res3 = backend.file_reader(c)
    res4 = backend.file_reader(d)

    # Then
    assert res1 == list
    assert res2 != list
    assert res3 != list
    assert res4 != list
