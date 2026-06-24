#!C:\Program Files\Python312\python
import random
import copy
import argparse
from symtable import Symbol
import time
import os
import sys
import matplotlib.pyplot as plt
import statistics

# Constants
COLUMNS = [0] *5
ROWS =  [[0] * 5] *3
LINES = (
    (1,1,1),    (1,1,1,1),  (1,1,1,1,1),
    (1,1,2),    (1,1,2,1),  (1,1,2,1,1),    (1,1,2,3),  (1,1,2,3,3),
    (1,1,3),    (1,1,3,1),  (1,1,3,1,1),
    (1,2,1),    (1,2,1,2),  (1,2,1,2,1),
    (1,2,2),    (1,2,2,2),  (1,2,2,2,1),                (1,2,2,2,3),
    (1,2,3),    (1,2,3,2),  (1,2,3,2,1),
    (1,3,1),    (1,3,1,3),  (1,3,1,3,1),
    (1,3,2),    (1,3,2,3),  (1,3,2,3,1),    (1,3,2,1),  (1,3,2,1,3),
    (1,3,3),    (1,3,3,3),  (1,3,3,3,1), 

    (2,1,1),    (2,1,1,1),  (2,1,1,1,2),
    (2,1,2),    (2,1,2,1),  (2,1,2,1,2),    (2,1,2,3),  (2,1,2,3,2),
    (2,1,3),    (2,1,3,1),  (2,1,3,1,2),
    (2,2,1),    (2,2,1,2),  (2,2,1,2,2),
    (2,2,2),    (2,2,2,2),  (2,2,2,2,2),
    (2,2,3),    (2,2,3,2),  (2,2,3,2,2),
    (2,3,1),    (2,3,1,3),  (2,3,1,3,2),
    (2,3,2),    (2,3,2,3),  (2,3,2,3,2),    (2,3,2,1),  (2,3,2,1,2),
    (2,3,3),    (2,3,3,3),  (2,3,3,3,2), 

    (3,1,1),    (3,1,1,1),  (3,1,1,1,3),
    (3,1,2),    (3,1,2,1),  (3,1,2,1,3),    (3,1,2,3),  (3,1,2,3,1),
    (3,1,3),    (3,1,3,1),  (3,1,3,1,3),
    (3,2,1),    (3,2,1,2),  (3,2,1,2,3),
    (3,2,2),    (3,2,2,2),  (3,2,2,2,3),                (3,2,2,2,1),
    (3,2,3),    (3,2,3,2),  (3,2,3,2,3),
    (3,3,1),    (3,3,1,3),  (3,3,1,3,3),
    (3,3,2),    (3,3,2,3),  (3,3,2,3,3),    (3,3,2,1),  (3,3,2,1,1),
    (3,3,3),    (3,3,3,3),  (3,3,3,3,3),
)
LINES2 = []
for line in LINES:
    line2 = list(line)
    line2[1] += 3
    line2[2] += 6
    if (len(line2)) > 3:
        line2[3] += 9
        if (len(line2)) > 4:
            line2[4] += 12
    LINES2.append(line2)
print(LINES2)

SYMBOLS = {
    " 3 ": {"weight":  1, "lines": [], "value": 0},
    " 4 ": {"weight":  1, "lines": [], "value": 0},
    " 5 ": {"weight":  1, "lines": [], "value": 0},
    " 6 ": {"weight":  1, "lines": [], "value": 0},
    " 7 ": {"weight":  1, "lines": [], "value": 0},
    " 8 ": {"weight":  1, "lines": [], "value": 0},
    " 9 ": {"weight":  1, "lines": [], "value": 0},
    " T ": {"weight":  2, "lines": [], "value": 0}, 
    " J ": {"weight":  3, "lines": [], "value": 0}, 
    " Q ": {"weight":  4, "lines": [], "value": 0}, 
    " K ": {"weight":  6, "lines": [], "value": 0}, 
    " A ": {"weight": 12, "lines": [], "value": 0},
}

