#include <stdlib.h>
#include <stdio.h>

#ifndef FUSIONCLASS_LIBRARY_H
#define FUSIONCLASS_LIBRARY_H

typedef struct {
    unsigned char *barras;
    unsigned char *tipoFusion;
    unsigned char *resultado;
    unsigned char *compaAni;
    unsigned char **compaEquipo;
} FusionData;

static void FusionData_dealloc(FusionData* self);

static FusionData *FusionData_new();

static int FusionData_init(FusionData *self, unsigned char *fusionLine);

static int *FusionData_getFusionData(FusionData *self, int fusionNumb);

static int FusionData_setFusionData(FusionData *self, int fusionNumb, int *data);

static unsigned char *FusionData_getAsLine(FusionData *self);

#endif
