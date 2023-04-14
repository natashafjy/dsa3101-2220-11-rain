import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
import pickle

# Setting Seed value
seed = 3101
np.random.seed(seed)

def preprocess(df):
    """
    The function removes the columns date, time, station and T{i}S{j}_station number, where i,j ranges from 1 to 6 (inclusive)
    These columns are removed as they are not useful features for the model and are only there for human understandability.
    Any NA values are replaced with 0.

    Args:
        df (pandas Dataframe): data that has been read in from sliding_window_data.csv.  
    
    Returns:
        pandas Dataframe with no NA values and the stated columns dropped.

    """
    # drop the date, time and station labels 
    drop_cols = ["date","time","station"]
    for i in range(1,7):
        for j in range(1,7):
            drop_cols.append(f"T{i}S{j}_station number")
    processed_df = df.drop(drop_cols, axis=1, inplace=False)
    processed_df.fillna(value=0, inplace=True)
    return processed_df


def train(X_train, y_train):
    """
    Fits an XGBoost model on a subset of the full dataset given as input.

    Args:
        X_train (pandas Dataframe): training data for all features 
        y_train (pandas Dataframe): labels for training data 

    Returns:
        A trained XGBoost model instance

    """
    model = xgb.XGBRegressor(n_estimators=500, 
                             max_depth=10,
                             grow_policy="lossguide",
                             learning_rate=0.01,
                             objective="reg:squarederror",
                             reg_alpha=0.5,
                             reg_lambda=0.5,
                             tree_method="hist",
                             random_state=seed,
                             )
    model.fit(X_train, y_train)
    return model

def evaluate(y_pred, y_true):
    """
    Calculates False Negative rate, False Positive Rate and F1 score of the model prediction
    and prints the 3 metrics to 5dp.
    Assumes any value > 0.0 is considered as prediction as rain.

    Args:
        y_pred (pandas Dataframe): predicted labels from the model
        y_true (pandas Dataframe): true label
    
    Returns:
        List containing the 3 metrics calculated in the order of 
        [False Negative Rate, False Positive Rate and F1 score]

    """
    threshold = 0.0
    result = pd.DataFrame({'predicted': y_pred, 'actual': y_true}, columns=['predicted', 'actual'])
    fn = result[result['actual'] > threshold]  ## all actual positives
    fn = fn[round(fn['predicted'], 1) <= threshold]
    fnr = len(fn) / len(result[result['actual'] > threshold])

    fp = result[result['actual'] == threshold]  ## all actual negatives
    fp = fp[round(fp['predicted'], 1) > threshold]
    fpr = len(fp) / len(result[result['actual'] == threshold])

    tp = result[result['actual'] > threshold] ## all actual positive
    tp = tp[round(tp['predicted'], 1) > threshold]
    tp = len(tp)

    f1 = tp / (tp + 0.5*(len(fp) + len(fn)))
    print(f'False negative rate (FN/FN+TP) is : {fnr:.5f}')
    print(f'False positive rate (FP/FP+TN) is : {fpr:.5f}')
    print(f'F1 score is [ TP/(TP + 0.5(FP+FN)) ]: {f1:.5f}')
    return [fnr, fpr, f1]

def save(model, filename):
    """
    Save the model to the given filename as a pickle file

    Args:
        model: Trained model to be saved
        filename : file name where model is to be saved
    
    """
    pickle.dump(model, open(filename, "wb"))


def main():
    # Import subset (2 million rows) of dataset
    # Pre-process data
    sliding_window_data = pd.read_csv('sliding_window_data.csv', nrows=2000000)
    cleaned_data = preprocess(sliding_window_data)
    X_all = cleaned_data.iloc[:,1:]
    y_all = cleaned_data.iloc[:,0]

    # Train-Test split
    # Train 80% - Test 20%
    # Total number of rows = 2 million
    X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, random_state=seed)

    # Train XGBoost model
    xgboost_model = train(X_train, y_train)

    # Evaluate model performance and print some statistics
    prediction = xgboost_model.predict(X_test)
    evaluate(prediction, y_test)

    # Save model into XGBoost.pkl in current directory
    filename = "XGBoost.pkl"
    save(xgboost_model, filename)

if __name__ == "__main__":
    main()

