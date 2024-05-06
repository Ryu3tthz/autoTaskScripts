import json
import math
import random
import re
import time
import urllib.parse

import pdfplumber
import PyPDF2
import requests

# config
DEBUG = True
workPath = "./fund/result"

jsonpCallbackNum = math.floor(random.uniform(0.1, 1) * (100000000 + 1))
timeStamp = int(time.time() * 1000)
currentDate = time.strftime("%Y-%m-%d", time.localtime())
currentDateYYYYMMDD = time.strftime("%Y%m%d", time.localtime())


def getFundJSONList(startDate="2021-04-12", endDate=currentDate, queryWords="发售公告"):

    # requestBaseUrl = "http://www.sse.com.cn/disclosure/fund/announcement/json/fund_bulletin_publish_order.json"
    # downloadBaseUrl = "http://www.sse.com.cn"
    requestQueryBaseUrl = "http://query.sse.com.cn/commonQuery.do?"
    requestQueryString1 = "jsonCallBack=jsonpCallback" + str(jsonpCallbackNum)
    requestQueryString2 = "&isPagination=true&pageHelp.pageSize=50&pageHelp.pageNo=1&pageHelp.  beginPage=1&pageHelp.cacheSize=2&pageHelp.endPage=1&type=inParams&sqlId=COMMON_PL_JJXX_JJGG_NEW_L"
    requestQueryString3 = "&TITLE=" + urllib.parse.quote(queryWords)
    requestQueryString4 = "&SECURITY_CODE=& BULLETIN_TYPE=reits01%2Cfund01%2Creits02%2Cfund02%2Creits03%2Cfund03%2Creits04%2Cfund04%2Creit   s05%2Cfund05%2Creits06%2Cfund06"
    requestQueryString5 = (
        "&START_DATE="
        + startDate
        + "&END_DATE="
        + endDate
        + "&DATE_DESC=1&DATE_ASC=&CODE_DESC=&CODE_ASC=&OTHER_TYPE=&_="
        + str(timeStamp)
    )

    requestQueryUrl = (
        requestQueryBaseUrl
        + requestQueryString1
        + requestQueryString2
        + requestQueryString3
        + requestQueryString4
        + requestQueryString5
    )

    header = {
        "Accept": """*/*""",
        "Accept-Encoding": """gzip, deflate""",
        "Accept-Language": """zh-CN,zh;q=0.9""",
        "Connection": """keep-alive""",
        # "Cookie": '''ba17301551dcbaf9_gdp_session_id=73999a7f-cb73-4d50-a9ac-b69e5a92b681;    gdp_user_id=gioenc-e4c45632%2C3e1b%2C59bd%2Cc3bb%2C9ad4d89g9340;   ba17301551dcbaf9_gdp_session_id_sent=73999a7f-cb73-4d50-a9ac-b69e5a92b681;    ba17301551dcbaf9_gdp_sequence_ids= {%22globalKey%22:66%2C%22VISIT%22:2%2C%22PAGE%22:10%2C%22VIEW_CLICK%22:37%2C%22VIEW_CHANGE   %22:6%2C%22CUSTOM%22:15}''',
        "DNT": """1""",
        "Host": """query.sse.com.cn""",
        "Referer": """http://www.sse.com.cn/""",
        "User-Agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,   like Gecko) Chrome/118.0.0.0 Safari/537.36""",
    }
    re = requests.get(requestQueryUrl, headers=header, timeout=10)

    resultList = []
    if re.status_code == 200:
        response = re.text
        indexL = response.find("{")
        indexR = response.rfind("}") + 1
        responseStr = response[indexL:indexR]
        responseJsonObject = json.loads(responseStr)
        for item in responseJsonObject["result"]:
            resultList.append(item)
    return resultList


def setDir(date):
    import os

    path = workPath + "/" + date.replace("-", "")
    if not os.path.exists(path):
        os.makedirs(path)


def downloadPDF(fundObejct):
    downloadBaseUrl = "http://www.sse.com.cn"
    downloadUrl = downloadBaseUrl + fundObejct["URL"].replace("//", "")
    request = requests.get(downloadUrl, timeout=10)
    if request.status_code == 200:
        savePath = (
            workPath
            + "/"
            + fundObejct["SSEDATE"].replace("-", "")
            + "/SH_"
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
for e in resultList:
    if (e["SSEDATE"] == currentDate) != DEBUG:
        fundCount += 1
        path = downloadPDF(e)
        newFundTables = searchTables(getTables(path), ["认购份额"])
        newFundList.append(e)
        code = e["SECURITY_CODE"]
        fundText = pdf2txt(path).replace("\n", "")
        allCodeMatches = re.findall(re.compile(code[0:-1] + "[0-9]"), fundText)
        for i in allCodeMatches:
            if i != code:
                codeList.append(i)
        pattern = re.compile(
            r"网上现金认购的.+?(\d{4}年\d{1,2}月\d{1,2}日至\d{1,4}年\d{1,2}月\d{1,2}日)"
        )
        if DEBUG:
            print(code, end=" ")
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
            + newFundList[i]["TITLE"].replace("基金份额发售公告", "")
            + "\n"
            + "基金认购简称："
            + newFundList[i]["FUND_EXPANSION_ABBR"]
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
