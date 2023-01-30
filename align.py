#!/bin/usr/env python
import re
from collections import defaultdict
import sys
from frTreat import *
from deep_translator import GoogleTranslator

if (not (len(sys.argv) >= 4)):
    raise Exception("\033[91mLa ligne de commande doit être de la forme : \npython3 align.py source target text\033[0m")
else :
    src = sys.argv[1]
    trg = sys.argv[2]

# --------------- EXTRAIT DU DEBUT DU TP --------------- #
def getSrcTrg (file):
    prevsrctrg = 'trg'
    sentssrc = []
    sentstrg = []
    try:
        file = open (file)
    except OSError as err:
        print ("\033[91mErreur lors de l'ouverture du fichier\033[0m")
    for line in file:
            line = line.strip()
            m = re.search('\\((src|trg)\\)="([0-9]*)">(.*)', line)
            if(m):
                    srctrg = m.group(1)
                    id = m.group(2)
                    toks = m.group(3)
                    if srctrg == 'src':
                            if prevsrctrg == 'src':
                                    sentssrc[-1] += toks
                            else:
                                    sentssrc.append(toks)
                    if srctrg == 'trg':
                            if prevsrctrg == 'trg':
                                    sentstrg[-1] += toks
                            else:
                                    sentstrg.append(toks)
                    prevsrctrg = srctrg
    return (cleanPonc(sentssrc), cleanPonc(sentstrg))

# -------- ON NETTOIE LA PONCTUATION DES TEXTES -------- #

def cleanPonc (sentTab):
    for i in range (len(sentTab)) :
            sentTab[i] = re.sub(r'[^\w\s\']','',sentTab[i])
    return sentTab


# ----- ON CHERCHE A FAIRE UN TABLEAU DE FREQUENCE ----- #

def freqTab (sentssrc, sentstrg):
    freqsrctrg = defaultdict(lambda: defaultdict(int))

    for i in range (min(len(sentssrc),len(sentstrg))):
        sentsrc = sentssrc[i].split()
        senttrg = sentstrg[i].split()
        length = min(len(sentsrc),len(senttrg))
        for j in range (length):
            numsrc = 0
            numtrg = 0
            if (j<length-2 and sentsrc[j].isdigit() and sentsrc[j+1].isdigit()):
                sentsrc[j+1]=sentsrc[j]+sentsrc[j+1]
                numsrc = 1
            if (j<length-2 and senttrg[j].isdigit() and senttrg[j+1].isdigit()):
                senttrg[j+1]=senttrg[j]+senttrg[j+1]
                numtrg = 1
            freqsrctrg[sentsrc[j+numsrc]][senttrg[j+numtrg]] += 1
    return freqsrctrg

# --------------- ON NETTOIE LES DOUBLONS -------------- #

def cleanFreq (freqsrctrg, limit):
    ret = defaultdict(lambda: defaultdict(int))
    for motsrc in freqsrctrg :
        if (motsrc not in ret):
            max = (0, "")
            for mottrg in freqsrctrg[motsrc] :
                if (freqsrctrg[motsrc][mottrg] > max[0]):
                    max = (freqsrctrg[motsrc][mottrg], mottrg)
            if (max[0]>limit):
                ret[motsrc][max[1]]=max[0]
    return ret
        
# ----------------- NOTE DU DICO RENDU ---------------- #

