import pandas as pd
import sqlite3 as lite
import numpy as np
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics

% matplotlib inline
# connect to database and load all the tables into separate dataframes
conn = lite.connect("../hotels.db")
rating = pd.read_sql("SELECT * FROM Rating;", conn)
hinfo = pd.read_sql("SELECT * FROM H_info;", conn) # contains averages for ratings
cities = pd.read_sql("select distinct(location) from H_info;", conn).values

# Unused tables
# weight = pd.read_sql("SELECT * FROM Aspect_weight;", conn)
# key = pd.read_sql("SELECT * FROM Key;", conn)

# Warning, vocab and review are heavy on memory
# vocab = pd.read_sql("SELECT * FROM Aspect_vocab;", conn)
# review = pd.read_sql("SELECT * FROM Review;", conn)
# conn.close()  

# connect to database and load all the tables into separate dataframes
aspects = ['value', 'room', 'location', 'cleanliness']

def avg_aspect_weight(hid, aspect):
    Weight_q = """select avg(%s) from Aspect_weight 
            where hotel_id = %d; """ % (aspect, hid)
    vec = pd.read_sql(Weight_q, conn).values[0][0]
    if vec:
        return vec
    else:
        return -1


def avg_rating(hid, aspects):
    O, V, R, L, C = aspects
    avgRating_q = """select %s, %s, %s, %s, %s from H_info 
            where hotel_id = %d; """ % (O, V, R, L, C, hid)
    vec = pd.read_sql(avgRating_q, conn).values[0][0]
    if vec:
        return vec
    return

def connect():
	key = pd.read_sql("SELECT * FROM Key;", conn)
	hinfo = pd.read_sql("SELECT * FROM Hotel_info;", conn)
	rating = pd.read_sql("SELECT * FROM Rating;", conn)
	weight = pd.read_sql("SELECT * FROM Aspect_weight;", conn)
	return key, hinfo, rating, weight

def get_hotel_info(city=None):
    if city:
        end = "WHERE Hotel_info.location = '%s';" % city
    else:
        end = ";"
    select = '''
    SELECT Hotel_info.hotel_id, Hotel_info.price, Hotel_info.location
    FROM Hotel_info 
    JOIN 
    (SELECT DISTINCT(hotel_id)
    FROM Key) as dKey
    ON dKey.hotel_id = Hotel_info.hotel_id
    '''
    hotelids = pd.read_sql(select + end, conn).values
    return hotelids

def avg_aspect(hid, aspect):
    Weight_q = """select avg(%s) from Aspect_weight 
            where hotel_id = %d; """ % (aspect, hid)
    vec = pd.read_sql(Weight_q, conn).values[0][0]
    if vec:
        return vec
    else:
        return -1

# two clear clusters in kmeans
cluster0, cluster1 = 'budget', 'extravagant'

