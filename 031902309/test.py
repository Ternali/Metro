from SSCode import ssc
from SSCSimilarityCompute import ssc_similarity

one = ssc.getSSCCode("汉")
two = ssc.getSSCCode("权")
ssc_similarity.computeSSCSimilarity(ssc1=one, ssc2=two)

