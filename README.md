# hadoop
MapReduce jobs using Python mrjob library and AWS

Installation and guides can be found here : https://github.com/Yelp/mrjob. You should be able to do a conda install for anaconda distro.

test1 and test2 are simple get started scripts provided by mrjob repository. Pairs_Test is used to calculate conditional probabilities of bigrams and PageRank is an attempt at running a simplified page rank algorithm.

mrjob_running_instructions outlines some of the useful command line arguments to use in order to execute the MR jobs locally as well as on AWS. For the latter, a .conf file needs to be referenced in order to hook up to your respective AWS account. NOTE: when specifying an output folder in S3, make sure the folder isn't actually created. The framework should automatically create the folder when the MR jobs is exeuted via EMR.
