from conllu import parse_incr, parse, parse_tree_incr, parse_tree
from conllu import TokenTree, TokenList, Token
from conllu.exceptions import ParseException
from conllu.serializer import serialize
import pandas as pd 
import re 
import os
from collections import defaultdict
from collections import Counter


"""This script parses a conllu file using the conllu library and allows the user to search the file for
# dependency relations, which can be restricted to specific POSs for both head and dependent. The program
# additionally compares the index of a dependent and that of its head to determine the amount of head initial
# and head final relations found in the specific file  """


"""
The format for the query file (plain txt file) is the following (example for word order query w/ subject and object):
nameofqueryelement: deprel (or POS) / LABEL

Example:
deprel: obj, iobj, xcomp, ccomp/O
posdep:
poshead: VERB/V
secondddeprel: nsubj,csubj/S
seconddepos:



"""


class UD_Query:
    """ Class UD_Query contains a query object, initialized with the name of the file to be processed and the query file"""
    def __init__(self,conllu_file, query_file ):
        
        def pros_file(conllu_file):
            """Processes conllu file using conllu library"""
            data_file = open(conllu_file, "r", encoding="utf-8")
            data= data_file.read()
            sentences = parse_tree(data)
            return sentences
        


        def process_query(file1):
            """Processes query file in specific format. Returns one dictionnary w/ the query itself and another one w/ the labels"""
            with open(file1) as my_file:
                # dictionnary for storing query and queried elements
                query_dict = {}
                # dictionnary to store queried elements and their labels
                labels_dict = {}
                Lines = my_file.readlines()
                for line in Lines:
                    line = line.strip()
                    # gets query element (first element in line before:)
                    queryposition = re.sub(r':(.*)\/(.*)',"",line)
                    
                    queryposition = queryposition.replace(":","")
                    
                    # get the query label (element before /)
                    label = re.findall(r"\/(.*)",line)
                    queries = re.findall(r':(.*)\/',line)
                    # gets the query itself
                    queries = re.sub(r'^(.*?):', '', line)
                    queries = re.sub(r'/(.*)', '', queries)
                    
                    if len(queries)!= 0:
                        # splits in case there are several labels to search for
                        query = queries.split(",")
                        qlist = [x.strip() for x in query if x]
                        
                        # if particular deprel/Pos to search for 
                        if qlist == ['']:
                            qlist = []
                            query_dict[queryposition] = qlist
                        else:
                            query_dict[queryposition] = qlist

                        if label ==[]:
                            labels_dict[tuple(qlist)] = []
                        
                        else:
                            labels_dict[tuple(qlist)] = label[0]
                    else:
                        query_dict[queryposition] = []
            # in the case that there is no queried element for the head but a label, key is set to X for retrieval
            new_dict_labels = {}
            for i in labels_dict:
                if i == ():
                    temp = ['X']
                    new_dict_labels[tuple(temp)] = labels_dict[i]
                else:
                    new_dict_labels[i] = labels_dict[i]
                    
            
            return query_dict, new_dict_labels
        
      
        self.conllu_file = pros_file(conllu_file)
        self.query_file, self.labels = process_query(query_file)
        nom_file = conllu_file.replace(".conllu","")
        # gets name of language from file 
        nom_file = re.sub(r"C:\\(.*)\\","",nom_file)
        self.filename = nom_file

saami_test = UD_Query("C:\\Users\\Ilinca V\\Documents\\saamiexample.conllu","C:\\Users\\Ilinca V\\Documents\\query.txt")


def _get_as_dict(tree_node: TokenTree):
    """Creates three dictionnary from token tree for look up, w/ id, head and deprel as keys"""
    dict_id = {}
    dict_head = defaultdict(list)
    dict_rel = defaultdict(list)
    to_traverse = [tree_node]
    while len(to_traverse):
        node = to_traverse.pop()
        
        specs_list = [node.token["head"], node.token["upos"],node.token["deprel"]]
        specs_list1 = [node.token["id"], node.token["upos"],node.token["head"]]

        specs_list2 = [node.token["id"], node.token["upos"],node.token["deprel"]]
        dict_id.update({node.token["id"]:specs_list})
        dict_head[node.token["head"]].append(specs_list2)
        dict_rel[node.token["deprel"]].append(specs_list1)
        to_traverse.extend(node.children) 
    sorted_dict_head = dict(sorted(dict_head.items()))
    sorted_dict_rel = dict(sorted(dict_rel.items()))
    sorted_dict_id = dict(sorted(dict_id.items()))
    

    return sorted_dict_id,sorted_dict_head, sorted_dict_rel




