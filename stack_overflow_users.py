import requests


URL = "https://api.stackexchange.com/2.2/users?site=stackoverflow"


def fetch_stack_overflow_profiles(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Failed to retrieve Stack Overflow user data: Status Code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return str(e)
