#import libraries
from scipy.stats import betabinom
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#***************************************************************************************************************
#function name: calculate_N_plus
#precondition: document collection is loaded from a csv to a pandas dataframe
#postcondition: returns the number of relevant documents in the document collection
#***************************************************************************************************************

def calculate_N_plus(data, topic_as_string):
    N_plus = len(data[data[topic_as_string]=='True'])
    return N_plus


#***************************************************************************************************************
#function name: calculate_N_minus
#precondition: document collection is loaded from a csv to a pandas dataframe
#postcondition: returns the number of relevant documents in the document collection
#***************************************************************************************************************

def calculate_N_minus(N_plus, N):
    N_minus = N - N_plus
    return N_minus


#***************************************************************************************************************
#function name: get_Z_value
#precondition: 
#postcondition: returns Z, smallest number of docs reviewed to reach 80% recall
#***************************************************************************************************************

def get_Z_value(data, topic_as_string, N_plus):
    trues = 0
    for i in range(len(data)):
        if (data[topic_as_string][i] == 'True'):
            trues = trues + 1
            if (trues / N_plus > .80):
                recall_doc = i
                break 
    return recall_doc


#***************************************************************************************************************
#function name: get_Zplus_value
#precondition: 
#postcondition: 
#***************************************************************************************************************

def get_Zplus_value(data, Zval, topic_as_string):
    Zplus = len(data.iloc[:Zval][data[topic_as_string]=='True'])
    return Zplus


#***************************************************************************************************************
#function name: get_Zplus_value
#precondition: 
#postcondition: 
#***************************************************************************************************************

def get_Zminus_value(Zval, Zplus):
    Zminus = Zval - Zplus
    return Zminus


#***************************************************************************************************************
#function name: get_Z0list
#precondition: 
#postcondition: 
#***************************************************************************************************************

def get_Z0(N, Zval):
    Z0 = N - Zval
    return Z0


#***************************************************************************************************************
#function name: get_Z0list
#precondition: 
#postcondition: 
#***************************************************************************************************************

def get_Z0list(data, Zval, topic_as_string):
    Z0plus = data.iloc[:Zval][data[topic_as_string]=='True']
    return Z0plus


#***************************************************************************************************************
#function name: get_Z0plus_value
#precondition: 
#postcondition: 
#***************************************************************************************************************

def get_Z0plus_value(data, topic_as_string):
    Zplus = len(data.iloc[:][data[topic_as_string]=='True'])
    return Zplus


#***************************************************************************************************************
#function name: get_Z0minus_value
#precondition: 
#postcondition: 
#***************************************************************************************************************

def get_Z0minus_value(Z0, Z0plus):
    Z0minus = Z0 - Z0plus
    return Z0minus


#***************************************************************************************************************
#function name: generate_samples
#precondition: 
#postcondition: 
#***************************************************************************************************************

# DDL to LG : I would give this a more specific name like generate_prefix_for_budget.
#
# Maybe rename size to G. 
#
# Comments on comments: 
#         "function name: generate_samples" -> new name
#
#          I would add an overall comment : "Finds longest prefix of collection permutation that will be fully coded after coding G documents."   
#
#          "find first [size] unreviewed documents" -> something like "prefix is docs prior to G+1'st unreviewed doc"
          
def generate_prefix(data, size, Z):
    prefix = pd.DataFrame()
    unreviewed = 0
    
    #find first [size] unreviewed documents
    for i in range(len(data)):
        prefix = prefix.append(data.iloc[i])
        if data.index[i] > Z:
            unreviewed += 1
            if unreviewed > size:
                break
    
    # #find [size+1] to next unreviewed doc(excluded)
    # for j in range(i+1, len(data)):
    #     if data.index[j] > Z:
    #         prefix = prefix.append(data.iloc[j])
    #     else:
    #         break
    return prefix


#***************************************************************************************************************
#function name: compute_M
#precondition: 
#postcondition: 
#***************************************************************************************************************

