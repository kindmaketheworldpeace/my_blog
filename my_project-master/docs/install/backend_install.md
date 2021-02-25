# 本地启动后端项目

## 系统要求

- 数据库：mysql
- Python版本: python2.7 (务必使用python2.7, 推荐2.7.15)

## 安装说明

#### 1.安装requirements.txt文件中的python包
    pip install -r requirements.txt
#### 2.数据库初始化： 本模版工程的具体使用过程如下：
    manage.py migrate    (初始化数据库表)
#### 3.在项目文件夹同级的目录里建立logs文件夹（如不清楚可以直接runserver后看错误提示信息）
#### 4.在conf/default.py中，配置BK_PAAS_HOST的地址
    # 蓝鲸智云开发者中心的域名
    BK_PAAS_HOST = 'http://paas.szbke.com'
#### 5.在template/index.html里配置本地环境下启动的域名和端口
    // 本地开发环境访问url
    window.siteUrl = "http://dev.szbke.com:8001/"
    # 注意本地启动域名的根域名需要和蓝鲸根域名一致，端口自定义（只要端口不冲突即可）
#### 6.修改本地hosts
假设配置`window.siteUrl`为`http://dev.szbke.com:8001/`, 部署机器IP为`127.0.0.1`
    
    127.0.0.1 dev.szbke.com
#### 7.启动项目
    python manage.py runserver dev.szbke.com:8001
#### 8.访问
    http://dev.szbke.com:8001
    
    
