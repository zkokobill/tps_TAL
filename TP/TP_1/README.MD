		
							ORGANISATION DES FICHIERS

Le fichier tp1.Py : contient le script permettant de traiter les fichiers
LE FICHIER convertion.py : contient le scripts qui permettra de convertir(dans la partie analyse morphosyntaxique) en annotation standard.
Le dossier Data : contient les fichiers sur lesquels sont appliqués les scripts. Les fichiers texte bruts
Le dossier Data Obtained : contient les fichiers obtenus après exécution des scripts (laissé vide pour le test et doit être présent sinon erreur)
Le dossier fichier_Ref : Contient les annotations standard différents des annotations nltk
Le fichier Data\wsj.structures.syntaxiques : fichier déclaratif contenant ces structures syntaxiques.Il est appelé dans la partie 2 du TP
Le fichier Data\convertisseur.ner : Contient les équivalents des étiquettes nltk en étiquette standard

Le dossier data_obtained_draft est la version que nous avons obtenus en simulant de nous même




									COMMENT EXECUTER ?

Le code est conçu de façon à être exécuter sur plusieurs fichiers et il fait directement l'analyse syntaxique, morpho-syntaxique et extraction
d'entitées nommées.

Pour le fichier wsj_0010_sample.txt par exemple : il suffit d'entrer PYTHON data\wsj_0010_sample.txt 
Pour exécuter à la fois le fichier sample et le fichier formal-tst.NE.key.04oct95_sample.txt il faudra donc faire :
PYTHON data\wsj_0010_sample.txt data\formal-tst.NE.key.04oct95_sample.txt
Tous les résultats sont stockés dans le dossier data_obtained.





				'1. EVALUATION DE L’ANALYSE MORPHO-SYNTAXIQUE DE LA PLATEFORME NLTK'

Pour convertir en annotation standard : faire python convertion.py data_obtained\wsj_0010_sample.txt.pos.nltk  fichier_ner\wsj_0010_sample.txt.pos.ref
et pareil pour autres fichiers
Pour évaluer : python evaluate.py data_obtained\wsj_0010_sample.txt.pos.univ.nltk   fichier_ref\wsj_0010_sample.txt.pos.univ.ref

Dans la première évaluation on a un pourcentage de ressemblance égal à 93,66% alors qu'après conversion en annotation
plus générale on a une augmentation du pourcentage qui passe à 95,41 %. Ceci est dû au fait que les annotations 
standard sont plus générales ce qui pousse à la ressemblance plus poussée des deux annotations.




					2. ANALYSE SYNTAXIQUE
On obtiendra ici en sortie par exemple wsj_0010_sample.txt.chk.nltk





					3 . EXTRACTION DES ENTITÉS NOMMÉES'
On a trois sortie pour le fichier wsj_0010_sample par exemple:
wsj_0010_sample.txt.ne.nltk : pour les entités nommées du fichier en annotation NLTK
wsj_0010_sample.txtne.nltk (ici, pas de "." entre "t" et "ne") : pour les entités nommées NLTK transformées au format standard
wsj_0010_sample.txt.etiquettes_en_bio.txt : pour la transformation du texte en fichier B-I-O


On devrait donc avoir pour chaque fichier sample(texte d'entrée) : après avoir exécuté tp1.py et convertion.py 6 fichiers dans le dossier data_obtained
