typedef enum {
    MID_Copy,
    MID_Copy_PaperSupply,
    MID_Copy_ReduceEnlarge,
    MID_Copy_OriginalSize,
    MID_Copy_OriginalBindingPosition,
    MID_Copy_OutputBindingPosition,
    MID_Copy_EdgeErase,
    MID_Copy_PaperSupply_Auto,
    MID_Copy_PaperSupply_Tray1XX,
    MID_Copy_PaperSupply_Tray2XX,
    MID_Copy_PaperSupply_Tray3XX,
    MID_Copy_PaperSupply_Tray4XX,
    MID_Copy_PaperSupply_Tray5XX,
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
    MID_Copy_ReduceEnlarge_Preset400,
    MID_Copy_OriginalSize_Auto,
    MID_Copy_OriginalSize_A3297x420mm,
    MID_Copy_OriginalSize_A4297x210mm,
    MID_Copy_OriginalSize_A4210x297mm,
    MID_Copy_OriginalSize_B4257x364mm,
    MID_Copy_OriginalSize_B5257x182mm,
    MID_Copy_OriginalSize_B5182x257mm,
    MID_Copy_OriginalSize_8K270x390mm,
    MID_Copy_OriginalSize_16K270x195mm,
    MID_Copy_OriginalSize_A5148x210mm,
    MID_Copy_OriginalSize_11x17,
    MID_Copy_OriginalSize_85x14,
    MID_Copy_OriginalSize_85x13,
    MID_Copy_OriginalSize_85x11,
    MID_Copy_OriginalSize_85x11,
    MID_Copy_OriginalSize_CustomSizeXXXxXXXmm,
    MID_Copy_OriginalBindingPosition_FliponLongEdge,
    MID_Copy_OriginalBindingPosition_FilponShortEdge,
    MID_Copy_OutputBindingPosition_FliponLongEdge,
    MID_Copy_OutputBindingPosition_FilponShortEdge
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
    bool DisplayPara;
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
extern HSM_STATE OPS_StateCopy_PaperSupply;
extern HSM_STATE OPS_StateCopy_ReduceEnlarge;
extern HSM_STATE OPS_StateCopy_OriginalSize;
extern HSM_STATE OPS_StateCopy_OriginalBindingPosition;
extern HSM_STATE OPS_StateCopy_OutputBindingPosition;
extern HSM_STATE OPS_StateCopy_EdgeErase;
