########################
## Matthew Chimitt 
## mmc200005
## Assignment 3 Part II
########################

#imports 
import string
import urllib3
import re
import random
from tabulate import tabulate


## PREPROCESS METHOD
def preprocess(url):
  tweets = []

  ## read in the text file
  http = urllib3.PoolManager()
  response = http.request('GET', url)
    # Process each line
  for line in response.data.decode('utf-8').split('\n'):
    # do not include any empty lines
    if not line:
      continue
    line = line.strip()
    
    # getting rid of the ID and Timestamp sections leaving just the tweet
    line = line[50:]
    
    # make every word lowercase
    line = line.lower() 
    
    # removes any word that starts with @
    line = " ".join(filter(lambda x: x[0] != '@', line.split()))

    # Getting rid of links
    line = re.sub(r"http\S+", "", line)
    line = re.sub(r"https\S+", "", line)
    line = re.sub(r"www\S+", "", line)

    # remove hashtags (#)
    line = line.replace('#', '')
    
    # removing punctuation (not sure if this is needed?)
    # (allows for "potato" and "potato." to be 
    #   registered as using the same word)
    line = line.translate(str.maketrans('', '', string.punctuation))

    line = line.strip()

    # add to the tweets list
    tweets.append(line)

    # print(line)
  return tweets


# distance using jaccard distance
def distance(a, b):
  # perform set operations
  a = set(a.split())
  b = set(b.split())
  union = a.union(b)
  intersection = a.intersection(b)
  
  # get the distance
  # distance = (union - intersection) / ab_union or 1 - (intersection / union)
  distance = 1 - (len(intersection) / len(union))
  return distance



## K MEANS FUNCTION
def k_means(tweets, k):

  print("K-Means Cluster  -----  k = " + str(k))

  old = []
  # pick the initial centroids from the set of tweets
  # select k different tweets to be centers
  centroids = random.sample(tweets, k)
  print("\nInitial Centroids: {}".format(centroids))

  # instantiating the clusters list
  clusters = []
  for i in range(k):
    c = []
    clusters.append(c)

  # iterating while there is no convergence
  iter = 1
  while(converged(old, centroids) == False):
    print("\niter: " + str(iter))
    
    ## fixing the accumulation problem
    clusters = clear_clusters(k)

    # assign clusters
    for tweet in tweets:
      assign_cluster(clusters, centroids, tweet)
    
    # set the current centroids to be old
    old = centroids
    # update centroids
    centroids = update_centroids(clusters)
    
    iter = iter + 1
  
  sse = calc_sse(clusters, centroids)


  print_results(clusters, centroids, sse, k, iter)

  return clusters, centroids, sse  



## Fixes a problem that I had where the clusters would accumulate over iterations
def clear_clusters(k):
  new_clusters = []
  for i in range(k):
    c = []
    new_clusters.append(c)
  return new_clusters



## ASSIGN TWEETS TO CLUSTERS
def assign_cluster(clusters, centroids, tweet):
  # initially in the first cluster
  shortest_distance = distance(tweet, centroids[0])
  shortest_cluster = 0

  # loop through every centroid and determine which is closer to tweet
  for c in range(len(centroids)):
    current = distance(tweet, centroids[c])
    if(current < shortest_distance):
      shortest_distance = current
      shortest_cluster = c

  # append the tweet to the closest cluster
  clusters[shortest_cluster].append(tweet)

  # debugging
  # print("Cluster: " + str(shortest_cluster) + "   ---------   tweet: " + tweet)



## UPDATE CENTERS METHOD
def update_centroids(clusters):
  centroids = []

  # update the centroids by:
  #   the tweet within the cluster with the smallest distance between 
  #   all other tweets in the cluster is the new centroid

  # loop through the clusters
  for c in range(len(clusters)):
    
    # initial values
    min_distance_sum = -1
    cluster = clusters[c]
    new_center = cluster[0]
    
    # c refers to the cluster
    for current in clusters[c]:
      # current refers to the current tweet
      # get the distacne from the current tweet to every tweet in cluster
      distance = distance_to_every_other_tweet_in_cluster(current, clusters[c])

    # if distance is less than the min, or the min is still -1, update
    if(distance < min_distance_sum or min_distance_sum < 0):
      min_distance_sum = distance
      new_center = current
    

    # print("New center for cluster " + str(c) + ": " + new_center)  
    # print(min_distance_sum)

    # add the new centroid to the list
    centroids.append(new_center)

  print("Updated Centroids: {}".format(centroids))

  return centroids



