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
OUTPUT = ["",]
COLUMNS = [0] *5
ROWS =  [[0] * 5] *3
PAYLINES = (

    # straight
    (1,1,1),    (1,1,1,1),  (1,1,1,1,1),
    (2,2,2),    (2,2,2,2),  (2,2,2,2,2),
    (3,3,3),    (3,3,3,3),  (3,3,3,3,3),

    # Y-axis (bilateral) symmetry
    # Valleys
    #                       0 0 . 0 0
    #                       . . 0 . .
    #                       . . . . .
    (1,1,2),    (1,1,2,1),  (1,1,2,1,1),    
    
    #                       0 0 . 0 0
    #                       . . . . .  
    #                       . . 0 . .
    (1,1,3),    (1,1,3,1),  (1,1,3,1,1),
    #                       0 . . . 0
    #                       . 0 0 0 .  
    #                       . . . . .
    (1,2,2),    (1,2,2,2),  (1,2,2,2,1),                  
    #                       0 . . . 0
    #                       . 0 . 0 .  
    #                       . . 0 . .
    (1,2,3),    (1,2,3,2),  (1,2,3,2,1),
    #                       0 . . . 0
    #                       . . . . .  
    #                       . 0 0 0 .
    (1,3,3),    (1,3,3,3),  (1,3,3,3,1),    
    #                       . . . . .
    #                       0 0 . 0 0  
    #                       . . 0 . .
    (2,2,3),    (2,2,3,2),  (2,2,3,2,2),
    #                       . . . . .
    #                       0 . . . 0  
    #                       . 0 0 0 .
    (2,3,3),    (2,3,3,3),  (2,3,3,3,2),    
                            

    # Hills
    #                       . 0 0 0 .
    #                       0 . . . 0  
    #                       . . . . .
    (2,1,1),    (2,1,1,1),  (2,1,1,1,2),
    #                       . . 0 . .
    #                       0 0 . 0 0  
    #                       . . . . .
    (2,2,1),    (2,2,1,2),  (2,2,1,2,2),
    #                       . 0 0 0 .
    #                       . . . . .  
    #                       0 . . . 0
    (3,1,1),    (3,1,1,1),  (3,1,1,1,3),    
    #                       . . 0 . .
    #                       . 0 . 0 .  
    #                       0 . . . 0
    (3,2,1),    (3,2,1,2),  (3,2,1,2,3),
    #                       . . . . .
    #                       . 0 0 0 .  
    #                       0 . . . 0
    (3,2,2),    (3,2,2,2),  (3,2,2,2,3),
    #                       . . 0 . .
    #                       . . . . .  
    #                       0 0 . 0 0
    (3,3,1),    (3,3,1,3),  (3,3,1,3,3),
    #                       . . . . .
    #                       . . 0 . .  
    #                       0 0 . 0 0
    (3,3,2),    (3,3,2,3),  (3,3,2,3,3),
          
    # Ws
    #                       0 . 0 . 0
    #                       . 0 . 0 .  
    #                       . . . . .
    (1,2,1),    (1,2,1,2),  (1,2,1,2,1),
    #                       0 . 0 . 0
    #                       . . . . .  
    #                       . 0 . 0 .
    (1,3,1),    (1,3,1,3),  (1,3,1,3,1),
    #                       0 . . . 0
    #                       . . 0 . .  
    #                       . 0 . 0 .
    (1,3,2),    (1,3,2,3),  (1,3,2,3,1),
    #                       . . 0 . .
    #                       0 . . . 0  
    #                       . 0 . 0 .
    (2,3,1),    (2,3,1,3),  (2,3,1,3,2),
    #                       . . . . .
    #                       0 . 0 . 0  
    #                       . 0 . 0 .
    (2,3,2),    (2,3,2,3),  (2,3,2,3,2),

    # Ms
    #                       . 0 . 0 .
    #                       0 . 0 . 0  
    #                       . . . . .
    (2,1,2),    (2,1,2,1),  (2,1,2,1,2),    
    #                       . 0 . 0 .
    #                       0 . . . 0  
    #                       . . 0 . .
    (2,1,3),    (2,1,3,1),  (2,1,3,1,2),
    #                       . 0 . 0 .
    #                       . . 0 . .  
    #                       0 . . . 0
    (3,1,2),    (3,1,2,1),  (3,1,2,1,3),    
    #                       . 0 . 0 .
    #                       . . . . .  
    #                       0 . 0 . 0            
    (3,1,3),    (3,1,3,1),  (3,1,3,1,3),
    #                       . . . . .
    #                       . 0 . 0 .  
    #                       0 . 0 . 0
    (3,2,3),    (3,2,3,2),  (3,2,3,2,3),

    # Z-axis (rotational) symmetry
    # Ns
    #                       0 . . 0 .
    #                       . . 0 . .  
    #                       . 0 . . 0
                (1,3,2,1),  (1,3,2,1,3),
    #                       . 0 . . .
    #                       0 . 0 . 0  
    #                       . . . 0 .
                (2,1,2,3),  (2,1,2,3,2),
    #                       . . . 0 .
    #                       0 . 0 . 0  
    #                       . 0 . . .
                (2,3,2,1),  (2,3,2,1,2),
    #                       . 0 . . 0
    #                       . . 0 . .  
    #                       0 . . 0 .
                (3,1,2,3),  (3,1,2,3,1),

    # 1-Sided Hills
    #                       . . . . 0
    #                       . 0 0 0 .  
    #                       0 . . . .
                            (3,2,2,2,1),
    #                       0 0 . . .
    #                       . . 0 . .  
    #                       . . . 0 0   
                (1,1,2,3),  (1,1,2,3,3),
    #                       0 . . . .
    #                       . 0 0 0 .  
    #                       . . . . 0
                            (1,2,2,2,3),
    #                       . . . 0 0
    #                       . . 0 . .  
    #                       0 0 . . .
                (3,3,2,1),  (3,3,2,1,1),

    # Non-symmetric
    #                       0 . . . .
    #                       . . . . 0  
    #                       . 0 0 0 .
                            (1,3,3,3,2),
    #                       0 . . . .
    #                       . . . . .  
    #                       . 0 0 0 0
                            (1,3,3,3,3),
    #                       . . . . 0
    #                       0 . . . .  
    #                       . 0 0 0 .
                            (2,3,3,3,1),
   
    #                       . 0 0 0 .
    #                       . . . . 0  
    #                       0 . . . .
                            (3,1,1,1,2),
    #                       . 0 0 0 0
    #                       . . . . .  
    #                       0 . . . .
                            (3,1,1,1,1),
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



MIN_VAL = 1
SYMBOLS = {
    " B ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    " C ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    " D ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    " E ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    " G ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    " H ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    " I ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    "10 ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0}, 
    " J ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0}, 
    " Q ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0}, 
    " K ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0}, 
    " A ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    "FS ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    "WD ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
}
WLD = "WD "
FS  = "FS "
KEYS_SYMBOLS = list(SYMBOLS.keys())
LEN_SYMBOLS = len(KEYS_SYMBOLS)
DISTRO_SYMBOLS = []
for key in KEYS_SYMBOLS:
    cnt = int(1000 / SYMBOLS[key]["worth"])
    DISTRO_SYMBOLS += [key,]*cnt

