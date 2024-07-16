#!/usr/bin/env python3
"""
Main file - End-to-end integration test
"""
import requests


def register_user(email: str, password: str) -> None:
    """tests the app server register endpoint"""
    data = {'email': email, 'password': password}
    res = requests.post('http://172.23.112.35:5000/users',
                        data=data)
    assert res.status_code == 200
    res = res.json()
    assert 'email' in res
    assert res['email'] == email
    assert 'message' in res
    assert res['message'] == 'user created'


def log_in_wrong_password(email: str, password: str) -> None:
    """tests the auth endpoint with fake password"""
    data = {'email': email, 'password': password}
    res = requests.post('http://172.23.112.35:5000/sessions',
                        data=data)
    assert res.status_code == 401


def log_in(email: str, password: str) -> None:
    """tests the auth endpoint with correct credentials"""
    data = {'email': email, 'password': password}
    res = requests.post('http://172.23.112.35:5000/sessions',
                        data=data)
    assert res.status_code == 200

    session_id = res.cookies.get('session_id')
    assert session_id is not None
    res = res.json()
    assert 'email' in res
    assert res['email'] == email
    assert 'message' in res
    assert res['message'] == 'logged in'
    return session_id


def profile_unlogged() -> None:
    """tests access to the profile page unauthenticated"""
    res = requests.get('http://172.23.112.35:5000/profile')
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """tests user access to the profile page"""
    cookies = {'session_id': session_id}
    res = requests.get('http://172.23.112.35:5000/profile', cookies=cookies)
    assert res.status_code == 200
    res = res.json()
    assert 'email' in res


def log_out(session_id: str) -> None:
    """tests logout endpoint"""
    cookies = {'session_id': session_id}
    url = 'http://172.23.112.35:5000/sessions'
    res = requests.delete(url, cookies=cookies)
    assert res.status_code == 200
    session_id = res.cookies.get('session_id')
    assert session_id is None


def reset_password_token(email: str) -> str:
    """tests the reset_password endpoint"""
    data = {'email': email}
    url = 'http://172.23.112.35:5000/reset_password'
    res = requests.post(url, data=data)
    assert res.status_code == 200
    res = res.json()
    assert 'email' in res
    assert res['email'] == email
    assert 'reset_token' in res
    return res['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """tests the update password endpoint"""
    data = {'email': email,
            'reset_token': reset_token,
            'new_password': new_password}
    res = requests.put('http://172.23.112.35:5000/reset_password', data=data)
    assert res.status_code == 200
    res = res.json()
    assert 'email' in res
    assert res['email'] == email
    assert 'message' in res
    assert res['message'] == "Password updated"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
