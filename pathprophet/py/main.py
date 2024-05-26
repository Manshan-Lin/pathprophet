from flask import Flask,render_template,flash,request
import os
from werkzeug.utils import secure_filename
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS={'jpg','png','jpeg','webp','gif'}

app=Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename,operation):
    print(f"The operation is {operation} and filename is {filename}")
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newFilename=f"static/{filename}"
            cv2.imwrite(newFilename,imgProcessed)
            return newFilename
        case "cwebp":
            newFilename=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg":
            newFilename=f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpeg":
            newFilename=f"static/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng":
            newFilename=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
            

@app.route("/")
def home():
    return render_template("断面图上传页面.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        operation=request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "ERROR: No Selected File"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            newFilename=processImage(filename,operation)
            flash(f"Your Image is processed and is available <a href='/{newFilename}' target='_blank'>here</a>")
            return render_template("断面图上传页面.html")   
    return render_template("断面图上传页面.html")


app.run(debug=True)