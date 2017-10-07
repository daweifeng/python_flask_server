from flask import Flask
from flask_restful import reqparse, Resource, Api
import werkzeug

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('audio', type=werkzeug.datastructures.FileStorage, location='files')
# parser.add_argument('audio')

class IndexRoute(Resource):
  def get(self):
    return 'Hello, world'

class AudioFile(Resource):
  def post(self):
    arg = parser.parse_args()
    # print(arg['audio'])
    arg['audio'].save('temp.m4a')
    audio_handler()

api.add_resource(AudioFile, '/api/audio')
api.add_resource(IndexRoute, '/')

# Handle audio files
def audio_handler():
  with open('temp.m4a') as f:
    print(f)
    def transcribe_file(speech_file):
      from google.cloud import speech
      from google.cloud.speech import enums
      from google.cloud.speech import types
      client = speech.SpeechClient()

      with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

      audio = types.RecognitionAudio(content = content)
      config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')
      
      response = client.recognize(config, audio)
      #Print the first alternative of all the consecutive results.
      for result in response.results:
        print('Transcript: {}'.format(result.alternative[0].transcript))
    transcribe_file(f)
  f.close() 

if __name__ == '__main__':
  app.run(debug=True)

