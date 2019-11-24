from bysykkel_status_requests import bysykkel_status_request, bysykkel_info_request, get_table

def test_bysykkel_status_request():
    response = bysykkel_status_request()
    assert response, 'test failed because response code was not in 200 or 300 range'
    assert response.status_code==200, 'test failed because response code was not 200'


def test_bysykkel_info_request():
    response = bysykkel_info_request()
    assert response, 'test failed because response code was not in 200 or 300 range'
    assert response.status_code==200, 'test failed because response code was not 200'

def test_get_table():
    table, success = get_table()
    assert success, 'test failed because no data was returned'
    assert len(table) > 0, 'test failed because there were no rows'
    for i in range(len(table)):
        assert len(table[i]) == 3, 'test failed because the number of columns for row {0} was not 3'.format(i)
