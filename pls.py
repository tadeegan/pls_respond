import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

from gi.repository import GLib

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/templates'
#GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD) + '/pls_respond_uploaded'

# Initialize
app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = set(['tsv'])

fname = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('landing.html')



@app.route('/upload', methods=['POST'])
def upload():
    # Get the the uploaded file
    file = request.files['hidden-upload']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file from the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        global fname 
        fname = filename
        return redirect(url_for('uploaded_file' ,filename=filename))

#gets file from local directory
@app.route('/alltime/<filename>')
def uploaded_file(filename):
  return render_template('index.html', filename=filename)

#def file_into_html(file):
    #return render_template('landing.html', file=send_from_directory(app.config['UPLOAD_FOLDER'], filename))

@app.route('/alltime')
def test():
    global fname
    return render_template('index.html', filename=fname)

@app.route('/weekly')
def test2():
    global fname
    return render_template('bar_index.html', filename=fname)

@app.errorhandler(404)
def page_not_found(error):
    return 'oopsie 404'

if __name__ == '__main__':
    app.run(
        #host='0.0.0.0',
        #port=int("8000"),
        debug = True
    )