# Calculates the distance from one tweet to every other in the cluster
def distance_to_every_other_tweet_in_cluster(tweet, cluster):
  distance_sum = 0
  # loop through every tweet in the cluster
  for t in cluster:
    # add the distance of the current tweet and the parameter tweet to the sum
    distance_sum += distance(tweet, t)
  # return the sum
  return distance_sum



## CALCULATE THE SSE
## take the sum of all the sums of the distances^2 between tweets in a cluster to the centroid of said cluster
def calc_sse(clusters, centroids):
  sse = 0
  # loop k times (loop through clusters) 
  for k in range(len(clusters)):
    for tweet in clusters[k]:
      sse += pow(distance(centroids[k], tweet), 2)
  return sse



## DETERMINES IF CONVERGED OR NOT
def converged(old, current):
  # if first iteration, there are no old centroids
  if(len(old) == 0):
    return False
  # if the old and the current centroids are the same, then convergence!
  elif(old == current):
    return True
  # otherwise no convergence
  else:
    return False
  


# Prints the results of a k means experiment
def print_results(clusters, centroids, sse, k, iters):
  # Printing the information from the output  
  print("\nResults for K-Means Cluster where k = " + str(k))
  print("Converged in " + str(iters) + " iterations.\n")

  ## COMMENTING THIS OUT BECAUSE IT JUST KINDA FILLS THE TERMINAL IN A UNREADABLE WAY
  ## Would normally print the clusters and the centroids
  #   for i in range(k):
  #     print("Cluster " + str(i+1) + ": {}".format(clusters[i]))
  #   for i in range(k):
  #     print("Centroid " + str(i+1) + ": " + centroids[i])
  size_of_clusters = get_size_of_cluster(clusters)
  print("\nSize of Clusters:")
  print(size_of_clusters)
  print("sse: " + str(sse))
  print("\n\n")



# formats the clusters for printing in the table
def get_size_of_cluster(clusters):
  # formats the clusters for the table
  # returns a string where each line has the cluster number followed by size
  sizes = []
  for cluster in clusters:
    sizes.append(len(cluster))
  ret = ""
  for i in range(len(clusters)):
    ret += "" + str(i+1) + ": " + str(sizes[i]) + " tweets\n"
  
  return ret



## PRINTS THE OUTPUT TABLE
def print_table(k_values, clusters_list, sse_list):
  # table of results
  print("\n\nTABLE OF RESULTS:\n")
  
  # column titles
  table = [["Value of k", "sse", "Size of each cluster"]]

  # for every k means trial, print it
  for i in range(len(k_values)):
    entry = [str(k_values[i]), str(sse_list[i]), get_size_of_cluster(clusters_list[i])]
    table.append(entry)
    # separator
    table.append(["----------------------", "----------------------", "----------------------"])
  # tabulate!
  print(tabulate(table, headers='firstrow'))



## MAIN METHOD!!!!
if __name__ == '__main__':
  url = "https://mchimitt.github.io/Health-Tweets/usnewshealth.txt"
  tweets = preprocess(url)

  # k values to test on
  k_values = [5, 10, 15, 20, 50]

  clusters_list = []
  centroids_list = []
  sse_list = []

  print("BEGINNING EXPERIMENTS:\n\n\n")

  # perform k-means on the five k values
  for k in k_values:
    clusters, centroids, sse = k_means(tweets, k)
    clusters_list.append(clusters)
    centroids_list.append(centroids)
    sse_list.append(sse)
  
  # print the table
  print_table(k_values, clusters_list, sse_list)
  
