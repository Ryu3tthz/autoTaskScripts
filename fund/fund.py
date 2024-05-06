import json
import math
import random
import re
import time
import urllib.parse
import os
import pdfplumber
import PyPDF2
import requests


class Fund:

    def __init__(self, startDate="2021-04-12", queryWords="发售公告", queryType="all",workPath = "./result") -> None:
        self.startDate = startDate
        self.currentDate = time.strftime("%Y-%m-%d", time.localtime())
        self.queryWords = queryWords
        if queryType in ["sse", "szse"]:
            self.queryType = queryType
        else:
            self.queryType = "all"
        self.workPath = workPath
        self.timeStamp = int(time.time() * 1000)
        self.fundJSONObjects,self.fundJSONObjectsFiltered = {"sse":[],"szse":[]},{"sse":[],"szse":[]}
        if not os.path.exists(self.workPath):
            os.makedirs(self.workPath)
        self.currentDayPath = self.workPath + "/" + self.currentDate.replace("-", "")
        if not os.path.exists(self.currentDayPath):
            os.makedirs(self.currentDayPath)

    def _getFundJSONObjects(self) -> None:
        jsonpCallbackNum = math.floor(
            random.uniform(0.1, 1) * (100000000 + 1))
        requestQueryUrl = {
            "sse":
            ("http://query.sse.com.cn/commonQuery.do?"
             + "jsonCallBack=jsonpCallback"
             + str(jsonpCallbackNum)
             + "&isPagination=true&pageHelp.pageSize=50&pageHelp.pageNo=1&pageHelp.  beginPage=1&pageHelp.cacheSize=2&pageHelp.endPage=1&type=inParams&sqlId=COMMON_PL_JJXX_JJGG_NEW_L"
             + "&TITLE="
             + urllib.parse.quote(self.queryWords)
             + "&SECURITY_CODE=& BULLETIN_TYPE=reits01%2Cfund01%2Creits02%2Cfund02%2Creits03%2Cfund03%2Creits04%2Cfund04%2Creits05%2Cfund05%2Creits06%2Cfund06"
             + "&START_DATE="
             + self.startDate
             + "&END_DATE="
             + self.currentDate
             + "&DATE_DESC=1&DATE_ASC=&CODE_DESC=&CODE_ASC=&OTHER_TYPE=&_="
             + str(self.timeStamp)),

            "szse": "http://www.szse.cn/api/disc/announcement/annList?random="
            + str(random.uniform(0.1, 1))
        }
        header = {
            "sse": {
        "Accept": """*/*""",
        "Accept-Encoding": """gzip, deflate""",
        "Accept-Language": """zh-CN,zh;q=0.9""",
        "Connection": """keep-alive""",
        # "Cookie": '''ba17301551dcbaf9_gdp_session_id=73999a7f-cb73-4d50-a9ac-b69e5a92b681;    gdp_user_id=gioenc-e4c45632%2C3e1b%2C59bd%2Cc3bb%2C9ad4d89g9340;   ba17301551dcbaf9_gdp_session_id_sent=73999a7f-cb73-4d50-a9ac-b69e5a92b681;    ba17301551dcbaf9_gdp_sequence_ids= {%22globalKey%22:66%2C%22VISIT%22:2%2C%22PAGE%22:10%2C%22VIEW_CLICK%22:37%2C%22VIEW_CHANGE   %22:6%2C%22CUSTOM%22:15}''',
        "DNT": """1""",
        "Host": """query.sse.com.cn""",
        "Referer": """http://www.sse.com.cn/""",
        "User-Agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,   like Gecko) Chrome/118.0.0.0 Safari/537.36""",
        },
            "szse":{
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        # "Content-Length": "106",
        "Content-Type": "application/json",
        "DNT": "1",
        "Host": "www.szse.cn",
        "Origin": "http://www.szse.cn",
        "Referer": "http://www.szse.cn/disclosure/fund/etf/index.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "X-Request-Type": "ajax",
        "X-Requested-With": "XMLHttpRequest",
        }
        }
        payload = {
            "sse":"",
            "szse":{
            "seDate": [self.startDate, self.currentDate],
            "searchKey": [self.queryWords],
            "channelCode": ["etfNotice_disc"],
            "pageSize": 50,
            "pageNum": 1}
        }

        try:
            request = requests.get(
                requestQueryUrl[self.queryType],
                headers=header[self.queryType],
                json=payload[self.queryType],
                timeout=10,
            )
        except requests.exceptions.RequestException as e:
            print(e)
        if request.status_code == 200:
            response = request.text
            if self.queryType == "sse":
                responseJsonObject = json.loads(
                    response[response.find("{") : response.rfind("}") + 1]
                )
                for o in responseJsonObject["result"]:
                    self.fundJSONObjects["sse"].append(o)
            if self.queryType == "szse":
                responseJsonObject = json.loads(request.text)
                for o in responseJsonObject["data"]:
                    self.fundJSONObjects["szse"].append(o)
        else:
            print("Request failed")

    def getFundJSONObjects(self)-> dict:
        return self.fundJSONObjects

    def _fundFilter(self,date) -> None:
        for o in self.fundJSONObjects["sse"]:
            if o["SSEDATE"] == date:
                self.fundJSONObjectsFiltered["sse"].append(o)
        for o in self.fundJSONObjects["szse"]:
            if o["publishTime"] == date:
                self.fundJSONObjectsFiltered["szse"].append(o)

    def fundFilter(self) -> int:
        self._fundFilter(self.currentDate)
        return len(self.fundJSONObjectsFiltered)

    def _downloadPDF(self,_type,isCurrentDate = True) -> None:
        downloadBaseUrl = {
            "sse": "http://www.sse.com.cn",
            "szse": "http://disc.static.szse.cn"
        }
        request = requests.get(downloadBaseUrl[_type] + self.fundJSONObjectsFiltered[_type]["URL" if _type == "sse" else "attachPath"].replace("//", ""), timeout=10)
        savePath = (workPath + "/" + fundObejct["SSEDATE"].replace("-", "") +
                    "/" + fundObejct["SECURITY_CODE"] + "_" +
                    fundObejct["SSEDATE"].replace("-", "") + "_" +
                    fundObejct["TITLE"] + ".pdf")

    def downloadPDF(self)->None:
        if self.type != "all":
            self._downloadPDF(self.type)
        else:
            self._downloadPDF("sse")
            self._downloadPDF("szse")
    downloadBaseUrl = "http://www.sse.com.cn"
    downloadUrl = downloadBaseUrl + fundObejct["URL"].replace("//", "")
    request = requests.get(downloadUrl, timeout=10)
    if request.status_code == 200:
        savePath = (
            workPath
            + "/"
            + fundObejct["SSEDATE"].replace("-", "")
            + "/"
            + fundObejct["SECURITY_CODE"]
            + "_"
            + fundObejct["SSEDATE"].replace("-", "")
            + "_"
            + fundObejct["TITLE"]
            + ".pdf"
        )
        setDir(fundObejct["SSEDATE"])
        with open(savePath, "wb") as file:
            file.write(request.content)
            file.close()
        return savePath
    return ""
# TODO