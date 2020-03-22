#include "hsm.h"
#include "menu.h"
#include "LangString.h"


STRING_ID Copy_PaperSupplyString[7] = {
    SID_PaperSupply,
    SID_Auto,
    SID_Tray1XX,
    SID_Tray2XX,
    SID_Tray3XX,
    SID_Tray4XX,
    SID_Tray5XX
};

HSM_EVENT OPS_Copy_PaperSupplyHndlr(HSM *This, HSM_EVENT event, void *param)
{
    switch (event){
        case HSME_ENTRY:
            printf("entry Copy_PaperSupply\n");
            break;
        case HSME_EXIT:
            printf("exit Copy_PaperSupply\n");
            break;
        case HSME_INIT:
            basic.curValue = 0;
            basic.minValue = 0;
            basic.maxValue = 5;
            menuset(basic.curValue, 5, &basic.MenuItem);
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
    _LCD_Menu(Copy_PaperSupplyString, basic.MenuItem);
    return 0;
}

