#ifndef __LANGSTRING_H_
#define __LANGSTRING_H_

#include "type.h"

extern wchar_t wstringTableEng[];
extern tUint32 strTableSize;

typedef enum STRING_ID
{
SID_Copy,	//"Copy"
SID_PaperSupply,	//"Paper Supply"
SID_ReduceEnlarge,	//"Reduce/Enlarge"
SID_OriginalSize,	//"Original Size"
SID_OriginalBindingPosition,	//"Original - Binding Position"
SID_OutputBindingPosition,	//"Output - Binding Position"
SID_EdgeErase,	//"Edge Erase"
SID_Auto,	//"Auto"
SID_FliponLongEdge,	//"Flip on Long Edge"
SID_25400,	//"(25 - 400)"
SID_MinusPlus,	//"-     +"
SID_Tray1A4,	//"Tray 1: A4"
SID_Tray2A4,	//"Tray 2: A4"
SID_50A3A5,	//"50% A3->A5"
SID_70A3A4B4B5,	//"70% A3->A4,B4->B5"
SID_A3297x420mm,	//"A3     (297x420mm)"
SID_A4297x210mm,	//"A4     (297x210mm)"
SID_FilponShortEdge,	//"Filp on Short Edge"
SID_040,	//"(0 - 40)"
SID_Qty,	//"Qty."
SID_mm,	//"mm"
SID_Tray1XX,	//"Tray 1:XX"
SID_Tray2XX,	//"Tray 2:XX"
SID_Tray3XX,	//"Tray 3:XX"
SID_Tray4XX,	//"Tray 4:XX"
SID_Tray5XX,	//"Tray 5:XX"
SID_100,	//"100%"
SID_70A3A4B4B5_2,	//"70% A3->A4, B4->B5"
SID_81B4A4B5A5,	//"81% B4->A4, B5->A5"
SID_86A3B4A4B5,	//"86% A3->B4, A4->B5"
SID_115B4A3B5A4,	//"115% B4->A3, B5->A4"
SID_122A4B4A5B5,	//"122% A4->B4, A5->B5"
SID_141A4A3B5B4,	//"141% A4->A3, B5->B4"
SID_200A5A3,	//"200% A5->A3"
SID_Preset400,	//"Preset 400%"
SID_A4210x297mm,	//"A4     (210x297mm)"
SID_B4257x364mm,	//"B4     (257x364mm)"
SID_B5257x182mm,	//"B5     (257x182mm)"
SID_B5182x257mm,	//"B5     (182x257mm)"
SID_8K270x390mm,	//"8K     (270x390mm)"
SID_16K270x195mm,	//"16K    (270x195mm)"
SID_A5148x210mm,	//"A5     (148x210mm)"
SID_11x17,	//"11 x 17\""
SID_85x14,	//"8.5 x 14\""
SID_85x13,	//"8.5 x 13\""
SID_85x11,	//"8.5 x 11\""
SID_CustomSizeXXXxXXXmm,	//"Custom Size(XXXxXXXmm     )"
SID_MaxStringCount
} STRING_ID;

#endif