
## 说明：

1. 备份hmtl目录到html2，新建monitor 
2. 运行AutoRecovery.py  
3. 在html2文件内修改内容
4. 环境：python2.x
    
## 功能：

    1. html2内修改的内容会实时更新到html 
    2. html内恶意新增的文件会被移除并备份到monitor
    
## 使用:
`python AutoRecovery.py -s /tmp/html -t /var/www/html -m /tmp/monitor`
