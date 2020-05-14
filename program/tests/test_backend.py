from program.backend import file_reader, file_upload


def test_file_reader():
    """Test file reader."""
    # Given
    a = "data.csv"

    # When
    res1 = file_reader(a)
    res2 = file_reader(a)

    # Then
    assert type(res1) == list
    assert type(res2) != int


def test_file_upload():
    """Test file upload."""
    # Given
    a = "data.csv"
    b = "data.img"

    # When
    res1 = file_upload(a)
    res2 = file_upload(a)
    res3 = file_upload(b)

    # Then
    assert type(res1) == str
    assert res2 == "File uploaded succesfully!"
    assert res3 == "File is not in the correct format"
