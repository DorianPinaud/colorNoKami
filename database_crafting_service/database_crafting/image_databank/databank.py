from PIL import Image as ImagePIL

import time

import os

import httpx

from io import BytesIO


class ImagesDatabank:

    def __init__(self, storage_path):

        self.storage_path = storage_path

    def register(self, host: str, hash: str, name: str) -> ImagePIL.Image:

        path = f"{self.storage_path}/{hash}_{name}"

        if self.has(host, hash, name):
            return ImagePIL.open(path)
        else:
            time.sleep(0.5)
            request = httpx.get(f"{host}/data/{hash}/{name}")
            image = ImagePIL.open(BytesIO(request.content))
            image.save(path)
            return image

    def has(self, host: str, hash: str, name: str) -> bool:
        path = f"{self.storage_path}/{hash}_{name}"
        return os.path.exists(path)

    def get(self, host: str, hash: str, name: str):
        path = f"{self.storage_path}/{hash}_{name}"
        return ImagePIL.open(path)
