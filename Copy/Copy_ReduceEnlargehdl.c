#include "hsm.h"
#include "menu.h"
#include "mid.h"
#include "LangString.h"

eMenuID Copy_ReduceEnlargeList[11] = {
    MID_Copy_ReduceEnlarge_Auto,
    MID_Copy_ReduceEnlarge_100,
    MID_Copy_ReduceEnlarge_50A3A5,
    MID_Copy_ReduceEnlarge_70A3A4B4B5,
    MID_Copy_ReduceEnlarge_81B4A4B5A5,
    MID_Copy_ReduceEnlarge_86A3B4A4B5,
    MID_Copy_ReduceEnlarge_115B4A3B5A4,
    MID_Copy_ReduceEnlarge_122A4B4A5B5,
    MID_Copy_ReduceEnlarge_141A4A3B5B4,
    MID_Copy_ReduceEnlarge_200A5A3,
    MID_Copy_ReduceEnlarge_Preset400
};
stMenuStruct MS_Copy_ReduceEnlarge = { MID_Copy_ReduceEnlarge, SID_ReduceEnlarge, Copy_ReduceEnlargeList};

stMenuEntryInfo MEntry_Copy_ReduceEnlarge_Auto = { MID_Copy_ReduceEnlarge_Auto, SID_Auto, QUAL_TYPE, 0, 0, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_ReduceEnlarge_100 = { MID_Copy_ReduceEnlarge_100, SID_100, QUAL_TYPE, 0, 1, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_ReduceEnlarge_50A3A5 = { MID_Copy_ReduceEnlarge_50A3A5, SID_50A3A5, QUAL_TYPE, 0, 2, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_ReduceEnlarge_70A3A4B4B5 = { MID_Copy_ReduceEnlarge_70A3A4B4B5, SID_70A3A4B4B5_2, QUAL_TYPE, 0, 3, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_ReduceEnlarge_81B4A4B5A5 = { MID_Copy_ReduceEnlarge_81B4A4B5A5, SID_81B4A4B5A5, QUAL_TYPE, 0, 4, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_ReduceEnlarge_86A3B4A4B5 = { MID_Copy_ReduceEnlarge_86A3B4A4B5, SID_86A3B4A4B5, QUAL_TYPE, 0, 5, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_ReduceEnlarge_115B4A3B5A4 = { MID_Copy_ReduceEnlarge_115B4A3B5A4, SID_115B4A3B5A4, QUAL_TYPE, 0, 6, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_ReduceEnlarge_122A4B4A5B5 = { MID_Copy_ReduceEnlarge_122A4B4A5B5, SID_122A4B4A5B5, QUAL_TYPE, 0, 7, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_ReduceEnlarge_141A4A3B5B4 = { MID_Copy_ReduceEnlarge_141A4A3B5B4, SID_141A4A3B5B4, QUAL_TYPE, 0, 8, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_ReduceEnlarge_200A5A3 = { MID_Copy_ReduceEnlarge_200A5A3, SID_200A5A3, QUAL_TYPE, 0, 9, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_ReduceEnlarge_Preset400 = { MID_Copy_ReduceEnlarge_Preset400, SID_Preset400, QUAL_TYPE, 0, 10, 0, 0, 0, 0, 0};

STRING_ID Copy_ReduceEnlargeString[12] = {
    SID_ReduceEnlarge,
    SID_Auto,
    SID_100,
    SID_50A3A5,
    SID_70A3A4B4B5_2,
    SID_81B4A4B5A5,
    SID_86A3B4A4B5,
    SID_115B4A3B5A4,
    SID_122A4B4A5B5,
    SID_141A4A3B5B4,
    SID_200A5A3,
    SID_Preset400
};

HSM_EVENT OPS_Copy_ReduceEnlargeHndlr(HSM *This, HSM_EVENT event, void *param)
{
    switch (event){
        case HSME_ENTRY:
            printf("entry Copy_ReduceEnlarge\n");
            break;
        case HSME_EXIT:
            printf("exit Copy_ReduceEnlarge\n");
            break;
        case HSME_INIT:
            basic.curValue = 0;
            basic.minValue = 0;
            basic.maxValue = 10;
            menuset(basic.curValue, 10, &basic.MenuItem);
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
    _LCD_Menu(Copy_ReduceEnlargeString, basic.MenuItem);
    return 0;
}

