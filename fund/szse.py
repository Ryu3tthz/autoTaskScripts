import json
import random
import re
import time
import os
import pdfplumber
import PyPDF2
import requests
import csv

# config
DEBUG = False
workPath = "./result"
MAXTRYTIMES = 10

timeStamp = int(time.time() * 1000)
currentDate = time.strftime("%Y-%m-%d", time.localtime())
if DEBUG:
    currentDate = "2024-05-14"
currentDateYYYYMMDD = time.strftime("%Y%m%d", time.localtime())


def getFundJSONList(
    startDate="2024-02-18", endDate=currentDate, queryWords="发售公告", type=""
) -> list:

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
        "channelCode": ["fundinfoNotice_disc"],
        "pageSize": 10,
        "pageNum": 1,
    }
    for i in range(MAXTRYTIMES):
        re = requests.post(requestQueryUrl, headers=header,
                           timeout=10, json=payload)
        if re.status_code == 200:
            break
        else:
            time.sleep(10)

    resultList = []
    responseJsonObject = json.loads(re.text)
    for item in responseJsonObject["data"]:
        resultList.append(item)
    return resultList


def setDir(date) -> None:
    path = workPath + "/" + date.replace("-", "")
    if not os.path.exists(path):
        os.makedirs(path)


def downloadPDF(fundObejct) -> str:
    downloadBaseUrl = "http://disc.static.szse.cn"
    downloadUrl = downloadBaseUrl + fundObejct["attachPath"].replace("//", "")
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
    if not os.path.exists(savePath):
        request = requests.get(downloadUrl, timeout=10)
        if request.status_code == 200:
            setDir(fundObejct["publishTime"][0:10].replace("-", ""))
            with open(savePath, "wb") as file:
                file.write(request.content)
                file.close()
        else:
            return ""
    return savePath


def pdf2txt(pdfPath) -> str:
    pdfFile = open(pdfPath, "rb")
    pdfReader = PyPDF2.PdfReader(pdfFile)
    text = ""
    for i in range(len(pdfReader.pages)):
        page = pdfReader.pages[i]
        text += page.extract_text().encode("UTF-8", "ignore").decode("UTF-8")
    pdfFile.close()

    return text


def saveTxt(txtPath, text) -> None:
    with open(txtPath, "w", encoding="utf-8") as file:
        file.write(text)
        file.close()


def readTxt(txtPath) -> str:
    with open(txtPath, "r", encoding="utf-8") as file:
        text = file.read()
        file.close()
        return text


def getTables(pdfFilePath) -> list:
    tables = []
    with pdfplumber.open(pdfFilePath) as pdf:
        for page in pdf.pages:
            tables.append(page.extract_tables())
    return tables


def searchTables(tables, keyWordList) -> list:
    result = []
    for rowIndex in range(len(tables) - 1):
        flag = False
        if len(tables[rowIndex]) != 0 and len(tables[rowIndex][0]) == 4:
            for keyWord in keyWordList:
                if (
                    keyWord in tables[rowIndex][0][0][0] or tables[rowIndex][0][0][1]
                ) and tables[rowIndex] not in result:
                    result.append(tables[rowIndex][0])
                    flag = True
                    break
        if (
            (len(tables[rowIndex]) == 1)
            and (len(tables[rowIndex + 1]) == 1)
            and (len(tables[rowIndex][0]) + len(tables[rowIndex + 1][0]) == 4)
        ):
            temp = tables[rowIndex][0] + tables[rowIndex + 1][0]
            for keyWord in keyWordList:
                if keyWord in temp[0][0][0] or temp[0][0][1]:
                    result.append(temp)
                    flag = True
                    break
        if flag:
            break
    return result


# TODO def checkFundRate():


def main():
    resultList = getFundJSONList()
    fundCount = 0
    for e in resultList:
        if (e["publishTime"][0:10] == currentDate) != DEBUG:
            fundCount += 1
    if DEBUG:
        print("DEBUG")
    print(str(currentDateYYYYMMDD) + "_SZ: " + str(fundCount) + " fund")
    newFundList = []
    codeList = []
    subscriptionList = []
    newFundTables = []
    for e in resultList:
        t = e["publishTime"][0:10]
        if (e["publishTime"][0:10] == currentDate) != DEBUG:
            path = downloadPDF(e)
            newFundTables.append(
                searchTables(getTables(path), ["认购份额", "认购金额", "认购费率"])
            )
            newFundList.append(e)
            code = e["secCode"][0]
            if not os.path.exists(path[0:-3] + "txt"):
                fundText = re.sub(r"[\s\n]+", "", pdf2txt(path))
                saveTxt(path[0:-3] + "txt", fundText)
            else:
                fundText = readTxt(path[0:-3] + "txt")
            codeList.append(code)
            if DEBUG:
                print(code, end=" ")
            pattern = re.compile(
                r"(.{5,20})(\d{4}年\d{1,2}月\d{1,2}日(?:起至|至)\d{1,4}年\d{1,2}月\d{1,2}日)"
            )  # 20
            matches = re.findall(pattern, fundText)
            for match in matches:
                if "网上现金" in match[0]:
                    if match[1] not in subscriptionList:
                        subscriptionList.append(match[1])
                    else:
                        print(code + ": O1")
                        break
    if fundCount != len(newFundTables) | fundCount != len(subscriptionList):
        print("Error!")
    else:
        if fundCount != 0:
            with open("fund.csv", "a") as file:
                writer = csv.writer(file, delimiter=",")
                for code in codeList:
                    writer.writerow(
                        [currentDateYYYYMMDD, "SH", code, currentDateYYYYMMDD, " "]
                    )
            file.close()
        print("START--------------------------------SZ")
        sampleString = ""
        for i in range(fundCount):
            title = newFundList[i]["title"]
            sampleString += (
                str(i + 1)
                + "、基金名称："
                + title[title.find("：") + 1: title.rfind("份额发售公告")].replace(
                    "基金基金", "基金"
                )
                + "\n"
                + "基金认购简称："
                + newFundList[i]["secName"][0]
                + "\n"
                + "基金认购代码："
                + codeList[i]
                + "\n发行市场：深圳\n发行时间："
                + subscriptionList[i]
                + "\n认购费率如下所示：\n\n"
                + str(newFundTables[i][0][0][0])
                + "          "
                + str(newFundTables[i][0][0][1])
                + "\n"
                + str(newFundTables[i][0][1][0])
                + "                "
                + str(newFundTables[i][0][1][1])
                + "\n"
                + str(newFundTables[i][0][2][0])
                + "        "
                + str(newFundTables[i][0][2][1])
                + "\n"
                + str(newFundTables[i][0][3][0])
                + "            "
                + str(newFundTables[i][0][3][1])
                + "\n\n"
            )
        print(sampleString, end="END--------------------------------SZ\n\n")


main()
