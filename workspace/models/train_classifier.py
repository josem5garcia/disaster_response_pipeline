import sys, pickle, re
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sqlalchemy import create_engine

def load_data(database_filepath):
    '''
    Loads data from the database
    INPUTS: database path
    OUTPUT: messages, categories and categories names
    '''
    table_name = 'messages_disaster'
    engine = create_engine(f"sqlite:///{database_filepath}")
    df = pd.read_sql_table(table_name, con=engine)
    X = df["message"]
    y = df.drop(["message","id","genre","original"], axis=1)
    category_names = y.columns
    
    return X, y, category_names


def tokenize(text):
    '''
    Tokenizes text
    INPUTS: text
    OUTPUT: tokenized text
    '''
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)
    
    return clean_tokens

def build_model():
    '''
    Creates the ML model with a pipeline and GridSearch
    INPUTS: None
    OUTPUT: model
    '''
    pipeline = Pipeline([
                         ('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultiOutputClassifier(RandomForestClassifier()))
                        ])
    
    parameters = {
                  'clf__estimator__n_estimators': [50, 100]
                 } 
    cv = GridSearchCV(pipeline, param_grid=parameters)    
    
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    '''
    Test the performance of the model
    INPUTS: model, X & Y test data, and names of the categories
    OUTPUT: 
    '''
    y_pred = model.predict(X_test)
    
    print(classification_report(y_pred, Y_test.values, target_names=category_names))
    
    print('Accuracy Score: {}'.format(np.mean(Y_test.values == y_pred)))


def save_model(model, model_filepath):
    '''
    Save model into directory
    INPUTS: model and path
    OUTPUT: None
    '''
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
