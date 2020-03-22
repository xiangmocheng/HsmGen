#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Benjamin

import os
import sys
import xlrd
import re
from enum import Enum
from HsmCodeGen import HdlGen
from HsmCodeGen import HdlGen_Enum
from HsmCodeGen import HdlGen_Value
from HsmCodeGen import initGen2
from HsmCodeGen import defGen
from HsmCodeGen import externDefGen

class MenuLevel(Enum):
    Root = 1
    Common = 2 #中间
    Leaf = 3
    Option = 4
    Quantity = 5
    Special = 6

class MenuColor(Enum):
    Red = 10
    Orange = 51
    Yellow = 13
    Green = 17
    LightBlue = 40
    Blank = 64

excel = 'LTCXXXX_L2_A3_MFP_MenuTree_Ver0.1_Rev002_200318.xls'
#excel = '\\LTCXXXX_L1_A3_MFP_4LineLCD_MenuTree_Ver0.1_Rev003_.xls'
languageH = 'LangString.h'
languageC = 'LangString.c'
menuH = 'mid.h'
#convertTableList = ['Copy','CopyHotKey']
#convertTableList = ['Phone Book']
convertTableList = ['CopyHotKey']
#convertTableList = ['Copy','ID Card Copy']

#punctuation = " '/.,%-/>\":"
punctuation = " '/.,%-/><\[\]\?\":"

#去掉字符串中的符号，变为ID
def String2ID(text):
    id = re.sub(r'[{}]+'.format(punctuation),'',text)
    return id

#查找字串对应的SID
# 输入参数s: 字符串
def findSID(s):
    for line in languageCList:            
        #if len(re.findall(s, line)) != 0:
        cstring = line[2:line.find(r'\0"')]
        cstring = cstring.replace('\\\"', '\"')
        if(s == cstring):
            s = line[line.index("//")+2:-1]
            return s
    return ''

#生成MenuStructure文件，其中包括MID, SID, MIDList
#XXXList[] = {MID_XXX,MID_XXX}
#MS_XXX = { MID_XXX, SID_XXX, XXXList};
#输入参数: IDList: 当前level所有item的ID，包括title
def genMSFile(IDList, SID):
    tID = IDList[0]
    if len(IDList) < 1:
        return None
    s1 = 'stMenuStruct MS_'+tID+' = { MID_'+tID+', '+ SID +', '+tID+'List};\n\n'
    s2 = 'eMenuID '+tID+'List['+str(len(IDList)-1)+'] = {\n'
    if len(IDList) == 1:
        s2 += '    MID_'+IDList[0]+',\n'
    else:
        for i in range(1, len(IDList)):
            s2 += '    MID_'+IDList[i]+',\n'
    s2 = s2[:-2]+'\n};\n'
    return s2+s1

#生成MenuEntry文件
#MenuType   DisplayPara CurValue	MinValue	MaxValue	ValueType	ValueId	ValueSubId
#title: tID: 当前项的ID
#menuEntry: 当前项的SID
def genMEntry(tID, SID, row):
    s = 'stMenuEntryInfo MEntry_' + tID + " = { MID_" + tID + ', ' + SID + ', '
    menuEntryInfo = currentSheet.row_values(row, infoCol, infoCol + 8)
    try:
        for item in menuEntryInfo:
            if item == '':
                s += '0, '
            else:
                if type(item) == float:
                    item = str(int(item))
                s += item + ', '
        s = s[:-2] + '};\n'
    except:
        print(item)
    return s

def genMEntryList(tID, MEntryList):
    s = '\n\nstMenuEntryInfo* '+tID+'MEntryList['+str(len(MEntryList))+'] = {\n'
    for mentry in MEntryList:
        s += '    '+mentry + ',\n'
    s = s[:-2] + '\n};\n'
    return s

def genMStructureList(tID, MStructureList):
    s = '\n\nstMenuStruct* '+tID+'MStructureList['+str(len(MStructureList))+'] = {\n'
    for mstructure in MStructureList:
        s += '    MS_'+mstructure + ',\n'
    s = s[:-2] + '\n};\n'
    return s

def genMIDList(MIDList):
    s = 'typedef enum {\n'
    for mid in MIDList:
        s += '    '+mid + ',\n'
    s = s[:-2] + '\n}eMenuID;\n'
    return s

#判断单元格是否为空
#不为空，返回值：True
#为空，返回值：False
def ifCellEmpty(cell):
    if cell.ctype != 6 and cell.ctype != 0:
        return True
    else:
        return False

