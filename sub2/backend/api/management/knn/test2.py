
def test() :
    data = [ { "삼성": 1, "갤럭시": 3, "노트": 5 },
    { "갤럭시": 3, "노트": 5 , "폭발": 3},
    { "LG": 1, "G4": 1, "스마트폰": 1 }]

    itemBase = {}
    featureBase = {}

    for idx in range(len(data)):
        item = data[idx]
        if itemBase[int(idx)] is None :
            itemBase[idx] = {}

        print(item)

        for i in range(len(item)) :
            if featureBase[int(item[i])] is None :
                featureBase[item[i]] = []
            itemBase[idx][item[i]] = item[item[i]] * 1
            featureBase[item[i]].push(idx)
    
    for a in itemBase :
        print(a)

    for b in featureBase :
        print(b)   
test()