class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class Printer:

    failed_count = 0
    passed_count = 0
    
    def step(self, message):
        """
        Print out a descriptive message explaining what we're doing
        """
        print ("{0}* {1}{2}" . format (bcolors.OKBLUE, message, bcolors.ENDC))

    def todo(self, message): 
        print ("{0}* **TODO:** {1}{2}" . format (bcolors.FAIL, message, bcolors.ENDC))

    def info(self, message):
        print ("{0}* **INFO:** {1}{2}" . format (bcolors.OKBLUE, message, bcolors.ENDC))     

    def record_pass(self, message):

        self.passed_count = self.passed_count+1
        self.print_pass(message)
        

    def record_fail(self, message):

        self.failed_count = self.failed_count+1
        self.print_fail(message)

    def scenario(self, message):
        print (" ")
        print ("{0}##{1}{2}\n" . format (bcolors.OKGREEN, message, bcolors.ENDC))
        
    def print_pass(self, message):         
        print ("{0}* {1}{2}" . format (bcolors.OKGREEN, message, bcolors.ENDC))

    def print_fail(self, message): 
        print ("{0}* {1}{2}" . format (bcolors.FAIL, message, bcolors.ENDC))
        

    def print_summary(self):

        assertion_count = float(self.failed_count + self.passed_count)
        if assertion_count > 0:
            pass_percentage = float(self.passed_count) / assertion_count * 100
        else:
            pass_percentage = "n/a"
        print ("\n-")
        print ("* **Failed:** {0}" . format (self.failed_count))
        print ("* **Passed:** {0}" . format (self.passed_count))
        print ("* **Pass Rate:** {0} %" . format ( pass_percentage ))
        print ("\n-")

    