#读取单元格并转化为字符串
def readCell(row, col):
    cell = currentSheet.cell(row, col)
    cell_value = cell.value
    if cell.ctype in (2,3) and int(cell_value) == cell_value:
        cell_value = int(cell_value)
    return str(cell_value)

#判断当前菜单级别，主要是判断当前列是否包括完整子项
#输入参数：row, col: 当前坐标位置，也就是title位置
#         nrows: 当前级别的范围
def findMenuLevel(row, col, nrows):
    #0. 颜色特殊处理
    xfx = currentSheet.cell_xf_index(row, col)
    xf = book.xf_list[xfx]
    bgx = xf.background.pattern_colour_index
    if(bgx == MenuColor.LightBlue.value):
        return MenuLevel.Special

    #0.1 读取menu type
    menuType = currentSheet.cell(row, infoCol).value
    if(menuType == 'QUANT_TYPE'):
        return MenuLevel.Quantity

    #1. 判断是否有下一级，如果没有，则为Option列
    subCell = currentSheet.cell(row + 1, col)
    for colIndex in range(col + 1, ncols): #go through next level position
        tmpCell = currentSheet.cell(row + 1, colIndex)
        if(tmpCell.value == subCell.value): #find same submenu
            #2. 在下一级找到了相同子项，
            #在当前列查找下一个title，如果有说明当前列还有下一级菜单（不全面，因为存在只有一个子项的菜单）
            titleCell = currentSheet.cell(row, col)
            for rowIndex in range(row + 1, nrows): #go through current level
                tmpCell = currentSheet.cell(rowIndex, col)
                if(tmpCell.value == titleCell.value): #find same title
                    return MenuLevel.Common

            #try to find leaf node
            # row colIndex -> row+1
            #3. 在判断子项的子项是否有下一级
            nextCellx = row + 2
            nextCell = currentSheet.cell(row + 2, colIndex)
            for leafIndex in range(colIndex + 1, ncols): #try to find next level 
                leafCell = currentSheet.cell(nextCellx, leafIndex)
                if(leafCell.value == nextCell.value): #find it, not leaf node
                    #print("It's not leaf node!")
                    return MenuLevel.Common
            return MenuLevel.Leaf
    return MenuLevel.Option

#查找上级菜单
def findUpperLevelItem(row, col):
    baseCell = currentSheet.cell(row, col)
    for colIndex in range(col - 1, 0, -1):
        tmpCell = currentSheet.cell(row, colIndex)
        if(tmpCell.value == baseCell.value):
            for rowIndex in range(row - 1, 0, -1):
                tmpCell = currentSheet.cell(rowIndex, colIndex)
                if ifCellEmpty(tmpCell) == False:
                    return (currentSheet.cell(rowIndex + 1, colIndex).value)
    return ''

#查找下级菜单的首项坐标
def findNextLevelItemBegin(row, col, nrows):
    if col + 2 >= ncols:
        return None
    for rowIndex in range(row, nrows - 1):
        baseCell = currentSheet.cell(rowIndex + 1, col)
        if ifCellEmpty(baseCell):
            for colIndex in range(col + 1, ncols): #try to find next level position
                tmpCell = currentSheet.cell(rowIndex + 1, colIndex)
                if(tmpCell.value == baseCell.value):
                    #print((row + 1, colIndex))
                    return (rowIndex + 1, colIndex)
    print("Don't find next level item")
    return None