def note (dico, src, trg):
    ret = 0.
    print("_" * 44)
    print("|"+" " * 17 + "|"+" " * 17 + "|" + " "*6 + "|")
    print("| mot source      | mot cible       | freq |")
    print("|"+"_" * 17 + "|"+"_" * 17 + "|" + "_"*6 + "|")
    for msrc in dico :
        for mtrg in dico[msrc] :
            motsrc = msrc.replace("_", " ")
            mottrg = mtrg.replace("_", " ")
            if(not motsrc.isdigit() and not mottrg.isdigit()):
                tradsrc = GoogleTranslator(source=src, target=trg).translate(motsrc).lower()
                tradtrg = GoogleTranslator(source=trg, target=src).translate(mottrg).lower()
            
            if (motsrc.isdigit()
                or mottrg.isdigit()
                or tradsrc == mottrg
                or tradtrg == motsrc
                or motsrc == mottrg):
                color = "\033[92m"
                ret += 1
            else :
                color = "\033[91m"
            reset = "\033[0m"
            freq = str(dico[msrc][mtrg])
            
            print ("| "+color+motsrc+reset
                       + " " * (15-len(motsrc))
                       + " | "+color+mottrg+reset
                   + " " * (15-len(mottrg))
                   + " | " + freq
                   + " " * (4-len(freq))
                   + " | ", end="")
            if (color == "\033[91m") :
                print (tradsrc + " " * (15-len(tradsrc)) + "|" )
            else:
                print(" " * 15 + "|")
    try :
        ret = str(round(ret*100/len(dico)))+"%"
    except ZeroDivisionError as err:
        print ("\033[91mOupsie le dictionnaire est vide.\033[0m")
    
    print("|"+" " * 17 + "|"+" " * 17 + "|" + " "*6 + "|")
    print ("Pourcentage de \"réussite\" d'après google traduction : "
           +ret+"\n")
    return ret

# ---------------------- AFFICHE --------------------- #

def affiche (freqsrctrg) :
    for motsrc in freqsrctrg :
        for mottrg in freqsrctrg[motsrc] :
            print (freqsrctrg[motsrc][mottrg], motsrc, mottrg)

# --------------- GENERE DICTIONNAIRE ---------------- #
def cleanDic(text):
    (sentssrc, sentstrg) = getSrcTrg (text)
    sentssrc = list(map(lambda s: s.lower(), sentssrc))
    sentstrg = list(map(lambda s: s.lower(), sentstrg))
    if (src == "fr"):
        sentssrc = cleanAp(sentssrc)
    else :
        sentstrg = cleanAp(sentstrg)
    if (src=="es"):
        sentstrg = cleanPron(sentstrg)
    elif (trg=="es"):
        sentssrc = cleanPron(sentssrc)
    return (sentssrc,sentstrg)

def genereDico (text):
    (sentssrc, sentstrg) = cleanDic(text)
    dico = freqTab (sentssrc, sentstrg)
    return dico

# --------------- FUSION DICTIONNAIRES --------------- #

def fusion (dico1, dico2):
    for motsrc in dico2 :
        if motsrc not in dico1:
                dico1[motsrc] = dico2[motsrc]
        else :
            for mottrg in dico2[motsrc]:
                if mottrg in dico2[motsrc]:
                    dico1[motsrc][mottrg] += dico2[motsrc][mottrg]
                else:
                    dico1[motsrc][mottrg] = dico2[motsrc][mottrg]
    return dico1

# --------------------- DISTANCE --------------------- #

def mini(tab):
    minimum = (0, 0)
    for i in range (len(tab)):
        for j in range (len(tab[i])):
            if (tab[i][j] < tab[minimum[0]][minimum[1]]):
                minimum = (i, j)
    return minimum

def levenshtein (mot1, mot2) :
    cout = 0
    D = []
    for i in range(len(mot1)+1):
        D.append([0]*(len(mot2)+1))
        D[i][0] = i
    for j in range(len(mot2)+1):
        D[0][j] = j
        
    for i in range (1, len(mot1)+1) :
        for j in range (1, len(mot2)+1):
            if mot1[i-1] == mot2[j-1] : cout = 0
            else: cout = 1
            D[i][j] = min(D[i-1][j]+1,
                          D[i][j-1]+1,
                          D[i-1][j-1]+cout)
    return D[len(mot1)][len(mot2)]