WLD = "W"
FS  = "F"
MNY_TYPES = (100, 200, 300, 400, 600, 1200)
SYMBOL_DISTRO = [" W "] + [" 3 "]*12 + [" 4 "]*12 + [" 5 "]*12 + [" 6 "]*12 + [" 7 "]*12 + [" 8 "]*12 + [" 9 "]*12 + \
          [" T "]*2  + [" J "]*3 + [" Q "]*4 + [" K "]*6 + [" A "]*1 + [" F "] + \
          [100]*12 + [200]*6 + [300]*4 + [400]*3 + [600]*2 + [1200]
BUILD_OUT = [
    "testing",
]

# Functions
def my_decorator(func):
    def wrapper(statement):
        choice = random.choice(range(len(BUILD_OUT)))
        line = str(statement).replace("'","") + BUILD_OUT[choice]
        func(line)
    return wrapper

@my_decorator
def my_print(statement):
    print(statement)


######################################## CLASSES  ########################################
class SL(object):
    def __init__(self, num_lines, denom, multi, credit, automate, verbose):
        self.num_lines = num_lines
        self.denom = denom
        self.multi = multi
        self.credit = credit
        self.automate = automate
        self.verbose = verbose
        self.total_rtp = 0
        self.cost = denom * multi
        self.line_cost = denom / num_lines
        
        self.ret = 0
        self.columns = copy.deepcopy(COLUMNS)
        self.rows = copy.deepcopy(ROWS)
        self.session_symbols = None
        self.num_fs = 0
        self.orbs = []
        self.symbols = copy.deepcopy(SYMBOLS)
        self.symbols_w_value = {}

    def reset(self):
        self.ret = 0
        self.columns = copy.deepcopy(COLUMNS)
        self.rows = copy.deepcopy(ROWS)
        self.session_symbols = None
        self.num_fs = 0
        self.num_orbs = []
        self.symbols = copy.deepcopy(SYMBOLS)
        self.symbols_w_value = {}


    def execute(self):

        self.columns = copy.deepcopy(COLUMNS)
        self.rows =  copy.deepcopy(ROWS)
        self.session_symbols = []
        self.symbols = copy.deepcopy(SYMBOLS)

        for ii in range(5):

            self.columns[ii] = random.sample(SYMBOL_DISTRO, 3)

            self.session_symbols += self.columns[ii]

        for jj in range(3):

            self.rows[jj] = [self.columns[0][jj], self.columns[1][jj], self.columns[2][jj], self.columns[3][jj], self.columns[4][jj]]
            row_str = str(self.rows[jj]).replace("'","").replace(",","")
            print(row_str)

        self.get_ss_lines()

        self.get_ret()

    def get_ret(self):
        symbols_keys = self.symbols.keys()
        for key in symbols_keys:
            total_value = 0
            for line in self.symbols[key]["lines"]:
                if line in LINES2:
                    value = self.symbols[key]["weight"]*len(line)
                    total_value += value
            self.symbols[key]["value"] = total_value
            if total_value > 0:
                self.symbols_w_value[key] = (self.symbols[key])

            self.ret += total_value

           

    def get_ss_lines(self):
        symbols_keys = self.symbols.keys()
        for key in symbols_keys:
            indeces = [ii+1 for ii,x in enumerate(self.session_symbols) if x in (key, WLD)]
            self.symbols[key]["lines"] = self.get_lines(indeces)

    def get_lines(self, indeces):

        lines = []
        col1 = [ x for x in indeces if x >= 1  and x <= 3]
        for ii in col1:
            col2 = [ x for x in indeces if x >= 4  and x <= 6]
            for jj in col2:
                col3 = [ x for x in indeces if x >= 7 and x <= 9]
                for kk in col3:
                    line = [ii, jj, kk]
                    col4 = [ x for x in indeces if x >= 10 and x <= 12]
                    if len(col4) == 0:
                        lines.append(line)
                    else:
                        for ll in col4:
                            line.append(ll)
                            col5 = [ x for x in indeces if x >= 13 and x <= 15]
                            if len(col5) == 0:
                                lines.append(line)
                            else:
                                for mm in col5:
                                    line.append(mm)
                                    lines.append(line)

        return lines

    def get_additions(self):
        self.num_fs = len([x for x in self.session_symbols if x == FS])
        self.orbs = [x for x in self.session_symbols if x in MNY_TYPES]
        print("n-fs:", self.num_fs,"orbs:", self.orbs)
        
    def algorithm1(self):
        pass

    def run(self):

        # init
        self.reset()

        # user input
        user_input_str = input(">")

        # execute
        symbols = self.execute()
       
        # update ret
        self.get_ret()
        
        # addition
        self.get_addition()
                
        # update ret, credit, rtp
        prf = self.ret - self.cost
        rtp = self.ret / self.cost
        self.total_rtp += rtp
        self.credit += prf
        my_print((self.ctr, -self.cost, self.ret, self.credit, rtp))
        
        if self.verbose:
            time.sleep(0.1)

        self.ctr += 1