#MID的规则：title = root + upper + self
#          sub = root + title + self
#查找当前Level的所有子项，非leaf节点
def findCurLevelItem(row, col, nrows):
    list = []
    MIDList = []
    SIDList = []
    AllMEntryContent = ''

    titleString = currentSheet.cell(row, col).value
    titleID = String2ID(titleString)
    titleSID = findSID(titleString)
    SIDList.append(titleSID)

    upperLevelItem = findUpperLevelItem(rowx, colx)
    if(upperLevelItem == ''):
        titleMID = titleID
        parentID = ''
    else:
        upperID = String2ID(upperLevelItem)
        parentID = upperID
        if(upperID == rootTitle):
            titleMID = rootTitle + '_' + titleID
        else:
            titleMID = rootTitle + '_' + upperID + '_' + titleID

    list.append(titleString)
    MIDList.append(titleMID)

    MEntryContent = genMEntry(titleMID, titleSID, row)
    MEntryList.append('MEntry_'+titleMID)
    MenuIDList.append('MID_'+titleMID)
    menuEntryF.write(MEntryContent)

    for rowIndex in range(row + 1, nrows): #
        curCell = currentSheet.cell(rowIndex, col)
        if ifCellEmpty(curCell) and curCell.value not in list: #found a new item
            #这里要找到excel中记录menu entry info对应的那一行
            tmpCell = currentSheet.cell(rowIndex, nextLevlItemPos[1])
            if curCell.value == tmpCell.value:
                subString = curCell.value
                subID = String2ID(subString)
                subSID = findSID(subString)
                SIDList.append(subSID)
                if rootTitle == titleID:
                    subMID = titleID + '_'+ subID
                else:
                    subMID = rootTitle + '_' + titleID + '_' + subID
                MIDList.append(subMID)
                list.append(subString)

                MEntryContent = genMEntry(subMID, subSID, rowIndex)
                MEntryList.append('MEntry_'+subMID)
                MenuIDList.append('MID_'+subMID)
                menuEntryF.write(MEntryContent)
                AllMEntryContent += MEntryContent

    print(MIDList)
    hdlPath = path + '\\'+MIDList[0]+'hdl.c'
    while os.path.exists(hdlPath):
        hdlPath = hdlPath[:-2]+'_1.c'
    with open(hdlPath,'w') as f:
        f.write('#include "hsm.h"\n#include "menu.h"\n#include "mid.h"\n#include "LangString.h"\n\n')
        MS = genMSFile(MIDList, titleSID)
        f.write(MS)
        f.write(AllMEntryContent)
        hdl = HdlGen(path, MIDList, SIDList, parentID)
        f.write(hdl)
        initF.write(initGen2(MIDList[0], parentID))
        if MS != None:
            menuSturctureF.write(MS)
            MStructureList.append(MIDList[0])

    return list

#查找当前Level的所有子项，leaf节点
def findLeafLevelItem(row, col, nrows):
    list = []
    MIDList = []
    SIDList = []
    AllMEntryContent = ''

    titleString = currentSheet.cell(row, col).value
    titleID = String2ID(titleString)
    titleSID = findSID(titleString)
    SIDList.append(titleSID)

    upperLevelItem = findUpperLevelItem(rowx, colx)
    if(upperLevelItem == ''):
        titleMID = titleID
        parentID = ''
    else:
        upperID = String2ID(upperLevelItem)
        parentID = upperID
        if(upperID == rootTitle):
            titleMID = rootTitle + '_' + titleID
        else:
            titleMID = rootTitle + '_' + upperID + '_' + titleID

    list.append(titleString)
    MIDList.append(titleMID)

    baseCell = currentSheet.cell(row + 1, col)
    for colIndex in range(col + 1, ncols): #try to find next level position
        tmpCell = currentSheet.cell(row + 1, colIndex)
        if(tmpCell.value == baseCell.value):
            for rowIndex in range(row + 1, nrows):
                leafCell = currentSheet.cell(rowIndex, colIndex)
                if ifCellEmpty(leafCell):
                    #0. 颜色特殊处理
                    xfx = currentSheet.cell_xf_index(rowIndex, colIndex)
                    xf = book.xf_list[xfx]
                    bgx = xf.background.pattern_colour_index
                    if(bgx == MenuColor.Orange.value):
                        continue
                    list.append(leafCell.value)
                    subString = leafCell.value
                    subID = String2ID(subString)
                    subSID = findSID(subString)
                    SIDList.append(subSID)
                    if rootTitle == titleID:
                        subMID = titleID + '_'+ subID
                    else:
                        subMID = rootTitle + '_' + titleID + '_' + subID
                    MIDList.append(subMID)

                    MEntryContent = genMEntry(subMID, subSID, rowIndex)
                    MEntryList.append('MEntry_'+subMID)
                    MenuIDList.append('MID_'+subMID)
                    menuEntryF.write(MEntryContent)
                    AllMEntryContent += MEntryContent

            hdlPath = path + '\\'+MIDList[0]+'hdl.c'
            while os.path.exists(hdlPath):
                hdlPath = hdlPath[:-2]+'_1.c'
            with open(hdlPath,'w') as f:
                f.write('#include "hsm.h"\n#include "menu.h"\n#include "mid.h"\n#include "LangString.h"\n\n')
                MS = genMSFile(MIDList, titleSID)
                f.write(MS)
                f.write(AllMEntryContent)
                hdl = HdlGen_Enum(path, MIDList, SIDList, parentID)
                f.write(hdl)
                initF.write(initGen2(MIDList[0], parentID))

                if MS != None:
                    menuSturctureF.write(MS)
                    MStructureList.append(MIDList[0])
                return list

