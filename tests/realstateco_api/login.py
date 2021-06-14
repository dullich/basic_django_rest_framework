from http import HTTPStatus
import requests
from bs4 import BeautifulSoup

#class for login in Django admin for requests as authenticated user
class Login():
    
    def __init__(self):
        self._csrfmiddlewaretoken = ""

    def get_csrf_token(self):
        return self._csrfmiddlewaretoken

    #each request must have the csrf token, this appears in 2 parts: header and input field within the form
    #the csfr token sent in the request is obtained from the form
    def extract_csrf_token(self, html):
        soup = BeautifulSoup(html, "html.parser")
        input=soup.find("input", {"name": "csrfmiddlewaretoken"})
        if input:
            return input.attrs["value"]
        
        return ""

    #for authentication it's neccesary to send the csrfmiddlewaretoken obtained in the extract_csrf_token method
    def login(self, url, username, password):
        new_session = requests.session()
        response = new_session.get(url)
        
        self._csrfmiddlewaretoken = self.extract_csrf_token(response.text)

        login_json = {
            "csrfmiddlewaretoken": self._csrfmiddlewaretoken,
            "username": username,
            "password": password,
            "next": "/admin/"
        }

        headers = {
            "Referer": url
        }

        response = new_session.post(url, data=login_json, headers=headers)
        assert response.status_code == HTTPStatus.OK
        return new_session