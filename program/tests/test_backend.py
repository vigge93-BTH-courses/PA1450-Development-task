from program.backend import file_reader, process_file, get_attributes


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
    res1 = process_file(a)
    res2 = process_file(a)
    res3 = process_file(b)

    # Then
    assert type(res1) == str
    assert res2 == "File uploaded succesfully!"
    assert res3 == "File is not in the correct format"


def test_get_attributes():
    """Test get attributes."""
    # When
    res1 = get_attributes()

    # Then
    assert type(res1) == list
