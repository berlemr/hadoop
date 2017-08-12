from mrjob.job import MRJob
from mrjob.step import MRStep

class PageRankSeed(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.initial_map,
                   reducer = self.initial_reducer)]

    def initial_map(self, _, line):
        t = line.split()
        yield (t[0],t[1])

    def initial_reducer(self, t, x):
        t_dict = dict()
        adj_list = []
        for i in x:
            adj_list.append(i)
        z = [[i, 1.0/len(adj_list)] for i in adj_list]
        t_dict = {'score' : 1, 'links' : z}
        yield t, t_dict

if __name__ == '__main__':
    PageRankSeed.run()