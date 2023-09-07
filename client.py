import requests

def synthesize_text_to_speech(image, text, language_code, voice_name, speaking_rate, pitch, gender):
    url = "http://127.0.0.1:8085/synthesize" 
    data = {
        "image": image,
        "text": text,
        "voice_languageCode": language_code,
        "voice_name": voice_name,
        "gender" : gender,
        "pitch": pitch,
        "speakingRate": speaking_rate
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result_url = response.json()
        print(result_url)
    else:
        print("Error:", response.text)


    
image = input("Enter Image Name: ")
text = input("Enter text: ")
language_code = input("Enter language code: ")
voice_name = input("Enter Voice_name: ")
gender = input("Enter Gender: ")
pitch = float(input("Enter Pitch: "))
speaking_rate = float(input("Enter Speaking Rate: "))

synthesize_text_to_speech(image, text, language_code, voice_name, speaking_rate, pitch, gender)

