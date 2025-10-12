import requests

with open("../model/0017.tif", "rb") as f:
    files = {"file": f}
    response = requests.post("http://127.0.0.1:8000/predict/", files=files)

with open("rezultat.png", "wb") as out:
    out.write(response.content)
