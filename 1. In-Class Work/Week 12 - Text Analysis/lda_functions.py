import numpy as np
import pandas as pd

def get_top_words(model, features, n_terms=10):
    """
    Displays the top N terms for a lda model generated by scikitlearn
    """
    ls_keywords = []
    ls_freqs = []
    topic_id = []

    for i,topic in enumerate(model.components_):
        # Sorting and finding top keywords
        word_idx = np.argsort(topic)[::-1][:n_terms]
        freqs = list(np.sort(topic)[::-1][:n_terms])
        keywords = [features[i] for i in word_idx]
    
        # Saving keywords and frequencies for later
        ls_keywords = ls_keywords + keywords
        ls_freqs = ls_freqs + freqs
        topic_id = topic_id + [i+1] * n_terms
    

        # Printing top keywords for each topic
        print(i, ', '.join(keywords))

    return pd.DataFrame({'keywords':ls_keywords, 'frequency':ls_freqs, 'topic_id':topic_id})

def get_top_docs(doctopics, n_docs=3, docnames=None):
    """
    Creates a Data Frame with the top n documents for each topic
    """
    if docnames is None:
        docnames = ['doc_'+str(i) for i in range(doctopics.shape[0])]
        
    ls_docs  = []
    ls_probs = []
    topic_id = []

    for i, topic in enumerate(np.transpose(doctopics)):
        # Sorting and finding top keywords
            doc_idx = np.argsort(topic)[::-1][:n_docs]
            probs = list(np.sort(topic)[::-1][:n_docs])
            top_documents = [docnames[i] for i in doc_idx]
    
            ls_docs = ls_docs + top_documents
            ls_probs = ls_probs + probs
            topic_id = topic_id + [i+1] * n_docs

            
    return pd.DataFrame({'documents':ls_docs, 'proportion':ls_probs, 'topic_id':topic_id})

