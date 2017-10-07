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
  f.close() 

if __name__ == '__main__':
  app.run(debug=True)

