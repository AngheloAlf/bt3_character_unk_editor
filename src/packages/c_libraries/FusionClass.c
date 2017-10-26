//
// Created by AngheloAlf10 on 22-10-2017.
//

#include "FusionClass.h"

static void FusionClass_dealloc(FusionData* self){
    free(self->barras);
    free(self->tipoFusion);
    free(self->resultado);
    free(self->compaAni);
    free(self->compaEquipo);

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *FusionClass_new(PyTypeObject *type, PyObject *args, PyObject *kwds){
    FusionData *self;

    self = (FusionData *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->barras = malloc(sizeof(char)*3);
        self->tipoFusion = malloc(sizeof(char)*3);
        self->resultado = malloc(sizeof(char)*3);
        self->compaAni = malloc(sizeof(char)*3);
        self->compaEquipo = malloc(sizeof(char *)*3);
        for(int i = 0; i<3; i++){
            self->compaEquipo[i] = malloc(sizeof(char)*4);
        }

        self->printData = 0;
    }

    return (PyObject *)self;
}

static int FusionClass_init(FusionData *self, PyObject *args, PyObject *kwds) {
    PyObject *repr, *printData = PyBool_FromLong(0);
    unsigned char *buffer;
    char *reprChar;
    int buffer_size;
    static char *kwlist[] = {"fusionData", "printData", NULL};

    //Raise error
    char *errMsg, *parsedErrMsg;
    int errMsgLen;

    int i;

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "y#|O!", kwlist, &buffer, &buffer_size, &PyBool_Type, &printData)) {
        return -1;
    }

    if(!buffer){ //Error
        Py_DECREF(printData);
        return -1;
    }

    if(buffer_size != 24){
        errMsg = "'fusionData' parameter length must be equal to 24. Got %i.";
        errMsgLen = (int)strlen(errMsg);

        parsedErrMsg = malloc(errMsgLen*sizeof(char));
        sprintf(parsedErrMsg, errMsg, buffer_size);

        PyErr_SetString(PyExc_ValueError, parsedErrMsg);
        return -1;
    }

    //PrintData
    if(PyObject_IsTrue(printData)){
        self->printData = 1;
    }
    else{
        self->printData = 0;
    }
    Py_DECREF(printData);

    //printf("for(i = 0; i<3; i++)\n");
    for(i = 0; i<3; i++){
        //printf("\tself->barras[%i] = buffer[%i]\n", i, i);
        //printf("\tbuffer[%i] = %i\n", i, buffer[i]);
        self->barras[i] = buffer[i];
    }
    //printf("for(i = 0; i<3; i++)\n");
    for(i = 0; i<3; i++){
        //printf("\tself->tipoFusion[%i] = buffer[%i]\n", i, i+3);
        //printf("\tbuffer[%i] = %i\n", i+3, buffer[i+3]);
        self->tipoFusion[i] = buffer[i+3];
    }
    //printf("for(i = 0; i<3; i++)\n");
    for(i = 0; i<3; i++){
        //printf("\tself->resultado[%i] = buffer[%i]\n", i, i+6);
        //printf("\tbuffer[%i] = %i\n", i+6, buffer[i+6]);
        self->resultado[i] = buffer[i+6];
    }
    //printf("for(i = 0; i<3; i++)\n");
    for(i = 0; i<3; i++){
        //printf("\tself->compaAni[%i] = buffer[%i]\n", i, i+9);
        //printf("\tbuffer[%i] = %i\n", i+6, buffer[i+9]);
        self->compaAni[i] = buffer[i+9];
    }
    //printf("for(i = 0; i<3; i++)\n");
    for(i = 0; i<3; i++){
        //printf("\tfor(int j = 0; j<4; j++)\n");
        for(int j = 0; j<4; j++){
            //printf("\t\tself->compaEquipo[%i][%i] = buffer[%i]\n", i, j, 12 + i*4 + j);
            //printf("\t\tbuffer[%i] = %i\n", 12 + i*4 + j, buffer[12 + i*4 + j]);
            self->compaEquipo[i][j] = buffer[12 + i*4 + j];
        }
    }

    //Printear datos
    if(self->printData){
        repr = FusionClass_repr(self);
        if(!repr){
            //Error
            return -1;
        }
        reprChar = PyUnicode_AsUTF8(repr);
        Py_DECREF(repr);
        printf("%s\n", reprChar);
    }

    return 0;
}

