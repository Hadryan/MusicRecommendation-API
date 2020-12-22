import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

def get_music():
    df = pd.read_csv('./data_musik_no_duplicate.csv')
    df = df[["title","artist","top genre","year","bpm","nrgy","dnce","dB","live","val","dur","acous","spch","pop","combine_cleaned"]]
    return df

def get_cos_sim(data):
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0)
    tfidf_matrix = tf.fit_transform(data)
    cos_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cos_sim

def modelling_recommendation(title, cos_sim, df):
    recommended_title = []
    recommended_artist = []
    recommended_genre = []

    indices = pd.Series(df.title)

    idx = indices[indices == title].index[0]
    print(idx)

    score_series = pd.Series(cos_sim[idx]).sort_values(ascending = False)

    top_10_indexes = list(score_series.iloc[1:21].index)
    
    for i in top_10_indexes:
        recommended_title.append(list(df.title)[i])
        recommended_artist.append(list(df.artist)[i])
        recommended_genre.append(list(df['top genre'])[i])

    recommended_music = pd.DataFrame(columns=['title','artist','genres'])
    recommended_music['title'] = recommended_title
    recommended_music['artist'] = recommended_artist
    recommended_music['genres'] = recommended_genre
        
    return recommended_music

def results(music_title):    
    if music_title == '' or music_title == ' ' or music_title == '  ':
        return 'Music title cannot be empty'
    find_music = get_music()
    list_title = find_music['title'].values.tolist()
    cos_sim = get_cos_sim(find_music['combine_cleaned'])
    
    if find_music['title'].str.contains(music_title).any():
    
        for i in range(len(list_title)):
            tmp_title = list_title[i]
            if music_title in tmp_title:
                music_title = tmp_title
                break
                
        recommendations = modelling_recommendation(music_title,cos_sim,find_music)
        return recommendations.to_dict('records')

    else:
        return 'Music not in Database'
