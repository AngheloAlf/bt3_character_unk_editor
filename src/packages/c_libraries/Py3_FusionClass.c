//
// Created by AngheloAlf10 on 26-10-2017.
//

#include "Py3_FusionClass.h"

static void FusionClass_dealloc(FusionClass* self){
    FusionData_dealloc(self->data);

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *FusionClass_new(PyTypeObject *type, PyObject *args, PyObject *kwds){
    FusionClass *self;

    self = (FusionClass *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->data = FusionData_new();
        self->printData = 0;
    }

    return (PyObject *)self;
}

static int FusionClass_init(FusionClass *self, PyObject *args, PyObject *kwds){
    //printf("FusionClass_init()\n");
    PyObject *repr, *printData = PyBool_FromLong(0);
    unsigned char *buffer;
    char *reprChar;
    int buffer_size;
    static char *kwlist[] = {"fusionData", "printData", NULL};

    //Raise error
    char *errMsg, *parsedErrMsg;
    int errMsgLen;

    //printf("if(!PyArg_ParseTupleAndKeywords(args, kwds, \"y#|O!\", kwlist, &buffer, &buffer_size, &PyBool_Type, &printData))\n");
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "y#|O!", kwlist, &buffer, &buffer_size, &PyBool_Type, &printData)){
        return -1;
    }

    //printf("if(!buffer)\n");
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

    FusionData_init(self->data, buffer);

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

static PyObject *FusionClass_getFusionData(FusionClass *self, PyObject *args){
    //printf("FusionClass_getFusionData()\n");
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

    data = FusionData_getFusionData(self->data, fusionNumb);

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

static PyObject *FusionClass_setFusionData(FusionClass *self, PyObject *args){
    //printf("FusionClass_setFusionData()\n");
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

    //printf("FusionData_setFusionData(self->data, fusionNumb, data);\n");
    FusionData_setFusionData(self->data, fusionNumb, data);
    //printf("free(data);\n");
    free(data);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *FusionClass_getAsLine(FusionClass *self){
    //printf("FusionClass_getFusionData()\n");
    unsigned char *buffer = FusionData_getAsLine(self->data);

    PyObject *line = Py_BuildValue("y#", buffer, 24);
    Py_INCREF(line);
    free(buffer);
    return line;
}

static PyObject *FusionClass_print(FusionClass *self){
    return FusionClass_repr(self);
}

static PyObject *FusionClass_repr(FusionClass *self){
    //printf("FusionClass_repr()\n");
    PyObject *barras = PyList_New(3);
    PyObject *tipoFusion = PyList_New(3);
    PyObject *resultado = PyList_New(3);
    PyObject *compaAni = PyList_New(3);
    PyObject *compaEquipo = PyList_New(3);
    PyObject *aux;
    PyObject *repr;
    for(int i = 0; i < 3; i++){
        PyList_SetItem(barras, i, PyLong_FromLong(self->data->barras[i]));
    }
    for(int i = 0; i < 3; i++){
        PyList_SetItem(tipoFusion, i, PyLong_FromLong(self->data->tipoFusion[i]));
    }
    for(int i = 0; i < 3; i++){
        PyList_SetItem(resultado, i, PyLong_FromLong(self->data->resultado[i]));
    }
    for(int i = 0; i < 3; i++){
        PyList_SetItem(compaAni, i, PyLong_FromLong(self->data->compaAni[i]));
    }
    for(int i = 0; i < 3; i++){
        aux = PyList_New(4);
        for(int j = 0; j < 4; j++){
            PyList_SetItem(aux, j, PyLong_FromLong(self->data->compaEquipo[i][j]));
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
