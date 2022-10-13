# pip install --upgrade google-cloud-texttospeech
# https://cloud.google.com/text-to-speech/docs/libraries#client-libraries-install-python

import PyPDF2
from google.cloud import texttospeech
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file("fit-parity-365321-953cd61874e5.json")


def synthesize_text(text, audio_file_name):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(audio_file_name, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file : ' + audio_file_name)


filename = 'ShortStory.pdf'
pdf_file = open(filename, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = pdf_reader.numPages

for number in range(number_of_pages):
    page = pdf_reader.getPage(number)
    synthesize_text(page.extractText(), f"{filename}.{number}.mp3")
