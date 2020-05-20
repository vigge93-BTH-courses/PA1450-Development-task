from program.backend import file_reader, process_file, get_attributes, get_data, ext_check, insert_values_to_datapoints_table, insert_values_to_attribute_table, access_db, close_db, initialize_table, initiate_database 
import os
import tempfile

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
    b = tempfile.NamedTemporaryFile(prefix="test", suffix=".img")

    # When
    res1 = process_file(a)
    res2 = process_file(a)
    res3 = process_file(b.name)

    # Then
    assert type(res1) == str
    assert res2 == "File uploaded succesfully!"
    assert res3 == "File is not in the correct format"

    # Removes the file the file
    b.close()

def test_initiate_database():
    # When
    res1 = initiate_database()

    # Then
    assert os.path.isfile('instance\weather_data.db')

def test_access_db():
    # When
    res1 = access_db()

    # Then
    assert os.path.isfile('instance\weather_data.db')

def test_initialize_table():
    # Given
    db = access_db()
    c = db.cursor()
    # When
    table = initialize_table(db, c)
    db = access_db()
    c = db.cursor()
    names = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for name in names:
        res1 = name[0]
    # Then
    assert res1 == 'Datapoints'

def test_get_attributes():
    """Test get attributes."""
    # When
    res1 = get_attributes()

    # Then
    assert type(res1) == dict

def test_get_data():
    pass

def test_ext_check():
    # Given
    a = "data.csv"
   # b = tempfile.NamedTemporaryFile(prefix="test", suffix=".img")

    # When
    res1 = ext_check(a)
  #  res2 = ext_check(b)

    # Then
    assert type(res1) == list
  #  assert res2 == "File is not in the correct format"

def test_close_db():
    # Given
    db = access_db()
    is_closed = False

    # When
    close_db(db)
    try:
        res1 = db.cursor()
    except:
        is_closed = True
    
    # Then
    assert is_closed
