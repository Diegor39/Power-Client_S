import azure.cognitiveservices.speech as sSDK

speech_key, service_region = "e21c5662cc5c4e7aa983ba12c67f6a90", "eastus"
speech_config = sSDK.SpeechConfig(subscription=speech_key, region=service_region)

speech_recognizer = sSDK.SpeechRecognizer(speech_config=speech_config)
print("Say something...")

result = speech_recognizer.recognize_once()

if result.reason == sSDK.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))