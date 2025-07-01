from requests import Response


class RequestException(Exception):
    def __init__(self, res: Response):
        self.res = res

    def __str__(self):
        if self.res.status_code == 200:
            return self.res.json()["message"]
        else:
            return f"{self.res.status_code} {self.res.text}"