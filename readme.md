# Fraud Case Study

## Problem Statement

We have been tasked with identifying fraudulent events based on data provided to us by an online event planning company.  Since out product will be identifying potential fraud for further investigation, as opposed to automatically taking down 'fraud' events, we expect that the best approach will be to minimize false negatives.  The business is better suited by a product that is overly cautious in its initial screen, allowing the human agents to make final decision based on their experience or, perhaps less often, contact with the customer.

## Data

The training data came in json format, with XXX,XXX rows and 44 features.  The features contained a lot of information, but not all of it appeared to be helpful in identifying fraud.


imbalanced classes

stratified train_test_split
more methods discussed below

## Pipeline

### Training Data

### Test Data

## Model Selection and Improvement

Literature on the subject indicated that a standard Logistic Regression might perform well in this scenario.  We ran this model with standard hyperparameters and got the following results:
#### 500 Sample subset

| Scoring Metric | Train Score |
|----------------|-------------|
| Accuracy       | 0.92        |
| Recall         | 0.30        |
| F1-score       | 0.42        |

Given the class imbalance, this high-accuracy, poor-recall model is not all that much of a shock.


#### 500 Sample subset
with class_weights='balanced'
| Scoring Metric | Train Score | Test Score |
|----------------|-------------|------------|
| Accuracy       | 0.81        | 0.82
| Recall         | 0.85        | 0.82
| F1-score       | 0.44        | 0.45
| Precision      | 0.29        | 0.31


#### Full Dataset
| Scoring Metric | Train Score | Test Score |
|----------------|-------------|------------|
| Accuracy       | 0.78        | 0.78       |
| Recall         | 0.85        | 0.84       |
| F1-score       | 0.41        | 0.40       |
| Precision      | 0.27        | 0.27       |

to improve this model: oversample, undersample, SMOTE, 


We also wanted to give a non-linear model a shot, so we put together a Random Forest.  

#### 500 Sample subset
| Scoring Metric | Train Score | Test Score |
|----------------|-------------|------------|
| Accuracy       | 0.96        | 0.90       |
| Recall         | 0.97        | 0.64       |
| F1-score       | 0.83        | 0.54       |
| Precision      | 0.73        | 0.47       |


#### Full Dataset
| Scoring Metric | Train Score | Test Score |
|----------------|-------------|------------|
| Accuracy       | 0.83        | 0.79       |
| Recall         | 0.92        | 0.88       |
| F1-score       | 0.50        | 0.49       |
| Precision      | 0.34        | 0.34       |


## Flask Implementation

## Results

