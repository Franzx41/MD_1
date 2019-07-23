from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import make_scorer, f1_score, confusion_matrix
from sklearn.model_selection import GridSearchCV
import pandas as pd

class Model:
    
    def __init__(self, data, label):
        self.X_train, self.X_test, self.y_train, self.y_test = self.__split_data(data, label)
        self.parameters = {'criterion':('gini', 'entropy'), 
                      'min_samples_split':[2, 3, 4, 6, 8, 10], 
                      'max_depth':[10, 12, 14, 16, 18, 20, 22, None],
                      'min_samples_leaf':[1,2,3]
                     }
        self.best_parameters = {}
    
    def __split_data(self, data, label):
        y = data[label]
        X = data.drop([label], axis=1)
        # 75% training and 25% test
        return train_test_split(X, y, test_size=0.25, random_state=1)

    def find_best_parameters(self, cv=3, average='binary'):
        scorer = make_scorer(f1_score, average=average)
        clf = DecisionTreeClassifier(random_state=1)
        grid = GridSearchCV(clf, self.parameters, scoring=scorer, cv=cv)
        grid = grid.fit(self.X_train, self.y_train)
        return grid
    
    def set_best_parameters(self, parameters):
        self.best_parameters = parameters
    
    def train_test(self):
        clf = DecisionTreeClassifier(**self.best_parameters, random_state=1)
        clf = clf.fit(self.X_train, self.y_train)    
        y_train_pred = clf.predict(self.X_train)
        y_test_pred = clf.predict(self.X_test)
        self.report(y_train_pred, y_test_pred)
        
    def report(self, y_train_pred, y_test_pred):
        print("Train:")
        print("F1 Score:", f1_score(self.y_train, y_train_pred))
        print()
        print("Test:")
        print("F1 Score:", f1_score(self.y_test, y_test_pred))
        tn, fp, fn, tp = confusion_matrix(self.y_test, y_test_pred).ravel()
        print("True negatives: ", tn)
        print("True positives: ", tp)
        print("False negatives: ", fn)
        print("False positives: ", fp)
        