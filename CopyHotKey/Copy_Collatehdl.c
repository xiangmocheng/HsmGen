#include "hsm.h"
#include "menu.h"
#include "mid.h"
#include "LangString.h"

eMenuID CopyList[3] = {
    MID_Copy_Off,
    MID_Copy_On,
    MID_Copy_OnRotate
};
stMenuStruct MS_Copy = { MID_Copy, SID_Copy, CopyList};

stMenuEntryInfo MEntry_Copy_Off = { MID_Copy_Off, SID_Off, QUAL_TYPE, 0, 0, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_On = { MID_Copy_On, SID_On, QUAL_TYPE, 0, 1, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_OnRotate = { MID_Copy_OnRotate, SID_OnRotate, QUAL_TYPE, 0, 2, 0, 0, 0, 0, 0};

STRING_ID CopyString[4] = {
    SID_Copy,
    SID_Off,
    SID_On,
    SID_OnRotate
};

HSM_EVENT OPS_CopyHndlr(HSM *This, HSM_EVENT event, void *param)
{
    switch (event){
        case HSME_ENTRY:
            printf("entry Copy\n");
            break;
        case HSME_EXIT:
            printf("exit Copy\n");
            break;
        case HSME_INIT:
            basic.curValue = 0;
            basic.minValue = 0;
            basic.maxValue = 2;
            menuset(basic.curValue, 2, &basic.MenuItem);
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
            HSM_Tran(This, &OPS_State, 0, NULL);
            return 0;
            break;
        default:
            return event;
    }
    _LCD_Menu(CopyString, basic.MenuItem);
    return 0;
}