MNY = {
    "1x ": {"worth":    1, "lines": [], "pay_lines": [],  "value": 0},
    "2x ": {"worth":    2, "lines": [], "pay_lines": [],  "value": 0},
    "3x ": {"worth":    3, "lines": [], "pay_lines": [],  "value": 0},
    "4x ": {"worth":    4, "lines": [], "pay_lines": [],  "value": 0},
    "5x ": {"worth":    5, "lines": [], "pay_lines": [],  "value": 0},
    "MNI": {"worth":   50, "lines": [], "pay_lines": [],  "value": 0},
    "MNR": {"worth":  100, "lines": [], "pay_lines": [],  "value": 0},
    "MXI": {"worth":  200, "lines": [], "pay_lines": [],  "value": 0},
    "MJR": {"worth":  500, "lines": [], "pay_lines": [],  "value": 0},
    "GRD": {"worth":10000, "lines": [], "pay_lines": [],  "value": 0},
}
GRAND_WORTH = MNY["MJR"]["worth"]*10
KEYS_MNY = list(MNY.keys())
LEN_MNY = len(KEYS_MNY)
DISTRO_MNY = []
for key in KEYS_MNY:
    cnt = int(1000 / MNY[key]["worth"])
    DISTRO_MNY += [key]*cnt

SYMBOLS_MNY = {}
SYMBOLS_MNY.update(SYMBOLS)
SYMBOLS_MNY.update(MNY)
LEN_SYMBOLS_MNY = LEN_SYMBOLS + LEN_MNY
KEYS_SYMBOLS_MNY = KEYS_SYMBOLS + KEYS_MNY
DISTRO_SYMBOLS_MNY = DISTRO_SYMBOLS + DISTRO_MNY

#print(DISTRO_SYMBOLS_MNY)
#sys.exit()



