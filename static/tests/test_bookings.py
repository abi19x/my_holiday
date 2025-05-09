def login(client):
    client.post('/register', data={
        'name': 'Bob',
        'email': 'bob@example.com',
        'password': 'pass'
    })
    client.post('/login', data={'email': 'bob@example.com', 'password': 'pass'})

def test_booking_submission(client):
    login(client)
    res = client.post('/bookings/new', data={
        'type': 'Holiday',
        'start_date': '2025-05-01',
        'end_date': '2025-05-03',
        'notes': 'Vacation trip'
    }, follow_redirects=True)
    assert b'Booking request submitted' in res.data
