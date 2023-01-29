### CONVERSION DES ANNOTATIONS NLTK EN ANNOTATION STANDARD
import sys

result = lambda x : (str(x[0]) + "\t" + str(x[1]) + " " + "\n" , " " + "\n")[x[0]=="juju"]

def transformation_contenu_du_fichier_en_dictionnaire(contenu_fichier) :
    ## RECUPERATION DU CONTENU EN CLASSANT DANS UN DICTIONNAIRE
    contenu_fichier =  list(contenu_fichier.split("\n"))
    contenu_fichier =  [tuple(x.split()) for x in contenu_fichier]
    return dict(contenu_fichier)

def du_dictionnaire_au_contenu_de_fichier (dictionnaire) :
    return [ result(x) for x in dictionnaire ]


##ON OUVRE LE FICHIER DES ANNOTATIONS STANDARD
fichier_annotation_standard = open("POSTags_PTB_Universal_Linux.txt" , "r")
contenu_fichier_annotation_standard = fichier_annotation_standard.read()
dict_contenu_fichier_annotation_standard = transformation_contenu_du_fichier_en_dictionnaire(contenu_fichier_annotation_standard)


## POUR CHACUN DES FICHIERS
for i in range (1 , len(sys.argv)) :
    chemin_du_fichier = sys.argv[i]
    print(chemin_du_fichier)

    ## ON OUVRE LE FICHIER DES ANNOTATIONS OBTENUES AVEC NLTK
    fichier_des_annotations_nltk = open(chemin_du_fichier,"r")
    contenu_fichier_annotation_nltk = fichier_des_annotations_nltk.readlines()
    liste_contenu_nltk = []

    #LE FICHIER DE REFERENCE A UN TRAITEMENT DIFFERENT
    if "pos.ref" in chemin_du_fichier :
        fichier_ref = True
        i = 0
        for line in contenu_fichier_annotation_nltk :
            liste_contenu_nltk.append(line[:-1])
            #SUPPRESSION DE L'ESPACE APRES LE MOT
            while (liste_contenu_nltk[i][-1] == " " and liste_contenu_nltk[i] != " ") :
                liste_contenu_nltk[i] = liste_contenu_nltk[i][:-1]
            i = i + 1

        #ON ENLEVE LA TABULATION ET ON TRANSFORME EN DICTIONNAIRE
        for i in range(0 , len(liste_contenu_nltk) - 1) :
            if liste_contenu_nltk[i] == " " :
                liste_contenu_nltk[i] = "juju\tjiji"""

    else :
        fichier_ref = False
    #ON RECUPERE LIGNE PAR LIGNE
        for line in contenu_fichier_annotation_nltk :
            liste_contenu_nltk.append(line[:-2])

    
    liste_contenu_nltk = [x.split("\t") for x in liste_contenu_nltk]

    contenu_fichier_nltk_key_mot = [x[0] for x in liste_contenu_nltk]
    contenu_fichier_nltk_valeur_annot  = [x[1] for x in liste_contenu_nltk]
    
    #CHAQUE ELEMENT DANS ITEMS, ON LE REMPLACE PAR SA VRAIE VALEUR
    for i in range (0, len(contenu_fichier_nltk_valeur_annot) - 1) :
        if contenu_fichier_nltk_valeur_annot[i] in dict_contenu_fichier_annotation_standard.keys() :
            contenu_fichier_nltk_valeur_annot[i] = dict_contenu_fichier_annotation_standard[contenu_fichier_nltk_valeur_annot[i]]
    
    #ON RANGE LE TOUT DANS UNE LISTE
    liste_contenu_nltk = []
    for i in range (0, len(contenu_fichier_nltk_key_mot) - 1) :
        liste_contenu_nltk.append((contenu_fichier_nltk_key_mot[i] , contenu_fichier_nltk_valeur_annot[i]))

    #ON ECRIT LE NOUVEAU FICHIER
    if fichier_ref == True :
        fichier_des_annotations_nltk_new = open("fichier_ref/wsj_0010_sample.txt.pos.univ.ref","w")
    else :
        fichier_des_annotations_nltk_new = open(chemin_du_fichier.replace("pos","pos.univ"),"w")
    
    fichier_des_annotations_nltk_new.write("".join(du_dictionnaire_au_contenu_de_fichier(liste_contenu_nltk)))


    fichier_des_annotations_nltk.close()
    fichier_des_annotations_nltk_new.close()

fichier_annotation_standard.close()