def findQuantityLevelItem(row, col, nrows):
    list = []
    MIDList = []
    SIDList = []


    titleString = currentSheet.cell(row, col).value
    titleID = String2ID(titleString)
    titleSID = findSID(titleString)
    SIDList.append(titleSID)

    upperLevelItem = findUpperLevelItem(rowx, colx)
    if(upperLevelItem == ''):
        titleMID = titleID
        parentID = ''
    else:
        upperID = String2ID(upperLevelItem)
        parentID = upperID
        if(upperID == rootTitle):
            titleMID = rootTitle + '_' + titleID
        else:
            titleMID = rootTitle + '_' + upperID + '_' + titleID

    list.append(titleString)
    MIDList.append(titleMID)
    
    rangeCell = currentSheet.cell(row + 1, col)
    SIDList.append(findSID(rangeCell.value))
    for colIndex in range(col + 1, ncols): #try to find next level position
        tmpCell = currentSheet.cell(row + 2, colIndex)
        if ifCellEmpty(tmpCell):
            unitCell = currentSheet.cell(row + 2, colIndex+1)
            SIDList.append(findSID(unitCell.value))
            break

    hdlPath = path + '\\'+MIDList[0]+'hdl.c'
    while os.path.exists(hdlPath):
        hdlPath = hdlPath[:-2]+'_1.c'
    with open(hdlPath,'w') as f:
        f.write('#include "hsm.h"\n#include "menu.h"\n#include "mid.h"\n#include "LangString.h"\n\n')
        MS = genMSFile(MIDList, titleSID)
        f.write(MS)

        hdl = HdlGen_Value(path, MIDList, SIDList, parentID)
        f.write(hdl)
        initF.write(initGen2(MIDList[0], parentID))
        if MS != None:
            menuSturctureF.write(MS)
            MStructureList.append(MIDList[0])
        return list


#查找当前菜单的结束位置
#找到下一个title不是当前title的菜单，即结束（不全面）
#要考虑到当前列为选项:
#两行，在当前结束
#超过4行，肯定是选项
#4或者3行，向下读，读到相同结束，未读到相同，则为在当前结束
def findCurLevelEnd(row, col, nrows):
    subItemList = []
    titleCell = currentSheet.cell(row, col)
    subCell_1 = currentSheet.cell(row + 1, col)
    subCell_2 = currentSheet.cell(row + 2, col)
    subCell_3 = currentSheet.cell(row + 3, col)

    subCell_4 = currentSheet.cell(row + 4, col)

    #子项第二项为空，说明只有一个子项，在第三行结束
    if ifCellEmpty(subCell_2) == False:
        return row + 2

    #子项第四项不为空，说明超过4行，此列是选项，读到选项结束
    if ifCellEmpty(subCell_4) == True:
        for rowIndex in range(row + 5, nrows):
            tmpCell = currentSheet.cell(rowIndex, col)
            if ifCellEmpty(tmpCell) == False:
                return rowIndex

    #4或者3行，向下读，读到相同结束，未读到相同，则为在当前结束
    if ifCellEmpty(subCell_1):
        subItemList.append(subCell_1.value)
    if ifCellEmpty(subCell_2):
        subItemList.append(subCell_2.value)
    if ifCellEmpty(subCell_3):
        subItemList.append(subCell_3.value)

    row = row + 4

    while row < nrows: 
        tmpCell = currentSheet.cell(row, col)
        if ifCellEmpty(tmpCell):
            if(tmpCell.value == titleCell.value):
                tmpSubCell = currentSheet.cell(row+1, col)
                tmpSubCell_2 = currentSheet.cell(row+2, col)
                #title下的第一项不在sub item list 中，说明是同title的不同菜单，应该结束
                if tmpSubCell.value not in subItemList or tmpSubCell_2.value not in subItemList: 
                    return row - 1
                else:
                    if ifCellEmpty(currentSheet.cell(row+3, col)):
                        subItemList.append(currentSheet.cell(row+3, col).value)
                    row = row + 4
            else:
                return row - 1
        else:
            row = row + 1
    return nrows


