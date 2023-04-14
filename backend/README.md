This folder contains the following subfolders relating to the backend:

```bash
dsa3101-2220-11-rain
│       
└───backend
    │      
    ├───data
    │ 
    ├───data-collection-preparation
    │   │  
    │   └───exploratory_notebooks
    │ 
    ├───flask-app
    │   │       
    │   ├───data
    │   └───dump 
    │   
    ├───kriging
    │ 
    └───models 
        │       
        ├───exploratory_notebooks
        ├───save_models
        └───tests
```

To do unit testing for models:
```bash
cd backend/models/tests
pytest
```

To do unit testing for flask-app:
```bash
cd backend/flask-app
pytest
```
