from datetime import datetime
import numpy as np

import aiohttp
import asyncio
import cv2
import dlib


URL = "https://api.stackexchange.com/2.2/users?site=stackoverflow"
MAX_USERS = 10


def filter_profile_data(data):
    data = data["items"]
    data = data[: min(MAX_USERS, len(data))]
    keys_to_keep = ["reputation", "location", "display_name", "link", "profile_image"]
    filtered_data = []
    for raw_user in data:
        user = {}
        for key in keys_to_keep:
            user[key] = raw_user[key] if key in raw_user else None
        filtered_data.append(user)
    return filtered_data


async def fetch_stack_overflow_profiles(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    data = filter_profile_data(data)
                    return data
                else:
                    return f"Failed to retrieve Stack Overflow user data: Status Code {response.status}"
        except aiohttp.ClientError as e:
            return str(e)
        except asyncio.TimeoutError:
            return "User data request timed out"


async def download_profile_image(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.read()
                    array = np.asarray(bytearray(data), dtype=np.uint8)
                    image = cv2.imdecode(array, -1)
                    return image
                else:
                    return f"Failed to retrieve user profile image: Status Code {response.status}"
        except aiohttp.ClientError as e:
            return f"Profile image could not be downloaded: {str(e)}"
        except asyncio.TimeoutError:
            return "User profile image request timed out"


def detect_face_in_image(image):
    detector = dlib.get_frontal_face_detector()
    faces, _, _ = detector.run(image, 1, -1)
    for face in faces:
        cv2.rectangle(
            image,
            (face.left(), face.top()),
            (face.right(), face.bottom()),
            (0, 255, 0),
            4,
        )
    cv2.imwrite(f"{datetime.now()}.jpg", image)
