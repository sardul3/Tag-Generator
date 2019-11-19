from time import sleep
from datetime import datetime
from picamera import PiCamera
import requests

api_key = 'acc_de4aa995ecbada5'
api_secret = 'be3352b00d8d20c96aa024ba70e0d139'



from flask import Flask, render_template
app = Flask(__name__)


now_time = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
camera = PiCamera()

tags = None

@app.route('/')
def index():
    try:
        for i in range(1):
            if camera.closed:
                print('closed')
            else:
                sleep(5)
                camera.annotate_text=now_time
                camera.capture('./static/images/%s.jpg'%i)
                
                
                
    finally:
        camera.close()
        image_url = "/home/pi/timeseries/static/images/0.jpg"
        response = requests.post('https://api.imagga.com/v2/tags?image_url=%s' % image_url, auth=(api_key, api_secret),files={'image': open(image_url, 'rb')})
        data = response.json()
        tags = data["result"]["tags"]

    
    return render_template('index.html', tags=tags, len=len(tags))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
    
    