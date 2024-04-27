# Stack Overflow User Profiles and Face Detection


## About The Project
This is a simple Gradio application that fetches the top 10 user profiles based on reputation from Stack Overflow API, downloads their profile images, attempts to detect faces within those images using `dlib`, presents it in an intuitive user interface.


### Features
* Fetch user profiles from Stack Overflow.
* Download profile images asynchronously.
* Detect faces in the images using the `dlib` library.
* Display the results in a user-friendly web interface using Gradio.


## Installation

### Prerequisites
* Python 3.8 or higher
* pip 

### Installing Dependencies
1. Clone the repository:
```sh
git clone https://github.com/ardaatahan/technical-challenge.git
cd technical-challenge
```

2. Install the required packages:
```sh
pip install -r requirements.txt
```

### Usage 
To run the project:

1. Start the application:
```sh
python stack_overflow_users.py
```
2. Open your web browser and navigate to the link provided by Gradio.

### How It Works
1. The application makes a call to the Stack Overflow API to fetch the top 10 user profiles.
2. It then asynchronously downloads the profile images of these users.
3. Each image is processed to detect faces using the `dlib` library.
4. Results are displayed in a Gradio interface, showing the user details along with their profile image marked with detected faces.