def plot_two_hotel(Hinfo1, Hinfo2):
    len1 = int(len(Hinfo1))
    len2 = int(len(Hinfo2))
    x1, O1, V1, R1, L1, C1 = np.zeros(len1), np.zeros(len1), np.zeros(len1), np.zeros(len1), np.zeros(len1), np.zeros(len1)
    x2, O2, V2, R2, L2, C2 = np.zeros(len2), np.zeros(len2), np.zeros(len2), np.zeros(len2), np.zeros(len2), np.zeros(len2)
    for i in xrange(len1):
        hid, x1[i], loc, O1[i], V1[i], R1[i], L1[i], C1[i] = Hinfo1[i]
        
    for j in xrange(len2):
        hid, x2[j], loc, O2[j], V2[j], R2[j], L2[j], C2[j] = Hinfo2[j]
        
    x1mean, O1mean, V1mean, R1mean, L1mean, C1mean = np.mean(x1), np.mean(O1), np.mean(V1), np.mean(R1), np.mean(L1), np.mean(C1)
    x2mean, O2mean, V2mean, R2mean, L2mean, C2mean = np.mean(x2), np.mean(O2), np.mean(V2), np.mean(R2), np.mean(L2), np.mean(C2)
    
    x1med, O1med, V1med, R1med, L1med, C1med = np.median(x1), np.median(O1), np.median(V1), np.median(R1), np.median(L1), np.median(C1)
    x2med, O2med, V2med, R2med, L2med, C2med = np.median(x2), np.median(O2), np.median(V2), np.median(R2), np.median(L2), np.median(C2)
    
    
    label1 = "%s, hotel_count=%d" % (cluster0, len1)
    label2 = "%s, hotel_count=%d" % (cluster1, len2)
    labelsub = "median"
    
    # big overall plot
    fig = plt.figure(figsize=(20,4))
    # scatterplot of the ratings against price
    plt.scatter(x1, O1, color='red', alpha=0.2, label=label1) 
    plt.scatter(x2, O2, color='blue', alpha=0.2, label=label2) 
    # marker
    plt.scatter(x1med, O1med, color='cyan', marker='x', s=150, linewidths=5)  
    plt.scatter(x2med, O2med, color='yellow', marker='x', s=150, linewidths=5)
    plt.xlabel('Price', fontsize=16)
    plt.ylabel('Average Aspect:Overall', fontsize=16)
    
    
    maxO1, maxO2 = np.max(O1), np.max(O2)
    plt.ylim([np.min(O1), max(maxO1, maxO2) + 1])
    fig.tight_layout()
    plt.legend()    
    
    # Four subplots for Value, Room, Location, Cleanliness ratings for each location
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 7))
    ax1.scatter(x1, V1, color='red', alpha=0.2)
    ax1.scatter(x2, V2, color='blue', alpha=0.2)
    ax1.scatter(x1med, V1med, color='cyan', marker='x', s=150, linewidths=5, label=labelsub)
    ax1.scatter(x2med, V2med, color='yellow', marker='x', s=150, linewidths=5, label=labelsub)
    ax1.set_xlabel('Price', fontsize=16)
    ax1.set_ylabel('Average Aspect:Value', fontsize=16)
    maxV1, maxV2 = np.max(V1), np.max(V2)
    ax1.set_ylim([1., 5.5])
    
    ax2.scatter(x1, R1, color='red', alpha=0.2)
    ax2.scatter(x2, R2, color='blue', alpha=0.2)
    ax2.scatter(x1med, R1med, color='cyan', marker='x', s=150, linewidths=5)
    ax2.scatter(x2med, R2med, color='yellow', marker='x', s=150, linewidths=5)
    ax2.set_xlabel('Price', fontsize=16)
    ax2.set_ylabel('Average Aspect:Room', fontsize=16)
    maxR1, maxR2 = np.max(R1), np.max(R2)
    ax2.set_ylim([1., 5.5])

    ax3.scatter(x1, L1, color='red', alpha=0.2)
    ax3.scatter(x2, L2, color='blue', alpha=0.2)
    ax3.scatter(x1med, L1med, color='cyan', marker='x', s=150, linewidths=5)
    ax3.scatter(x2med, L2med, color='yellow', marker='x', s=150, linewidths=5)
    ax3.set_xlabel('Price', fontsize=16)
    ax3.set_ylabel('Average Aspect:Location ', fontsize=16)
    maxL1, maxL2 = np.max(L1), np.max(L2)
    ax3.set_ylim([1., 5.5])

    ax4.scatter(x1, C1, color='red', alpha=0.2)
    ax4.scatter(x2, C2, color='blue', alpha=0.2)
    ax4.scatter(x1med, C1med, color='cyan', marker='x', s=150, linewidths=5)
    ax4.scatter(x2med, C2med, color='yellow', marker='x', s=150, linewidths=5)
    ax4.set_xlabel('Price', fontsize=16)
    ax4.set_ylabel('Average Aspect:Cleanliness', fontsize=16)
    maxC1, maxC2 = np.max(C1), np.max(C2)
    ax4.set_ylim([1., 5.5])
    
    ax1.legend(loc='best')
    fig.tight_layout()
    price_diff = x2med - x1med
    ydiff = O2med - O1med, V2med - V1med, R2med - R1med, L2med - L1med, C2med - C1med
    print "Blue cluster minus red cluster median price difference: %.4f" % price_diff
    print "Median overall rating difference: %.4f" % ydiff[0]
    print "Median value rating difference: %.4f" % ydiff[1]
    print "Median room rating difference: %.4f" % ydiff[2]
    print "Median location rating difference: %.4f" % ydiff[3]
    print "Median cleanliness rating difference: %.4f" % ydiff[4]
    return [x1med,  O1med, V1med,  R1med, L1med,  C1med], [x2med, O2med,V2med,R2med, L2med,C2med]

plot_two_hotel(Hinfo1, Hinfo2)    
    
# aspect = 'location'
Hinfo_NOLA = get_hotel_info('New_Orleans_Louisiana')
Hinfo_SF = get_hotel_info('San_Francisco_California')
plot_two_aspect('value', Hinfo_SF, Hinfo_NOLA)

def get_avgdf(hinfo):
    df = pd.DataFrame()
    print hinfo.head()
    columns = ['price', 'avgO', 'avgV', 'avgR', 'avgL', 'avgC']
    df[['hotel_id', 'location']] = hinfo[['hotel_id', 'location']]
    # subtract off the mean then divide by the standard deviation to normalize each column
    for col in columns:
        df[col] = (hinfo[col] - hinfo[col].mean()) / hinfo[col].std()
    return df

df = get_avgdf(hinfo)
print df.head()

X = df[['price', 'avgO', 'avgV', 'avgR', 'avgL']].values
sim_euclidean = 1 / (1 + squareform(pdist(X, metric='euclidean')))
sim_cosine = 0.5 * squareform(pdist(X, metric='cosine'))
similarities = squareform(pdist(X, metric='cosine'))
print similarities[:5, :5]
# cities = pd.read_sql("select distinct(location) from Hotel_info;", conn).values
# aspect = 'location'
# city1 = 'New_Orleans_Louisiana'
# city2 = 'San_Francisco_California'
# Hinfo1 = get_hotel_info(city1)
# Hinfo2 = get_hotel_info(city2)
# plot_aspect(aspect, Hinfo1)
# plot_aspect(aspect, Hinfo2)

# hotelids = get_hotel_info(city=None)

# key, hinfo, rating, weight = connect()

# metric='cosine returns 0.5 * (1 - cos(x1, x2)) which ranges from [0,1]
# with 0 being "close" and 1 being "far"
sim = sim_cosine
k = 34
indices = range(len(X))
indices.remove(k)
row_k = sim[k, indices]
print row_k[:10]
# indices of the matrix X
idx = np.argsort(row_k)[-1:-11:-1]
idx = np.argsort(row_k)[:10]
print row_k[idx]
print "HOTEL NUMBER %d:" % k
print hinfo.ix[k]
print "TOP TEN SIMILAR HOTELS"
print hinfo.ix[idx]
print "SIMILARITY SCORES"
print sim[k, idx]