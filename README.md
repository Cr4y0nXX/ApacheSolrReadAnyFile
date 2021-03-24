# ApacheSolrReadAnyFile

Apache Solr <= 8.8.1 存在任意文件读取漏洞，可读取服务器任意文件和目录。

## Environment

------

Python：>= Python 3.7

OS：ALL

## Install

------

clone

```
git clone https://github.com/Cr4y0nXX/ApacheSolrReadAnyFile.git
```

or download zip

## POC

------

### 简述

使用多线程方式批量对目标url进行漏洞探测，并输出结果。

### Usage

```
ApacheSolrReadAnyFile_POC.py [-h] [-f FILE] [-T THREAD] [-t TIMEOUT] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The url file, default is ./url.txt   目标url文件，一行一个
  -T THREAD, --Thread THREAD
                        Number of thread, default is 32   线程数，默认32
  -t TIMEOUT, --timeout TIMEOUT
                        request timeout(default 3)   请求超时，默认3秒
  -o OUTPUT, --output OUTPUT
                        Vuln url output file, default is
                        ./2021-03-24_11-10-20.txt   输出所有存在漏洞的url，默认以当前时间为文件名
```

所有参数均为可选参数，都有默认值，但必须有目标url文件，一行一个目标地址。

### 演示

```
python ApacheSolrReadAnyFile_POC.py -f ./url1.txt -T 32
```

![image](README.assets/image-20210324110302152.png)

700多个目标，使用32线程情况下2分钟即可扫完

![image](README.assets/image-20210324110917437.png)

## EXP

------

单线程的方式，每次对一个目标进行验证和利用，若存在漏洞可输入文件或路径得到结果。

### Usage

```
ApacheSolrReadAnyFile_EXP.py [-h] -u URL [-t TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The target address, (ip:port) or url    指定目标url
  -t TIMEOUT, --timeout TIMEOUT
                        request timeout(default 3)    指定请求超时，默认3秒
```

-u为必选参数。

### 演示

```
python ApacheSolrReadAnyFile_EXP.py -u 1*****3:8983
```

![image](README.assets/image-20210324111756267.png)

也可输入目录，得到目录下所有文件。