//
// Created by AngheloAlf10 on 26-10-2017.
//

#include "Py3_TransformClass.h"

static void TransformClass_dealloc(TransformClass* self){
    TransformData_dealloc(self->data);

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *TransformClass_new(PyTypeObject *type, PyObject *args, PyObject *kwds){
    TransformClass *self;

    self = (TransformClass *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->data = TransformData_new();
        self->printData = 0;
    }

    return (PyObject *)self;
}

static int TransformClass_init(TransformClass *self, PyObject *args, PyObject *kwds){
    PyObject *repr, *printData = PyBool_FromLong(0);
    unsigned char *buffer;
    char *reprChar;
    int buffer_size;
    static char *kwlist[] = {"transformData", "printData", NULL};

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

    if(buffer_size != 22){
        errMsg = "'transformData' parameter length must be equal to 22. Got %i.";
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

    TransformData_init(self->data, buffer);

    //Printear datos
    if(self->printData){
        repr = TransformClass_repr(self);
        if(!repr){
            //Error
            return -1;
        }
        reprChar = PyUnicode_AsUTF8(repr);
        Py_DECREF(repr);
        printf("%s\n", reprChar);
        free(reprChar);
    }

    return 0;
}

static PyObject *TransformClass_getTransformData(TransformClass *self, PyObject *args){
    int transformNumb, *data;
    PyObject *listData, *item;

    //Raise error
    char *errMsg, *parsedErrMsg;
    int errMsgLen;

    if(! PyArg_ParseTuple(args, "i", &transformNumb)){
        return NULL;
    }

    if(transformNumb < 0 || transformNumb > 3){
        errMsg = "Parameter can't be greater than 3 or less than 0. Got %i.";
        errMsgLen = (int)strlen(errMsg);

        parsedErrMsg = malloc(errMsgLen*sizeof(char));
        sprintf(parsedErrMsg, errMsg, transformNumb);

        PyErr_SetString(PyExc_ValueError, parsedErrMsg);
        return NULL;
    }

    data = TransformData_getTransformData(self->data, transformNumb);

    listData = PyList_New(5);
    Py_INCREF(listData);
    if(listData == NULL){
        free(data);
        return NULL;
    }
    for(int i = 0; i<5; i++){
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

static PyObject *TransformClass_setTransformData(TransformClass *self, PyObject *args){
    int transformNumb, listSize, *data;
    PyObject *listData, *item;

    //Raise error
    char *errMsg, *parsedErrMsg;
    int errMsgLen;

    if(! PyArg_ParseTuple(args, "iO!", &transformNumb, &PyList_Type, &listData)){
        return NULL;
    }

    Py_INCREF(listData);

    if(transformNumb < 0 || transformNumb > 3){
        errMsg = "First parameter (int) can't be greater than 3 or less than 0. Got %i.";
        errMsgLen = (int)strlen(errMsg);

        parsedErrMsg = malloc(errMsgLen*sizeof(char));
        sprintf(parsedErrMsg, errMsg, transformNumb);

        PyErr_SetString(PyExc_ValueError, parsedErrMsg);
        return NULL;
    }

    listSize = (int)PyList_Size(listData);
    if(listSize != 5){
        errMsg = "Second parameter (list) length can't be different from 5. Got %i.";
        errMsgLen = (int)strlen(errMsg);

        parsedErrMsg = malloc(errMsgLen*sizeof(char));
        sprintf(parsedErrMsg, errMsg, listSize);

        PyErr_SetString(PyExc_ValueError, parsedErrMsg);
        return NULL;
    }

    data = malloc(listSize*sizeof(int));
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
    TransformData_setTransformData(self->data, transformNumb, data);
    //printf("free(data);\n");
    free(data);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *TransformClass_getR3Command(TransformClass *self){
    PyObject *r3Command = PyLong_FromLong(TransformData_getR3Command(self->data));
    if(r3Command == NULL){
        return NULL;
    }
    Py_INCREF(r3Command);
    return r3Command;
}

static PyObject *TransformClass_setR3Command(TransformClass *self, PyObject *args){
    int r3Command;

    //Raise error
    char *errMsg, *parsedErrMsg;
    int errMsgLen;

    if(! PyArg_ParseTuple(args, "i", &r3Command)){
        return NULL;
    }

    if(r3Command < 0 || r3Command > 255){
        errMsg = "First parameter (int) can't be greater than 255 or less than 0. Got %i.";
        errMsgLen = (int)strlen(errMsg);

        parsedErrMsg = malloc(errMsgLen*sizeof(char));
        sprintf(parsedErrMsg, errMsg, r3Command);

        PyErr_SetString(PyExc_ValueError, parsedErrMsg);
        return NULL;
    }

    TransformData_setR3Command(self->data, r3Command);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *TransformClass_getBonus(TransformClass *self){
    PyObject *bonus = PyLong_FromLong(TransformData_getBonus(self->data));
    if(bonus == NULL){
        return NULL;
    }
    Py_INCREF(bonus);
    return bonus;

}

static PyObject *TransformClass_setBonus(TransformClass *self, PyObject *args){
    int bonus;

    //Raise error
    char *errMsg, *parsedErrMsg;
    int errMsgLen;

    if(! PyArg_ParseTuple(args, "i", &bonus)){
        return NULL;
    }

    if(bonus < 0 || bonus > 255){
        errMsg = "First parameter (int) can't be greater than 255 or less than 0. Got %i.";
        errMsgLen = (int)strlen(errMsg);

        parsedErrMsg = malloc(errMsgLen*sizeof(char));
        sprintf(parsedErrMsg, errMsg, bonus);

        PyErr_SetString(PyExc_ValueError, parsedErrMsg);
        return NULL;
    }

    TransformData_setBonus(self->data, bonus);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *TransformClass_getAsLine(TransformClass *self){
    unsigned char *buffer = TransformData_getAsLine(self->data);

    PyObject *line = Py_BuildValue("y#", buffer, 22);
    Py_INCREF(line);
    free(buffer);
    return line;
}

static PyObject *TransformClass_print(TransformClass *self){
    return TransformClass_repr(self);
}

static PyObject *TransformClass_repr(TransformClass *self){
    PyObject *trans = PyList_New(4);
    PyObject *barras = PyList_New(4);
    PyObject *aniCam = PyList_New(4);
    PyObject *aura = PyList_New(4);
    PyObject *abs = PyList_New(4);
    int r3Command, bonus;
    PyObject *repr;
    for(int i = 0; i < 4; i++){
        PyList_SetItem(trans, i, PyLong_FromLong(self->data->trans[i]));
    }
    for(int i = 0; i < 4; i++){
        PyList_SetItem(barras, i, PyLong_FromLong(self->data->barras[i]));
    }
    for(int i = 0; i < 4; i++){
        PyList_SetItem(aniCam, i, PyLong_FromLong(self->data->aniCam[i]));
    }
    for(int i = 0; i < 4; i++){
        PyList_SetItem(aura, i, PyLong_FromLong(self->data->aura[i]));
    }
    for(int i = 0; i < 4; i++){
        PyList_SetItem(abs, i, PyLong_FromLong(self->data->abs[i]));
    }

    r3Command = TransformData_getR3Command(self->data);
    bonus = TransformData_getBonus(self->data);

    repr = PyUnicode_FromFormat("<TransformClass: {trans: %R, barras: %R, aniCam: %R, aura: %R, abs: %R, "
                                        "r3Command: %i, bonus: %i}>",
                                trans, barras, aniCam, aura, abs, r3Command, bonus);
    Py_DECREF(trans);
    Py_DECREF(barras);
    Py_DECREF(aniCam);
    Py_DECREF(aura);
    Py_DECREF(abs);
    return repr;
}


PyMODINIT_FUNC PyInit_TransformClass(void) {
    PyObject* m;

    if (PyType_Ready(&TransformClassType) < 0)
        return NULL;

    m = PyModule_Create(&TransformClassModule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&TransformClassType);
    PyModule_AddObject(m, "TransformClass", (PyObject *)&TransformClassType);
    return m;
}