# DDL to LG: I'm confused by this function.  Why doesn't it take the prefix as input?
# M is the just the length of the prefix, and M_plus and M_minus can be found by scanning over the prefix.  
def compute_M(sample, topic_as_string, Z):
    Mvalues = { 'M' : 0, 'M_plus' : 0, 'M_minus' : 0, 'sample-size' : len(sample)}
    
    #create a list of the PRNs for the sample to perform comparison
    PRN_list = sample['PRNs'].tolist()
    
    indexes = []
    for i in range(len(PRN_list)):
        indexes = indexes + (sample.index[sample['PRNs']==PRN_list[i]].tolist())
    
    for i in range(len(indexes)):
        
        if (indexes[i] >= Z):
            Mvalues['M'] += 1
            if sample.loc[indexes[i]][topic_as_string] == 'True':
                Mvalues['M_plus'] += 1
            else:
                Mvalues['M_minus'] += 1
    return Mvalues


#***************************************************************************************************************
#function name: compute_conf_intsUOSCI
#precondition: 
#postcondition: 
#***************************************************************************************************************

# DDL to LG: There's two errors in this:
#
#     1. "i" should range over all and only the values of Nplus that are logically possible after seeing the sample.
# If I understand range(), you have it running from 1 to N-1 which, even if we wanted all possible values of Nplus
# before seeing the sample, should be range(0, N+1) not range(1,N). 
# to cover from 0 to N.  Let me know if I'm misunderstanding 
#     2. The posterior distribution is for the shifted variable Nplustwiddle - Mplus, so need to adjust for that in ratio
#
# See my version below, called compute_WSR_approx_UOSCI
#
#
def compute_conf_intsUOSCI(N, sample):
    confint = []
    for i in range(1,N):
        prior = betabinom.pmf(i, N, 1/99, 1)
        Npost = N - sample['sample-size']
        apost = (1/99) + sample['M_plus']
        bpost = 1 + sample['M'] - sample['M_plus']
        posterior = betabinom.pmf(i, Npost, apost, bpost)
        if (prior < 20 * posterior):
            confint.append(i)
    sample['conf_upperUOSCI'] = max(confint)
    sample['conf_lowerUOSCI'] = min(confint)
    #checking the adjacent elements
    for i in range(1, len(confint)):
        if(confint[i] != confint[i-1]+1):
            print("The interval has a missing value after " + confint[i])
    print("The interval is an unbroken sequence of N values")
    print(sample)


#***************************************************************************************************************
#function name: compute_WSR_approx_UOSCI
#precondition: 
#postcondition: 
#***************************************************************************************************************

# This corrects the two errors I spotted in compute_conf_intsUOSCI. 
# I've also restructured the code to make it track the math and our notation
# more closely.  A crucial thing for clarity is to recognize that
# the prior and posterior distribution should be computed just once
# and then used.  So I use frozen rvs for that.
#
# I don't actually know Python so check carefully and ask questions if anything seems off. 

def compute_WSR_approx_UOSCI(N, sample):
    confint = []
    #
    prior_N = N
    prior_a = 1/99
    prior_b = 1
    prior_dist = betabinom(prior_N, prior_a, prior_b)
    #
    M = sample['sample-size']
    Mplus = sample['M_plus']
    Mminus = sample['M_minus']
    posterior_N = N - M
    posterior_a = a + Mplus
    posterior_b = b + Mminus
    posterior_dist = betabinom(posterior_N, posterior_a, posterior_b) 
    #
    Nplus_min = Mplus 
    Nplus_max = N - Mminus
    # I think range(x, y) runs from x to y-1  
    for Nplus_twiddle in range(Nplus_min, Nplus_max+1):
        prior_prob = prior_dist.pmf(Nplus_twiddle)
        # posterior_dist is a distribution over the values from 0 to
        # N - M, but where those values have the interpretation (Nplus_twiddle - Mplus).
        # So we have posterior probabilities for Nplus_twiddle - Mplus = 0 through
        # Nplus_twiddle - Mplus = N - M, i.e. for Nplus_twiddle ranging 
        # from Mplus to N - M + Mplus, i.e. Mplus to N - Mminus as they should.    
        posterior_prob = posterior_dist.pmf(Nplus_twiddle - Nplus_min) 
        if (prior_prob < 20 * posterior_prob):
            confint.append(Nplus_twiddle)
    #
    sample['conf_upperUOSCI'] = max(confint)
    sample['conf_lowerUOSCI'] = min(confint)
    #checking the adjacent elements
    for i in range(1, len(confint)):
        if(confint[i] != confint[i-1]+1):
            print("The interval has a missing value after " + confint[i])
    print("Confidence set is an unbroken interval")
    print(sample)

    


    
