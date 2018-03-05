cd /home/zhx/FPproject
/home/zhx/FPproject/env/bin/gunicorn -w4 -D wsgi

ps aux |grep gunicorn|grep FPproject|grep -v grep


