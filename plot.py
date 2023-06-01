import pandas as pd 
import os 
import itertools
import numpy 
import matplotlib.pyplot as plt
from scipy.spatial import distance
import seaborn as sns


""" This script generates a hierarchy dendrogram based on dependency relation frequency data """

ud_directory ="C:\\Users\\Ilinca V\\stats_vecs_uralic\\"
text_files = [f for f in os.listdir(ud_directory) if "distance"  not in f and 'uralic' in f and f.endswith('.csv')  ]

temps = pd.read_csv("C:\\Users\\Ilinca V\\stats_vecs_uralic\\WORD_ORDER_uralic.csv", index_col=0)
get_ind = temps.index
bigdataf = pd.DataFrame(index = get_ind,columns=["Vec"])

def get_vec(name : str):
    "Converts dataframe values into vectors containing the frequency values for the different patterns"
    df = pd.read_csv(str("C:\\Users\\Ilinca V\\stats_vecs_uralic\\"+name), index_col=0)
    df =df.fillna(0)

    new_df = pd.DataFrame(index = df.index, columns=["Vecs"])
    for i in df.index:
        total = 0 
        values = []
        freq = []
        for j in df.columns:
            total = total + df.loc[i,j]
            values.append(df.loc[i,j])
        
        numpy.asarray(values)
        freq = values/total
        new_df.loc[i,"Vecs"] = freq

    return new_df


list_dfs = []
for i in text_files:
   temp_vec = get_vec(i)
   list_dfs.append(temp_vec)

def concatenate(list_of_dfs:list):
    "Concatenates the frequency vectors from the dataframes"
    results = pd.DataFrame(index = temps.index, columns=["Vecs"])
    for i in temps.index:
        res_arr = []
        for j in list_of_dfs:
            res_arr.append(j.loc[i,"Vecs"])
        res = numpy.hstack(res_arr)
        results.loc[i,"Vecs"] = res
    results =results.fillna(0)
    return results

# concatenated dataframe 
to_calc = concatenate(list_dfs)


from scipy.spatial import distance



def dist_matrx(df:pd.DataFrame):
    "Creates cosine distance matrix"
    reversed_df = pd.DataFrame(index = ["Vecs"], columns = df.index)
    for i in reversed_df.columns:
        reversed_df[i]= df.loc[i] 
    final_df = pd.DataFrame(index = df.index, columns = df.index)

    for j in reversed_df.columns: 
        col_lang = reversed_df.loc["Vecs",j]
        for i,row in df.iterrows():
            row_lang = df.loc[i,"Vecs"]
            cos_res = distance.cosine(col_lang,df.loc[i,"Vecs"])
            final_df.loc[i,j] = cos_res
    final_df = final_df[final_df.columns].astype(float)
    final_df = final_df.fillna(0)
    return final_df


# distance matrix containing the data for Uralic 
distance_matrix = dist_matrx(to_calc)

sns.heatmap(distance_matrix)
plt.show()
X = numpy.array(distance_matrix.values)

from sklearn.cluster import AgglomerativeClustering
from scipy.cluster import hierarchy

from scipy.cluster.hierarchy import ClusterWarning
from warnings import simplefilter
simplefilter("ignore", ClusterWarning)
clusters = hierarchy.linkage(X, method="weighted")

dendrogram = hierarchy.dendrogram(clusters,labels = temps.index)

plt.show()
