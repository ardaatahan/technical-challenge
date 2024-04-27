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
    faces, _, _ = detector.run(image, 1, -0.5)
    for face in faces:
        cv2.rectangle(
            image,
            (face.left(), face.top()),
            (face.right(), face.bottom()),
            (0, 255, 0),
            4,
        )
    return image


def process_users():
    profiles = asyncio.run(fetch_stack_overflow_profiles(URL))
    # TODO better error handling
    if type(profiles) is str:
        return profiles
    user_content = []
    for profile in profiles:
        image_url = profile["profile_image"]
        image = asyncio.run(download_profile_image(image_url)) if image_url else None
        # TODO better error handling
        if image is None:
            continue
        if type(image) is str:
            continue
        image = detect_face_in_image(image)
        user_html = f"""
        <div style='display: flex; flex-direction: column; align-items: center; margin-bottom: 50px;'>
            <div style='margin-bottom: 10px;'>
                <img src="{image}" alt="Profile image" style='width: 100%; height: 100%; object-fit: cover;'>
            </div>
            <div style='text-align: center; font-size: 16px;'> 
                <strong style='font-size: 18px;'>Name:</strong> {profile.get('display_name')}
                <br>
                <strong style='font-size: 18px;'>Reputation:</strong> {profile.get('reputation')}
                <br>
                <strong style='font-size: 18px;'>Location:</strong> {profile.get('location', 'Not available')}
                <br>
                <a href="{profile.get('link')}" target="_blank" style='font-size: 16px; color: blue; text-decoration: none;'>View Profile</a>
            </div>
        </div>
        """
        user_content.append(user_html)
    return "".join(user_content)
