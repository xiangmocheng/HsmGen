'''
Created on 2020年2月24日

@author: AmberLi
'''
import xlrd
import re
import os
import time

punctuation = " '/.,%-/><\[\]\?\":"
lineList = []
HList = []
file = 'LTCXXXX_L2_A3_MFP_MenuTree_Ver0.1_Rev002_200318.xls'
#file = 'LTCXXXX_L1_A3_MFP_4LineLCD_MenuTree_Ver0.1_Rev003_.xls'

CFileHead = '#include "type.h"\n#include <wchar.h>\n\nwchar_t wstringTableEng[]={\n'
CFileEnd = '};\n\ntUint32 strTableSize = sizeof(wstringTableEng);\n'

HFileHead = '#ifndef __LANGSTRING_H_\n#define __LANGSTRING_H_\n\n#include "type.h"\n\n\
extern wchar_t wstringTableEng[];\nextern tUint32 strTableSize;\n\n\
typedef enum STRING_ID\n{\n'
HFileEnd = 'SID_MaxStringCount\n} STRING_ID;\n\n#endif'

def removePunctuation(text):
    try:
        text = re.sub(r'[{}]+'.format(punctuation),'',text)
        return text.strip()
    except Exception as e:
        print("error: "+ str(e))

def symbolHandle(s):
    if s == '-     +':
        return 'MinusPlus'
    if s == '***':
        return '3Stars'
    if s == '%':
        return 'percent'
    return s

def readexcel(path,CFile,HFile):
       
    workbook = xlrd.open_workbook(path, formatting_info=True) #打开此地址下的exl文档
    print (workbook.sheet_names()) 
    #sheet1 = workbook.sheet_by_name('Copy')  #进入第n张表

    #选取sheet的范围
    startSheet = 3
    endSheet = 4
        
    for s in range(startSheet,endSheet):   #遍历sheet
        sheet1 = workbook.sheets()[s]  #进入第n张表

        nrows = sheet1.nrows  #get total row number
        ncols = sheet1.ncols  #get total row number
        print("[SheetInfo]total rows: "+str(nrows)+", total cols: "+str(ncols))

        FirstRow = sheet1.row_values(0) #读取一行的数据
        #infoCol = FirstRow.index('MenuType') #menutype列
        ncols = FirstRow.index('MenuType') - 2 #定位菜单列的范围
        
        for m in range(ncols):
            old_List=sheet1.col_values(m)  #获取第n列的内容
            max_row=len(old_List)
        
            for i in range(max_row):
                #获取单元格字体颜色
                xf_idx  = sheet1.cell_xf_index(i,m)
                xf_list = workbook.xf_list[xf_idx]    
                f = workbook.font_list[xf_list.font_index]
                color = workbook.colour_map[f.colour_index]
                #print(color)
                #动态或者不确定的字符串背景定义为红色，不会取值
                #如果已有，则退出for循环，不增加重复数据
                if color == (255, 0, 0) or old_List[i] in lineList or old_List[i] == '':
                    continue
                else:
                    print(old_List[i])
                    covString = str(old_List[i])
                    h = symbolHandle(covString)
                    h = removePunctuation(h) #remove other chars for macro define in H file
                    c = covString.strip()
                    c = c.replace('\"\"','\"') #modify "" to \", the final string in C file
                    c = c.replace('\"','\\\"') #modify "" to \", the final string in C file
                    if c != '' and c not in lineList: 
                        lineList.append(c)
                        h = 'SID_'+h
                        if h in HList:
                            h = h+'_2'
                        HList.append(h)
                        
                        Hline = h+',\t//"'+c+'"'+'\n'
                        Cline = 'L"'+c+'\\0"\t//'+h+'\n'
                        HFile.write(Hline)
                        CFile.write(Cline) 


if __name__ == '__main__':
    start = time.time()
    path = os.getcwd()
    print(path)
    CFile = open("LangString.c",'w')
    HFile = open("LangString.h",'w')
    CFile.write(CFileHead)
    HFile.write(HFileHead)

    readexcel(file,CFile,HFile)

    CFile.write(CFileEnd)
    HFile.write(HFileEnd)
    CFile.close()
    HFile.close()
    end = time.time()
    print("Time used:",end-start)