# Functions
def my_decorator(func):
    def wrapper(statement):
        choice = random.choice(range(len(OUTPUT)))
        line = str(statement) +" "+ OUTPUT[choice]
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
        self.symbols = copy.deepcopy(SYMBOLS_MNY)
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
        self.symbols = copy.deepcopy(SYMBOLS_MNY)
        self.symbols_w_value = {}
        self.addition_ctr = 0
        self.ctr = 0
        self.max_ctr = 0
        self.win = 0

    
            
    def free_spin(self):
        total_addition = 0
        for ii in range(3):
            #os.system("cls")
            my_print(("FS", ii+1))
            total_addition += self.spin()
            if self.verbose:
                time.sleep(0.2)

        my_print(("FS Complete.", total_addition))

        return total_addition
    
    def hold_and_spin(self):
        total_addition = 0
        rows = copy.deepcopy(self.rows)
        spins = 3
        orb_falls = False
        
        while spins > 0:
            #os.system("cls")
            num_orbs = 0
            my_print(("H&S", spins, "left"))
            orb_falls = False
            orbs = 0
            grand_hit = False
            for row in range(3):
                for col in range(5):
                    if rows[row][col] not in KEYS_MNY:
                        hs_symbols = DISTRO_MNY + [0] * (num_orbs + 1) ** 4
                        symbol = random.choice(hs_symbols)
                        if symbol in KEYS_MNY:
                            rows[row][col] = symbol
                            orb_falls = True
                            num_orbs += 1
                            orbs += MNY[symbol]["worth"]
                        else:
                            rows[row][col] = "  "
                    else:
                        orbs += MNY[rows[row][col]]["worth"]
                        num_orbs += 1
                    if rows[row][col] == "GRD":
                        grand_hit = True
                            
                row_str = str(rows[row]).replace("'","")
                my_print(row_str)
            if grand_hit or num_orbs > 14:
                #if self.verbose:
                print(self.ctr, "GRAND!")
                total_addition += GRAND_WORTH
                return total_addition

            if orb_falls == False:
                spins -= 1
            my_print("")
            if self.verbose:
                time.sleep(0.2)

        addition = self.cost*orbs
        total_addition += addition

        my_print(("H&S Complete.", total_addition))

        return total_addition
        
    def get_additions(self):
        total_addition = 0
        self.num_fs = 0
        self.orbs = []

        # free spins
        self.num_fs = len([x for x in self.session_symbols if x == FS])
        if self.num_fs > 2:
            my_print("FS!")
            total_addition += self.free_spin()
            if self.verbose:
                time.sleep(0.2)
            self.addition_ctr += 1

        # hold and spin
        self.orbs = [MNY[x]["worth"] for x in self.session_symbols if x in KEYS_MNY]
        if len(self.orbs) > 5:
            my_print(("H&S!"))
            total_addition += self.hold_and_spin()
            if self.verbose:
                time.sleep(0.2)
            self.addition_ctr += 1
            

        return total_addition

    def get_paylines(self):
        paylines = 0
        self.symbols_w_value = {}
        for key in KEYS_SYMBOLS_MNY:
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
                    my_print(("LINES!", key, self.symbols_w_value[key]["pay_lines"], round(self.symbols_w_value[key]["value"],2)))
                    time.sleep(0.2)

            paylines += total_value

        return paylines
        


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
        self.symbols = copy.deepcopy(SYMBOLS_MNY)
        symbols_keys = self.symbols.keys()
        for key in symbols_keys:
            indeces = [ii+1 for ii,x in enumerate(self.session_symbols) if x in (key, WLD)]
            self.symbols[key]["lines"] = self.get_lines(indeces)

            

    def get_session_symbols(self):
        self.session_symbols = []
        self.columns = copy.deepcopy(COLUMNS)
        for ii in range(5):

            self.columns[ii] = random.sample(DISTRO_SYMBOLS_MNY, 3)
            self.session_symbols += self.columns[ii]

        for jj in range(3):
            self.rows =  copy.deepcopy(ROWS)
            self.rows[jj] = [self.columns[0][jj], self.columns[1][jj], self.columns[2][jj], self.columns[3][jj], self.columns[4][jj]]
            row_str = str(self.rows[jj])
            my_print(row_str)

        my_print("")

    def spin(self):
        # init
        ret = 0
        if self.verbose:
            os.system("cls")
        
        self.get_session_symbols()
        self.get_session_lines()
        paylines  = self.get_paylines()
        additions = self.get_additions()
        ret += paylines + additions

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
                user_input = input(">")
                if user_input in ("q", "e"):
                    break

            # spin
            ret = self.spin()
            
            # update ret, credit, rtp
            self.win = ret - self.cost
            rtp = ret / self.cost
            total_rtp += rtp
            self.credit += self.win

            #results
            self.ctr += 1

            my_print(("ctr", self.ctr, "cost", -self.cost, "ret", round(ret,2), "cr", round(self.credit,2), "\n"))
            
            if self.verbose:
                time.sleep(0.1)

            if ret >= GRAND_WORTH:
                break

        self.mean_rtp = total_rtp / self.ctr
        #os.system("cls")
        my_print(("ctr", self.ctr, "cr", round(self.credit,2), "mean-rtp", round(self.mean_rtp,4)))

# Tests
def test(args):
    sl = SL(args.num_lines, args.denom, args.multi, args.credit, args.automate, args.verbose)
    #sl.reset()
    #sl.run()
    #sl.spin()
    #sl.get_session_symbols()
    #sl.get_session_lines()
    #indeces = []
    #sl.get_lines(indeces)
    #sl.get_paylines()
    #sl.get_additions()
    #sl.free_spin()
    #sl.hold_and_spin()

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
    parser.add_argument("-n", "--num_lines", type=int, default=len(PAYLINES2), help="num_lines:1 - 100")
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
    



    
