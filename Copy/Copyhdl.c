#include "hsm.h"
#include "menu.h"
#include "mid.h"
#include "LangString.h"

eMenuID CopyList[6] = {
    MID_Copy_PaperSupply,
    MID_Copy_ReduceEnlarge,
    MID_Copy_OriginalSize,
    MID_Copy_OriginalBindingPosition,
    MID_Copy_OutputBindingPosition,
    MID_Copy_EdgeErase
};
stMenuStruct MS_Copy = { MID_Copy, SID_Copy, CopyList};

stMenuEntryInfo MEntry_Copy_PaperSupply = { MID_Copy_PaperSupply, SID_PaperSupply, MENU_TYPE, 0, 0, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_ReduceEnlarge = { MID_Copy_ReduceEnlarge, SID_ReduceEnlarge, MENU_TYPE, 0, 0, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_OriginalSize = { MID_Copy_OriginalSize, SID_OriginalSize, MENU_TYPE, 0, 0, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_OriginalBindingPosition = { MID_Copy_OriginalBindingPosition, SID_OriginalBindingPosition, MENU_TYPE, 0, 0, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_OutputBindingPosition = { MID_Copy_OutputBindingPosition, SID_OutputBindingPosition, MENU_TYPE, 0, 0, 0, 0, 0, 0, 0};
stMenuEntryInfo MEntry_Copy_EdgeErase = { MID_Copy_EdgeErase, SID_EdgeErase, QUANT_TYPE, 0, 2, 0, 40, 0, 0, 0};

STRING_ID CopyString[7] = {
    SID_Copy,
    SID_PaperSupply,
    SID_ReduceEnlarge,
    SID_OriginalSize,
    SID_OriginalBindingPosition,
    SID_OutputBindingPosition,
    SID_EdgeErase
};

HSM_EVENT OPS_CopyHndlr(HSM *This, HSM_EVENT event, void *param)
{
    static stValueItem value = {0,0,5};
    switch (event){
        case HSME_ENTRY:
            printf("entry Copy\n");
            break;
        case HSME_EXIT:
            printf("exit Copy\n");
            break;
        case HSME_INIT:
            basic.curValue = value.curValue;
            basic.minValue = value.minValue;
            basic.maxValue = value.maxValue;
            menuset(basic.curValue, basic.maxValue, &basic.MenuItem);
            break;
        case HSME_PWR:
            return 0;
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
            value.curValue = basic.curValue;
            value.minValue = basic.minValue;
            value.maxValue = basic.maxValue;
            switch(basic.curValue){
               case 0:
                    HSM_Tran(This, &OPS_StateCopy_PaperSupply, 0, NULL);
                    break;
               case 1:
                    HSM_Tran(This, &OPS_StateCopy_ReduceEnlarge, 0, NULL);
                    break;
               case 2:
                    HSM_Tran(This, &OPS_StateCopy_OriginalSize, 0, NULL);
                    break;
               case 3:
                    HSM_Tran(This, &OPS_StateCopy_OriginalBindingPosition, 0, NULL);
                    break;
               case 4:
                    HSM_Tran(This, &OPS_StateCopy_OutputBindingPosition, 0, NULL);
                    break;
               case 5:
                    HSM_Tran(This, &OPS_StateCopy_EdgeErase, 0, NULL);
                    break;
            }
            return 0;//need confirm
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

