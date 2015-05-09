# -*-IBM model 1 -*-
from nltk.tokenize import RegexpTokenizer
from math import pow
import operator

def readfile(f):
    f1=open(f,"r")
    english_lines={}
    hindi_lines={}
    i=0
    for line in f1:
        #print i
        line_read=line.rstrip("\n")
        lines=line_read.split("###")
        english_line=lines[0]
        hindi_line=lines[1]
        #print hindi_line
        english_lines[i]=english_line
        hindi_lines[i]=hindi_line
        i=i+1
    return english_lines,hindi_lines
            #find length of english words
    
        
            
#remove sepcial characters from text
def remove_special_characters(text):
	tokenizer = RegexpTokenizer(r'\w+')
        list=tokenizer.tokenize(text)
	print " ".join(list)
	#print " ".join(list)
        return " ".join(list)

#read file and return the lines
def readfile1(filename):
	dictval = {}
	linenumber=0
        with open(filename,"r") as text:
               for line in text:
#			print "line",line
			dictval[linenumber]=line
			linenumber=linenumber+1
	#print dictval
        return dictval
#read file and preprocess the text
def preprocess(filename):
	lines = readfile(filename)
        processed_lines={}
        for line in lines:
		#processed_line=remove_special_characters(line)
                #processed_lines.append(processed_line)
		processed_lines.append(line)
        return processed_lines

#calculating translation probabilities for each word english-foreign language word pair
def translation_probabilites_for_all_word_pairs(E,F):
    E_wordlist={}
    F_wordlist={}
    tr={}
    eng_words={}
    foreign_words={}
    count={}
    total={}
    
    for k,v in E.items():
        E_wordlist[k]=v.split()
    print "hello"
    
    for k,v in F.items():
        F_wordlist[k]=v.split()
    for i in  range(len(E_wordlist)):
        for englishword in E_wordlist[i]:
            if englishword not in eng_words:
                eng_words[englishword]=0
    #print "english done"
    
    for i in range(len(F_wordlist)):
            for foreignword in F_wordlist[i]:
                if foreignword not in foreign_words:
                    foreign_words[foreignword]=0
                    #print i
    #print "hindi done"
    #print "eng",len(eng_words)
    #print "hindi",len(foreign_words)
    k=1
    tr={}
    for i in range(len(E)):
         #print i
         for e in E_wordlist[i]:
             if e not in tr.keys():
                 tr[e]={}
             for f in F_wordlist[i]:
                 if f not in tr[e].keys():
                     tr[e][f]=1/float(len(eng_words))

    for i in range(len(E)):
         print i
         for e in E_wordlist[i]:
             if e not in tr.keys():
                 tr[e]={}
             for f in F_wordlist[i]:
                 if f not in tr[e].keys():
                     tr[e][f]=1/float(len(eng_words))
                            
    
                 
    #print tr
            
            
    
    print "iteration started now..."
    #no of iterations is 5
    for j in range(5):
        print "iteration="+str(j)
                
        for e in tr.keys():
            count[e]={}
            for f in tr[e].keys():
                count[e][f]=0
                total[f]=0
        
        s_total={}
        j=j+1
        for i in  range(len(E_wordlist)):
            for e in E_wordlist[i]:
                s_total[e]=0
                for f in F_wordlist[i]:
                    s_total[e]=s_total[e]+tr[e][f]
                    
            for e in E_wordlist[i]:
                for f in F_wordlist[i]:
                    if not s_total[e]==0 :
                        count[e][f]=count[e][f]+(tr[e][f]/s_total[e])
                        total[f]=total[f]+(tr[e][f]/s_total[e])
                        
        file1=open("tr_prob","w")
	m=0        
#        for f in foreign_words.keys():
#	    #print m
#	    m=m+1
#            for e in eng_words.keys():
#                if not total[f]==0 :
#                    tr[e][f]=count[e][f]/total[f]
#                    if(tr[e][f]>0.7):
#                        file1.write("\n"+f)
#                        file1.write("->"+e+str(tr[e][f])+";")

        for e in tr.keys():
	    #print m
	    m=m+1
            for f in tr[e].keys():
                if not total[f]==0 :
                    tr[e][f]=count[e][f]/total[f]
                    if(tr[e][f]>0.7):
                        file1.write("\n"+f)
                        file1.write("->"+e+str(tr[e][f])+";")
        file1.close()           
    print "done"
    return tr      
                        
       
def translation_probability_for_a_sentence_pair(E,F,tr):
	p=0
	trp=0
	for e in E:
		for f in F:
			trp=trp+tr[e][f]
	p=trp/(pow(len(E),len(F)))
	return p


def translation_probability_for_all_sentence_pairs(E,F,tr):
	sentence_probab=[[0 for col in range(2)] for row in range(len(E))]
	E_wordlist={}
	F_wordlist={}
	for k,v in E.items():
		 E_wordlist[k]=v.split()
	#print E_wordlist
	#F_wordlist = [line.split() for line in F]
	for k,v in F.items():
		 #print v
		 F_wordlist[k]=v.split()
	
	for k in range(len(E)):
		sentence_probab[k][0]=k
		sentence_probab[k][1]=(translation_probability_for_a_sentence_pair(E_wordlist[k],F_wordlist[k],tr))
	return sentence_probab


def reverse_sort_2d_array(sentence_probab):
	return sorted(sentence_probab, key=operator.itemgetter(1), reverse=True)

def save_output(p,english_lines,foreign_lines):
	fo = open("output.txt", "w")
	# output for top 500 probabilities
	for i in range(499):
		if len(p) >= i:
			fo.write(str(p[i][1])+' : '+english_lines[p[i][0]]+' ; '+str(foreign_lines[p[i][0]])+'\n')
	fo.close()
	print 'The program has been executed successfully.You may check the ouput.txt file'



#Execution begins from below---------
#sys.setdefaultencoding("utf8")
english_lines,foreign_lines=readfile('parallel_corpus')
print "lines read"
tr=translation_probabilites_for_all_word_pairs(english_lines,foreign_lines)
#sentence_probabilties=translation_probability_for_all_sentence_pairs(english_lines,foreign_lines,tr)
#sorted_sentence_probabilties=reverse_sort_2d_array(sentence_probabilties)
#save_output(sorted_sentence_probabilties,english_lines,foreign_lines)



            
                    
            
            
    
