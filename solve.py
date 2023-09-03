from PIL import Image
import pytesseract as pyt
import requests as rq
from io import BytesIO
from bs4 import BeautifulSoup
from base64 import b64decode


url = 'http://localhost:3000/'
cookies = {}


def get_image(html: str):
    soup = BeautifulSoup(html, "html.parser")
    base64 = soup.find("img")["src"][22:]
    byteimage = BytesIO(b64decode(base64))
    return byteimage


def get_interest_tag(html: str, interest_tag: str):
    soup = BeautifulSoup(html, 'html.parser')
    desired_text = soup.find_all(interest_tag)[1].text.strip()
    return desired_text


solved = 0
max_solve = 295

while solved < max_solve:

    # first requets
    request = rq.get(url, cookies=cookies)

    captcha = Image.open(get_image(request.text))
    guess = pyt.image_to_string(captcha).strip('\n')
    print("OCR says:", guess)

    payload = {
        "captcha": guess
    }

    # answer to captcha
    answer = rq.post(url, cookies=cookies, data=payload)

    message = get_interest_tag(answer.text, 'h4')
    print(message)
    solved = int(message.split()[3])
