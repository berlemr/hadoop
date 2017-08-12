from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONProtocol

class PageRank(MRJob):

    INPUT_PROTOCOL = JSONProtocol 

    def steps(self):
        return [MRStep(
                mapper=self.map_task_main,
                reducer=self.reduce_task_main)
                ] * 3 #iterations

    def map_task_main(self, node_id, node):

        yield node_id, ('node', node)
        try:
            for link in node.get('links'):
                yield link[0], ('score', node['score'] * link[1])
        except:
            pass

    def reduce_task_main(self, node_id, node):

        node_dict = {}
        score = 0
        for p,val in node:
            if p == 'node':
                node_dict = val
            else:
                score = score + val
        damping = 0.85
        node_dict['score'] = (damping * score) + (1 - damping)
                
        yield node_id, node_dict

if __name__ == '__main__':
    PageRank.run()