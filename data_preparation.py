import pandas as pd
import numpy as np
import re


def Clean_CSV_Raw():

    # read CSV
    df = pd.read_csv('top10s.csv', encoding='cp1252')
    df = df[["title", "artist", "top genre", "year", "bpm", "nrgy",
             "dnce", "dB", "live", "val", "dur", "acous", "spch", "pop"]]

    # Joining evry column in row to a list
    combine = []
    for row in df.index:
        tmp = str(df[df.index == row][["title", "artist", "top genre", "year", "bpm", "nrgy",
                                       "dnce", "dB", "live", "val", "dur", "acous", "spch", "pop"]].values[0]).split("'")
        combine.append(''.join(tmp))

    list_of_text = combine

    # Clean the List of string data
    clean_spcl = re.compile('[/(){}\[\]\|@.,;"&?®\-]')
    paragraf = ['\n']

    for i in range(len(list_of_text)):
        text = list_of_text[i]
        text = text.lower()  # lowercase text
        text = clean_spcl.sub('', text)
        text = ' '.join(word for word in text.split() if word not in paragraf)
        list_of_text[i] = text

    # list to df
    df_clean = pd.DataFrame(list_of_text, columns=['combine_cleaned'])
    # concat df with df_clean
    joined_df = pd.concat([df, df_clean], axis=1, sort=False)

    return joined_df


def drop_duplikasi(df_musik):
    df_musik = df_musik[["title", "artist", "top genre", "year", "bpm", "nrgy",
                         "dnce", "dB", "live", "val", "dur", "acous", "spch", "pop", "combine_cleaned"]]
    df_clean = df_musik.drop_duplicates(
        subset='title', keep='first', inplace=False, ignore_index=False)
    df_clean.to_csv(r'data_musik_no_duplicate.csv')
    return df_clean


if __name__ == "__main__":
    data = Clean_CSV_Raw()
    drop_duplikasi(data)