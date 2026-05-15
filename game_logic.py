
class GameState:
    def __init__(self,board, rows,cols):
        self.board= board

        self.rows =rows

        self.cols=cols
        self.matched =[[False]   *   cols for _ in  range(  rows)]

        self.flipped=[]


        self.matches_found= 0
        self.total_pairs =(  rows * cols) //  2
        self.locked =False

    def is_complete( self ):

        return self.matches_found== self.total_pairs

    def flip_card(self, r,c):

        if self.matched[r][c]:
            return False
        

        if (r,c) in self.flipped:

            return False


        if self.locked:
            return False

        self.flipped.append( (r,c) )
        return True

    def check_match( self ):
        if len(self.flipped)!= 2:
            return None

        r1,c1= self.flipped[0]

        r2,c2 =self.flipped[1]

        if self.board[r1][c1]== self.board[r2][c2]:
            self.matched[r1][c1] =True

            self.matched[r2][c2]= True
            self.matches_found +=1
            self.flipped =[]


            return True
        else:
            return False

    def reset_flipped(self ):


        self.flipped= []
