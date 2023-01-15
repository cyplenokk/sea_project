count = 0
slov = {}
spisok = []
count = 1
count2 = 0
spisok2 = []
def TumbaWords(A, w, L):
    global count
    if len(w) == L:
        if 'ЫЫ' or 'ШШ' or 'ЧЧ' or 'ОО' in w:
            print(w)
            count += 1
        return
    for c in A:
        TumbaWords(A, w + c, L)
TumbaWords('ЫШЧО', '', 3)
print(count)



