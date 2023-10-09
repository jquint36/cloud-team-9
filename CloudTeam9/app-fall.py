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
    <label for"file" style="color:red; font-size:20px;">Hello User!! Enter a key below</label><br>

    <input type="text" id="keyInput" placeholder="Enter your a Key...">
    <br><br>
    <button type="button" onclick="buttonPressed()" style="height:20px;width:100px">Enter Key</button>           
    <br>
</div>
                """
    
    if key:
        index_html += "<br>Key = "+key+"<br>"
        for file in list_files():
            index_html += f"<li><a href=\"/display/{file}\">{file}</a> <a href=\"/delete/{file}\" style=\"color: red;\">[Delete]</a></li>\n"
        index_html += "</ul>"
        
        index_html += f"""
        <br><br>
        <form method="post" enctype="multipart/form-data" action="/upload">
            <div>
                <label for"file" style="color:red; font-size:20px;">Upload a file below to key {key}</label><br>
                <input type="text" name="key" required value="{key}">
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
    #key = request.files['key']
    #print(key)
    file = request.files['form_file']
    image = Image.open(file)
    exifdata = image.getexif()
    
    print(exifdata)
    
    storage.upload_file("testing12312312312312312", file.filename,file)
    #file.save(os.path.join("./files", file.filename))
    
    return redirect("/")

@app.route('/display/<filename>')
def display_image(filename):
    template = '''<div style="position: absolute; top: 10px; left: 10px;">
                    <a href="/">Back</a>
                    <br><img src="/files/{{filename}}" alt="{{filename}}" style="width:800px; height:auto;"><br>
                    <a href="/files/{{filename}}" download style="margin-bottom: 10px;">Download</a>
                    
                    
                    <table>

                        <tr>
                            <th>File Name:</th>
                            <th>test.jpg</th>
                        </tr>
                        <tr>
                            <th>Location:</th>
                            <th>my house</th>
                        </tr>
                        <tr>
                            <th>Size:</th>
                            <th>1mb</th>
                        </tr>
                    </table>
                  </div>
                  '''
                  
    return render_template_string(template, filename=filename)

@app.route('/delete/<filename>')
def delete_file(filename):
    #For security so people can't just delete any path, only in this file path
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