def search(tree: TokenTree, deprel : list, deppos: list, depphead: list):
    """Searches tree for deprel , pos of head and pos of dependent. Returns a list of tuples, storing deprel and index of pos and pos and index of head element"""
    rel = None
    dict_id,dict_head, dict_rel = _get_as_dict(tree)
    deprelquery = deprel
    depposquery = deppos
    headposquery = depphead
    elements = []
    for i in deprelquery:
        # checks for deprel 
        if i in dict_rel:
            # specific dep rel query 
            if depposquery != []:
                rel = dict_rel[i]
                for j in rel:
                    
                    if rel not in elements and j[1] in depposquery:
                        cc = j
                        cc.append(i)
                        elements.append(cc)
            else: 
                rel = dict_rel[i]
                for j in rel:
                    if rel not in elements:
                        cc = j
                        cc.append(i)
                        elements.append(j)            
    # obtained: a list of elements who have the right pos/ deprel
    # next step:check for POS of head
    poss = []
   
    for i in elements:
        
        index_head = i[2]
        head_element = dict_id[index_head]
        
        if headposquery != [] and headposquery!= ['']:
            if head_element[1] in headposquery:
             
                poss.append((index_head,head_element[1]))
            else: 
                poss.append(None)
        if headposquery == []:
            # if no specific pos for head, set POS to X
            poss.append((index_head,'X'))
    # to do next: map lists for query 
    # function to find other deprel 
    # elements left
    dep_indices = [(x[0],x[3]) for x in elements]
    temp =  list(zip(dep_indices, poss))
    left_after_pos =  [x for x in temp if x[1] != None]
    return left_after_pos 


def three_query(search_res1 :list, search_res2 :list):
    """In the event two different relations are queried, checks if the head elements of both dependent match. Returns triple tuple"""
    # combines results of both queries
    combined = search_res2 + search_res1
    dicttest = {}
    for i in combined:
        tempi = int(i[1][0])
        poshead = i[1][1]
        templist = i[0]
        if (tempi,poshead) in dicttest.keys():
            dicttest[(tempi,poshead)].append(templist)
        else:    
            dicttest[(tempi,poshead)] = [templist]
    to_analyze = []
    for i in dicttest.keys():
        if len(dicttest[i]) == 2:
            temp_tuple = (i, dicttest[i][0],dicttest[i][1])
            to_analyze.append(temp_tuple)
    # returns three query 
    return to_analyze


def make_query(tree:TokenTree,deprel,posdep,poshead,seconddeprel,seconddeppos ):
    """Query fonction combining seach and three_query. Returns list of tuples"""
    deprel1 = deprel
    posdep = posdep
    poshead = poshead
    deprel2 = seconddeprel
    posdep2 = seconddeppos
    query1 = search(tree,deprel1, posdep, poshead)
   
    if not (deprel2 == [] and posdep2 == [] and posdep2 == []):
        query2 = search(tree, deprel2, posdep2, poshead)
      
        tuple_results = three_query(query1,query2)
    else:
        tuple_results = query1
    
    return tuple_results


def get_order(list_of_tuples,labels_dict:dict):
    """Looks for labels of element in the tuple results of the queries, returns list of the patterns found."""
    patterns = []

    for i in list_of_tuples:
        dicts = dict(i)

        tempdict = sorted(dicts)
        pattern = ""
        for i in tempdict:
            for p in labels_dict:
               
                    if dicts[i] in p:
                        label = labels_dict[p]
                        print(label)
                   
                        pattern += label  
                
                

        patterns.append(pattern)
  
    return patterns



# STRUCTURE FOR QUERY FILE:
# queryname: query/label (if any)
query = UD_Query("C:\\Users\\Ilinca V\\Documents\\saamiexample.conllu","C:\\Users\\Ilinca V\\Documents\\query.txt")
print(query.filename)
test_tree = query.conllu_file[0]
query_dict= query.query_file
labels_dict = query.labels
#récupérer les fichiers conllu
# loop qui crée le query object pour chanque fichier conllu



def count_patterns(list_of_patterns):
    """Counts how many different patterns are found in one tree and returns a dictionnary with the patterns and their occurences."""
    flat_list = []
    if any(isinstance(i, list) for i in list_of_patterns):
        flat_list = [item for sublist in list_of_patterns for item in sublist]
    else:
        flat_list = list_of_patterns
    pattern_occurence = Counter(flat_list)
    return pattern_occurence

def get_patterns_for_one_file(query:UD_Query):
    """Applies function above to the whole .conllu file. Returns dictionnary containing the results."""
    stock_patterns = []
    for i in query.conllu_file:
        query_results = make_query(i,**query_dict)
        stock_patterns.append(get_order(query_results,query.labels))
    
    count = count_patterns(stock_patterns)
    count = dict(count)
    # returns dict w/patterns and values
    return count
    

 
def make_df(objlist :list):
    """Applies function above to the whole .conllu file for a list of objects and creates dataframe to store the results."""
    dataf = pd.DataFrame()
    # A faire: récupérer les patterns pour mettre dans dataframe
    dict_res = {}
    for i in objlist:
    # récupérer les noms pour dataframe
        res = get_patterns_for_one_file(i)
        dict_res[i.filename] = res
    dataf.index = dict_res.keys()
    for i in dict_res.keys():
        results =dict_res[i]
        for j in results.keys():
            if j in dataf.columns:
                dataf.loc[i,j] =+ results[j] 
            else:
                dataf.loc[i,j] = results[j] 
    return dataf

if __name__ == "__main__":


    ud_directory ="...\\Uralic_UD\\"
    text_files = [f for f in os.listdir(ud_directory) if f.endswith('.conllu')]
    languages = []

    query_direc = "...\\Documents\\query.txt"
    for i in text_files:
        obj1 = UD_Query(str(ud_directory+i),query_direc)
        languages.append(obj1)
        print(obj1.query_file)
        print(obj1.labels)

    df = make_df(languages)
    df.to_csv("NADPOS_ALL.csv")
    
 
