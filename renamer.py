'''
@Author       : Primimy
@Date         : 2020-07-25 06:41:49
'''
import glob
import os
import os.path
UpperMax = 3
os.system("")
sourceFile = input("\033[32;1mSourceFile:\033[0m ").strip('"')
targetFile = input("\033[32;1mTargetFile:\033[0m ").strip('"')
suffix = input("\033[32;1msuffix(default: .ass):\033[0m ")
suffix = '.ass' if suffix == '' else suffix
sourceFolder, targetFolder = sourceFile[:sourceFile.rfind('\\') + 1], targetFile[:targetFile.rfind('\\') + 1]
sourceFiles = [f for f in glob.glob(glob.escape(sourceFolder)+"*.ass")]
targetFiles = [f for f in glob.glob(glob.escape(sourceFolder)+"*.mkv")]
sourceFileName, targetFileName = sourceFile.split('\\')[-1], targetFile.split('\\')[-1]
sourceFileSignString, targetFileSignString = sourceFileName[:sourceFileName.find('01')], targetFileName[:targetFileName.find('01')]
tempS = [s for s in sourceFiles if s.find(sourceFileSignString) != -1]
tempT = [t[:t.rfind('.')]+suffix for t in targetFiles if t.find(targetFileSignString) != -1]
tempS.sort()
tempT.sort()
for s, t in zip(tempS, tempT):
    print(s, '    ', t)
    # os.rename(s,t)
