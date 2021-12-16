import numpy as np 

from dwave.system.samplers import DWaveSampler
from dwave.embedding import embed_bqm, unembed_sampleset, majority_vote,embed_ising
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%m-%d-%H.%M.%S")



#start code to connect to d wave
##################################################
#sampler = DWaveSampler(solver='DW_2000Q_6',token='DEV-76a26fe9d6b5acd4e67793b0987934a72275b6a6') # 2000Q solver,

#####################################################################################################################
print("Connected to sampler", sampler.solver.name)




#embedding
# from helpers.embedding import DirectEmbeddingComposite
# sampler_embedded = DirectEmbeddingComposite(sampler)

from dwave.system.composites import EmbeddingComposite
sampler_embedded = EmbeddingComposite(sampler)

#encode h and J
J = { (0,0):0, (0,1):1, (0,2):1, (0,3):0, (0,4):0,
(1,2):1, (1,4):1,
(2,3):1, (2,4):1 }    # should these be 1 or -1???

h = [-1.5,-2.5,-3.5,-0.5,-1.5]  #k can vary but here k = 0.5?


##code for annealing
runs= 100   #no. runs
results = sampler_embedded.sample_ising(h, J, 
    num_reads=runs,
    annealing_time=200)

print("QPU time used:", results.info['timing']['qpu_access_time'], "microseconds.")
print(results)
# print(sampleset.info["timing"]) 
# print(sampleset.info['problem_id']) 
# print(sampleset.info['embedding_context'])
# print(sampleset.info['warnings'])
energy = results.record.energy
sample = results.record.sample.tolist()   ##to list???sample.tolist()
num_occurrences= results.record.num_occurrences
s = results.record.sample


num=len(sample) # number of unique solutions
sampledict={} # empty dictionary for samples
energydict={} # empty dictionary for energies
occdict={} # empty dictionary for occurances
sdict = {}
for k in range(num): # loop through dictionary to create list of samples and energies
    sampledict[k+1]=sample[k] # add sample to dictionary
    energydict[k+1]=energy[k] # add energy to to dictionary
    occdict[k+1]=num_occurrences[k] # add number of occurrences to dictionary
    sdict[k+1] = s[k]

bundledict={"sample":sampledict,"s":sdict, "energy":energydict,"num_occurrences":occdict, "timing":results.info} # bundle dictionary together  #'embedding_context':results.info['embedding_context']

filename='outputdata'+'QAtest' + current_time +'.txt' # file name
filename= 'DwaveDataOut/' +filename # file name plus path
f=open(filename,'w') # open the file to write
f.write(str(bundledict)) # write information
f.close() # close file

PAND = results.to_pandas_dataframe(sample_column=True)  
filename1='PANDAS-outputdata-'+'QAtest-' + current_time +'.txt' # file name
filename1= 'DwaveDataOut/' + filename1 # file name plus path
f1=open(filename1,'w') # open the file to write
f1.write(str(PAND)) # write information
f1.close() # close file
