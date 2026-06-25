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
PAYLINES = (
    (1,1,1),    (1,1,1,1),  (1,1,1,1,1),
    (1,1,2),    (1,1,2,1),  (1,1,2,1,1),    (1,1,2,3),  (1,1,2,3,3),
    (1,1,3),    (1,1,3,1),  (1,1,3,1,1),
    (1,2,1),    (1,2,1,2),  (1,2,1,2,1),
    (1,2,2),    (1,2,2,2),  (1,2,2,2,1),                (1,2,2,2,3),
    (1,2,3),    (1,2,3,2),  (1,2,3,2,1),
    (1,3,1),    (1,3,1,3),  (1,3,1,3,1),
    (1,3,2),    (1,3,2,3),  (1,3,2,3,1),    (1,3,2,1),  (1,3,2,1,3),
    (1,3,3),    (1,3,3,3),  (1,3,3,3,1),    (1,3,3,3,2),  (1,3,3,3,3), 

    (2,1,1),    (2,1,1,1),  (2,1,1,1,2),
    (2,1,2),    (2,1,2,1),  (2,1,2,1,2),    (2,1,2,3),  (2,1,2,3,2),
    (2,1,3),    (2,1,3,1),  (2,1,3,1,2),
    (2,2,1),    (2,2,1,2),  (2,2,1,2,2),
    (2,2,2),    (2,2,2,2),  (2,2,2,2,2),    
    (2,2,3),    (2,2,3,2),  (2,2,3,2,2),
    (2,3,1),    (2,3,1,3),  (2,3,1,3,2),
    (2,3,2),    (2,3,2,3),  (2,3,2,3,2),    (2,3,2,1),  (2,3,2,1,2),
    (2,3,3),    (2,3,3,3),  (2,3,3,3,2),    (2,3,3,3,1),

    (3,1,1),    (3,1,1,1),  (3,1,1,1,3),    (3,1,1,1,2),  (3,1,1,1,1),
    (3,1,2),    (3,1,2,1),  (3,1,2,1,3),    (3,1,2,3),  (3,1,2,3,1),
    (3,1,3),    (3,1,3,1),  (3,1,3,1,3),
    (3,2,1),    (3,2,1,2),  (3,2,1,2,3),
    (3,2,2),    (3,2,2,2),  (3,2,2,2,3),                (3,2,2,2,1),
    (3,2,3),    (3,2,3,2),  (3,2,3,2,3),
    (3,3,1),    (3,3,1,3),  (3,3,1,3,3),
    (3,3,2),    (3,3,2,3),  (3,3,2,3,3),    (3,3,2,1),  (3,3,2,1,1),
    (3,3,3),    (3,3,3,3),  (3,3,3,3,3),    
)
PAYLINES2 = []
for line in PAYLINES:
    line2 = list(line)
    line2[1] += 3
    line2[2] += 6
    if (len(line2)) > 3:
        line2[3] += 9
        if (len(line2)) > 4:
            line2[4] += 12
    PAYLINES2.append(line2)


SYMBOLS = {
    " 3 ": {"worth":  1, "lines": [], "pay_lines": [], "value": 0},
    " 4 ": {"worth":  1, "lines": [], "pay_lines": [], "value": 0},
    " 5 ": {"worth":  1, "lines": [], "pay_lines": [], "value": 0},
    " 6 ": {"worth":  1, "lines": [], "pay_lines": [], "value": 0},
    " 7 ": {"worth":  1, "lines": [], "pay_lines": [], "value": 0},
    " 8 ": {"worth":  1, "lines": [], "pay_lines": [], "value": 0},
    " 9 ": {"worth":  1, "lines": [], "pay_lines": [], "value": 0},
    " T ": {"worth":  2, "lines": [], "pay_lines": [], "value": 0}, 
    " J ": {"worth":  3, "lines": [], "pay_lines": [], "value": 0}, 
    " Q ": {"worth":  4, "lines": [], "pay_lines": [], "value": 0}, 
    " K ": {"worth":  6, "lines": [], "pay_lines": [], "value": 0}, 
    " A ": {"worth": 12, "lines": [], "pay_lines": [], "value": 0},
    "MINI":{"worth": 100, "lines": [], "pay_lines": [], "value": 0},
    "MINOR":{"worth": 200, "lines": [], "pay_lines": [], "value": 0},
    "MAXI":{"worth":  500, "lines": [], "pay_lines": [], "value": 0},
    "MAJOR":{"worth": 1000, "lines": [], "pay_lines": [], "value": 0},
    "GRAND":{"worth": 5000, "lines": [], "pay_lines": [], "value": 0},
}

