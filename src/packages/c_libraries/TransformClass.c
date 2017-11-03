//
// Created by AngheloAlf10 on 22-10-2017.
//

#include "TransformClass.h"

static void TransformData_dealloc(TransformData* self){
    free(self->trans);
    free(self->barras);
    free(self->aniCam);
    free(self->aura);
    free(self->abs);

    free(self);
}

static TransformData *TransformData_new(){
    TransformData *self = malloc(sizeof(TransformData));

    if (self != NULL) {
        self->trans = malloc(sizeof(char)*4);
        self->barras = malloc(sizeof(char)*4);
        self->aniCam = malloc(sizeof(char)*4);
        self->aura = malloc(sizeof(char)*4);
        self->abs = malloc(sizeof(char)*4);

        self->command = 255;
        self->bonus = 0;
    }

    return self;
}

static void TransformData_init(TransformData *self, unsigned char *transformLine){
    int i;

    //printf("for(i = 0; i<4; i++)\n");
    for(i = 0; i<4; i++){
        //printf("\tself->trans[%i] = transformLine[%i]\n", i, i);
        //printf("\transformLine[%i] = %i\n", i, transformLine[i]);
        self->trans[i] = transformLine[i];
    }
    //printf("for(i = 0; i<4; i++)\n");
    for(i = 0; i<4; i++){
        //printf("\tself->barras[%i] = transformLine[%i]\n", i, i+4);
        //printf("\transformLine[%i] = %i\n", i+3, transformLine[i+4]);
        self->barras[i] = transformLine[i+4];
    }
    //printf("for(i = 0; i<4; i++)\n");
    for(i = 0; i<4; i++){
        //printf("\tself->aniCam[%i] = transformLine[%i]\n", i, i+8);
        //printf("\transformLine[%i] = %i\n", i+6, transformLine[i+8]);
        self->aniCam[i] = transformLine[i+8];
    }
    //printf("for(i = 0; i<4; i++)\n");
    for(i = 0; i<4; i++){
        //printf("\tself->aura[%i] = transformLine[%i]\n", i, i+12);
        //printf("\transformLine[%i] = %i\n", i+6, transformLine[i+12]);
        self->aura[i] = transformLine[i+12];
    }
    //printf("for(i = 0; i<4; i++)\n");
    for(i = 0; i<4; i++){
        //printf("\tself->abs[%i] = transformLine[%i]\n", i, i+16);
        //printf("\transformLine[%i] = %i\n", i+6, transformLine[i+16]);
        self->abs[i] = transformLine[i+16];
    }

    self->command = transformLine[20];
    self->bonus = transformLine[21];

    return;
}

static int *TransformData_getTransformData(TransformData *self, int transformNumb){
    int *data;

    if(transformNumb < 0 || transformNumb > 3){
        return NULL;
    }

    data = malloc(5*sizeof(int));

    data[0] = self->trans[transformNumb];
    data[1] = self->barras[transformNumb];
    data[2] = self->aniCam[transformNumb];
    data[3] = self->aura[transformNumb];
    data[4] = self->abs[transformNumb];

    return data;
}

static int TransformData_setTransformData(TransformData *self, int transformNumb, int *data){
    if(transformNumb < 0 || transformNumb > 3){
        return -1;
    }

    //printf("\tself->trans[%i] = (unsigned char)data[0]; == %i\n", transformNumb, data[0]);
    self->trans[transformNumb] = (unsigned char)data[0];
    //printf("\tself->barras[%i] = (unsigned char)data[1]; == %i\n", transformNumb, data[1]);
    self->barras[transformNumb] = (unsigned char)data[1];
    //printf("\tself->aniCam[%i] = (unsigned char)data[2]; == %i\n", transformNumb, data[2]);
    self->aniCam[transformNumb] = (unsigned char)data[2];
    //printf("\tself->aura[%i] = (unsigned char)data[3]; == %i\n", transformNumb, data[3]);
    self->aura[transformNumb] = (unsigned char)data[3];
    //printf("\t\tself->abs[%i] = (unsigned char)data[4]; == %i\n", transformNumb, data[4]);
    self->abs[transformNumb] = (unsigned char)data[4];

    return 0;
}

static int TransformData_getR3Command(TransformData *self){
    return (int)self->command;
}

static int TransformData_setR3Command(TransformData *self, int r3Command){
    if(r3Command>255 || r3Command<0){
        return -1;
    }
    self->command = (unsigned char)r3Command;
    return 0;
}

static int TransformData_getBonus(TransformData *self){
    return (int)self->bonus;
}

static int TransformData_setBonus(TransformData *self, int bonus){
    if(bonus>255 || bonus<0){
        return -1;
    }
    self->bonus = (unsigned char)bonus;
    return 0;
}

static unsigned char *TransformData_getAsLine(TransformData *self){
    int i, bufferSize = 22;
    unsigned char *buffer = malloc(bufferSize*sizeof(char));

    for(i = 0; i<4; i++){
        buffer[i] = self->trans[i];
    }
    for(i = 0; i<4; i++){
        buffer[i+4] = self->barras[i];
    }
    for(i = 0; i<4; i++){
        buffer[i+8] = self->aniCam[i];
    }
    for(i = 0; i<4; i++){
        buffer[i+12] = self->aura[i];
    }

    for(i = 0; i<4; i++){
        buffer[i+16] = self->abs[i];
    }
    buffer[20] = self->command;
    buffer[21] = self->bonus;
    return buffer;
}
