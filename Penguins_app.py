### Classification web app (Streamlit)
import numpy as np
import pandas as pd
import streamlit as st
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import plotly.express as px
from tensorflow import keras

st.title("Penguins Classification Using Machine Learning")
st.write("""
## Prediction using different classifiers
""")

classifier_name=st.sidebar.selectbox("Select Classifier", ("KNN", "SVM", "Random Forest"))

data= pd.read_csv("peng.csv")

X=data.iloc[:, -4:]
y=data.iloc[:, :1]

st.write("Shape of dataset", X.shape)
st.write("Number of classes", len(np.unique(y)))

def add_parameter_ui(clf_name):
    params=dict()
    if clf_name=="KNN":
        K=st.sidebar.slider("K", 1,15 )
        params["K"]=K
    elif clf_name=="SVM":
         C=st.sidebar.slider("C", 0.01,10.0 )
         params["C"]=C
    else:
        max_depth=st.sidebar.slider("max_depth", 2,15 )
        n_estimators=st.sidebar.slider("n_estimators", 1,100 )
        params["max_depth"]=max_depth
        params["n_estimators"]=n_estimators

    return params

params=add_parameter_ui(classifier_name)
def get_classifier(clf_name, params):
    if clf_name=="KNN":
        clf=KNeighborsClassifier(n_neighbors=params["K"])
    
    elif clf_name=="SVM":
         clf=SVC(C=params["C"])
    else:
        clf=RandomForestClassifier(n_estimators=params["n_estimators"],
                                    max_depth=params["max_depth"], random_state=100)

    return clf
clf=get_classifier(classifier_name, params)

##classification
X_train, X_test, y_train, y_test=train_test_split(X,y, test_size=0.2, random_state=100)
clf.fit(X_train, y_train)
y_pred=clf.predict(X_test)
acc=accuracy_score(y_test, y_pred)
st.write(f"Classifier={classifier_name}")
st.write(f"Accuracy={acc}")

###plotting
pca=PCA(2)
X_projected=pca.fit_transform(X)
x1 = X_projected[:, 0]
x2 = X_projected[:, 1]

N=344
colors = np.random.rand(N)
fig=plt.figure()
plt.scatter(x1, x2, c=colors, cmap="viridis")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar()
st.pyplot(fig)