WLD = " W "
FS  = " F "
MNY_TYPES = (3,6,9,12,18,36)
JP_TYPES = ("MINI","MINOR","MAXI","MAJOR","GRAND")
SYMBOL_DISTRO = [" W "]*30 + [" 3 "]*120 + [" 4 "]*120 + [" 5 "]*120 + [" 6 "]*120 + [" 7 "]*120 + [" 8 "]*120 + [" 9 "]*120 + \
          [" T "]*60  + [" J "]*40 + [" Q "]*30 + [" K "]*20 + [" A "]*10 + [" F "]*6 + ["MINI",]*3 + ["MINOR",]*2 + ["MAXI",] + ["MAJOR",] + \
          [MNY_TYPES[0]]*120 + [MNY_TYPES[1]]*60 + [MNY_TYPES[2]]*40 + [MNY_TYPES[3]]*30 + [MNY_TYPES[4]]*20 + [MNY_TYPES[5]*10]
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
        self.paylines = copy.deepcopy(PAYLINES2)[:self.num_lines]
        self.denom = denom
        self.multi = multi
        self.credit = credit
        self.automate = automate
        self.verbose = verbose
        self.mean_rtp = 0
        self.cost = denom * multi
        self.adj_symbol_worth = self.cost / num_lines
        
        self.columns = copy.deepcopy(COLUMNS)
        self.rows = copy.deepcopy(ROWS)
        self.session_symbols = []
        self.num_fs = 0
        self.orbs = []
        self.symbols = copy.deepcopy(SYMBOLS)
        self.symbols_w_value = {}
        self.addition_ctr = 0
        self.ctr = 0
        self.max_ctr = 0
        self.win = 0

    def reset(self):
        self.columns = copy.deepcopy(COLUMNS)
        self.rows = copy.deepcopy(ROWS)
        self.session_symbols = []
        self.num_fs = 0
        self.num_orbs = []
        self.symbols = copy.deepcopy(SYMBOLS)
        self.symbols_w_value = {}
        self.addition_ctr = 0
        self.ctr = 0
        self.max_ctr = 0
        self.win = 0

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

    def get_session_lines(self):
        symbols_keys = self.symbols.keys()
        for key in symbols_keys:
            indeces = [ii+1 for ii,x in enumerate(self.session_symbols) if x in (key, WLD)]
            self.symbols[key]["lines"] = self.get_lines(indeces)

    def get_ret(self):
        ret = 0
        symbols_keys = self.symbols.keys()
        for key in symbols_keys:
            total_value = 0
            for line in self.symbols[key]["lines"]:
                if line in self.paylines:
                    self.symbols[key]["pay_lines"].append(line)
                    value = self.adj_symbol_worth * self.symbols[key]["worth"]*len(line)
                    total_value += value
            self.symbols[key]["value"] = total_value
            if total_value > 0:
                self.symbols_w_value[key] = (self.symbols[key])
                if self.verbose:
                    my_print(("LINES AWARDED", key, self.symbols_w_value[key]["pay_lines"], round(self.symbols_w_value[key]["value"],2)))
                    time.sleep(0.2)

            ret += total_value

        additions = self.get_additions()
        ret += additions

        return ret
            
    def free_exec(self):
        total_addition = 0
        for ii in range(3):
            #os.system("clear")
            my_print(("FREE SPIN", ii+1))
            total_addition += self.execute()
            if self.verbose:
                time.sleep(0.2)

        return total_addition
    
    def hold_and_exec(self):
        total_additon = 0
        rows = copy.deepcopy(self.rows)
        spins = 3
        orb_falls = False
        while spins > 0:
            #os.system("clear")
            num_orbs = 0
            my_print(("HOLD & SPIN", spins, "spins left"))
            orb_falls = False
            for row in range(3):
                for col in range(5):
                    if rows[row][col] not in MNY_TYPES + JP_TYPES:
                        symbol = random.choice(SYMBOL_DISTRO + [0]*num_orbs*1000)
                        if symbol in MNY_TYPES + JP_TYPES:
                            rows[row][col] = symbol
                            orb_falls = True
                            num_orbs += 1
                        else:
                            rows[row][col] = "  "
                    else:
                        num_orbs += 1
                            
                row_str = str(rows[row]).replace("'","")
                my_print(row_str)
            if num_orbs > 14:
                print("GRAND JACKPOT WON!")
                total_additon += SYMBOLS["GRAND"]["worth"]

            if orb_falls == False:
                spins -= 1
            my_print("")
            if self.verbose:
                time.sleep(0.2)


        for row in range(3):
            addition = sum([x for x in rows[row] if x in MNY_TYPES])
            addition2 = sum([SYMBOLS[x]["worth"] for x in rows[row] if x in JP_TYPES])
            total_additon += addition + addition2

        my_print(("HOLD & SPIN BONUS Complete. Bonus", total_additon))

        
        return total_additon
        



    def get_additions(self):
        total_addition = 0

        # free spins
        self.num_fs = len([x for x in self.session_symbols if x == FS])
        if self.num_fs > 2:
            my_print("FREE GAMES TRIGGERED!")
            total_addition += self.free_exec()
            if self.verbose:
                time.sleep(0.2)
            self.addition_ctr += 1

        # hold and spin
        self.orbs = [x for x in self.session_symbols if x in MNY_TYPES + JP_TYPES]
        if len(self.orbs) > 5:
            my_print(("HOLD & SPIN TRIGGERED!"))
            total_addition += self.hold_and_exec()
            if self.verbose:
                time.sleep(0.2)
            self.addition_ctr += 1
            

        return total_addition

    def execute(self):
        #os.system("clear")
        self.columns = copy.deepcopy(COLUMNS)
        self.rows =  copy.deepcopy(ROWS)
        self.session_symbols = []
        self.num_fs = 0
        self.orbs = []
        self.symbols = copy.deepcopy(SYMBOLS)
        self.symbols_w_value = {}
        

        for ii in range(5):

            self.columns[ii] = random.sample(SYMBOL_DISTRO, 3)
            self.session_symbols += self.columns[ii]

        for jj in range(3):

            self.rows[jj] = [self.columns[0][jj], self.columns[1][jj], self.columns[2][jj], self.columns[3][jj], self.columns[4][jj]]
            row_str = str(self.rows[jj]).replace("'","").replace(",","")
            my_print(row_str)

        my_print("")

        self.get_session_lines()
        ret = self.get_ret()

        return ret

    def run(self):

        # init
        self.reset()
        self.ctr = 0
        self.max_ctr = 180
        total_rtp = 0
        init_credit = self.credit

        while self.credit > self.cost and self.ctr < self.max_ctr:

            # user input
            if not self.automate:
                user_input = input("press to spin (q to quit)...")
                if user_input in ("q", "e"):
                    break

            # execute
            ret = self.execute()
            
                    
            # update ret, credit, rtp
            self.win = ret - self.cost
            rtp = ret / self.cost
            total_rtp += rtp
            self.credit += self.win
            my_print((self.ctr, -self.cost, round(ret,2), round(self.credit,2), "\n"))
            
            if self.verbose:
                time.sleep(0.1)

            self.ctr += 1

            if ret >= SYMBOLS["GRAND"]["worth"]:
                break

            
        self.mean_rtp = total_rtp / self.ctr
        os.system("clear")
        my_print(("ctr", self.ctr, "cr", round(self.credit,2), "mean-rtp", round(self.mean_rtp,4)))

# Tests

def test(args):
    sl = SL(args.num_lines, args.denom, args.multi, args.credit, args.automate, args.verbose)
    sl.run()
    


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
            if args.iterations > 1:
                args.automate = True
                args.verbose = False
            sl = SL(args.num_lines, args.denom, args.multi, args.credit, args.automate, args.verbose)

            sl.run()

            if sl.credit > 2 * args.credit:
                succ_cnt += 1

            if sl.win > args.credit:
                succ_cnt += 1

            final_rtp_array[ii] = sl.mean_rtp
            final_credit_array[ii] = sl.credit
            addition_ctr_array[ii] = sl.addition_ctr
            ctr_array[ii] = sl.ctr
            if args.iterations == 1:
                print("mean-rtp:", final_rtp_array[ii], "acc", sl.addition_ctr / (sl.ctr - 1))
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
    parser.add_argument("-c", "--credit", type=int, default=1000, help="credit")
    parser.add_argument("-d", "--denom", default=1, help="denom")
    parser.add_argument("-m", "--multi", default=10, help="multi:1-10")
    parser.add_argument("-n", "--num_lines", type=int, default=len(PAYLINES2), help="num_lines:10 - 95")
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
    



    
