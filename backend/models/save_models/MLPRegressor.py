import pandas as pd
import numpy as np
import pickle
from sklearn.neural_network import MLPRegressor
from tqdm.autonotebook import tqdm


#Setting Seed value
seed = 3101
np.random.seed(3101)

def preprocess(df):
    """
    The function removes the columns date, time, station and T{i}S{j}_station number, where i,j ranges from 1 to 6 (inclusive)
    These columns are removed as they are not useful features for the model and are only there for human understandability.
    Any NA values are replaced with 0.

    Args:
        df (pandas dataframe): data that has been read in from sliding_window_data.csv.  
    
    Returns:
        pandas dataframe with no NA values and the stated columns dropped.

    """
    #drop the date, time and station labels 
    drop_cols = ["date","time","station"]
    for i in range(1,7):
        for j in range(1,7):
            drop_cols.append(f"T{i}S{j}_station number")
    processed_df = df.drop(drop_cols, axis=1, inplace=False)
    processed_df.fillna(value=0, inplace=True)
    return processed_df

def train(df_iterator):
    """
    Fits a MLPRegressor with the specified parameters on the full train dataset given in the form of an iterator.

    Args:
        df_iterator (pandas TextFileReader): iterator for the train_dataset with 
        train_label in the 1st column and remaining columns are the feature 
        variables.

    Returns:
        A trained MLPRegressor instance

    """
    regression_model = MLPRegressor(activation="relu", hidden_layer_sizes=(32,), solver="adam", random_state=seed, shuffle=True)
    for batch in tqdm(df_iterator):
        batch = preprocess(batch)
        regression_model.partial_fit(batch.iloc[:,1:], batch.iloc[:,0])
    return regression_model


def evaluate(y_pred,y_true):
    """
    Calculates False Negative rate, False Positive Rate and F1 score of the model prediction
    and prints the 3 metrics to 5dp.
    Assumes any value > 0.0 is considered as prediction as rain.

    Args:
        y_pred (pandas dataframe): predicted labels from the model
        y_true (pandas dataframe): true label
    
    Returns:
        List containing the 3 metrics calculated in the order of 
        [False Negative Rate, False Positive Rate and F1 score]

    """
    threshold = 0.0
    result = pd.DataFrame({'predicted': y_pred, 'actual': y_true}, columns=['predicted', 'actual'])
    fn = result[result['actual'] > threshold]
    fn = fn[round(fn['predicted'],1) <= threshold]
    fnr = len(fn)/len(result[result['actual'] > threshold])

    fp = result[result['actual'] == threshold]
    fp = fp[round(fp['predicted'],1) > threshold]
    fpr = len(fp)/len(result[result['actual'] == threshold])

    tp = result[result['actual'] > threshold]
    tp = tp[round(tp['predicted'],1) > threshold]
    tp = len(tp)

    f1 = tp/(tp+0.5*(len(fp)+len(fn)))
    print(f'False negative rate is : {fnr:.5f}')
    print(f'False positive rate (FP/FP+TN) is : {fpr:.5f}')
    print(f'F1 score is [ TP/(TP + 0.5(FP+FN)) ]: {f1:.5f}')
    return [fnr, fpr, f1]

def save(model, filename):
    """
    Saved the model to the given filename as a pickle file

    Args:
        model: Trained model to be saved
        filename : file name where model is to be saved
    
    """
    pickle.dump(model, open(filename, "wb"))


def main():
    # Train Test split
    # Train 80% - Test 20%
    # Total number of rows = 25 million

    test_index = range(10_000_000,15_000_000+1)

    # Generate iterator for train dataset
    chunksize = 1_000_000
    sliding_window_data = pd.read_csv("sliding_window_data.csv", chunksize=chunksize, iterator=True, skiprows=test_index)

    # Create test dataset
    test_dataset = pd.read_csv("sliding_window_data.csv", header=0, nrows=5_000_000, skiprows=range(1,10_000_000))
    test_dataset = preprocess(test_dataset)

    # Train MLPRegressor model
    mlpregressor_model = train(sliding_window_data)

    # Evaluate model performance and print some statistics
    prediction = mlpregressor_model.predict(test_dataset.iloc[:,1:])
    evaluate(prediction,test_dataset.iloc[:,0])

    # Save model into MLPRegressor.pkl in current directory
    filename = "MLPRegressor.pkl"
    save(mlpregressor_model, filename)


if __name__ == "__main__":
    main()
