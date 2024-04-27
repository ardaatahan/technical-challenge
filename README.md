# Stack Overflow User Profiles and Face Detection
The live application demo can be found [here](https://huggingface.co/spaces/ardaatahan/stack_overflow_users).


## About The Project
This is a simple Gradio application that fetches the top 10 user profiles based on reputation from Stack Overflow API, downloads their profile images, attempts to detect faces within those images using `dlib`, and presents them in an intuitive user interface.


### Features
* Fetch user profiles from Stack Overflow.
* Download profile images asynchronously.
* Detect faces in the images using the `dlib` library.
* Display the results in a user-friendly web interface using Gradio.


## Installation

### Prerequisites
* Python 3.8 or higher
* pip3 

### Installing Dependencies
1. Clone the repository:
```sh
git clone https://github.com/ardaatahan/technical-challenge.git
cd technical-challenge
```

2. dlib requires cmake. If cmake is not installed:
```sh
brew install cmake
```
or you can follow [this](https://cgold.readthedocs.io/en/latest/first-step/installation.html) guide if you are using a different package manager/OS.

3. Install the required packages:
```sh
pip3 install -r requirements.txt
```

### Usage 
To run the project:

1. Start the application:
```sh
python3 stack_overflow_users.py
```

2. Open your web browser and navigate to the link provided by Gradio.

3. Press Generate button to fetch users and display results or Clear button to clear the results.

### How It Works
1. The application makes a call to the Stack Overflow API to fetch the top 10 user profiles.
2. It then asynchronously downloads the profile images of these users.
3. Each image is processed to detect faces using the `dlib` library.
4. Results are displayed in a Gradio interface, showing the user details along with their profile image marked with detected faces.

### Third Party Libraries Used
`numpy`:
* Use Case: Used extensively for handling arrays, which is crucial when manipulating image data received from profile images. numpy allows efficient operations on images, such as transformations and decoding, which are essential for the image processing steps prior to applying face detection algorithms.
* Why Chosen: Chosen for its performance and wide support in the Python ecosystem, especially in data manipulation and numerical operations which are fundamental in image processing tasks.

`gradio`:
* Use Case: Facilitates the creation of a user-friendly interface that displays the Stack Overflow profiles and the results of the face detection process. Gradio makes it straightforward to create interactive blocks for displaying images and text, which are essential for the output of this project.
* Why Chosen: Gradio is particularly effective for creating demo applications quickly and with minimal code. It supports a wide range of inputs and outputs, making it ideal for projects that require showcasing machine learning or image processing results in an intuitive way.

`aiohttp`:
* Use Case: Used to handle asynchronous HTTP requests to the Stack Overflow API. This is important for non-blocking data retrieval, allowing the application to perform other tasks, such as processing images, while waiting for HTTP responses.
* Why Chosen: aiohttp is chosen for its ability to handle asynchronous web requests efficiently, which helps in maintaining responsiveness and scalability of the application when dealing with I/O-bound tasks like network requests.

`opencv`:
* Use Case: Provides a variety of image processing functionalities which are used to decode images from bytes, convert image formats, and prepare images for face detection. The headless version is used to reduce the overhead since GUI features of OpenCV are not needed.
* Why Chosen: The headless version of OpenCV reduces the installation footprint and removes unnecessary dependencies on GUI libraries, which is beneficial for deployment in server environments or containers where graphical user interfaces are not utilized.

`dlib`:
* Use Case: Employs robust machine learning algorithms to detect faces in images. dlib offers one of the most effective and accurate face detection models available, making it suitable for projects that require reliable facial recognition.
* Why Chosen: Despite its complex setup, dlib is selected for its superior performance in face detection compared to other libraries. Its face detector is based on a modification of the standard Histogram of Oriented Gradients (HOG) + Linear SVM method, which is well-suited for this application given its accuracy and efficiency in detecting human faces.
