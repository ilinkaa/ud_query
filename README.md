# ud_query

# UD Dependency relations analysis for quantitative typology

'queries.py' contains code which executes a query (saved as text file by the user) and extracts the corresponding dependency relations from UD files in conllu format, using the python conllu library. 
The query format is as follows:

  deprel: obj, iobj, xcomp, ccomp/O
  posdep:   
  poshead: VERB/V
  seconddeprel: nsubj, csubj/S
  seconddeppos: 
  
With the fields on the left being mandatory and both dependency relations and pos tags can be specified. What comes after the slash indicates the label under which the relation is to be represented. 
The data is then extracted and stored in a dataframe, which contains all the occurences of the relations found for each label combination. In the case of the example above, this corresponds to all the different
word order combinations. 

'plot.py' takes the resulting dataframes as input, and converts their data into frequency vectors, which can then be concatened together into one single dataframe. From there, a cosine distance matrix is computed
and represented as a heatmap. Afterwards, cluster analysis is applied to the matrix, resulting in a dendrogram. 

This was developed with the intent of exploring the extent to which the frequency of the different patterns for specific dependency relations can be used to group languages of the same family together. The issue of automatic
language classification within the same family has been previously adressed by Liu (2014), in which different dependency measures are used to find common/diverging patterns among Romance languages. 
Additionnally, the position of syntactic units has been used in order to explore the statistical relevance of Greenbergian universals. Here, we examine whether word/ component order as found in UD data can
also be useful for quantitative typology/ language classification for languages with freer/ less predictable word order. For this, we measure word order, as well as the frequency of head-initial
dependencies for four different syntactic constituent combinations: verb-object, verb-auxiliary, noun-adjective and noun-adposition, within the languages available on UD for two different language
families: Uralic and Romance languages. For this, we choose the languages for which corpora bigger than 10K tokens are available, respectively Finnish, Estonian, Hungarian, Komi-Zyrian, Erzya and North Saami, French, Italian,
Spanish,Portugese, Catalan and Romanian. We extract the frequencies for the different combinations, as well as word order, organize them into vectors and use cosine distance to obtain a matrix which is then
used for clustering using the average method. 

The goal is to determine whether clustering for languages for which word order is more fixed is more likely to be succesful when compared to languages with freer word/constituent order. Moreover, we also look at how
constituent order correlates for the four different combinations. 

After compiling the different frequency ration into vectors, we obtain the following heatmap for Uralic languages:

![image](https://github.com/ilinkaa/ud_query/assets/92783469/d25bd6ce-bda6-4547-87d4-9bf8bd9980c8)



Hungarian (Ugric) is set apart from other Uralic languages, being the most different from Finnish (Balto-Finnic) and closest to Komi-Zyrian (Permic).
With regards to clustering, we obtain the following: 

![image](https://github.com/ilinkaa/ud_query/assets/92783469/7582b6a7-cdcc-4a37-9ae0-7a3c9b86c376)


Hungarian has its own branch, with the other languages being grouped together. The other group is split into a cluster containing Ezrya and Komi-Zyrian, and another in which Finnish is grouped together with Estonian, and the resulting group is joined with North Saami. The languages represented here would fall into 5 branches: Ugric, Permic, Mordvinic and Saamic. However, it is important to note that Uralic language 
classification is still up for debate. Here, Estonian and Finnish are correctly grouped together, both falling into the commonly accepted Batlo-Finnic group. Saami however should constitue its own branch, but should be closer to Finnic languages than it is to Hungarian.  
Furthermore, Komi and Ezrya might be grouped together because both of these languages on UD have been produced based on the same translations from Russian, which might be reflected in the dataset. 

In the case of Romance languages, we obtained the following clusters: 

![image](https://github.com/ilinkaa/ud_query/assets/92783469/a493a598-5a96-492b-bb43-1541ddbc45e8)

The cluster succesfully distinguishes between Western Romance and Eastern Romance (Romanian), splitting between two clusters. Inside the second cluster, Spanish and Portuguese are judged to be the most similar, followed by Italian,
with French being the most different inside the group. This follows traditional classifications of Romance languages, with the two Ibero-Romance languages joined together, while a distinction within the Western Romance group
being made between Gallo-Romance and Italic-Romance. If we compared the obtained dendrogram to that represented in Liu (2013), which is based on dependency distance measures exclusively, we can see that Spanish and Portuguese are also
clustered together, followed by Italian and Frehcn and then Romanian. 
It is also important to note that the difference between Romance languages is far less significant than the difference between Uralic languages, as reflected by the value on the y-axis. 

We then apply the Pearson correlation test to the retrieved frequencies of the four different syntactic combinations, and compare it to the one obtained in Courtin (2018). 

![image](https://github.com/ilinkaa/ud_query/assets/92783469/51a2fa68-1975-48af-ae7c-4e634028a792)


For Romance languages, no data for V-AUX was found, hence the 0 correlation. Moreover, the features which seems to correlate the most are N-ADJ and VO, which contradicts Courtin's findings (where noun-adjective was the element presenting the least correlation
with the rest). This can be explained by the fact that the language sample for our experiment is much smaller.

![image](https://github.com/ilinkaa/ud_query/assets/92783469/4e6df8e5-4644-4afa-9efe-79c7ad8379e0)

Here, the strongest correlations are found between verb-object and verb-auxiliary. Verb-object seems to correlate the most with other features, while noun-adjective is the feature that correlates the least, particularly with 
verb-object, like in the data observed by Courtin. 

Therefore, we can see that different elements can reflect language classification in different ways, and that the data available on UD might help investigate the general trends.

**References 

Alzetta, C., Dell’Orletta, F., Montemagni, S., & Venturi, G. (2018, May). Universal dependencies and quantitative typological trends. A case study on word order. In *Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018).


Chen, X., & Gerdes, K. (2017, September). Classifying languages by dependency structure. Typologies of delexicalized universal dependency treebanks. In *Proceedings of the fourth international conference on dependency linguistics (Depling 2017)*
 (pp. 54-63).

Courtin, M. (2018). Mesures de distances syntaxiques entre langues à partir de treebanks.

Liu, H., & Xu, C. (2012). Quantitative typological analysis of Romance languages. Poznań Studies in Contemporary Linguistics, 48(4), 597-625.





