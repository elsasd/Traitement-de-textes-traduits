### align.py :  

   - **getSrcTrg (file)** :  
      file : chaîne de caractères correspondans à un fichier dans tests.  
      Valeur retour : couple (sentssrc, sentstrg), où sentssrc et sentstrg deux tableaux de string, de la langue src et trg.  
      On récupère dans le fichier les mots source, que l'on aligne avec les motss target.  
        
   - **cleanPonc (sentTab)** :  
     sentTab : tableau de string.  
     valeur retour : tableau string.  
     Les strings contenues dans le tableau initiale sont nettoyées de leur ponctuation dans le tableau retour.  
       
   - **freqTab (sentssrc, sentstrg)** :  
     sentssrc : tableau de string de la langue source.  
     sentstrg : tableau de string de la langue target.  
     valeur retour : tableau deux dimensions de int, avec des strings en clef.  
     On stocke dans freqsrctrg[motsrc][mottrg] la fréquence d'alignement de motsrc avec mottrg.  
       
  - **cleanFreq (freqsrctrg, limit)** :  
    freqsrctrg : tableau deux dimensions de int, avec des strings en clef.  
    limit : entier.  
    valeur retour : tableau deux dimensions de int, avec des strings en clef.  
    Un seul mottrg (celui qui a la plus grande fréquence) correspond à un motsrc. Ne sont gardées que les fréquences supérieures à limit.  
      
  - **note (dico)** :  
    dico : tableau deux dimensions de int, avec des strings en clef.  
    valeur retour : entier.  
    correspond on nombre de mots "bien" traduits, selon un traducteur automatique.  
      
  - **main** :  
    On vérifie que le nombre d'arguments soit correct, puis on créee le tableau de fréquence. On gère les nettoyages propre à telle ou telle langue.  
  
  
### frTreat.py:  

  - **cleanAp (sentTab)** :  
    sentTab : tableau deux dimensions de int, avec des strings en clef.  
    valeur retour : tableau deux dimensions de int, avec des strings en clef.  
    On supprime les apostrophes (et les remplaces pas "e "). Par exemple "l'arche" devient "le arche", plus pratique pour l'alignement.  
  
  - **cleanPron (sent)** :  
    sentTab : tableau deux dimensions de int, avec des strings en clef.  
    valeur retour : tableau deux dimensions de int, avec des strings en clef.  
    On supprime les pronoms en début de phrase. Utile lorsque la langue en face est l'espagnol.  