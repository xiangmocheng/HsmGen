typedef enum {
    MID_Copy_Text,
    MID_Copy_PhotoText,
    MID_Copy_Photo,
    MID_Copy_11Sided,
    MID_Copy_12Sided,
    MID_Copy_21Sided,
    MID_Copy_22Sided,
    MID_Copy_Off,
    MID_Copy_On,
    MID_Copy_OnRotate,
    MID_Copy_Off,
    MID_Copy_2Pages,
    MID_Copy_4Pages,
    MID_Copy_Press1_PaperSupply,
    MID_Copy_Press1_ReduceEnlarge,
    MID_Copy_Press1_OriginalSize
}eMenuID;
//all menu ID end

//all menu type
typedef enum {
    QUAL_TYPE,              // use for enumerations
    QUANT_TYPE,             // use for numeric value
    MENU_TYPE,              // use for menu      =>  the entry is list, sub item is the sub menu entry   
    DYNAMIC_LIST_TYPE,      // use for phonebook/udisk browser menu
    WINDOW_TYPE,            // use for window/graphic menu
    SELECT_TYPE,            // use for Select Action Parameters  => the entry is list, sub item is parameter setting entry
    ENTRY_VALUE_TYPE,       // use for parameter name   => some parameter's sub menu,ex: A4L, the paper size sub menu
}eMenuType;

//menu entry structure
typedef struct _MenuEntryInfo{
    int MenuID;
    int StringID;
    eMenuType MenuType;
    int DisplayPara;
    int ValueType;
    int ValueId;
    int ValueSubId;
    int CurValue;
    int MinValue;
    int MaxValue;
    char* str;
}stMenuEntryInfo, *pstMenuEntryInfo;

//menu structure
typedef struct _MenuStruct{
    int MenuID;
    int StringID;
    eMenuID* pMenuIDList;
}stMenuStruct, *pstMenuStruct;

extern HSM_STATE OPS_StateCopy;
extern HSM_STATE OPS_StateCopy;
extern HSM_STATE OPS_StateCopy;
extern HSM_STATE OPS_StateCopy;
extern HSM_STATE OPS_StatePress1;
