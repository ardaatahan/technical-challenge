import numpy as np
import gradio as gr

import aiohttp
import asyncio
import cv2
import dlib
import base64


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
                    image = cv2.imdecode(array, 1)
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
    _, buffer = cv2.imencode(".jpg", image)
    image = base64.b64encode(buffer)
    return image, len(faces) > 0


def process_users():
    profiles = asyncio.run(fetch_stack_overflow_profiles(URL))
    if type(profiles) is str:
        return get_error_html(profiles)
    user_content = []
    for profile in profiles:
        image_url = profile["profile_image"]
        image = asyncio.run(download_profile_image(image_url)) if image_url else None
        if i == 0:
            image = None
        if image is None:
            user_html = get_user_html(None, profile, "", "Image for this user could not be fetched!")
            user_content.append(user_html)
            continue
        if type(image) is str:
            user_html = get_user_html(None, profile, "", image)
            user_content.append(user_html)
            continue
        image, face_exists = detect_face_in_image(image)
        face_message = (
            "Face detected and highlighted in the user profile image!"
            if face_exists
            else "No face detected in the user profile image!"
        )
        image = image.decode("utf-8")
        user_html = get_user_html(image, profile, face_message, None)
        user_content.append(user_html)
    return "".join(user_content)


def get_error_html(error_message):
    return f"""
        <div style='display: flex; flex-direction: column; align-items: center; margin-bottom: 5rem;'>
            <div style='text-align: center; font-size: 16px;'> 
                <strong style='font-size: 18px;'></strong> {error_message} Try generating again.
                <br>
            </div>
        </div>
        """


def get_user_html(image, profile, face_message, error_message):
    return f"""
        <div style='display: flex; flex-direction: column; align-items: center; margin-bottom: 5rem;'>
           {f"""<div style='margin-bottom: 1rem;'>
                <img src="data:image/jpeg;base64,{image}" alt="Profile image" style='width: 100%; height: 100%; object-fit: cover;'>
            </div>""" if error_message is None else f"""<div style='text-align: center; font-size: 16px; margin-bottom: 1rem;'> 
                <strong style='font-size: 18px;'></strong> {error_message} Try generating again.
                <br>
            </div>"""}
            <div style='text-align: center; font-size: 16px;'> 
                <strong style='font-size: 18px;'>Name:</strong> {profile.get("display_name", "Not available")}
                <br>
                <strong style='font-size: 18px;'>Reputation:</strong> {profile.get("reputation", "Not available")}
                <br>
                <strong style='font-size: 18px;'>Location:</strong> {profile.get("location", "Not available")}
                <br>
                <a href="{profile.get("link", "")}" target="_blank" style='font-size: 16px; color: blue; text-decoration: none;'>View Profile</a>
                {f"""<br>
                <span style='font-size: 16px; color: grey;'>{face_message}</span>""" if error_message is None else """"""}
            </div>
        </div>
        """


def get_html_content():
    html_content = process_users()
    return html_content


demo = gr.Interface(
    fn=get_html_content,
    inputs=[],
    outputs=gr.components.HTML(label="Stack Overflow User Profiles"),
    title="Stack Overflow User Profiles and Face Detection",
    css="footer{display:none !important}",
    allow_flagging="never",
)


if __name__ == "__main__":
    demo.launch()
