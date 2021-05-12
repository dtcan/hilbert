from tempfile import TemporaryFile
from flask import Flask, send_file, redirect
import os
import PIL.Image
import numpy as np

MAX = 13

def hilbert(n):
    if n < 2:
        return np.uint8(np.array([[1,1,1],[1,0,1],[1,0,1]]))
    b = hilbert(n-1)
    sep1 = np.uint8(np.zeros((b.shape[0],1)))
    sep1[-1,0] = 1
    a1 = np.concatenate((b,sep1,b),axis=1)
    sep2 = np.uint8(np.zeros((b.shape[0],1)))
    a2 = np.concatenate((b.T[:,::-1],sep2,b.T),axis=1)
    sep3 = np.uint8(np.zeros((1,a1.shape[1])))
    sep3[0][0] = 1
    sep3[0][-1] = 1
    return np.concatenate((a1,sep3,a2))

app = Flask(__name__)

@app.route("/<int:n>")
def get_curve(n):
    if n < 1:
        return redirect("1", code=302)
    elif n > MAX:
        return redirect(str(MAX), code=302)
    else:
        a = hilbert(n) * 255
        img = PIL.Image.fromarray(a)
        tempfile = TemporaryFile(suffix='png')
        img.save(tempfile, format='png')
        tempfile.seek(0,0)
        return send_file(tempfile, mimetype='image/png')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
