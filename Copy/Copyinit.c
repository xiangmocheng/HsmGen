    HSM_STATE_Create(&OPS_StateCopy, "Copy", OPS_CopyHndlr, &OPS_State);
    HSM_STATE_Create(&OPS_StateCopy_PaperSupply, "Copy.PaperSupply", OPS_Copy_PaperSupplyHndlr, &OPS_StateCopy);
    HSM_STATE_Create(&OPS_StateCopy_ReduceEnlarge, "Copy.ReduceEnlarge", OPS_Copy_ReduceEnlargeHndlr, &OPS_StateCopy);
    HSM_STATE_Create(&OPS_StateCopy_OriginalSize, "Copy.OriginalSize", OPS_Copy_OriginalSizeHndlr, &OPS_StateCopy);
    HSM_STATE_Create(&OPS_StateCopy_OriginalBindingPosition, "Copy.OriginalBindingPosition", OPS_Copy_OriginalBindingPositionHndlr, &OPS_StateCopy);
    HSM_STATE_Create(&OPS_StateCopy_OutputBindingPosition, "Copy.OutputBindingPosition", OPS_Copy_OutputBindingPositionHndlr, &OPS_StateCopy);
    HSM_STATE_Create(&OPS_StateCopy_EdgeErase, "Copy.EdgeErase", OPS_Copy_EdgeEraseHndlr, &OPS_StateCopy);
