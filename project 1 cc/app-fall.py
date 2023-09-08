"""
############################
# 1st phase - all in 1 app #
############################
1. flask hello world - done

2. add other flask endpoints - done

3. hard code responses - done

4. look up how to accept only POST (GET is default) - done

5. return html for GET / - done
<form method="post" enctype="multipart/form-data" action="/upload" method="post">
  <div>
    <label for="file">Choose file to upload</label>
    <input type="file" id="file" name="form_file" accept="image/jpeg"/>
  </div>
  <div>
    <button>Submit</button>
  </div>
</form>

6. in GET /files return a hardcoded list for initial testing - done
files = ['file1.jpeg', 'file2.jpeg', 'file3.jpeg']

7. in GET / call the function for GET /files and loop through the list to add to the HTML - done
GET /
    ...
    for file in list_files():
        index_html += "<li><a href=\"/files/" + file + "\">" + file + "</a></li>"

    return index_html

8. in POST /upload - lookup how to extract uploaded file and save locally to ./files - done
def upload():
    file = request.files['form_file']  # item name must match name in HTML form
    file.save(os.path.join("./files", file.filename))

    return redirect("/")
#https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/

9. in GET /files - look up how to list files in a directory - done

    files = os.listdir("./files")
    #TODO: filter jpeg only
    return files

10. filter only .jpeg - done
@app.route('/files')
def list_files():
    files = os.listdir("./files")
    for file in files:
        if not file.endswith(".jpeg"):
            files.remove(file)
    return files

11. return files content
"""
from flask import Flask, redirect, request, send_file
import os
app = Flask(__name__)

@app.route('/')
def index():
    index_html = """<form method="post" enctype="multipart/form-data" action="/upload" method="post">
                        <div>
                            <label for="file">Choose file to upload</label>
                            <input type="file" id="file" name="form_file" accept="image/jpeg"/>
                        </div>
                        <div>
                            <button>Submit</button>
                        </div>
                    </form>
                    """

    for file in list_files():
        index_html += "<li><a href=\"/files/" + file + "\">" + file + "</a></li>\n"

    return index_html

@app.route('/upload', methods = ['POST'])
def upload():
    file = request.files['form_file']  # item name must match name in HTML form
    file.save(os.path.join("./files", file.filename))

    return redirect("/")

@app.route('/files/<filename>')
def get_file(filename):
    
    return send_file("./files/"+filename)

def list_files():
    files = os.listdir("./files")
    jpegs = []
    for file in files:
        if file.endswith(".jpeg") or file.endswith(".jpg"):
            jpegs.append(file)
    return jpegs

app.run(host='0.0.0.0', port=8080)