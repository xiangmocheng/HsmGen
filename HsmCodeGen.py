#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Benjamin

import os
import sys
import xlrd

'''
从menuStructure文件生成太困难
应该在生成menuStructure的同时生成对应code
需要生成:
1. 定义
2. init函数
3. hdl函数
'''
#生成def
def defGen(path, MSList):
    code = ''
    for item in MSList:
        code += 'HSM_STATE OPS_State'+item+';\n'
    with open(path +'\\'+MSList[0]+'def.c','w') as f:
        f.write(code)

def externDefGen(MSList):
    code = '\n\n'
    for item in MSList:
        code += 'extern HSM_STATE OPS_State'+item+';\n'
    return code

#生成Init
def initGen(MSList):
    code = ''
    for item in MSList:
        state = 'OPS_State' + item
        name = item.replace("_", ".")
        hdl = 'OPS_'+item+'Hndlr'
        parent = ''
        code += '    HSM_STATE_Create(&'+ state +', "'+ name +'", '+ hdl +', &'+ parent +');\n'
    with open(os.getcwd() + '\\Copy\\'+MSList[0]+'init.c','w') as f:
        f.write(code)

def initGen2(item, parent):
    code = ''
    state = 'OPS_State' + item
    name = item.replace("_", ".")
    hdl = 'OPS_'+item+'Hndlr'
    parent = 'OPS_State'+parent
    code += '    HSM_STATE_Create(&'+ state +', "'+ name +'", '+ hdl +', &'+ parent +');\n'
    return code

def StringArrayGen(name, sidList):
    code = '\nSTRING_ID '+name+'String['+str(len(sidList))+'] = {\n'
    for sid in sidList:
        code += '    '+sid+',\n'
    code = code[:-2]+'\n};\n\n'
    return code

#生成hdl文件
def HdlGen(path, MenuList, SIDList, parentID):
    name = MenuList[0]
    maxIndex = len(MenuList) - 2
    handle = 'OPS_'+name+'Hndlr'

    code = StringArrayGen(name, SIDList)

    okOperation = ''
    for i in range(maxIndex+1):
        okOperation +=  '               case '+ str(i) +':\n\
                    HSM_Tran(This, &OPS_State'+ MenuList[i+1] +', 0, NULL);\n\
                    break;\n'

    code += 'HSM_EVENT '+handle+'(HSM *This, HSM_EVENT event, void *param)\n{\n\
    static stValueItem value = {0,0,'+ str(maxIndex) +'};\n\
    switch (event){\n\
        case HSME_ENTRY:\n\
            printf("entry '+name+'\\n");\n\
            break;\n\
        case HSME_EXIT:\n\
            printf("exit '+name+'\\n");\n\
            return 0;\n\
            break;\n\
        case HSME_INIT:\n\
            basic.curValue = value.curValue;\n\
            basic.minValue = value.minValue;\n\
            basic.maxValue = value.maxValue;\n\
            menuset(basic.curValue, basic.maxValue, &basic.MenuItem);\n\
            break;\n\
        case HSME_PWR:\n\
            return 0;\n\
            break;\n\
        case HSME_KEY_UP:\n\
            CycDecOne(&basic.curValue, basic.minValue, basic.maxValue);\n\
            menu_updown(&basic.MenuItem, basic.curValue, UP_ARROW);\n\
            printf("select up[%d]\\n",basic.curValue);\n\
            break;\n\
        case HSME_KEY_DOWN:\n\
            CycIncrOne(&basic.curValue, basic.minValue, basic.maxValue);\n\
            menu_updown(&basic.MenuItem, basic.curValue, DOWN_ARROW);\n\
            printf("select down[%d]\\n",basic.curValue);\n\
            break;\n\
        case HSME_KEY_OK:\n\
            value.curValue = basic.curValue;\n\
            value.minValue = basic.minValue;\n\
            value.maxValue = basic.maxValue;\n\
            switch(basic.curValue){\n'+okOperation+'            }\n\
            return 0;//need confirm\n\
            break;\n\
        case HSME_KEY_BACK:\n\
            HSM_Tran(This, &OPS_State'+ parentID +', 0, NULL);\n\
            return 0;\n\
            break;\n\
        default:\n\
            return event;\n\
    }\n\
    _LCD_Menu('+name+'String, basic.MenuItem);\n\
    return 0;\n\
}\n\n'
    return code

