import math
from sklearn.metrics import confusion_matrix

import sys
sys.path.insert(0, "backend/models/save_models")
from MLPRegressor import evaluate

def test_MLP_fpr():
    y_pred = [1.0, 1.0, 1.0, 0, 0, 1.0, 1.0, 0, 0]
    y_true = [1.0, 1.0, 0, 0, 1.0, 0, 1.0, 1.0, 1.0]

    cm = confusion_matrix(y_true, y_pred)

    test_TN = cm[0][0]
    test_FN = cm[1][0]
    test_TP = cm[1][1]
    test_FP = cm[0][1]

    test_fpr = (test_FP) / (test_FP + test_TN)

    fnr, fpr, f1 = evaluate(y_pred, y_true)

    assert(math.isclose(test_fpr, fpr))
    assert ((fpr >= 0) and (fpr <= 1))

def test_MLP_fnr():
    y_pred = [1.0, 1.0, 1.0, 0, 0, 1.0, 1.0, 0, 0]
    y_true = [1.0, 1.0, 0, 0, 1.0, 0, 1.0, 1.0, 1.0]

    cm = confusion_matrix(y_true, y_pred)

    test_TN = cm[0][0]
    test_FN = cm[1][0]
    test_TP = cm[1][1]
    test_FP = cm[0][1]

    test_fnr = (test_FN) / (test_FN + test_TP)

    fnr, fpr, f1 = evaluate(y_pred, y_true)

    assert(math.isclose(test_fnr, fnr))
    assert ((fnr >= 0) and (fnr <= 1))

def test_MLP_f1():
    y_pred = [1.0, 1.0, 1.0, 0, 0, 1.0, 1.0, 0, 0]
    y_true = [1.0, 1.0, 0, 0, 1.0, 0, 1.0, 1.0, 1.0]

    cm = confusion_matrix(y_true, y_pred)

    test_TN = cm[0][0]
    test_FN = cm[1][0]
    test_TP = cm[1][1]
    test_FP = cm[0][1]

    
    test_f1 = (test_TP) / (test_TP + 0.5 * (test_FP + test_FN))

    fnr, fpr, f1 = evaluate(y_pred, y_true)

    assert(math.isclose(test_f1, f1))
    assert ((f1 >= 0) and (f1 <= 1))



    