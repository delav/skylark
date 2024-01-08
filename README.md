# skylark

是一个以功能组件的方式编写测试用例的、通用的、开源的、分布式自动化测试平台。 可以简单高效的编写自动化测试用例，轻松管理和维护自动化项目。
理论上可支持任何类型的自动化测试，包括接口测试、 集成测试、UI测试、数据库测试等。

想了解更多请查看项目文档：[skylark docs](https://delav.github.io/skylark-doc/)

### 部署启动

#### 1.安装依赖
```sh
pip install -r requirements.txt
```

#### 2.初始化数据库
```sh
# django初始化数据表
python manage.py makemigrations
python manage.py migrate

# 导入项目中的skylark.sql
mysql -u(username) -p(password)
source /path/skylark.sql
```

#### 3.启动django服务
```sh
python manage.py runserver 8080
```

#### 4.启动celery服务
```sh
celery -A skylark worker -n master.%h -l info
```

#### 5.启动celery beat
```sh
celery -A skylark beat -l info
```