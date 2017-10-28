//
// Created by AngheloAlf10 on 22-10-2017.
//

#include "FusionClass.h"

static void FusionData_dealloc(FusionData* self){
    free(self->barras);
    free(self->tipoFusion);
    free(self->resultado);
    free(self->compaAni);
    for(int i = 0; i<3; i++){
        free(self->compaEquipo[i]);
    }
    free(self->compaEquipo);

    free(self);
}

static FusionData *FusionData_new(){
    FusionData *self = malloc(sizeof(FusionData));

    if (self != NULL) {
        self->barras = malloc(sizeof(char)*3);
        self->tipoFusion = malloc(sizeof(char)*3);
        self->resultado = malloc(sizeof(char)*3);
        self->compaAni = malloc(sizeof(char)*3);
        self->compaEquipo = malloc(sizeof(char *)*3);
        for(int i = 0; i<3; i++){
            self->compaEquipo[i] = malloc(sizeof(char)*4);
        }
    }

    return self;
}

static int FusionData_init(FusionData *self, unsigned char *fusionLine){
    int buffer_size;

    int i;

    //printf("for(i = 0; i<3; i++)\n");
    for(i = 0; i<3; i++){
        //printf("\tself->barras[%i] = fusionLine[%i]\n", i, i);
        //printf("\fusionLine[%i] = %i\n", i, fusionLine[i]);
        self->barras[i] = fusionLine[i];
    }
    //printf("for(i = 0; i<3; i++)\n");
    for(i = 0; i<3; i++){
        //printf("\tself->tipoFusion[%i] = fusionLine[%i]\n", i, i+3);
        //printf("\fusionLine[%i] = %i\n", i+3, fusionLine[i+3]);
        self->tipoFusion[i] = fusionLine[i+3];
    }
    //printf("for(i = 0; i<3; i++)\n");
    for(i = 0; i<3; i++){
        //printf("\tself->resultado[%i] = fusionLine[%i]\n", i, i+6);
        //printf("\fusionLine[%i] = %i\n", i+6, fusionLine[i+6]);
        self->resultado[i] = fusionLine[i+6];
    }
    //printf("for(i = 0; i<3; i++)\n");
    for(i = 0; i<3; i++){
        //printf("\tself->compaAni[%i] = fusionLine[%i]\n", i, i+9);
        //printf("\fusionLine[%i] = %i\n", i+6, fusionLine[i+9]);
        self->compaAni[i] = fusionLine[i+9];
    }
    //printf("for(i = 0; i<3; i++)\n");
    for(i = 0; i<3; i++){
        //printf("\tfor(int j = 0; j<4; j++)\n");
        for(int j = 0; j<4; j++){
            //printf("\t\tself->compaEquipo[%i][%i] = fusionLine[%i]\n", i, j, 12 + i*4 + j);
            //printf("\t\fusionLine[%i] = %i\n", 12 + i*4 + j, fusionLine[12 + i*4 + j]);
            self->compaEquipo[i][j] = fusionLine[12 + i*4 + j];
        }
    }

    return 0;
}

static int *FusionData_getFusionData(FusionData *self, int fusionNumb){
    int *data;

    if(fusionNumb < 0 || fusionNumb > 2){
        return NULL;
    }

    data = malloc(8*sizeof(int));

    data[0] = self->barras[fusionNumb];
    data[1] = self->tipoFusion[fusionNumb];
    data[2] = self->resultado[fusionNumb];
    data[3] = self->compaAni[fusionNumb];
    for(int i = 0; i < 4; i++){
        data[4+i] = self->compaEquipo[fusionNumb][i];
    }

    return data;
}

static int FusionData_setFusionData(FusionData *self, int fusionNumb, int *data){
    //printf("\tif(fusionNumb < 0 || fusionNumb > 2)\n");
    if(fusionNumb < 0 || fusionNumb > 2){
        return -1;
    }

    //printf("\tself->barras[%i] = (unsigned char)data[0]; == %i\n", fusionNumb, data[0]);
    self->barras[fusionNumb] = (unsigned char)data[0];
    //printf("\tself->tipoFusion[%i] = (unsigned char)data[1]; == %i\n", fusionNumb, data[1]);
    self->tipoFusion[fusionNumb] = (unsigned char)data[1];
    //printf("\tself->resultado[%i] = (unsigned char)data[2]; == %i\n", fusionNumb, data[2]);
    self->resultado[fusionNumb] = (unsigned char)data[2];
    //printf("\tself->compaAni[%i] = (unsigned char)data[3]; == %i\n", fusionNumb, data[3]);
    self->compaAni[fusionNumb] = (unsigned char)data[3];
    for(int i = 0; i < 4; i++){
        //printf("\t\tself->compaEquipo[%i][%i] = (unsigned char)data[%i]; == %i\n", fusionNumb, 4+i, 4+i, data[4+i]);
        self->compaEquipo[fusionNumb][i] = (unsigned char)data[4+i];
    }

    return 0;
}

static unsigned char *FusionData_getAsLine(FusionData *self){
    int i, bufferSize = 24;
    unsigned char *buffer = malloc(bufferSize*sizeof(char));

    for(i = 0; i<3; i++){
        buffer[i] = self->barras[i];
    }
    for(i = 0; i<3; i++){
        buffer[i+3] = self->tipoFusion[i];
    }
    for(i = 0; i<3; i++){
        buffer[i+6] = self->resultado[i];
    }
    for(i = 0; i<3; i++){
        buffer[i+9] = self->compaAni[i];
    }

    for(i = 0; i<3; i++){
        for(int j = 0; j<4; j++){
            buffer[12 + i*4 + j] = self->compaEquipo[i][j];
        }
    }
    return buffer;
}
