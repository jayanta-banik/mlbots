echo "Restarting Gunicorn"
echo "[HTTPS]..."
sudo systemctl daemon-reload
sudo systemctl start app
sudo systemctl enable app
sudo systemctl restart app
echo "Restarting Nginx"
sudo systemctl restart nginx
echo "[HTTP]..."
sudo systemctl daemon-reload
sudo systemctl start app_http
sudo systemctl enable app_http
sudo systemctl restart app_http
sudo systemctl restart nginx
echo "**********Done**********"

