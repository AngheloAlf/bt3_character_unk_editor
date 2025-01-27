//
// Created by AngheloAlf10 on 26-10-2017.
//
#include <Python.h>
#include <structmember.h>
#include "FusionClass.c"

#ifndef PY3_FUSIONCLASS_LIBRARY_H
#define PY3_FUSIONCLASS_LIBRARY_H

typedef struct {
    PyObject_HEAD
    FusionData *data;
    int printData;
} FusionClass;

static void FusionClass_dealloc(FusionClass* self);

static PyObject *FusionClass_new(PyTypeObject *type, PyObject *args, PyObject *kwds);

static int FusionClass_init(FusionClass *self, PyObject *args, PyObject *kwds);

static PyObject *FusionClass_getFusionData(FusionClass *self, PyObject *args);

static PyObject *FusionClass_setFusionData(FusionClass *self, PyObject *args);

static PyObject *FusionClass_getAsLine(FusionClass *self);

static PyObject *FusionClass_print(FusionClass *self);

static PyObject *FusionClass_repr(FusionClass *self);


PyDoc_STRVAR(
        FusionClass_getFusionData_doc,
        "getFusionData(fusionNumb)\n"
                "--\n"
                "\n"
                "Returns a list[int] with the data of the selected fusion.\n"
                "Arguments: (fusionNumb: 0<=int<=2)\n"
                "Doc blahblah doc doc doc."
);
PyDoc_STRVAR(
        FusionClass_setFusionData_doc,
        "setFusionData(fusionNumb, listData)\n"
                "--\n"
                "\n"
                "Returns None.\n"
                "Arguments: (fusionNumb: 0<=int<=2, listData: list[int])\n"
                "Doc blahblah doc doc doc."
);
PyDoc_STRVAR(
        FusionClass_getAsLine_doc,
        "getAsLine()\n"
                "--\n"
                "\n"
                "Returns the binary line of the fusions.\n"
                "Arguments: ()\n"
                "Doc blahblah doc doc doc."
);

static PyMethodDef FusionClass_methods[] = {
        /*{"name", (PyCFunction)Noddy_name, METH_NOARGS,
                "Return the name, combining the first and last name"
        },*/
        {"getFusionData", (PyCFunction)FusionClass_getFusionData, METH_VARARGS, FusionClass_getFusionData_doc},
        {"setFusionData", (PyCFunction)FusionClass_setFusionData, METH_VARARGS, FusionClass_setFusionData_doc},
        {"getAsLine", (PyCFunction)FusionClass_getAsLine, METH_NOARGS, FusionClass_getAsLine_doc},
        {NULL}  /* Sentinel */
};

static PyMemberDef FusionClass_members[] = {
        {NULL}  /* Sentinel */
};
static PyTypeObject FusionClassType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        "FusionClass.FusionClass",  /* tp_name */
        sizeof(FusionClass),         /* tp_basicsize */
        0,                          /* tp_itemsize */
        (destructor)FusionClass_dealloc, /* tp_dealloc */
        (printfunc)FusionClass_print, /* tp_print */
        0,                       /* tp_getattr */
        0,                       /* tp_setattr */
        0,                       /* tp_reserved */
        (reprfunc)FusionClass_repr, /* tp_repr */
        0,                       /* tp_as_number */
        0,                       /* tp_as_sequence */
        0,                       /* tp_as_mapping */
        0,                       /* tp_hash */
        0,                       /* tp_call */
        0,                       /* tp_str */
        0,                       /* tp_getattro */
        0,                       /* tp_setattro */
        0,                       /* tp_as_buffer */
        Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,       /* tp_flags */
        "FusionClass doc",         /* tp_doc */
        0,                         /* tp_traverse */
        0,                         /* tp_clear */
        0,                         /* tp_richcompare */
        0,                         /* tp_weaklistoffset */
        0,                         /* tp_iter */
        0,                         /* tp_iternext */
        FusionClass_methods,       /* tp_methods */
        FusionClass_members,       /* tp_members */
        0,                         /* tp_getset */
        0,                         /* tp_base */
        0,                         /* tp_dict */
        0,                         /* tp_descr_get */
        0,                         /* tp_descr_set */
        0,                         /* tp_dictoffset */
        (initproc)FusionClass_init,/* tp_init */
        0,                         /* tp_alloc */
        FusionClass_new,           /* tp_new */
};

static PyModuleDef FusionClassModule = {
        PyModuleDef_HEAD_INIT,
        "FusionClass",
        "Manejador para los datos de fusion.",
        -1,
        NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit_FusionClass(void);

#endif
