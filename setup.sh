echo "updating linux..."
sleep 2
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y

echo "downloading drivers and kernals..."
sleep 2
sudo apt-get install libhdf5-dev libc-ares-dev libatlas-base-dev libeigen3-dev python3-pip python3-dev python3-venv python3-opencv git nginx -y

echo "creating directory and venv"
sleep 1
mkdir mlbots
ls
cd mlbots
mkdir auths libs static records 
ls
python3 -m venv venv3
source venv3/bin/activate

echo "installing python libraries..."
sleep 2
pip install --upgrade setuptools
pip install gunicorn flask numpy pandas matplotlib flask_cors yagmail opencv-python
pip install tflite-runtime

# <---------------- copy to file ---------------->
echo "creating app..."
sleep 2
printf "
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return \"Hello World!\"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
" >> app.py

# <------------- end of copy to file ------------->

# python app.py

# <---------------- copy to file ---------------->
echo "creating gunicorn bridge..."
sleep 2
printf "
from app import app

if __name__ == '__main__':
    app.run()
" >> wsgi.py
# <------------- end of copy to file ------------->

# gunicorn --bind 0.0.0.0:5000 wsgi:app

deactivate

# sudo nano /etc/systemd/system/app.service

# <---------------- copy to file ---------------->
echo "creating service..."
sleep 2
sudo printf "
[Unit]

Description=Gunicorn instance to serve myproject
After=network.target

[Service]

User=pi
Group=www-data

WorkingDirectory=/home/pi/mlbots/
Environment=\"PATH=/home/pi/mlbots/venv3/bin\"
ExecStart=/home/pi/mlbots/venv3/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 wsgi:app

[Install]

WantedBy=multi-user.target
" | sudo tee /etc/systemd/system/app.service
# <------------- end of copy to file ------------->

sudo systemctl start app
sudo systemctl enable app
sleep 2
ls
sleep 4

# sudo nano /etc/nginx/sites-available/app

# <---------------- copy to file ---------------->
echo "creating server node"
sleep 2
sudo printf "
server {
    listen 80;
    server_name server_domain_or_IP;

location / {
  include proxy_params;
  proxy_pass http://unix:/home/pi/mlbots/app.sock;
    }
}
" | sudo tee /etc/nginx/sites-available/app

# <------------- end of copy to file ------------->

sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-available/default
sudo rm /etc/nginx/sites-enabled/default

echo "creating restart checkpoint..."
sleep 2
printf "
echo \"restarting http\"
sudo systemctl daemon-reload
sudo systemctl start app
sudo systemctl enable app
sudo systemctl restart app
sudo systemctl restart nginx
echo \"done\"
" >> rg

sudo chmod +x rg
./rg

sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
echo "completed!!"

for i in {10..0..-1}
do
echo -ne "System will restart in $i    \r"
sleep 1
done

sudo reboot


