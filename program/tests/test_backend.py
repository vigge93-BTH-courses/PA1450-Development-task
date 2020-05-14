from program.backend import file_reader, insert_values_to_attribute_table, insert_values_to_datapoints_table


def test_file_reader():
    # Given
    a = "data.csv"

    # When
    res1 = file_reader(a)
    res2 = file_reader(a)

    # Then
    assert type(res1) == list
    assert type(res2) != int


def test_file_upload():
    # Given
    a = "data.csv"

    # When
    res1 = file_reader(a)
    res2 = file_reader(a)

    # Then
    assert type(res1) == list
    assert type(res2) != int
