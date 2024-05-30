import cv2
import numpy
from flask import Flask, render_template, Response, stream_with_context, request

app = Flask('__name__')
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def video_stream():
    while True:
        ret, frame = video.read()
        # cv2.imshow("cam", frame)
        # frame = cv2.imread("test.png")
        if frame is not None:
            ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame +b'\r\n')
            key = cv2.waitKey(1)&0xFF
            if key == 27:
                video.release()
                break

@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='0.0.0.0', port='5000', debug=False)
