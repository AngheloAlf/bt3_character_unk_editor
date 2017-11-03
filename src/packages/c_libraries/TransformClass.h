#include <stdlib.h>
#include <stdio.h>

#ifndef TRANSFORMCLASS_LIBRARY_H
#define TRANSFORMCLASS_LIBRARY_H

typedef struct {
    unsigned char *trans;
    unsigned char *barras;

    unsigned char *aniCam;
    unsigned char *aura;
    unsigned char *abs;
    unsigned char command;
    unsigned char bonus;
} TransformData;

static void TransformData_dealloc(TransformData* self);

static TransformData *TransformData_new();

static void TransformData_init(TransformData *self, unsigned char *transformLine);

static int *TransformData_getTransformData(TransformData *self, int transformNumb);

static int TransformData_setTransformData(TransformData *self, int transformNumb, int *data);

static int TransformData_getR3Command(TransformData *self);

static int TransformData_setR3Command(TransformData *self, int r3Command);

static int TransformData_getBonus(TransformData *self);

static int TransformData_setBonus(TransformData *self, int bonus);

static unsigned char *TransformData_getAsLine(TransformData *self);

#endif