if __name__ == '__main__':
    print("1")
    book = xlrd.open_workbook(os.path.join(os.getcwd() , excel), formatting_info = True)

    languageHFile = open(os.path.join(os.getcwd() , languageH))
    languageCFile = open(os.path.join(os.getcwd() , languageC))
    languageHList = languageHFile.readlines()
    languageCList = languageCFile.readlines()
    menuHFile = open(os.path.join(os.getcwd() , menuH), "w")


    names = book.sheet_names()      #get all sheet names
    #print(names)
    MenuIDList = []
    externDef = ''

    #遍历每个页签
    for name in names:
        if name in convertTableList:
            path = os.getcwd() + '\\' + name
            try:
                os.mkdir(path)
            except:
                print("folder exist")
            initF =  open(path +'\\'+name+'init.c','w')
            #file = open(name+".txt","w")
            menuSturctureF = open(name+"_MStructure.c","w")
            menuSturctureF.write('#include "menu.h"\n#include "LangString.h"\n\n')
            menuEntryF = open(name+"_MEntry.c","w")
            menuEntryF.write('#include "menu.h"\n#include "LangString.h"\n\n')
            print("[SheetInfo]current sheet: "+name+", index: "+str(names.index(name)))

            currentSheet = book.sheets()[names.index(name)] #get convert sheet index by name
            nrows = currentSheet.nrows  #get total row number
            ncols = currentSheet.ncols  #get total row number
            print("[SheetInfo]total rows: "+str(nrows)+", total cols: "+str(ncols))

            FirstRow = currentSheet.row_values(0) #读取一行的数据
            infoCol = FirstRow.index('MenuType') #menutype列
            ncols = FirstRow.index('MenuType') - 2 #定位菜单列的范围

            rootRowx = 2 #Root position
            rootColx = 1

            root = currentSheet.cell(rootRowx,rootColx)
            print(root.value)

            rowx = rootRowx
            colx = rootColx
            nextLevlItemPos = (0,0)
            nextLevlItemPos = findNextLevelItemBegin(rowx, colx, nrows) #每个Level应该只执行一次
            currentLevel = 1
            rootTitle = String2ID(root.value)
            MEntryList = []
            MStructureList = []

            while rowx < nrows:
                curCell = currentSheet.cell(rowx,colx)
                #print(curCell.value)
                if ifCellEmpty(curCell): #found a new item
                    curLevelEnd = findCurLevelEnd(rowx, colx, nrows)
                    #print(curLevelEnd)
                    menuLevel = findMenuLevel(rowx, colx, curLevelEnd)

                    if menuLevel == MenuLevel.Common: #try to find next level position
                        LevelMenu = findCurLevelItem(rowx, colx, curLevelEnd)
                    elif menuLevel == MenuLevel.Leaf:
                        #print("menu level is leaf")
                        LevelMenu = findLeafLevelItem(rowx, colx, curLevelEnd)
                    elif menuLevel == MenuLevel.Special:
                        print("menu level is special")
                        LevelMenu = []
                        LevelMenu.append(curCell.value)
                    elif menuLevel == MenuLevel.Quantity:
                        LevelMenu = findQuantityLevelItem(rowx, colx, curLevelEnd)
                    elif menuLevel == MenuLevel.Option:
                        #print("menu level option")
                        LevelMenu = []
                    if LevelMenu:
                        print(LevelMenu)

                    #file.write(str(LevelMenu)+"\n")
                    rowx = curLevelEnd
                else:
                    rowx = rowx + 1
                if(rowx >= nrows):
                    if(nextLevlItemPos != None):
                        rowx = nextLevlItemPos[0]
                        colx = nextLevlItemPos[1]
                        nextLevlItemPos = findNextLevelItemBegin(rowx, colx, nrows) #每个Level应该只执行一次
                        currentLevel += 1
                        print("currentLevel is: " + str(currentLevel))
            #file.close()
            initF.close()
            
            menuEntryF.write(genMEntryList(rootTitle, MEntryList))
            print(MStructureList)

            defGen(path, MStructureList)
            externDef = externDefGen(MStructureList)
            #initGen(MStructureList)

            menuSturctureF.write(genMStructureList(rootTitle, MStructureList))
            menuSturctureF.close()
            menuEntryF.close()
    with open(os.path.join(os.getcwd() , menuH + '.base')) as menuHBaseFile:
        menuHContent = menuHBaseFile.read()
    menuHFile.write(genMIDList(MenuIDList))
    menuHFile.write(menuHContent)
    menuHFile.write(externDef)
    menuHFile.close()

