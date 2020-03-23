## Youtube Info Portal


**Tools And Technology Used**

1. Python3
2. Django
3. Django Rest Framework
4. MySql

**Notes**

* I am asuming that you already installed Python3, Git and MySql(5.7) in you system.
* You can run this project by simply downloading and executing `run.sh` script.
* Create a `env.py` as like as `example_env.py`.
* You have a database with same credentials as in `env.py`. If not then configure your own `env.py` file.
* Please execute `python manage.py run-data-loader` to scrap and seed initial data.
* Please execute `python manage.py run-auto-updater` to start auto update feature.

 

**Bash File Execution Command**
> **`bash run.sh`**
> 

**Manually Project Execution Commands**
> **`pip install -r requirements.txt`**
>
> **`python manage.py makemigrations`**\
> **`python manage.py migrate`**
>
> **`python manage.py run-data-loader`**
>
> **`python manage.py runserver`**
> 

**Project Testing Execution Command**
> **`python manage.py test`**
> 
>

**Sample API Urls**

- [127.0.0.1:8000/yutube-info/api/v1/videos/videos-details-data/?tags=zoo&performance=1](127.0.0.1:8000/yutube-info/api/v1/videos/videos-details-data/?tags=zoo&performance=1)

- [127.0.0.1:8000/yutube-info/api/v1/videos/videos-details-data/?tags=zoo](127.0.0.1:8000/yutube-info/api/v1/videos/videos-details-data/?tags=zoo)

- [127.0.0.1:8000/yutube-info/api/v1/videos/videos-details-data/?performance=1](127.0.0.1:8000/yutube-info/api/v1/videos/videos-details-data/?performance=1)