static PyObject *FusionClass_getFusionData(FusionData *self, PyObject *args){
    int fusionNumb, *data;
    PyObject *listData, *item;

    //Raise error
    char *errMsg, *parsedErrMsg;
    int errMsgLen;

    if(! PyArg_ParseTuple(args, "i", &fusionNumb)){
        return NULL;
    }

    if(fusionNumb < 0 || fusionNumb > 2){
        errMsg = "Parameter can't be greater than 2 or less than 0. Got %i.";
        errMsgLen = (int)strlen(errMsg);

        parsedErrMsg = malloc(errMsgLen*sizeof(char));
        sprintf(parsedErrMsg, errMsg, fusionNumb);

        PyErr_SetString(PyExc_ValueError, parsedErrMsg);
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

    listData = PyList_New(8);
    Py_INCREF(listData);
    if(listData == NULL){
        free(data);
        return NULL;
    }
    for(int i = 0; i<8; i++){
        item = PyLong_FromLong(data[i]);
        if(item==NULL){
            Py_DECREF(listData);
            free(data);
            return NULL;
        }
        PyList_SetItem(listData, i, item);
        Py_XDECREF(item);
    }
    free(data);
    return listData;
}

static PyObject *FusionClass_setFusionData(FusionData *self, PyObject *args){
    int fusionNumb, listSize, *data;
    PyObject *listData, *item;

    //Raise error
    char *errMsg, *parsedErrMsg;
    int errMsgLen;

    if(! PyArg_ParseTuple(args, "iO!", &fusionNumb, &PyList_Type, &listData)){
        return NULL;
    }

    Py_INCREF(listData);

    if(fusionNumb < 0 || fusionNumb > 2){
        errMsg = "First parameter (int) can't be greater than 2 or less than 0. Got %i.";
        errMsgLen = (int)strlen(errMsg);

        parsedErrMsg = malloc(errMsgLen*sizeof(char));
        sprintf(parsedErrMsg, errMsg, fusionNumb);

        PyErr_SetString(PyExc_ValueError, parsedErrMsg);
        return NULL;
    }

    listSize = (int)PyList_Size(listData);
    if(listSize != 8){
        errMsg = "Second parameter (list) length can't be different from 8. Got %i.";
        errMsgLen = (int)strlen(errMsg);

        parsedErrMsg = malloc(errMsgLen*sizeof(char));
        sprintf(parsedErrMsg, errMsg, listSize);

        PyErr_SetString(PyExc_ValueError, parsedErrMsg);
        return NULL;
    }

    data = malloc(8*sizeof(int));
    for(int i = 0; i < listSize; i++){
        item = PyList_GetItem(listData, i);
        if(item == NULL){
            Py_DECREF(listData);
            return NULL;
        }
        Py_INCREF(item);
        data[i] = (int)PyLong_AsLong(item);
        //printf("\tdata[%i] = %i\n", i, data[i]);
        Py_DECREF(item);
    }
    Py_DECREF(listData);

    self->barras[fusionNumb] = (unsigned char)data[0];
    self->tipoFusion[fusionNumb] = (unsigned char)data[1];
    self->resultado[fusionNumb] = (unsigned char)data[2];
    self->compaAni[fusionNumb] = (unsigned char)data[3];
    for(int i = 0; i < 4; i++){
        self->compaEquipo[fusionNumb][i] = (unsigned char)data[4+i];
    }
    free(data);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *FusionClass_getAsLine(FusionData *self){
    int i, bufferSize = 24;
    char *buffer = malloc(bufferSize*sizeof(char));

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

    PyObject *line = Py_BuildValue("y#", buffer, bufferSize);
    Py_INCREF(line);
    free(buffer);
    return line;
}

static PyObject *FusionClass_print(FusionData *self){
    return FusionClass_repr(self);
}

static PyObject *FusionClass_repr(FusionData *self){
    PyObject *barras = PyList_New(3);
    PyObject *tipoFusion = PyList_New(3);
    PyObject *resultado = PyList_New(3);
    PyObject *compaAni = PyList_New(3);
    PyObject *compaEquipo = PyList_New(3);
    PyObject *aux;
    PyObject *repr;
    for(int i = 0; i < 3; i++){
        PyList_SetItem(barras, i, PyLong_FromLong(self->barras[i]));
    }
    for(int i = 0; i < 3; i++){
        PyList_SetItem(tipoFusion, i, PyLong_FromLong(self->tipoFusion[i]));
    }
    for(int i = 0; i < 3; i++){
        PyList_SetItem(resultado, i, PyLong_FromLong(self->resultado[i]));
    }
    for(int i = 0; i < 3; i++){
        PyList_SetItem(compaAni, i, PyLong_FromLong(self->compaAni[i]));
    }
    for(int i = 0; i < 3; i++){
        aux = PyList_New(4);
        for(int j = 0; j < 4; j++){
            PyList_SetItem(aux, j, PyLong_FromLong(self->compaEquipo[i][j]));
        }
        PyList_SetItem(compaEquipo, i, aux);
    }

    repr = PyUnicode_FromFormat("<FusionClass: {barras: %R, tipoFusion: %R, resultado: %R, compaAni: %R, compaEquipo: %R}>",
                                          barras, tipoFusion, resultado, compaAni, compaEquipo);
    Py_DECREF(barras);
    Py_DECREF(tipoFusion);
    Py_DECREF(resultado);
    Py_DECREF(compaAni);
    Py_DECREF(compaEquipo);
    return repr;
}

PyMODINIT_FUNC PyInit_FusionClass(void) {
    PyObject* m;

    if (PyType_Ready(&FusionClassType) < 0)
        return NULL;

    m = PyModule_Create(&FusionClassModule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&FusionClassType);
    PyModule_AddObject(m, "FusionClass", (PyObject *)&FusionClassType);
    return m;
}