def dicoLev (text):
    dico = defaultdict(lambda: defaultdict(int))
    (sentssrc, sentstrg) = cleanDic(text)
    for l in range (min(len(sentssrc),len(sentstrg))):
        sentsrc = sentssrc[l].split()
        senttrg = sentstrg[l].split()
        dist = [0] * len(sentsrc)
        for i in range (len(sentsrc)):
            dist[i] = [0] * len(senttrg)
            for j in range (0, len(senttrg)):
                dist[i][j] = levenshtein (sentsrc[i], senttrg[j])
        (i, j) = mini(dist)
        for e in dist:
            print(e)
        while (dist[i][j] != 100):
            dico [sentsrc[i]][senttrg[j]] += 1
            dist[i] = list(map(lambda x: 100, dist[i]))
            for k in range (len(sentsrc)):
                dist[k][j] = 100
            (i, j) = mini(dist)
            for e in dist:
                print(e)
    return dico

# -------------------- SIMILITUDE -------------------- #

def maxi(tab):
    maximum = (0, 0)
    for i in range (len(tab)):
        for j in range (len(tab[i])):
            if (tab[i][j] > tab[maximum[0]][maximum[1]]):
                maximum = (i, j)
    return maximum

def simSousChaine (sub1, sub2):
    i = 0; j = 0
    sim = 0
    len1 = len (sub1)
    len2 = len (sub2)
    while ( i < len(sub1)
            and j < len(sub2)):
        if (sub1[i] == sub2[j]) :
            sim += 1; i += 1; j += 1
        else :
            if (len1 > len2) : i += 1
            elif (len2 > len1) : j += 1
            else : i += 1; j += 1      
    return round(sim/((len(sub1)+len(sub2))/2),2)

def similitude (mot1, mot2):
    sim = 0
    if (len(mot1) < 3
        or len(mot2) < 3):
        return simSousChaine(mot1, mot2)
    for i in range (len(mot1)-3):
            sub = mot1[i:i+3]
            sim += simSousChaine (sub, mot2)
    for i in range (len(mot2)):
            sub = mot1[i:i+3]
            sim += simSousChaine (sub, mot2)
    ret = (round(sim,2))/((len(mot1)+len(mot2))/2)
    return round(ret,2)
        
def dicoSim (text):
    dico = defaultdict(lambda: defaultdict(int))
    (sentssrc, sentstrg) = cleanDic(text)
    for l in range (min(len(sentssrc),len(sentstrg))):
        sentsrc = sentssrc[l].split()
        senttrg = sentstrg[l].split()
        sim = [0] * len(sentsrc)
        for i in range (len(sentsrc)):
            sim[i] = [0] * len(senttrg)
            for j in range (0, len(senttrg)):
                sim[i][j] = similitude (sentsrc[i], senttrg[j])
        (i, j) = maxi(sim)
        while (sim[i][j] != 0):
            dico [sentsrc[i]][senttrg[j]] += 1
            sim[i] = list(map(lambda x: 0, sim[i]))
            for k in range (len(sentsrc)):
                sim[k][j] = 0
            (i, j) = maxi(sim)
    return dico


if __name__ == '__main__' :
    print("DICTIONNAIRE ALIGNEMENT :")
    dico = genereDico(sys.argv[3])
    for i in range (4, len(sys.argv)):
        dico = fusion (dico, genereDico(sys.argv[i]))
    dico = cleanFreq(dico, 1)
    note(dico,src,trg)

    print("DICTIONNAIRE DISTANCE LEVENSHTEIN :")
    dico = dicoLev(sys.argv[3])
    for i in range (4, len(sys.argv)):
        dico = fusion (dico, dicoLev(sys.argv[i]))
    dico = cleanFreq(dico, 1)
    note(dico,src,trg)
    
    print("DICTIONNAIRE SIMILITUDE :")
    dico = dicoSim(sys.argv[3])
    for i in range (4, len(sys.argv)):
        dico = fusion (dico, dicoSim(sys.argv[i]))
    dico = cleanFreq(dico, 1)
    note(dico,src,trg)
