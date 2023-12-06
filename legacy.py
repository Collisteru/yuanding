# Legacy code no longer used in the project

def display_harmony_chains(self):
    harmony_chains = []
    for i in self.placed:
        for j in i.harmonized:
            newPair = (i,j)
            if not (j,i) in harmony_chains:
                harmony_chains.append(newPair)
    
    for i in harmony_chains:
        pieceOne = i[0]
        pieceTwo = i[1]
        print(f'{pieceOne.owner} ( {pieceOne.x},{pieceOne.y} ) -- {pieceTwo.owner} ( {pieceTwo.x},{pieceTwo.y} ) \n')