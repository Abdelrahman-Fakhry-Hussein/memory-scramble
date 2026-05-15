import random

from config import generate_emojis

def generate_board( rows,   cols ):
    num_pairs =(rows * cols) //     2

    # keep trying until clean board
    for attempt in   range( 10 ):
        all_emojis= generate_emojis( num_pairs)

        chosen =all_emojis[  : num_pairs]

        # make sure all unique
        if len(set(chosen)) !=   num_pairs:
            continue

        cards= chosen *2

        # verify each appears exactly twice
        ok =True

        for c in set(   cards ):
            if cards.count(c) !=2:
                ok= False
                break

        if not ok:
            continue

        random.shuffle( cards )

        # build 2d grid
        board=[]
        idx =0


        for i in range( rows ):

            row=[]


            for j in range(     cols):
                row.append( cards[idx] )

                idx +=1


            board.append(row)

        return board

    # fallback
    all_emojis =list(set( generate_emojis(num_pairs *2) ))[:num_pairs]


    cards =all_emojis*2

    random.shuffle(cards)
    board =[]
    
    
    idx=0
    for i in range(rows  ):

        row =[]
        for j in range( cols ):

            
            row.append(cards[idx])
            idx+=1
        board.append( row )
    return board
