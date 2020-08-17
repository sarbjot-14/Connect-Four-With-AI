"""
https://linuxize.com/post/how-to-install-flask-on-ubuntu-18-04/
"""
"""
in root app:
export FLASK_APP=run.py
export FLASK_ENV=development

pip install -r requirements.txt

all that was needed in virtual machine is 
sudo apt install python3-flask

cd app

export FLASK_APP=run.py

flask run --host=0.0.0.0

app.run(host= '0.0.0.0')



sudo rm -rf /usr/lib/python3/dist-packages/flask 

ssh -p24 -C sarbjots@csil-cpu8.csil.sfu.ca

"""

from app import app

if __name__ == "__main__":
    #app.run()
    #app.run(host= '0.0.0.0')
    app.run(host='0.0.0.0', port=80, debug=True)
