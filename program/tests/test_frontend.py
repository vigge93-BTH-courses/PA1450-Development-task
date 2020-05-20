import flask
from program import create_app
from program.frontend import allowed_file
from io import BytesIO

client = None


def setup_module():
    global client
    app = create_app({'TESTING': True, })

    client = app.test_client()


def test_index():
    # Given
    expected1 = b'Weather app'
    expected2 = b'Speed&'
    expected3 = b'Speed&'
    expected4 = b'Speed&'
    expected5 = b'Speed&'
    path1 = '/'
    path2 = '/?attribute=speed&timeIntervallType=year&timeArgument=["1999"]'
    path3 = '/?attribute=speed&timeIntervallType=months&timeArgument=["07"]'
    path4 = '/?attribute=speed&timeIntervallType=months&timeArgument=["2001-07"]'
    path5 = '/?attribute=speed&timeIntervallType=intervall&timeArgument=["1999-07-23","2010-05-20"]'

    # When
    response1 = client.get(path1)
    response2 = client.get(path2)
    response3 = client.get(path3)
    response4 = client.get(path4)
    response5 = client.get(path5)
    # Then
    assert expected1 in response1.data
    assert expected2 in response2.data
    assert expected3 in response3.data
    assert expected4 in response4.data
    assert expected5 in response5.data


def test_file_upload():
    # Given
    path = '/upload_historical'
    expected1 = b'Historical data upload'
    expected2 = b'Invalid file type'
    expected3 = b'No file part'
    expected4 = b'No selected file'
    expected5 = b'Invalid formatting of file'
    expected6 = b'Success!'
    data2 = {
        'file': (BytesIO(b'FILE CONTENT'), 'test.exe')
    }
    data3 = {
        'field': 'Value'
    }
    data4 = {
        'file': (BytesIO(b''), '')
    }
    data5 = {
        'file': (BytesIO(b'FILE CONTENT'), 'Test.csv')
    }
    st = '''Stationsnamn;Klimatnummer;Mäthöjd (meter över marken)
Karlskrona Sol;65075;2.0

Parameternamn;Beskrivning;Enhet
Solskenstid;summa 1 timme, 1 gång/tim;second

Tidsperiod (fr.o.m);Tidsperiod (t.o.m);Höjd (meter över havet);Latitud (decimalgrader);Longitud (decimalgrader)
2009-07-01 00:00:00;2020-05-07 12:00:00;10.0;56.1091;15.5870

Datum;Tid (UTC);Solskenstid;Kvalitet;;Tidsutsnitt:
2019-12-29;01:00:00;0;G;;Data från senaste fyra månaderna'''.encode('utf-8')
    data6 = {
        'file': (BytesIO(st), 'Test.csv')
    }

    # When
    response1 = client.get(path)
    response2 = client.post(path, data=data2, follow_redirects=True)
    response3 = client.post(path, data=data3, follow_redirects=True)
    response4 = client.post(path, data=data4, follow_redirects=True)
    response5 = client.post(path, data=data5, follow_redirects=True)
    response6 = client.post(path, data=data6, follow_redirects=True)
    # Then
    assert expected1 in response1.data
    assert expected2 in response2.data
    assert expected3 in response3.data
    assert expected4 in response4.data
    assert expected5 in response5.data
    assert expected6 in response6.data


def test_allowed_file():
    # Given
    filename1 = "test.csv"
    filename2 = "test.pdf"
    filename3 = "test.csv.exe"
    filename4 = "test"
    filename5 = ""
    filename6 = None
    filename7 = "te åäöst.csv"

    # When
    res1 = allowed_file(filename1)
    res2 = allowed_file(filename2)
    res3 = allowed_file(filename3)
    res4 = allowed_file(filename4)
    res5 = allowed_file(filename5)
    res6 = allowed_file(filename6)
    res7 = allowed_file(filename7)

    # Then
    assert res1 is True
    assert res2 is False
    assert res3 is False
    assert res4 is False
    assert res5 is False
    assert res6 is False
    assert res7 is True