#***************************************************************************************************************
#function name: compute_conf_intsTSCI
#precondition: 
#postcondition: 
#***************************************************************************************************************
#
# DDL: 
#

def compute_conf_intsTSCI(N, sample):
    confint = []
    for i in range(1,N):
        prior = betabinom.pmf(i, N, 1, 1)
        Npost = N - sample['sample-size']
        apost = 1 + sample['M_plus']
        bpost = 1 + sample['sample-size'] - sample['M_plus']
        posterior = betabinom.pmf(i, Npost, apost, bpost)
        if (prior < 20 * posterior):
            confint.append(i)
    sample['conf_upperTSCI'] = max(confint)
    sample['conf_lowerTSCI'] = min(confint)
    np.sort(confint)
    #checking the adjacent elements
    for i in range(1, len(confint)):
        if(confint[i] != confint[i-1]+1):
            print("The interval has a missing value after " + confint[i])
    print("The interval is an unbroken sequence of N values")
    print(sample)    
    

#***************************************************************************************************************
#function name: prune_conf_intsUOSCI
#precondition: 
#postcondition: 
#***************************************************************************************************************

def prune_conf_intsUOSCI(sample, N, Z_minus, Z_plus):
    adjusted_upper = N-(Z_minus + sample['M_minus'])
    sample['conf_upperUOSCI'] = min(adjusted_upper, sample['conf_upperUOSCI'])
    sample['conf_lowerUOSCI'] = Z_plus + sample['M_plus']
    print(sample)
    
    
#***************************************************************************************************************
#function name: prune_conf_intsTSCI
#precondition: 
#postcondition: 
#***************************************************************************************************************

def prune_conf_intsTSCI(sample, N, Z_minus, Z_plus):
    adjusted_lower = Z_plus + sample['M_plus']
    adjusted_upper = N-(Z_minus + sample['M_minus'])
    sample['conf_upperTSCI'] = min(adjusted_upper, sample['conf_upperTSCI'])
    sample['conf_lowerTSCI'] = max(adjusted_lower, sample['conf_lowerTSCI'])
    print(sample)
    
#***************************************************************************************************************
#function name: compute_LOSCI_recall
#precondition: 
#postcondition: 
#***************************************************************************************************************

def compute_UOSCI_recall(sample, Z_plus):
    sample['UOSCI_RECALL-lower'] = (Z_plus + sample['M_plus'])/sample['conf_upperUOSCI']
    sample['UOSCI_RECALL-upper'] = (Z_plus + sample['M_plus'])/sample['conf_lowerUOSCI']
    print(sample['UOSCI_RECALL-lower'])
    print(sample['UOSCI_RECALL-upper'])

    
#***************************************************************************************************************
#function name: compute_TSCI_recall
#precondition: 
#postcondition: 
#***************************************************************************************************************

def compute_TSCI_recall(sample, Z_plus):
    sample['TSCI_RECALL-lower'] = (Z_plus + sample['M_plus'])/sample['conf_upperTSCI']
    sample['TSCI_RECALL-upper'] = (Z_plus + sample['M_plus'])/sample['conf_lowerTSCI']

    print(sample['TSCI_RECALL-lower'])
    print(sample['TSCI_RECALL-upper'])
