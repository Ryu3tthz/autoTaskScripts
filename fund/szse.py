import json
import random
import re
import time

import pdfplumber
import PyPDF2
import requests

# config
DEBUG = True
workPath = "./fund/result"

timeStamp = int(time.time() * 1000)
currentDate = time.strftime("%Y-%m-%d", time.localtime())
currentDateYYYYMMDD = time.strftime("%Y%m%d", time.localtime())


def getFundJSONList(
    startDate="2021-04-12", endDate=currentDate, queryWords="发售公告", type=""
):

    requestQueryUrl = "http://www.szse.cn/api/disc/announcement/annList?random=" + str(
        random.uniform(0.1, 1)
    )

    header = {
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
    payload = {
        "seDate": [startDate, endDate],
        "searchKey": [queryWords],
        "channelCode": ["etfNotice_disc"],
        "pageSize": 50,
        "pageNum": 1,
    }
    request = requests.post(
        requestQueryUrl, headers=header, json=payload, timeout=10)

    resultList = []
    if request.status_code == 200:
        response = request.text
        responseJsonObject = json.loads(request.text)
        for item in responseJsonObject["data"]:
            resultList.append(item)
    return resultList


def setDir(date):
    import os

    path = workPath + "/" + date.replace("-", "")
    if not os.path.exists(path):
        os.makedirs(path)


def downloadPDF(fundObejct):
    downloadBaseUrl = "http://disc.static.szse.cn"
    downloadUrl = downloadBaseUrl + fundObejct["attachPath"].replace("//", "")
    request = requests.get(downloadUrl, timeout=10)
    if request.status_code == 200:
        savePath = (
            workPath
            + "/"
            + fundObejct["publishTime"][0:10].replace("-", "")
            + "/SZ_"
            + fundObejct["secCode"][0]
            + "_"
            + fundObejct["publishTime"][0:10].replace("-", "")
            + "_"
            + fundObejct["title"]
            + ".pdf"
        )
        setDir(fundObejct["publishTime"][0:10].replace("-", ""))
        with open(savePath, "wb") as file:
            file.write(request.content)
            file.close()
        return savePath
    return ""


def pdf2txt(pdfPath):
    pdfFile = open(pdfPath, "rb")
    pdfReader = PyPDF2.PdfReader(pdfFile)
    text = ""
    for i in range(len(pdfReader.pages)):
        page = pdfReader.pages[i]
        text += page.extract_text().encode("UTF-8", "ignore").decode("UTF-8")
    pdfFile.close()

    return text


def saveTxt(txtPath, text):
    with open(txtPath, "w", encoding="utf-8") as file:
        file.write(text)
        file.close()


def getTables(pdfFilePath):
    tables = []
    with pdfplumber.open(pdfFilePath) as pdf:
        for page in pdf.pages:
            tables.append(page.extract_tables())
    return tables


def searchTables(tables, keyWordList):
    result = []
    for keyWord in keyWordList:
        for table in tables:
            for row in table:
                if len(row) != 4:
                    continue
                for cells in row:
                    if len(cells) != 0:
                        for cell in cells:
                            if cell is not None:
                                if (keyWord in cell) and (row not in result):
                                    result.append(row)
    return result


resultList = getFundJSONList()
fundCount = 0
newFundList = []
codeList = []
subscriptionList = []
newFundTables = []
for e in resultList:
    t = e["publishTime"][0:10]
    if (e["publishTime"][0:10] == currentDate) != DEBUG:
        fundCount += 1
        path = downloadPDF(e)
        newFundTables = searchTables(getTables(path), ["认购份额"])
        newFundList.append(e)
        code = e["secCode"][0]
        fundText = pdf2txt(path).replace("\n", "")
        codeList.append(code)
        if DEBUG:
            print(code, end=" ")
        pattern = re.compile(
            r"网上现金认购的日期为.+?(\d{4}年\d{1,2}月\d{1,2}日至\s+\d{1,4}年\d{1,2}月\d{1,2}日)"
        )
        matches = re.findall(pattern, fundText)
        for match in matches:
            if match not in subscriptionList:
                subscriptionList.append(match)
if fundCount != len(newFundTables):
    print("Error!")
else:
    print(fundCount)
    sampleString = ""
    for i in range(fundCount):
        sampleString += (
            str(i + 1)
            + "、基金名称："
            + newFundList[i]["title"].replace("基金份额发售公告", "")
            + "\n"
            + "基金认购简称："
            + newFundList[i]["secName"][0]
            + "\n"
            + "基金认购代码："
            + codeList[i]
            + "\n发行市场：上海\n发行时间："
            + subscriptionList[i]
            + "\n认购费率如下所示：\n\n"
            + str(newFundTables[i][0][0])
            + "          "
            + str(newFundTables[i][0][1])
            + "\n"
            + str(newFundTables[i][1][0])
            + "                "
            + str(newFundTables[i][1][1])
            + "\n"
            + str(newFundTables[i][2][0])
            + "        "
            + str(newFundTables[i][2][1])
            + "\n"
            + str(newFundTables[i][3][0])
            + "            "
            + str(newFundTables[i][3][1])
            + "\n"
        )

    print(sampleString, end="")
