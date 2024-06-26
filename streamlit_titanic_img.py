# -*- coding: utf-8 -*-
"""Streamlit_Titanic_IMG.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VSJs-vp2AtLlHYvVeIQPN673XyNM_IQo
"""

# app.py

import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the saved voting classifier model
voting_clf_model = joblib.load('voting_clf_model.pkl')

# HTML and CSS to set the background image
page_bg_img = '''
<style>
body {
    background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQp7xnqk9bEdbVF7Wzmaag8G-ofnkxZyzo1tt_Exm_T6l7Hiw5KqtNeqhpi&s=10");
    background-size: cover;
}
.sidebar .sidebar-content {
    background: rgba(255, 255, 255, 0.8);
}
</style>
'''

# Set the background image
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title and description
st.title("Titanic Survival Prediction")
st.write("""
         Enter the details below to predict the survival on the Titanic.
         """)

# Function to get user input
def get_user_input():
    age = st.sidebar.slider("Age", 0.42, 80.0, 29.69, 0.1)
    sibsp = st.sidebar.slider("Siblings/Spouses Aboard", 0, 8, 0, 1)
    parch = st.sidebar.slider("Parents/Children Aboard", 0, 6, 0, 1)
    fare = st.sidebar.slider("Fare", 0.0, 512.3292, 32.20, 0.1)
    embarked = st.sidebar.selectbox("Embarked", ["S", "C", "Q"])
    pclass = st.sidebar.selectbox("Passenger Class", [1, 2, 3])
    sex = st.sidebar.selectbox("Sex", ["male", "female"])
    cabin_letter = st.sidebar.selectbox("Cabin Letter", ["A", "B", "C", "D", "E", "F", "G", "T", "n"])

    user_data = {
        'Age': age,
        'SibSp': sibsp,
        'Parch': parch,
        'Fare': fare,
        'Embarked': embarked,
        'Pclass': pclass,
        'Sex': sex,
        'CabinLetter': cabin_letter
    }

    features = pd.DataFrame(user_data, index=[0])
    return features

# Get user input
user_input = get_user_input()

# Preprocess input data
numeric_features = ['Age', 'SibSp', 'Parch', 'Fare']
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_features = ['Embarked', 'Pclass', 'Sex', 'CabinLetter']
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder())
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Apply preprocessing to user input
user_input_processed = preprocessor.fit_transform(user_input)

# Prediction
prediction = voting_clf_model.predict(user_input_processed)

# Display input data and prediction
st.subheader("User Input")
st.write(user_input)

st.subheader("Prediction")
st.write("Survived" if prediction[0] == 1 else "Did not survive")
