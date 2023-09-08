from flask import Flask, redirect, request, send_file, render_template_string
import os

app = Flask(__name__)

@app.route('/')
def index():
    index_html = """<form method="post" enctype="multipart/form-data" action="/upload">
                        <div>
                            <label for="file">Choose file to upload</label>
                            <input type="file" id="file" name="form_file" accept="image/jpeg"/>
                        </div>
                        <div>
                            <button>Submit</button>
                        </div>
                    </form>
                    <ul>
                    """
    
    for file in list_files():
        index_html += f"<li><a href=\"/display/{file}\">{file}</a> <a href=\"/delete/{file}\" style=\"color: red;\">[Delete]</a></li>\n"

    index_html += "</ul>"
    
    return index_html

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['form_file']
    file.save(os.path.join("./files", file.filename))
    
    return redirect("/")

@app.route('/display/<filename>')
def display_image(filename):
    template = '''<div style="position: absolute; top: 10px; left: 10px;">
                    <a href="/">Back</a>
                    <br><img src="/files/{{filename}}" alt="{{filename}}" style="width:800px; height:auto;"><br>
                    <a href="/files/{{filename}}" download style="margin-bottom: 10px;">Download</a>
                  </div>
                  '''
                  
    return render_template_string(template, filename=filename)

@app.route('/delete/<filename>')
def delete_file(filename):
    #For security so people can't just delete any path, only in this folder
    if "/" in filename or ".." in filename:
        return "Invalid filename", 400
    os.remove(os.path.join("./files", filename))
    return redirect("/")

@app.route('/files/<filename>')
def get_file(filename):
    return send_file(f"./files/{filename}")

def list_files():
    files = os.listdir("./files")
    return [file for file in files if file.endswith(('.jpeg', '.jpg'))]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
