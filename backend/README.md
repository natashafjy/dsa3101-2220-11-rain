## Folder structure

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
---

## Prediction Workflow

![image](https://user-images.githubusercontent.com/64476154/232062444-324b061d-d04c-4736-b0dd-cb179a0a4c3a.png)

Making use of the models and kriging, our prediction workflow is as follows:

1. The user selects a routine on the frontend's webpage, which returns the (latitude, longitudes) pairs for the start and end points of the user's chosen routine.

2. The most recent rainfall data will from data.gov.sg’s API, and converted into a format that can be passed into our model.

3. Our trained model predicts rainfall amounts at the weather stations throughout Singapore.

4. Kriging is then used to interpolate the values and determine the rainfall value at our point of interest.

---

## Unit Testing

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
