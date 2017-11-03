//
// Created by AngheloAlf10 on 26-10-2017.
//
#include <Python.h>
#include <structmember.h>
#include "TransformClass.c"

#ifndef PY3_FUSIONCLASS_LIBRARY_H
#define PY3_FUSIONCLASS_LIBRARY_H

typedef struct {
    PyObject_HEAD
    TransformData *data;
    int printData;
} TransformClass;

static void TransformClass_dealloc(TransformClass* self);

static PyObject *TransformClass_new(PyTypeObject *type, PyObject *args, PyObject *kwds);

static int TransformClass_init(TransformClass *self, PyObject *args, PyObject *kwds);

static PyObject *TransformClass_getTransformData(TransformClass *self, PyObject *args);

static PyObject *TransformClass_setTransformData(TransformClass *self, PyObject *args);

static PyObject *TransformClass_getR3Command(TransformClass *self);

static PyObject *TransformClass_setR3Command(TransformClass *self, PyObject *args);

static PyObject *TransformClass_getBonus(TransformClass *self);

static PyObject *TransformClass_setBonus(TransformClass *self, PyObject *args);

static PyObject *TransformClass_getAsLine(TransformClass *self);

static PyObject *TransformClass_print(TransformClass *self);

static PyObject *TransformClass_repr(TransformClass *self);


PyDoc_STRVAR(
        TransformClass_getTransformData_doc,
        "getTransformData(charNumb)\n"
                "--\n"
                "\n"
                "Returns a list[int] with the data of the selected transformation.\n"
                "Arguments: (charNumb: 0<=int<=3)\n"
                "Doc blahblah doc doc doc."
);
PyDoc_STRVAR(
        TransformClass_setTransformData_doc,
        "setTransformData(charNumb, listData)\n"
                "--\n"
                "\n"
                "Returns None.\n"
                "Arguments: (charNumb: 0<=int<=3, listData: list[int] )\n"
                "Doc blahblah doc doc doc."
);
PyDoc_STRVAR(
        TransformClass_getR3Command_doc,
        "getR3Command()\n"
                "--\n"
                "\n"
                "Returns a int with the r3Command data.\n"
                "Arguments: ()\n"
                "Doc blahblah doc doc doc."
);
PyDoc_STRVAR(
        TransformClass_setR3Command_doc,
        "setR3Command(r3Command)\n"
                "--\n"
                "\n"
                "Returns None.\n"
                "Arguments: (r3Command: 0<=int<=255)\n"
                "Doc blahblah doc doc doc."
);
PyDoc_STRVAR(
        TransformClass_getBonus_doc,
        "getBonus()\n"
                "--\n"
                "\n"
                "Returns a int with the bonus data.\n"
                "Arguments: ()\n"
                "Doc blahblah doc doc doc."
);
PyDoc_STRVAR(
        TransformClass_setBonus_doc,
        "setBonus(bonus)\n"
                "--\n"
                "\n"
                "Returns None.\n"
                "Arguments: (bonus: 0<=int<=255)\n"
                "Doc blahblah doc doc doc."
);
PyDoc_STRVAR(
        TransformClass_getAsLine_doc,
        "getAsLine()\n"
                "--\n"
                "\n"
                "Returns the binary line of the transformation.\n"
                "Arguments: ()\n"
                "Doc blahblah doc doc doc."
);


static PyMethodDef TransformClass_methods[] = {
        {"getTransformData", (PyCFunction)TransformClass_getTransformData, METH_VARARGS, TransformClass_getTransformData_doc},
        {"setTransformData", (PyCFunction)TransformClass_setTransformData, METH_VARARGS, TransformClass_setTransformData_doc},
        {"getR3Command", (PyCFunction)TransformClass_getR3Command, METH_NOARGS, TransformClass_getR3Command_doc},
        {"setR3Command", (PyCFunction)TransformClass_setR3Command, METH_VARARGS, TransformClass_setR3Command_doc},
        {"getBonus", (PyCFunction)TransformClass_getBonus, METH_NOARGS, TransformClass_getBonus_doc},
        {"setBonus", (PyCFunction)TransformClass_setBonus, METH_VARARGS, TransformClass_setBonus_doc},
        {"getAsLine", (PyCFunction)TransformClass_getAsLine, METH_NOARGS, TransformClass_getAsLine_doc},
        {NULL}  /* Sentinel */
};


static PyMemberDef TransformClass_members[] = {
        {NULL}  /* Sentinel */
};

static PyTypeObject TransformClassType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        "TransformClass.TransformClass",  /* tp_name */
        sizeof(TransformClass),         /* tp_basicsize */
        0,                          /* tp_itemsize */
        (destructor)TransformClass_dealloc, /* tp_dealloc */
        (printfunc)TransformClass_print, /* tp_print */
        0,                       /* tp_getattr */
        0,                       /* tp_setattr */
        0,                       /* tp_reserved */
        (reprfunc)TransformClass_repr, /* tp_repr */
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
        "TransformClass doc",         /* tp_doc */
        0,                         /* tp_traverse */
        0,                         /* tp_clear */
        0,                         /* tp_richcompare */
        0,                         /* tp_weaklistoffset */
        0,                         /* tp_iter */
        0,                         /* tp_iternext */
        TransformClass_methods,       /* tp_methods */
        TransformClass_members,       /* tp_members */
        0,                         /* tp_getset */
        0,                         /* tp_base */
        0,                         /* tp_dict */
        0,                         /* tp_descr_get */
        0,                         /* tp_descr_set */
        0,                         /* tp_dictoffset */
        (initproc)TransformClass_init,/* tp_init */
        0,                         /* tp_alloc */
        TransformClass_new,           /* tp_new */
};

static PyModuleDef TransformClassModule = {
        PyModuleDef_HEAD_INIT,
        "TransformClassClass",
        "Manejador para los datos de transformacion.",
        -1,
        NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit_TransformClass(void);

#endif
