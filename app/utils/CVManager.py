import requests

from typing import List

from app.schemas.TaskSchemas import Face


class CVManager:
    FACECLOUD_URL: str

    email: str
    password: str

    access_token: str

    def __init__(self, email: str, password: str, facecloud_url: str):
        self.email = email
        self.password = password
        self.FACECLOUD_URL = facecloud_url

        self.get_token()

    def get_token(self) -> None:
        r = requests.post(
            f"{self.FACECLOUD_URL}/api/v1/login",
            json={"email": self.email, "password": self.password},
        )
        result = r.json()

        self.access_token = result["data"]["access_token"]

    def detect(self, path_to_image: str) -> List[Face]:
        headers = {
            "Content-Type": "image/jpeg",
            "Authorization": f"Bearer {self.access_token}",
        }
        with open(path_to_image, "rb") as file:
            r = requests.post(
                f"{self.FACECLOUD_URL}/api/v1/detect",
                headers=headers,
                data=file.read(),
                params={"demographics": "true"},
            )
        if r.status_code == 400:
            self.get_token()
            headers = {
                "Content-Type": "image/jpeg",
                "Authorization": f"Bearer {self.access_token}",
            }
            with open(path_to_image, "rb") as file:
                r = requests.post(
                    f"{self.FACECLOUD_URL}/api/v1/detect",
                    headers=headers,
                    data=file.read(),
                    params={"demographics": "true"},
                )

        faces = []
        for face in r.json()["data"]:
            faces.append(
                Face(
                    sex=face["demographics"]["gender"],
                    age=face["demographics"]["age"]["mean"],
                    bbox=face["bbox"],
                )
            )

        return faces
