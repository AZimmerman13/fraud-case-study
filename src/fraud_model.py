from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score, precision_score
from sklearn.ensemble import RandomForestClassifier
from cleaning import clean_training_dataframe, make_corpus, prep_corpus, get_top_features_cluster \


if __name__ == "__main__":
    log_regression=False
    randomforest = False
    df = clean_training_dataframe('data/data.json') ## Entire dataset being trained
    # print('Making corpus...')
    # corpus = make_corpus(df)
    # stop_words = set(stopwords.words('english'))
    # extra = ['s', 'de', 'la', 'en', 'et', 'le', 'des', 'de la', 'les', 'vous', 'pour', 'rouen', 'us', 'dec', '00', '2013', '30', '10', 'us', 'www', 'new']
    # all_stop = stop_words.union(extra)
    # print('Prep corpus for tfidf...')
    # prepped_corpus = prep_corpus(corpus)
    
    # vectorizer = TfidfVectorizer(stop_words=all_stop, strip_accents='ascii', ngram_range=(1,2), max_features=5000)
    # X = vectorizer.fit_transform(prepped_corpus)
    # print('Starting kMeans...')
    # kmeans = KMeans(n_clusters=5, random_state=0) 
    # kmeans.fit(X.toarray())
    print('Making modelling dataframe...')
    # df_modelling = df.drop(['description', 'name', 'parsed_desc'], axis=1)
    df_modelling = df.drop(['description', 'name'], axis=1)

    # df_modelling['cluster'] = kmeans.labels_  
    # df_modelling = pd.get_dummies(df_modelling, columns=['cluster'], drop_first=True) 
    y = df_modelling.pop('fraud') 
    X = df_modelling.values
    ss = StandardScaler()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    X_train_scaled = ss.fit_transform(X_train)
    X_test_scaled = ss.transform(X_test)
    if log_regression:
        print('Starting Logistic Regression...')
        lr = LogisticRegression(verbose=True, n_jobs=-1, class_weight='balanced')
        lr.fit(X_train_scaled, y_train)
        preds = lr.predict(X_train_scaled)
        holdout_preds = lr.predict(X_test_scaled)
        # print(f"Training: F1: {f1_score(y_train, preds)}, Recall: {recall_score(y_train, preds)}, Accuracy: {lr.score(X_train_scaled, y_train)}, Precision: {precision_score(y_train, preds)}")
        # print(f"Test: F1: {f1_score(y_test, holdout_preds)}, Recall: {recall_score(y_test, holdout_preds)}, Accuracy: {lr.score(X_test_scaled, y_test)}, Precision: {precision_score(y_test, holdout_preds)}")
    if randomforest:
        print("Starting Random Forest...")
        thresh_list = [0.7, 0.81]
        for i in thresh_list:
            rf = RandomForestClassifier(class_weight='balanced', n_estimators=300, max_features=3, max_leaf_nodes=50, random_state=42, n_jobs=-2, oob_score=True)
            rf.fit(X_train_scaled, y_train)

            rfpreds = rf.predict_proba(X_train_scaled)
            rfpreds = (rfpreds[:,1] >= i).astype('int')

            holdout_preds_rf = rf.predict_proba(X_test_scaled)
            holdout_preds_rf = (holdout_preds_rf[:,1] >= i).astype('int')

            # print(f"With a threshold of {i}:\n")
            # print(f"Training: \nF1: {f1_score(y_train, rfpreds)}, \nRecall: {recall_score(y_train, rfpreds)}, \nAccuracy: {rf.score(X_train_scaled, y_train)}, \nPrecision: {precision_score(y_train, rfpreds)}\n")
            # print(f"Test: \nF1: {f1_score(y_test, holdout_preds_rf)}, \nRecall: {recall_score(y_test, holdout_preds_rf)}, \nAccuracy: {rf.score(X_test_scaled, y_test)}, \nPrecision: {precision_score(y_test, holdout_preds_rf)}\n\n\n")

    model = rf.fit(X, y) ## Final model created

    pickle_model = False
    if pickle_model:
        with open("static/model.pkl", 'wb') as f:
            pickle.dump(model, f)