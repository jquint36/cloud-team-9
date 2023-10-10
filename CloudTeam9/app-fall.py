from flask import Flask, redirect, request, send_file, render_template_string
import os
import storage

from PIL import Image
from PIL.ExifTags import TAGS

app = Flask(__name__)

@app.route('/')
def index():
    key = request.args.get('key')

    index_html = """
<script>    
    function buttonPressed() {
        const currentURL = window.location.href;

        // Create a URLSearchParams object from the URL
        const urlParams = new URLSearchParams(currentURL);

        // Get the value of the 'key' parameter
        const windowKey = urlParams.get('key');
        
        // Get the URL from the input field
        var key = document.getElementById("keyInput").value;
        console.log(windowKey)
        // Check if the Enter key (key code 13) was pressed
        window.location.href = "?key="+key;
    }
</script>

<!form method="post" enctype="multipart/form-data" action="/upload">
<div>
    <label for="file" style="color:blue; font-size:50px;">Welcome to Cloud 9</label><br><br>
    <label for"file" style="color:red; font-size:20px;">Hello User!! Enter a key below. Example: examplepublickey1092023</label><br>

    <input type="text" id="keyInput" placeholder="Enter your Key...">
    <br><br>
    <button type="button" onclick="buttonPressed()" style="height:20px;width:100px">Enter</button>           
    <br>
</div>
                """
    keyParam = "&"
    if key:
        index_html += "<br>Key = "+key+"<br>"
        for file in list_files(key):
            index_html += f"<li><a href=\"/display/{file+keyParam+key}\">{file}</a> <a href=\"/delete/{file+keyParam+key}\" style=\"color: red;\">[Delete]</a></li>\n"
        index_html += "</ul>"
        
        index_html += f"""
        <br><br>
        <form method="post" enctype="multipart/form-data" action="/upload">
            <div>
                <label for"file" style="color:red; font-size:20px;">Upload a file below to key</label><br>
                <input type="text" name="key" required value="{key}"><br>
                <input type="file" id="file" name="form_file" accept="image/jpeg"/ required><br><br>
            </div>
            <div>
                <button style="height:20px;width:100px">Submit</button>
            </div>
        </form>
                    """
    
    return index_html

@app.route('/upload', methods=['POST'])
def upload():
    key = request.form['key']
    file = request.files['form_file']
    image = Image.open(file)
    exifdata = image.getexif()
    
    obj = {}
    obj['Name'] = file.filename
    for tagid in exifdata:
        tagname = str(TAGS.get(tagid, tagid))
        value = str(exifdata.get(tagid))
        obj[tagname] = value
    print(obj)
    
    blob_size = storage.upload_file(key, file.filename,file)
    
    obj["blob_size"] = blob_size
    
    obj["Location"] = f"https://storage.cloud.google.com/{key}/{file.filename}"
    
    storage.add_db_entry(obj,key)
    
    #file.save(os.path.join("./files", file.filename))
    
    return redirect("/?key="+key)

@app.route('/display/<filename>')
def display_image(filename):
    result_list = filename.split('&')
    key = result_list[1]
    filename = result_list[0]
    #print(filename, key)
    
    obj = storage.fetch_db_entry({'Name': filename},key)[0]
    
    template = '''
                    <head>
                        <style>
                            table, th, td {
                                border: 2px solid black;
                            }
                        </style>
                    </head>
                '''+f'''
                    <div style="position: absolute; top: 10px; left: 10px;">
                    <button onclick="window.history.back()">Back</button>
                    <br><img src="https://storage.cloud.google.com/{key}/{filename}" alt="{filename}" style="width:800px; height:auto;"><br>
                    <a href="https://storage.cloud.google.com/{key}/{filename}" alt="{filename}" download style="margin-bottom: 10px;">Download</a>
                    
                    
                    <table>
                    '''
    for name, value in obj.items():
        template += f""" <tr>
                            <th>{name}:</th>
                            <th>{value}</th>
                        </tr>
                    """

    template +='''
                    </table>
                  </div>
                  '''
                  
    return render_template_string(template, filename=filename)

@app.route('/delete/<filename>')
def delete_file(filename):
    result_list = filename.split('&')
    key = result_list[1]
    filename = result_list[0]
    storage.delete_file(key,filename)
    return redirect("/?key="+key)
#def delete_file(filename):
#    #For security so people can't just delete any path, only in this file path
#    if "/" in filename or ".." in filename:
#        return "Invalid filename", 400
#    os.remove(os.path.join("./files", filename))
#    return redirect("/")


@app.route('/files/<filename>')
def get_file(filename):
    return send_file(f"./files/{filename}")

#def list_files():
#    files = os.listdir("./files")
#    return [file for file in files if file.endswith(('.jpeg', '.jpg'))]
def list_files(key):
    return storage.get_list_of_files(key)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)