def cleanAp (sentTab):
    ret = []
    for line in sentTab:
        line = line.replace ("' ","'")
        ret += [line]
    return ret

def cleanPron (sent):
    pron = ["je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"]
    ret = []
    for line in sent:
        for p in pron:
            line = line.replace(" "+p+" ", " "+p+"_")
            line = line.replace("\n"+p+" ", "\n"+p+"_")
            line = line.replace(" "+p+"\n", " "+p+"_")
        ret += [line]
    return ret
