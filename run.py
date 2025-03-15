from flask import Flask,stream_with_context,request,make_response,render_template, redirect, url_for,send_file,url_for
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import MultipleFileField,TextAreaField,SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
import os,time,json,binascii,webbrowser
app=Flask(__name__)
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
config={"dir":"./data/",'code':"utf-8"}
def encode(string):
    return binascii.hexlify(string.encode(config['code']))
def decode(HEX):
    HEX = eval(HEX)
    return binascii.unhexlify(HEX).decode(config['code'])
class Form(FlaskForm):
    files = MultipleFileField(label='Upload')
    submit = SubmitField(label="上传")
class TextForm(FlaskForm):
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Send')

@app.route('/font', methods=['GET', 'POST'])
def copy_font():
    return "Get-WindowsCapability -Online | ? Name -like 'OpenSSH*'"
    with open(config['dir']+"b'746578742e747874'",'r') as f:
        r=f.read()
    return r
    form = TextForm()
    copied_text= "1"
    if form.validate_on_submit():
        text = form.text.data
        copied_text = json.dumps(text)
        return render_template('font_page.html', form=form,text=copied_text)
    return render_template('font_page.html', form=form,text=copied_text)
@app.route("/",methods=['GET','POST'])
def index():
    form = Form()
    if request.method=="POST":
        for f in request.files.getlist("files"):
            if len(f.filename)==0:
                return render_template('500.html')
            f.save(os.path.join(config['dir'], str(encode(f.filename))))
    file_list=os.listdir(config['dir'])
    return render_template('index.html',form=form,file_list=file_list,encode=encode,decode=decode)
@app.route("/download/<path:filename>",methods=['get'])
def downloader(filename):
    response = make_response(
        send_file(
            os.path.join(config['dir'],filename),
            as_attachment=True,
            attachment_filename=decode(filename)
            )
    )
    return response
@app.route("/remove/<path:filename>")
def remove(filename):
    try:
        os.remove(config['dir']+filename)
    except:
        pass
    return redirect(url_for("index"))
if __name__=="__main__":
    #webbrowser.open("http://127.0.0.1")
    app.run(host='0.0.0.0',port=80,threaded=True,debug=True)