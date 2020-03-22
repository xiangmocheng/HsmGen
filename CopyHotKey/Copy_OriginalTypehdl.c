#include "hsm.h"
#include "menu.h"
#include "mid.h"
#include "LangString.h"

eMenuID CopyList[3] = {
    MID_Copy_Text,
    MID_Copy_PhotoText,
    MID_Copy_Photo
};
stMenuStruct MS_Copy = { MID_Copy, SID_Copy, CopyList};

stMenuEntryInfo MEntry_Copy_Text = { MID_Copy_Text, SID_Text, QUAL_TYPE, 0, 0, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_PhotoText = { MID_Copy_PhotoText, SID_PhotoText, QUAL_TYPE, 0, 1, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_Photo = { MID_Copy_Photo, SID_Photo, QUAL_TYPE, 0, 2, 0, 0, 0, 0, 0};

STRING_ID CopyString[4] = {
    SID_Copy,
    SID_Text,
    SID_PhotoText,
    SID_Photo
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

