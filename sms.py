import requests

url = "https://www.fast2sms.com/dev/bulkV2"

payload = {
    "sender_id": "FSTSMS",
    "message": "Hello! This is a test message from Python.",
    "language": "english",
    "route": "p",
    "numbers": "9635403297"  # Replace with recipient's number
}

headers = {
    'authorization': 'O9D6goAx0mbzq3lw5EZdrPuBf4VivKcpkHSaY1WTeIXCN82yJn14UGCixXNtHp8Tf6kOcPeKrqdDho7Q',
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache"
}

response = requests.post(url, data=payload, headers=headers)

print(response.text)
