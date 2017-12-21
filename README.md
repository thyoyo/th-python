```
nohup python /data/th_python/manage.py runserver -h 0.0.0.0 -p 5050 &

gunicorn -b "127.0.0.1:5000" -w 3 manage:app -D


mysql-connector 不同于 mysql-connector-python
执行pip search mysql-connector | grep --color mysql-connector-python
输出
mysql-connector-python-rf (2.1.3)        - MySQL driver written in Python
mysql-connector-python (2.0.4)           - MySQL driver written in Python
使用pip install mysql-connector-python-rf==2.2.2就可以了

# 升级
pip list --outdated #列出所有过期的库
import pip
from subprocess import call
for dist in pip.get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)

```
