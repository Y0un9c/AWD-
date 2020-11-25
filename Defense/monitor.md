
## 使用：

1. 备份/var/www/html目录到/tmp/html
2. 运行monitor.py  
3. 在/tmp/html文件内修改内容
4. 运行`python monitor.py -s /tmp/html -t /var/www/html -l /tmp/log -m /tmp/monitor`或 `python monitor.py -s /tmp/html`
    
## 功能：

1. /tmp/html内修改的内容会实时更新到html 
2. /var/www/html内恶意新增的文件会被移除并备份到monitor
3. 所有修改、删除、新增的操作均会记录进日志文件
    
## 说明：
1. 运行环境：python2.x
2. 参数说明：
    * -h 查看帮助
    * -s 源文件路径（备份的网站目录）
    * -t 目标文件地址（一般为/var/www/html）
    * -m 备份的被植入的文件（备份别人写上来的木马）
    * -l 日志文件位置
  -s参数是必须的，-m默认为'/tmp/monitor'、-l默认为/tmp/log、-t默认为/var/www/html
    
## 不足：
1. 使用XFTP，在/tmp/html中新建文件时，可能会在/var/www/html生成一个New File文件，只有重新运行脚本才能删除。
2. 实现的方法很傻逼。轻喷