def HdlGen_Enum(path, MenuList, SIDList, parentID):
    name = MenuList[0]
    maxIndex = len(MenuList) - 2
    handle = 'OPS_'+name+'Hndlr'

    code = StringArrayGen(name, SIDList)


    okOperation = ''

    code += 'HSM_EVENT '+handle+'(HSM *This, HSM_EVENT event, void *param)\n{\n\
    static stValueItem value = {0,0,'+ str(maxIndex) +'};\n\
    switch (event){\n\
        case HSME_ENTRY:\n\
            printf("entry '+name+'\\n");\n\
            break;\n\
        case HSME_EXIT:\n\
            printf("exit '+name+'\\n");\n\
            return 0;\n\
            break;\n\
        case HSME_INIT:\n\
            basic.curValue = value.curValue;\n\
            basic.minValue = value.minValue;\n\
            basic.maxValue = value.maxValue;\n\
            menuset(basic.curValue, basic.maxValue, &basic.MenuItem);\n\
            break;\n\
        case HSME_PWR:\n\
//            HSM_Tran(This, &OPS_Off, 0, NULL);\n\
            break;\n\
        case HSME_KEY_UP:\n\
            CycDecOne(&basic.curValue, basic.minValue, basic.maxValue);\n\
            menu_updown(&basic.MenuItem, basic.curValue, UP_ARROW);\n\
            printf("select up[%d]\\n",basic.curValue);\n\
            break;\n\
        case HSME_KEY_DOWN:\n\
            CycIncrOne(&basic.curValue, basic.minValue, basic.maxValue);\n\
            menu_updown(&basic.MenuItem, basic.curValue, DOWN_ARROW);\n\
            printf("select down[%d]\\n",basic.curValue);\n\
            break;\n\
        case HSME_KEY_OK:\n\
            printf("set value[%d]\\n",basic.curValue);\n'\
            +okOperation+'\n\
            return 0;\n\
            break;\n\
        case HSME_KEY_BACK:\n\
            HSM_Tran(This, &OPS_State'+ parentID +', 0, NULL);\n\
            return 0;\n\
            break;\n\
        default:\n\
            return event;\n\
    }\n\
    _LCD_Menu('+name+'String, basic.MenuItem);\n\
    return 0;\n\
}\n\n'
    return code
#    with open(path +'\\'+name+'hdl.c','w') as f:
#        f.write(code)

def HdlGen_Value(path, MenuList, SIDList, parentID):
    name = MenuList[0]
    maxIndex = len(MenuList) - 2
    handle = 'OPS_'+name+'Hndlr'

    code = StringArrayGen(name, SIDList)

    okOperation = ''

    code += 'HSM_EVENT '+handle+'(HSM *This, HSM_EVENT event, void *param)\n{\n\
    static stValueItem value = {0,0,'+ str(maxIndex) +'};\n\
    switch (event){\n\
        case HSME_ENTRY:\n\
            printf("entry '+name+'\\n");\n\
            break;\n\
        case HSME_EXIT:\n\
            printf("exit '+name+'\\n");\n\
            return 0;\n\
            break;\n\
        case HSME_INIT:\n\
            basic.curValue = value.curValue;\n\
            basic.minValue = value.minValue;\n\
            basic.maxValue = value.maxValue;\n\
            menuset(basic.curValue, basic.maxValue, &basic.MenuItem);\n\
            break;\n\
        case HSME_PWR:\n\
//            HSM_Tran(This, &OPS_Off, 0, NULL);\n\
            break;\n\
        case HSME_KEY_UP:\n\
            CycDecOne(&basic.curValue, basic.minValue, basic.maxValue);\n\
            menu_updown(&basic.MenuItem, basic.curValue, UP_ARROW);\n\
            printf("select up[%d]\\n",basic.curValue);\n\
            break;\n\
        case HSME_KEY_DOWN:\n\
            CycIncrOne(&basic.curValue, basic.minValue, basic.maxValue);\n\
            menu_updown(&basic.MenuItem, basic.curValue, DOWN_ARROW);\n\
            printf("select down[%d]\\n",basic.curValue);\n\
            break;\n\
        case HSME_KEY_OK:\n\
            printf("set value[%d]\\n",basic.curValue);\n'\
            +okOperation+'\n\
            return 0;\n\
            break;\n\
        case HSME_KEY_BACK:\n\
            HSM_Tran(This, &OPS_State'+ parentID +', 0, NULL);\n\
            return 0;\n\
            break;\n\
        default:\n\
            return event;\n\
    }\n\
    _LCD_RangeMenu ('+name+'String, basic.MenuItem );\n\
    return 0;\n\
}\n\n'
    return code
#    with open(path + '\\'+name+'hdl.c','w') as f:
#        f.write(code)


