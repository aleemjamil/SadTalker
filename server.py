from modify import DotDict,inference
import os
from flask import Flask, request, jsonify
import gtts
import pyttsx3
import os
import uuid
import requests
import json
import base64

app = Flask(__name__)

dic = {"fitness" : "./Client_data/fitness-en-us.png",
"nutrition" : "./Client_data/nutrition-en-us.png",
"therapy" : "./Client_data/therapy-en-us.png"}


def synthesize_speech(text, language_code, voice_name, speaking_rate, pitch, gender):
    url = "https://texttospeech.googleapis.com/v1beta1/text:synthesize?key=AIzaSyDUoPaGUnszVNnzLyUnFQICsLBOEyPvisc"

    payload={
      "audioConfig": {
        "audioEncoding": "MP3",
        "effectsProfileId": [
          "small-bluetooth-speaker-class-device"
        ],
        "pitch": pitch,
        "speakingRate": speaking_rate
      },
      "input": {
        "text": text
        },
      "voice": {
        "languageCode": language_code,
        "name":voice_name,
        "ssmlGender":gender
      }
    }

    headers = {
      'Content-Type': 'text/plain',
      'AIzaSyDUoPaGUnszVNnzLyUnFQICsLBOEyPvisc': ''
    }
    
    response = requests.request("POST", url, headers=headers, data=str(payload))
    print(response)
    audio_content_base64=json.loads(response.text)["audioContent"]
    audio_content = base64.b64decode(audio_content_base64)
    save_path = "./audio.mp3"
    with open(save_path,"wb") as f:
        f.write(audio_content)
    
    return save_path
    
default_args = {
    "driven_audio": './examples/driven_audio/bus_chinese.wav',
    "source_image": './examples/source_image/full_body_1.png',
    "ref_eyeblink": None,
    "ref_pose": None,
    "checkpoint_dir": './checkpoints',
    "result_dir": './results',
    "pose_style": 0,
    "batch_size": 2,
    "size": 256,
    "expression_scale": 1.0,
    "input_yaw": None,
    "input_pitch": None,
    "input_roll": None,
    "enhancer": None,
    "background_enhancer": None,
    "cpu": False,
    "face3dvis": False,
    "still": False,
    "preprocess": 'crop',
    "verbose": False,
    "old_version": False,
    "net_recon": 'resnet50',
    "init_path": None,
    "use_last_fc": False,
    "bfm_folder": './checkpoints/BFM_Fitting/',
    "bfm_model": 'BFM_model_front.mat',
    "focal": 1015.0,
    "center": 112.0,
    "camera_d": 10.0,
    "z_near": 5.0,
    "z_far": 15.0,
    "device" : "cuda"
}


@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    print("data", data)
    image = data['image']
    text = data['text']
    language_code = data['voice_languageCode']
    voice_name = data['voice_name']
    pitch = data['pitch']
    speaking_rate = data['speakingRate']
    gender = data['gender']
    
    audio = synthesize_speech(text, language_code, voice_name, speaking_rate, pitch, gender)
    args = DotDict(default_args)
    args.driven_audio = audio
    
    args.source_image = dic[image]
    args.enhancer = 'gfpgan'
    result_url = inference(args)
    
    import json
    return json.dumps(result_url)

app.run(host="0.0.0.0", port="8085")
