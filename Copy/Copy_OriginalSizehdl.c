#include "hsm.h"
#include "menu.h"
#include "LangString.h"


STRING_ID Copy_OriginalSizeString[17] = {
    SID_OriginalSize,
    SID_Auto,
    SID_A3297x420mm,
    SID_A4297x210mm,
    SID_A4210x297mm,
    SID_B4257x364mm,
    SID_B5257x182mm,
    SID_B5182x257mm,
    SID_8K270x390mm,
    SID_16K270x195mm,
    SID_A5148x210mm,
    SID_11x17,
    SID_85x14,
    SID_85x13,
    SID_85x11,
    SID_85x11,
    SID_CustomSizeXXXxXXXmm
};

HSM_EVENT OPS_Copy_OriginalSizeHndlr(HSM *This, HSM_EVENT event, void *param)
{
    switch (event){
        case HSME_ENTRY:
            printf("entry Copy_OriginalSize\n");
            break;
        case HSME_EXIT:
            printf("exit Copy_OriginalSize\n");
            break;
        case HSME_INIT:
            basic.curValue = 0;
            basic.minValue = 0;
            basic.maxValue = 15;
            menuset(basic.curValue, 15, &basic.MenuItem);
            break;
        case HSME_PWR:
//            HSM_Tran(This, &OPS_Off, 0, NULL);
            break;
        case HSME_KEY_UP:
            CycDecOne(&basic.curValue, basic.minValue, basic.maxValue);
            menu_updown(&basic.MenuItem, basic.curValue, UP_ARROW);
            printf("select up[%d]\n",basic.curValue);
            break;
        case HSME_KEY_DOWN:
            CycIncrOne(&basic.curValue, basic.minValue, basic.maxValue);
            menu_updown(&basic.MenuItem, basic.curValue, DOWN_ARROW);
            printf("select down[%d]\n",basic.curValue);
            break;
        case HSME_KEY_OK:
            printf("set value[%d]\n",basic.curValue);

            return 0;
            break;
        case HSME_KEY_BACK:
            HSM_Tran(This, &OPS_StateCopy, 0, NULL);
            return 0;
            break;
        default:
            return event;
    }
    _LCD_Menu(Copy_OriginalSizeString, basic.MenuItem);
    return 0;
}

