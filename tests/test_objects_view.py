def test_missing_dates(client):
    response = client.get("/objects")
    assert 400 == response.status_code

def test_missing_start_date(client):
    response = client.get("/objects",query_string={"end_date":"2023-02-03"})
    assert 400 == response.status_code

def test_missing_end_date(client):
    response = client.get("/objects",query_string={"start_date":"2023-02-03"})
    assert 400 == response.status_code

def test_invalid_start_date(client):
    response = client.get("/objects",query_string={"start_date":"2023-02-A3"})
    assert 400 == response.status_code

def test_invalid_end_date(client):
    response = client.get("/objects",query_string={"end_date":"2023-02-A3"})
    assert 400 == response.status_code

def test_max_days_range_exceeded(client):
    response = client.get("/objects",query_string={"start_date":"2023-01-01","end_date":"2023-02-28"})
    assert 400 == response.status_code

def test_succesful_req(client):
    response = client.get("/objects",query_string={"start_date":"2023-01-01","end_date":"2023-02-03"})
    assert 200 == response.status_code

def test_succesful_req_switched_dates(client):
    response = client.get("/objects",query_string={"end_date":"2023-01-01","start_date":"2023-02-03"})
    assert 200 == response.status_code

def test_succesful_req_multiple_requests(client):
    response = client.get("/objects",query_string={"start_date":"2023-01-01","end_date":"2023-02-01"})
    assert 200 == response.status_code