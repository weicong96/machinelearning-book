def readfile(filename):
    lines = [line for line in file(filename)]
    
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')

        rownames.append(p[0])

        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data
from math import sqrt
def pearson(v1,v2):
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1Sq = sum([pow(v,2) for v in v1])
    sum2Sq = sum([pow(v,3) for v in v2])

    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2)/len(v1)) * (sum2Sq - pow(sum2, 2)/len(v2)))
    if den == 0: return 0

    return 1.0-num / den
def printclust(clust,labels=None,n=0):
     # indent to make a hierarchy layout
     for i in range(n): print ' ',
     if clust.id<0:
         # negative id means that this is branch
         print '-'
     else:
         # positive id means that this is an endpoint
         if labels==None: print clust.id
         else: print labels[clust.id]
     # now print the right and left branches
     if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
     if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)
class bicluster:
  def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
    self.left=left
    self.right=right
    self.vec=vec
    self.id=id
    self.distance=distance
from PIL import Image,ImageDraw
def getheight(clust):
    if clust.left == None and clust.right==None: return 1

    return getheight(clust.left)+getheight(clust.right)
def getdepth(clust):
    if clust.left == None and clust.right==None: return 0

    return max(getdepth(clust.left), getdepth(clust.right))+ clust.distance
def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
    h = getheight(clust)*20
    w = 1200
    depth = getdepth(clust)

    scaling = float(w-150)/depth

    img = Image.new('RGB',(w,h),(255,255,255))
    draw = ImageDraw.Draw(img)

    draw.line((0,h/2,10,h/2), fill=(255,0,0))

    
def hcluster(rows,distance=pearson):
  distances={}
  currentclustid=-1

  # Clusters are initially just the rows, transform to actual entities
  clust=[bicluster(rows[i],id=i) for i in range(len(rows))]

  #In case length is not 1
  while len(clust)>1:
    lowestpair=(0,1)
    #Get distance of first two items as default closest
    closest=distance(clust[0].vec,clust[1].vec)
   
    # loop through every pair looking for the smallest distance
    for i in range(len(clust)):
      #Only look forward, don't look backward because distance difference is same no matter direction
      for j in range(i+1,len(clust)):
        # distances is the cache of distance calculations
        if (clust[i].id,clust[j].id) not in distances: 
          distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)

        d=distances[(clust[i].id,clust[j].id)]

        if d<closest:
          closest=d
          lowestpair=(i,j)

    # calculate the average of the two clusters
    mergevec=[
    (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 
    for i in range(len(clust[0].vec))]

    # create the new cluster
    newcluster=bicluster(mergevec,left=clust[lowestpair[0]],
                         right=clust[lowestpair[1]],
                         distance=closest,id=currentclustid)

    # cluster ids that weren't in the original set are negative
    currentclustid-=1
    del clust[lowestpair[1]]
    del clust[lowestpair[0]]
    clust.append(newcluster)

  return clust[0]

