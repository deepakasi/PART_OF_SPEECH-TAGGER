###################################
# CS B551 Fall 2015, Assignment #5
#
# Your names and user ids:
#Nethra C Sashikar necsashi
#Deepa Kasinathan deepkasi
# (Based on skeleton code by D. Crandall)
#
#
####
# train()
#We define the fuction train to calculate all the values beforhand needed for Part of Speech tagging
#self.pos has all the part of speech in it
#self.dpos has the count for number of occurences of part of speech
#self.ppos has probablity of each part of speech
#self.rpos has transition probablity between each  part of speech
#self.sword has list of word for each POS
#self.words has list of all words in the dataset
#self.initial has the initial probablity of each POS
# naive()
#POS of the word is calculated from the occurence of the word in each POS and assignned with POS with  maximum probablity value
# mcmc()
#We do sampling by assgning random POS for each word and sample word over each part of speech and decide the POS for next round sampling.
#we then continue by assigning the word with POS having maximum probability 
# max_marginal()
#We do mcmc with sampling done for thousand times
#and calculate the maximum POS of the word done similar to sampling
# Viterbi()
#We use the initial probability calculated and for the first word and take a product with its emission probability
#for the consecutive words we calculate the 12 values of transition from previous state and assign POS with maximum value 
#and repeat this till end of the sentence
#Finally we back propogate to find the path that resulted wit maximum probabilty to find the sequence of POS
# best()
#Best algorithm uses naive bayes with transition probability to find the probability of POS
#and assign the probability with maximum value for transition and naive bayes 
# posterior()
#We calculate the posterior after finding all POS for the sentences
#P(POS's/words) and find the log base 10 for the product of the probabilities P(POS/Word) for each word
#Assumptions made:
#For the values missing in the dataset we check if it is verb or adjective or  noun
#if it matches with any of the categories mentioned it is assigned with the POS
#else we assign a very small value for its presence and calculate probability for POS
#and assign the POS with maximum probability
####
import random
import math
import collections 
import bisect
# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    def __init__(self):
        self.pos=["adj","adv","adp","conj","det","noun","num","pron","prt","verb","x","."]
        self.dpos=dict()
        self.ppos=dict()
        self.rpos=dict()
        self.words=list()
        self.sword=collections.defaultdict(list)
        self.count=[0]*len(self.pos)
        self.initial=dict()
   



     

    # Do the training!
    #
    def train(self, data):
        ####Find initial Probablility####
        for i in range(0,len(self.pos)):
            self.initial[self.pos[i]]=0
        ###Initializing key for dictionary counting number of occurences of POS####
        for i in range(0,len(self.pos)):
            self.dpos[self.pos[i]]=0
        ###Initializing key for dictionary holding probablity of each POS###    
        for k in range(0,len(self.pos)):
            self.ppos[self.pos[k]]=0  
        ###Initianlizing key for dictionary holding key for each relation for POS###    
        for i in range(0,len(self.pos)):
            for j in range(0,len(self.pos)):
                self.rpos[self.pos[i]+"-"+self.pos[j]]=0
        for i in range(0,len(self.pos)):
            self.sword[self.pos[i]]= [0]     
        ####Loop for actual counting of POS####        
        for i in range(0,len(data)):
            (s, gt)=data[i]
            self.initial[gt[0]]+=1
            for k in range(0,len(s)):
                (self.sword[gt[k]]).append(s[k])
                self.words.append(s[k])


            for j in range(0,len(self.pos)):
                self.dpos[self.pos[j]]+=gt.count(self.pos[j])
               
        psum=0        
        ####Calculate total occurences of POS###
        for l in range(0,len(self.pos)):
            psum+=self.dpos[self.pos[l]]
        ####Calculate the probability of POS###    
        for j in range(0,len(self.pos)):
            self.ppos[self.pos[j]]=float(self.dpos[self.pos[j]])/float(psum)   
        ###Calcutaling n(s(i+1))/n(si)#####
        ind=0   
        for i in range(0,len(self.pos)):
            for j in range(0,len(self.pos)):
                temp=0
                for k in range(0,len(data)):
                    (s,gt)=data[k]
                    for l in range(0,len(gt)-1):
                        if(gt[l]==self.pos[i] and gt[l+1]==self.pos[j]):
                            temp=temp+1
                t= self.pos[i]+"-"+self.pos[j]                          
                self.rpos[t]=temp 
                ind=ind+1 
                self.rpos[t]=float(self.rpos[t])/float(self.dpos[self.pos[i]])                      
        ###Count of number of words for POS###
        for i in range(0,len(self.pos)):
            nethra=list(self.sword[self.pos[i]])
            self.count[i]=len(nethra)  
        #### Finding Initial Probability####
        for i in range(0,len(self.pos)):
            self.initial[self.pos[i]]=float(self.initial[self.pos[i]])/float(len(data) ) 
        
        pass

    # Functions for each algorithm.
    #
    def naive(self, sentence):
        w=list()       
        for i in range(0,len(sentence)):
            prob=list()
            c=self.words.count(sentence[i])
           
            if c==0:
                w.append("noun")    
            if c!=0:
                for j in range(0,len(self.pos)):
                    n=list(self.sword[self.pos[j]])
                    t=n.count(sentence[i])
                    p=float(t)/float(c)
                    prob.append(p) 
                k=prob.index(max(prob))  
                w.append(self.pos[k])   
  
        return [ [w], [] ]

    def mcmc(self, sentence, sample_count):
        Matrix = [[0 for x in range(len(sentence))] for x in range(5)] 
        for i in range(0,len(sentence)):
            p=self.pos[random.randint(0,11)]
            h=dict()
            for n in range(0,len(self.pos)):
                h[self.pos[n]]=0  
            c=self.words.count(sentence[i])

            for j in range(0,5):
                t=sentence[i]
                if c==0 and (t[-2:]== "\'s"or t[-2:]=="er" or t[-3:]=="ice " or t[-3:]=="ness" or t[-4:]=="sion" or t[-4:]=="ance" or t[-4:]=="ment" or t[-4:]=="hood" or t[-3:] =="dom " or t[-2:] =="cy" or t[-3:]=="ist" or t[-3:]=="ity" or t[-4:]=="ship"):
                    h[self.pos[5]]+=1
                    Matrix[j][i]=max(h, key=h.get) 
                elif c==0 and (t[-3:]=="ful" or t[-4:] =="eous" or t[-1:]=="y" or t[-3:]=="ish" or t[-3:]== "ble" or t[-3:]=="ial" or t[-3:]=="ent" or t[-3:]=="less" or t[-2:]=="ng" or t[-2:]=="ly" or t[-3:]=="ive" or t[-2:]=="ic"):
                    h[self.pos[0]]+=1
                    Matrix[j][i]=max(h, key=h.get)     
                elif c==0 and (t[-2:]=="ed" or t[-3:]=="ing"):
                    h[self.pos[9]]+=1
                    Matrix[j][i]=max(h, key=h.get) 
                elif c==0 :
                    h[self.pos[8]]+=1
                    Matrix[j][i]=max(h, key=h.get) 
                        
                else:        
                    prob=list()

                    for k in range(0,12):
                        n=list(self.sword[self.pos[k]])
                        t=n.count(sentence[i])
                        if sentence[i] not in n:
                            temp=0
                        elif t!=0 :
                            if i==0:
                                temp=(float(t)/float(c))
                            else:
                                temp=(float(t)/float(len(n)))*float(self.rpos[Matrix[j][i-1]+"-"+self.pos[k]])
                                    
                        else:
                            temp=0.00000000000000000000034      
                        prob.append(temp)
                    l=random.random()
                    ind=[m for m,v in enumerate(prob) if v >l]  
                    if not ind :
                        ind=[m for m,v in enumerate(prob) if v <l]  
                    p=random.choice(ind)
                    ind=bisect.bisect(prob,l)             
                    if ind >11:
                        m=max(prob,key=float)
                        k1=prob.index(m)
                        p=k1
                    else:
                        p=ind
                    h[self.pos[p]]+=1
                    Matrix[j][i]=max(h, key=h.get) 
                

    
        return [[Matrix[0],Matrix[1],Matrix[2],Matrix[3],Matrix[4]],[]]
        #return [ [ [ "noun" ] * len(sentence) ] * sample_count, [] ]

    def best(self, sentence):
        w=list()       
        for i in range(0,len(sentence)):
            prob=list()
            c=self.words.count(sentence[i])
            if i==0:
                for j in range(0,len(self.pos)):
                    if c==0:
                        p=0.00000000000000000000034
                    else:      
                        n=list(self.sword[self.pos[j]])
                        t=n.count(sentence[i])
                        p=float(t)/float(c)
                    prob.append(p) 
                k=prob.index(max(prob))  
                w.append(self.pos[k])   
            
            else:
                t=sentence[i]
                if c==0 and (t[-2:]== "\'s"or t[-2:]=="er" or t[-3:]=="ice " or t[-3:]=="ness" or t[-4:]=="sion" or t[-4:]=="ance" or t[-4:]=="ment" or t[-4:]=="hood" or t[-3:] =="dom " or t[-2:] =="cy" or t[-3:]=="ist" or t[-3:]=="ity" or t[-4:]=="ship"):
                    w.append(self.pos[5])    
                elif c==0 and (t[-3:]=="ful" or t[-4:] =="eous" or t[-1:]=="y" or t[-3:]=="ish" or t[-3:]== "ble" or t[-3:]=="ial" or t[-3:]=="ent" or t[-3:]=="less" or t[-2:]=="ng" or t[-2:]=="ly" or t[-3:]=="ive" or t[-2:]=="ic"):
                    w.append(self.pos[0])    
                elif c==0 and (t[-2:]=="ed" or t[-3:]=="ing"):
                    w.append(self.pos[9]) 
                    
                elif c==0:
                    w.append(self.pos[8])  
                   

                elif c!=0:
                    temp=w[i-1]
                    for j in range(0,len(self.pos)):
                        n=list(self.sword[self.pos[j]])
                        t=n.count(sentence[i])
                        p=float(t)/float(len(n))
                        x=self.rpos[temp+"-"+self.pos[j]]
                        prob.append(float(p*x)) 
                    k=prob.index(max(prob))  
                    w.append(self.pos[k])   
  
        return [ [w], [] ]
        #return [ [ [ "noun" ] * len(sentence)], [] ]

    def max_marginal(self, sentence):
        Matrix = [0 for x in range(len(sentence))]
        Mat = [0 for x in range(len(sentence))] 
        for i in range(0,len(sentence)):
            p=self.pos[random.randint(0,11)]
            h=dict()
            for n in range(0,len(self.pos)):
                h[self.pos[n]]=0  
            c=self.words.count(sentence[i])
            for j in range(0,100):
                t=sentence[i]
                if c==0 and (t[-2:]== "\'s"or t[-2:]=="er" or t[-3:]=="ice " or t[-3:]=="ness" or t[-4:]=="sion" or t[-4:]=="ance" or t[-4:]=="ment" or t[-4:]=="hood" or t[-3:] =="dom " or t[-2:] =="cy" or t[-3:]=="ist" or t[-3:]=="ity" or t[-4:]=="ship"):
                    h[self.pos[5]]+=1
                    Matrix[i]=max(h, key=h.get) 
                    Mat[i]=float(h[max(h,key=lambda s:h[s])] )/float(100)
                elif c==0 and (t[-3:]=="ful" or t[-4:] =="eous" or t[-1:]=="y" or t[-3:]=="ish" or t[-3:]== "ble" or t[-3:]=="ial" or t[-3:]=="ent" or t[-3:]=="less" or t[-2:]=="ng" or t[-2:]=="ly" or t[-3:]=="ive" or t[-2:]=="ic" or t[-5:]=="-like"):
                    h[self.pos[0]]+=1
                    Matrix[i]=max(h, key=h.get) 
                    Mat[i]=float(h[max(h,key=lambda s:h[s])] )/float(100)    
                elif c==0 and (t[-2:]=="ed" or t[-3:]=="ing"):
                    h[self.pos[9]]+=1
                    Matrix[i]=max(h, key=h.get) 
                    Mat[i]=float(h[max(h,key=lambda s:h[s])] )/float(100)
                elif c==0 :
                    h[self.pos[8]]+=1
                    Matrix[i]=max(h, key=h.get) 
                    Mat[i]=float(h[max(h,key=lambda s:h[s])] )/float(100)
                            
                else:   
                    prob=list()
                    for k in range(0,12):
                        n=list(self.sword[self.pos[k]])
                        t=n.count(sentence[i])
                        if sentence[i] not in n:
                            temp=0
                        elif t!=0 :
                            if i==0:
                                temp=(float(t)/float(c))
                            else:
                                temp=(float(t)/float(len(n)))*float(self.rpos[Matrix[i-1]+"-"+self.pos[k]])
                        else:
                            temp=0.00000000000000000000034      
                        prob.append(temp)
                    l=random.random()
                    ind=[m for m,v in enumerate(prob) if v >l]  
                    if not ind :
                        ind=[m for m,v in enumerate(prob) if v <l]  
                    p=random.choice(ind)
                    ind=bisect.bisect(prob,l)             
                    if ind >11:
                        m=max(prob,key=float)
                        k1=prob.index(m)
                        p=k1
                    else:
                        p=ind
                    h[self.pos[p]]+=1
                Matrix[i]=max(h, key=h.get) 

                Mat[i]=float(h[max(h,key=lambda s:h[s])] )/float(100)
        return [[Matrix],[Mat,]]


    def viterbi(self, sentence):
        M= [[0 for x in range(len(self.pos))] for x in range(len(sentence))] 
        N= [[-1 for x in range(len(self.pos))] for x in range(len(sentence))] 
        c=self.words.count(sentence[0])
        w=list()
        for j in range(0,len(self.pos)):   
            #M[0][j]=float(self.initial[self.pos[j]])
            c=self.words.count(sentence[0])
            n=list(self.sword[self.pos[j]])
            t=n.count(sentence[0])
            if c==0:
                c=0.00000000000000000000034 
                t=0.00000000000000000000000043 
            x=float(self.initial[self.pos[j]]*t/c)
            w.append(x)
        for j in range(0,len(self.pos)):
            M[0][j]=self.initial[self.pos[j]]
        for i in range(1,len(sentence)):
            c=self.words.count(sentence[i])
            for j in range(0,len(self.pos)):
                tprob=list()
                for k in range(0,len(self.pos)):
                    n=list(self.sword[self.pos[k]])
                    t=n.count(sentence[i])
                    if c==0:
                        c=0.00000000000000000000034 
                        t=0.00000000000000000000000043    
                    d=float(self.rpos[self.pos[j]+"-"+self.pos[k]]*M[i-1][j]*t)
                    tp=float(d)/float(c)
                    tprob.append(tp)
                M[i][j]=max(tprob,key=float)
                N[i][j]=tprob.index(M[i][j])  
        res=list()  
        t=list(w)
        nx=max(t)
        d=t.index(nx)
        res.append(self.pos[d])      
        for i in range(1,len(sentence)):
            t=list(N[i])
            nx=max(t,key=float)
            res.append(self.pos[nx])
        return [[res], [] ]


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #    Most algorithms only return a single labeling per sentence, except for the
    #    mcmc sampler which is supposed to return 5.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for max_marginal() and is the marginal probabilities for each word.
    #
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        prob=1
        #print "len",len(self.words)
        for i in range(0,len(sentence)):
            t=list(self.sword[label[i]])
            a=len(t)
            b=t.count(sentence[i])
            an=float(b)/len(self.words)
            bd=self.words.count(sentence[i])
            

            #if nc==0 or lc ==0:
            if bd==0:
                prob=0.00000000001
                #prob*=0.000000001
            else:   
                prob*=(float(b)*float(an))/(float(a)*float(bd) )  
            if prob==0:
                prob=0.00000000001    
        temp=math.log(prob,10)  
        return temp
    def solve(self, algo, sentence):
        if algo == "Naive":
            return self.naive(sentence)
        elif algo == "Sampler":
            return self.mcmc(sentence, 5)
        elif algo == "Max marginal":
            return self.max_marginal(sentence)
        elif algo == "MAP":
            return self.viterbi(sentence)
        elif algo == "Best":
            return self.best(sentence)
        else:
            print "Unknown algo!"

