import nltk
nltk.download('punkt')
from nltk import word_tokenize
from nltk import pos_tag
from nltk import RegexpParser
from nltk import ne_chunk
import sys


#FONCTION RECUPERATION DES ELEMENTS DANS LES TREE
def recupere_les_elements_dans_les_tree(liste_de_trees) :
    resultat_recuperation = []
    for i in range(0, len(liste_de_trees)) :
        elt = str(liste_de_trees[i].label()) + "\t"
        for j in range (0 , len(liste_de_trees[i])) :
            elt = elt + " " + str(liste_de_trees[i][j][0])
        resultat_recuperation.append(elt+"\n")
    return resultat_recuperation


#FONCTION QUI CONVERTIT LES NER NLTK EN NER STANDARD
def transformer_les_ner_nltk_en_nltk_standard(liste_ner_nltk , dict_ner_standard) :
    for i in range(0,len(liste_ner_nltk)) :
        if str(type(liste_ner_nltk[i])) == "<class 'nltk.tree.tree.Tree'>" :
            if str(liste_ner_nltk[i].label()) in dict_ner_standard.keys() :
                liste_ner_nltk[i].set_label(dict_ner_standard[str(liste_ner_nltk[i].label())])
    return liste_ner_nltk

                            #                   #
                            #   CODE PRINCIPAL  #
                            #                   #
