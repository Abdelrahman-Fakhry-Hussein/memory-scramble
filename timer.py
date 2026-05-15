import time

class Timer:
    def __init__( self,timeout_seconds ):

        self.timeout  = timeout_seconds

        self.start_time =None
        self.running=   False

    def start(self ):
        self.start_time= time.time()

        self.running =      True

    def get_remaining( self):
        if not self.running:


            return self.timeout

        elapsed =time.time() - self.start_time

        remaining= self.timeout -elapsed

        if remaining <=0:
            self.running =      False
            return 0
        return int( remaining )

    def is_expired(self ):

        if self.start_time is None:
            return False
        


        elapsed =time.time() - self.start_time

        return elapsed>= self.timeout

    def stop( self):
        self.running= False
