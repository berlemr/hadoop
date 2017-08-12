# -*- coding: utf-8 -*-

from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import operator

WORD_RE = re.compile(r"[\w']+")

class Pairs(MRJob):

    last_word = ""
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                reducer=self.reducer),
            MRStep(reducer=self.reducer_getTop10_probs)
        ]        

    def mapper(self, _, line):
        words = WORD_RE.findall(line.lower())
        
        if len(words) > 0:
            if self.last_word: #handles line continuation, if previous line is empty assume new paragraph
                pair = self.last_word, words[0]
                yield (pair[0],("*", 1))
                yield (pair[0], (pair[1], 1))
            
            bigram = zip(words[:-1],words[1:])
            for pair in bigram:
                yield (pair[0],("*", 1))
                yield (pair[0], (pair[1], 1))    
            
            self.last_word = words[-1] #seed to combine with first word of next line to create bigram with         
        else:
            self.last_word = ""
        
    #
    def reducer(self, word, counts):
        counter = 0.0;
        word_dict = dict()
        
        if word == 'for':
            for c in counts:
                if c[0] == "*":
                    counter = counter + c[1]
                else :
                    if c[0] in word_dict.keys():
                        word_dict[c[0]] = word_dict[c[0]] + 1.0
                    else: 
                        word_dict[c[0]] = 1.0
                    
        yield (word_dict, counter)
    

    def reducer_getTop10_probs(self, word, count):      
        s = sum(count)
        prob_dict = dict()
        if len(word) > 0:
            for k in word.keys():
                prob_dict[k] = word[k] / s
            sorted_prob_dict = sorted(prob_dict.items(), key=operator.itemgetter(1))
            for prob in sorted_prob_dict[-10:]: #specify top n,in this case 10
                yield prob[0],prob[1]
                
                
if __name__ == '__main__':
    Pairs.run()