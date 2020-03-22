#include "type.h"
#include <wchar.h>

wchar_t wstringTableEng[]={
L"Copy\0"	//SID_Copy
L"Paper Supply\0"	//SID_PaperSupply
L"Reduce/Enlarge\0"	//SID_ReduceEnlarge
L"Original Size\0"	//SID_OriginalSize
L"Original - Binding Position\0"	//SID_OriginalBindingPosition
L"Output - Binding Position\0"	//SID_OutputBindingPosition
L"Edge Erase\0"	//SID_EdgeErase
L"Auto\0"	//SID_Auto
L"Flip on Long Edge\0"	//SID_FliponLongEdge
L"(25 - 400)\0"	//SID_25400
L"-     +\0"	//SID_MinusPlus
L"Tray 1: A4\0"	//SID_Tray1A4
L"Tray 2: A4\0"	//SID_Tray2A4
L"50% A3->A5\0"	//SID_50A3A5
L"70% A3->A4,B4->B5\0"	//SID_70A3A4B4B5
L"A3     (297x420mm)\0"	//SID_A3297x420mm
L"A4     (297x210mm)\0"	//SID_A4297x210mm
L"Filp on Short Edge\0"	//SID_FilponShortEdge
L"(0 - 40)\0"	//SID_040
L"Qty.\0"	//SID_Qty
L"mm\0"	//SID_mm
L"Tray 1:XX\0"	//SID_Tray1XX
L"Tray 2:XX\0"	//SID_Tray2XX
L"Tray 3:XX\0"	//SID_Tray3XX
L"Tray 4:XX\0"	//SID_Tray4XX
L"Tray 5:XX\0"	//SID_Tray5XX
L"100%\0"	//SID_100
L"70% A3->A4, B4->B5\0"	//SID_70A3A4B4B5_2
L"81% B4->A4, B5->A5\0"	//SID_81B4A4B5A5
L"86% A3->B4, A4->B5\0"	//SID_86A3B4A4B5
L"115% B4->A3, B5->A4\0"	//SID_115B4A3B5A4
L"122% A4->B4, A5->B5\0"	//SID_122A4B4A5B5
L"141% A4->A3, B5->B4\0"	//SID_141A4A3B5B4
L"200% A5->A3\0"	//SID_200A5A3
L"Preset 400%\0"	//SID_Preset400
L"A4     (210x297mm)\0"	//SID_A4210x297mm
L"B4     (257x364mm)\0"	//SID_B4257x364mm
L"B5     (257x182mm)\0"	//SID_B5257x182mm
L"B5     (182x257mm)\0"	//SID_B5182x257mm
L"8K     (270x390mm)\0"	//SID_8K270x390mm
L"16K    (270x195mm)\0"	//SID_16K270x195mm
L"A5     (148x210mm)\0"	//SID_A5148x210mm
L"11 x 17\"\0"	//SID_11x17
L"8.5 x 14\"\0"	//SID_85x14
L"8.5 x 13\"\0"	//SID_85x13
L"8.5 x 11\"\0"	//SID_85x11
L"Custom Size(XXXxXXXmm     )\0"	//SID_CustomSizeXXXxXXXmm
L"Text\0"	//SID_Text
L"Photo & Text\0"	//SID_PhotoText
L"Photo\0"	//SID_Photo
L"1->1 Sided\0"	//SID_11Sided
L"1->2 Sided\0"	//SID_12Sided
L"2->1 Sided\0"	//SID_21Sided
L"Off\0"	//SID_Off
L"On\0"	//SID_On
L"On(Rotate)\0"	//SID_OnRotate
L"2 Pages\0"	//SID_2Pages
L"4 Pages\0"	//SID_4Pages
L"Toner Saver\0"	//SID_TonerSaver
L"2->2 Sided\0"	//SID_22Sided
};

tUint32 strTableSize = sizeof(wstringTableEng);
