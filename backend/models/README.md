```bash
│      
├───exploratory_notebooks
├───save_models 
└───tests
```

### This folder contains the code for the models.

`exploratory_notebooks` contains the Jupyter notebooks which contain code for model training, hyperparameter tuning, and model explainability.

`save_models` contains the scripts which can be run to obtain the final versions of the model, and also contain the saved models as pkl files.

`tests` contains the unit tests for data pre-processing and metric evaluation for the models 

### Summary of model performance

| | Random Forest | XGBoost | Passive Aggressive Regressor | MLP |
|--|:--:|:--:|:--:|:--:|
| FNR | 34.2% | 32.8% | 0.6% | 33.3% |
| FPR | 4.4% | 4.2% | 99.9% | 5.1% |
