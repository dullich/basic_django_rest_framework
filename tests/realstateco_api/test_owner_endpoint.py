from .login import Login
import json
import requests
from http import HTTPStatus
import jsonpath


BASE_URL_LOGIN = "http://localhost:8000/admin/login/"
BASE_URL_API = "http://localhost:8000/api/realstateco/"
API_OWNER = BASE_URL_API + "owner/"

#test if somebody is trying to access to a restricted path
def test_get_as_annonymous():
    response = requests.get(BASE_URL_API + "owner/")
    assert response.status_code == HTTPStatus.FORBIDDEN

#test if an authenticated user is trying to access to a restricted path
def test_get_as_user():
    login = Login()
    session = login.login(BASE_URL_LOGIN, "jfgomez", "RealState")
    response = session.get(API_OWNER)
    assert response.status_code == HTTPStatus.OK

#test adding a new owner
def test_new_owner():
    login = Login()
    session = login.login(BASE_URL_LOGIN, "jfgomez", "RealState")

    new_owner_json = {
        "csrfmiddlewaretoken": login.get_csrf_token(),
        "address": "Av. Siempre Viva 742",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Mus%C3%A9e_Rodin_1.jpg/800px-Mus%C3%A9e_Rodin_1.jpg",
        "birthday": "1994-06-09",
        "user": 2
    }
    
    response = session.post(API_OWNER, new_owner_json)
    assert response.status_code == HTTPStatus.OK
    response_json = json.load(response.text)
    json_id = jsonpath(response_json, "uuid")
    assert json_id