# Tests

def test(args):
    sl = SL(args.num_lines, args.denom, args.multi, args.credit, args.automate, args.verbose)
    ctr = 0
    while not sl.symbols_w_value:
        sl.execute()
        ctr += 1
    print(sl.symbols_w_value, sl.ret / ctr)
    
    

# Main Function
def main(args):
    if args.test == True:
        test(args)
    else:
        final_credit_array = [0]*args.iterations
        final_rtp_array = [0]*args.iterations
        addition_ctr_array = [0]*args.iterations
        ctr_array = [0]*args.iterations
        threshold  = 1000
        succ_cnt = 0
        for ii in range(args.iterations):
            sl = SL(args.num_lines, args.denom, args.multi, args.credit, args.automate, args.verbose)
            max_ctr = 180
            credit_array = [0]*max_ctr

            while sl.credit >= sl.cost:
                sl.run()
                credit_array[vp.ctr-2] = sl.credit

                if sl.ctr >= max_ctr:
                    succ_cnt += 1
                    break

                if sl.ret >= threshold: 
                    succ_cnt += 1
                    break

                if sl.credit >= args.credit + threshold:
                    succ_cnt += 1
                    break

            final_rtp_array[ii] = sl.total_rtp / (sl.ctr - 1)
            final_credit_array[ii] = sl.credit
            addition_ctr_array[ii] = sl.addition_ctr
            ctr_array[ii] = sl.ctr
            if args.iterations == 1:
                print("mean-rtp:", final_rtp_array[ii], "acc", sl.acc_ctr / (sl.ctr - 1))
                #plt.plot(credit_array[0:sl.ctr-1])
                #splt.show()
        if args.iterations > 1:
            succ_ctr_array = [x for ii, x in enumerate(ctr_array) if final_credit_array[ii] > sl.cost ]
            succ_credit_array = [x for ii, x in enumerate(final_credit_array) if final_credit_array[ii] > sl.cost ]
            print("succ-pct:", succ_cnt/args.iterations,
                  "mean-succ-cnt:", statistics.mean(succ_ctr_array),
                  "max-succ-prf:", max(succ_credit_array)-args.credit, "mean-succ-pft:", statistics.mean(succ_credit_array)-args.credit,
                  "mean-addition-cnt:", statistics.mean(addition_ctr_array), 
                  "mean-rtp", statistics.median(final_rtp_array))

# Command-line Execution
if __name__=="__main__":
    #args
    parser = argparse.ArgumentParser(description="vp")
    parser.add_argument("-c", "--credit", type=int, default=2000, help="credit")
    parser.add_argument("-d", "--denom", default=1, help="denom")
    parser.add_argument("-m", "--multi", default=10, help="multi:1-10")
    parser.add_argument("-n", "--num_lines", type=int, default=10, help="num_lines:1 - 36")
    parser.add_argument("-i", "--iterations", type=int, default=1, help="iterations")
    parser.add_argument("-a", "--automate", action="store_true", help="automate")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument("-t", "--test", action="store_true", help="test")
    
    args = parser.parse_args()
    if args.iterations > 1:
        args.verbose = False
        args.automate = True
        def my_print(statement):
            pass
    main(args)
    



    