print(len(sys.argv))
##DESAMBIGUATION MORPHO SYNTAXIQUE DU FICHIER SAMPLE
for i in range (1 , len(sys.argv)) :
    print(" OUVERTURE DU FICHIER CONTENANT LE TEXTE")
    chemin_fichier_sample = sys.argv[i]
    fichier_sample = open(chemin_fichier_sample, "r")
    print(" LECTURE DU FICHIER CONTENANT LE TEXTE")
    contenu_sample = fichier_sample.read()
    #print(contenu_sample)


    print("\n \n")
    #contenu_sample = contenu_sample.split()
    print(" TOKENIZATION DU TEXTE EN COURS")
    tokens_tag = pos_tag(word_tokenize(contenu_sample))
    tag = tokens_tag
    #print(tokens_tag)
    tokens_tag = list(tokens_tag)

    ##SEPARATION DES TOKENS ET SEPARATION
    result = lambda x : str(x[0]) + "\t" + str(x[1]) + " " + "\n"


    liste_contenu_tokens_tag = [ result(x) for x in tokens_tag ]
    #ON SUPPRIME LE CARACTERE "\n" DANS LE DERNIER ELEMENT
    liste_contenu_tokens_tag[-1] = liste_contenu_tokens_tag[-1][:-1]


    ## CONVERSION DES ETIQUETTES NLTK VERS LES ETIQUETTES STANDARD
    #fichier_des_etiquettes_standard = open("POSTags_PTB_Universal_Linux.txt","r")
    #contenu_fichier_des_etiquettes_standard = fichier_des_etiquettes_standard.read()


    ## ECRITURE DANS LE FICHIER
    new_chemin_de_fichier = chemin_fichier_sample.replace("data","data_obtained")
    fichier_desambigu = open(new_chemin_de_fichier+".pos.nltk","w")
    fichier_desambigu.write("".join(liste_contenu_tokens_tag))
    fichier_desambigu.close()


                                    #                               #
                                    #   PARTIE ANALYSE SYNTAXIQUE   #
                                    #                               #

    
    ### ANALYSE SYNTAXIQUE DES PHRASES DU FICHIER SAMPLE
    print(" ANALYSE SYNTAXIQUE DES PHRASES DU FICHIER SAMPLE")
    grammar = "Compound:  {<DT>?<JJ>*<NN>}"
    cp  = RegexpParser(grammar)
    resultat = cp.parse(tag)

    liste_des_compound_name = [x for x in list(resultat) if str(type(x)) == "<class 'nltk.tree.tree.Tree'>"]
    liste_des_compound_name = [str(x)+"\n" for x in liste_des_compound_name]

    print(" ECRITURE DANS LE FICHIER CHUNK")
    fichier_chunk = open(new_chemin_de_fichier+".chk.nltk", "w")
    fichier_chunk.write("".join(liste_des_compound_name))
    fichier_chunk.close()



    #GENERALISATION A LA RECONNAISSANCE DES STRUCTURE SYNTAXIQUE
    fichier_chunk = open(new_chemin_de_fichier+".chk.nltk", "a")
    fichier_structures_syntaxiques = open("data/wsj.structures.syntaxiques" , "r")

    liste_des_structures = []
    for structure_syntaxique in fichier_structures_syntaxiques.readlines() :
        if (structure_syntaxique[-1] == "\n") :
            liste_des_structures.append(structure_syntaxique[:-1])
        else :
            liste_des_structures.append(structure_syntaxique)

    liste_des_resultats = []
    for regle in liste_des_structures :
        print(regle)
        cp  = RegexpParser(regle)
        resultat = cp.parse(tag)
        resultat = [x for x in list(resultat) if str(type(x)) == "<class 'nltk.tree.tree.Tree'>"]
        resultat = "".join([str(x)+"\n" for x in resultat])
        print(resultat)
        print("\n \n")
        liste_des_resultats.append(resultat)


    for i in range(0, len(liste_des_resultats)) :
        if i == 0 :
            fichier_chunk.write ("\n \n ADJECTIF-NOM \n")
        elif i==1 :
            fichier_chunk.write ("\n \n Nom-Nom \n")
        elif i==2 :
            fichier_chunk.write ("\n \n ADJECTIF-Nom-Nom \n")
        elif i==3 :
            fichier_chunk.write ("\n \n ADJECTIF-ADJECTIF-Nom \n")
        
        fichier_chunk.write(liste_des_resultats[i])


    fichier_chunk.close()
    fichier_structures_syntaxiques.close()






                                    #                               #
                                    #   PARTIE ENTITES NOMMEES      #
                                    #                               #
    
    fichier_ner = open(new_chemin_de_fichier+".ne.nltk", "w")
    print("\n \n \n")
    print(" DETECTION DES ENTITES NOMMEES ")
    liste_ner = ne_chunk(tag , binary=False)
    liste_ner = [x for x in list(liste_ner) if str(type(x)) == "<class 'nltk.tree.tree.Tree'>"]


    #RECUPERATION DES MOTS DES NER
    result_liste_ner = recupere_les_elements_dans_les_tree(liste_ner)

    #ECRITURE DANS LE FICHIER DES NER
    fichier_ner.write("".join(result_liste_ner))

    #LECTURE DU FICHIER DU NER STANDARD
    fichier_ner_standard = open("data/convertisseur.ner","r")
    dict_ner_standard = {}
    for line in fichier_ner_standard.readlines() :
        j = line[:-1].split()
        dict_ner_standard[j[0]] = j[1]


    ### CONVERSION DES NER EN NER STANDARD
    liste_ner = transformer_les_ner_nltk_en_nltk_standard(liste_ner , dict_ner_standard)

    #ON RECUPERE LES NOUVELLES NER AVEC LEUR TEXTE
    result_liste_ner = recupere_les_elements_dans_les_tree(liste_ner)

    #ECRITURE DANS LE FICHIER
    fichier_ner_ecriture = open(new_chemin_de_fichier+"ne.nltk","w")
    fichier_ner_ecriture.write("".join(result_liste_ner))
    fichier_ner_ecriture.close()

    #TRANSFORMATION EN BIO
    liste_ner = ne_chunk(tag , binary=False)
    liste_ner = transformer_les_ner_nltk_en_nltk_standard(liste_ner , dict_ner_standard)
    annotation_bio = []
    for el in liste_ner :
        annot = "ki"
        if (str(type(el)) == "<class 'nltk.tree.tree.Tree'>") :
            annot = el.label()
            for i in range(len(el)) :
                if i == 0 :
                    annotation_bio.append(str(el[i][0]) + "  B-"+annot+"\n")
                else :
                    annotation_bio.append(str(el[i][0]) + " I-"+annot+"\n") 
        else :
            annotation_bio.append(str(el[0]) + "    O\n")

    fichier_annotation_bio = open(new_chemin_de_fichier+".etiquettes_en_bio.txt","w")
    fichier_annotation_bio.write("".join(annotation_bio))
    fichier_annotation_bio.close()

    #FERMETURE DU FICHIER NER
    fichier_ner.close()


    #FERMETURE DU FICHIER SAMPLE
    fichier_sample.close()
