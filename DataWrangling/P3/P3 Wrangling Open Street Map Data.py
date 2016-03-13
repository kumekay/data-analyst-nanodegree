
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Make all necessary imports
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import itertools
from collections import defaultdict
from pymongo import MongoClient
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import os
import foursquare


# In[2]:

OSMFILE = 'everett.osm'
JSONFILE = 'everett.osm.json'
SAMPLE_OSMFILE = 'sample_everett.osm'
SAMPLE_JSONFILE = 'sample_everett.osm.json'
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


# ## Database connection

# In[3]:

client = MongoClient("mongodb://localhost:27017")
db = client.osm


# ## Data preparation for mongodb

# In[5]:

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node["created"] = {}
        node['type'] = element.tag
        ats = element.attrib 
        for k in ats:
            if problemchars.search(k):
                continue
            if k in CREATED:
                node["created"][k] = ats[k]
                continue
            if k in ['lat', 'lon']:
                if not node.get('pos'):
                    node['pos'] = [None] * 2
                if k == "lon":
                    node["pos"][1] = float(ats[k])
                else: 
                    node["pos"][0] = float(ats[k])
                continue
            for tag in element:
                if tag.tag == 'nd':
                    if not node.get('node_refs'):
                        node['node_refs'] = []
                    node["node_refs"].append(tag.attrib['ref'])
                    continue
                if tag.tag == 'tag':
                    tats = tag.attrib
                    lc = lower_colon.search(tats['k'])
                    if lc:
                        if not node.get('address'):
                            node['address'] = {}
                        addr = tats['k'].split(':')
                        if addr[0] == 'addr' and len(addr) == 2:
                            node["address"][addr[1]] = tats['v']
                        continue
                    else:
                        node[tats['k']] = tats['v']
                        continue
                node
            node[k] = ats[k]
        pprint.pprint(node)
        return node
    else:
        return None


# In[83]:

def process_map(file_in, file_out, pretty = False):
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


# In[84]:

get_ipython().run_cell_magic(u'capture', u'', u'data = process_map(OSMFILE, JSONFILE, False);')


# In[242]:

get_ipython().run_cell_magic(u'capture', u'', u'data = process_map(SAMPLE_OSMFILE, SAMPLE_JSONFILE, False);')


# In[6]:

def count_tags(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    tags = get_tags(root)
    return tags

def get_tags(root):
    tags = {}
    tags[root.tag] = 1
    for child in root:
        ctags = get_tags(child)
        tag = child.tag
        for ctag in ctags:
            if ctag in tags:
                tags[ctag] += ctags[ctag]
            else:
                tags[ctag] = ctags[ctag]
    return tags


# In[7]:

tags = count_tags('everett.osm')
pprint.pprint(tags)


# ## Insert JSON Data to Database

# In[88]:

# Remove old database
db.everett.drop()

# Load new data
with open(JSONFILE) as f:
    for line in f:
        data = json.loads(line)
        db.everett.insert_one(data)


# ## Statistics

# In[89]:

# Total number of records:
total_records = db.everett.find().count()  
total_records


# In[90]:

# Number of nodes:
db.everett.find({"type":"node"}).count()


# In[93]:

# Number of ways:
db.everett.find({"type":"way"}).count()


# In[96]:

# Number of unique users
total_users = len(db.everett.distinct("created.user"))
total_users 


# In[97]:

# Top 10 contributors
top_10 = db.everett.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
                                 {"$sort":{"count":-1}},
                                 {"$limit":10}])
top_10_sum = 0 # Contributions by to 10 users
for doc in top_10:
    top_10_sum += doc['count']
    print(doc) 


# In[98]:

# Top 10 percentage
float(top_10_sum)/total_records*100


# In[100]:

# Number of users with 1 contribution
only_contribution_users = db.everett.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
                                                 {"$group":{"_id":"$count", "num_users":{"$sum":1}}},
                                                 {"$sort":{"_id":1}},
                                                 {"$limit":1}]).next()['num_users']
only_contribution_users


# In[101]:

# percent of users with 1 contribution
100.0*only_contribution_users/total_users


# In[9]:

# Average contribution per user
for doc in db.everett.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
                                 {"$group":{"_id": None, "average":{"$avg":"$count"}}}]):
    print(doc)


# In[10]:

# Contribution distribution
h = []
for d in db.everett.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},{"$sort":{"count":-1}}]):
    h.append(d['count'])


# In[11]:

plt.xlabel('Contributions')
plt.ylabel('Probability')
plt.title(r'Histogram of user contributions')
plt.yscale('log', nonposy='clip')
plt.hist(h, bins=15, normed=True, facecolor='green', alpha=0.5)      #use this to draw histogram of your data
plt.show()   


# ## Problems in dataset
# ### Street names

# In[12]:

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected_street_types = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", 
            "Way"]
expected_modifiers = ["Highway", "North", "South", "West", "Northeast", "Northwest", "Southeast", "Southwest"]

mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road"
            }


# In[13]:

streets = db.everett.find( { "address.street": { "$regex": street_type_re } } )
streets.count()


# In[14]:

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street_types:
            street_types[street_type].add(street_name)
            
def update_name(name, mapping):
    st = street_type_re.search(name)
    if st:
        wrong = st.group(0)
        name = street_type_re.sub(mapping[wrong], name)
    return name


# In[15]:

street_types = defaultdict(set)
# Not expected names:
for node in streets:
    audit_street_type(street_types, node['address']['street'])
# for st_type, ways in st_types.iteritems():
#     for name in ways:
#         better_name = update_name(name, mapping)
#         print name, "=>", better_name


# In[ ]:




# ### Phones

# In[16]:

# Review phone numbers
phones = db.everett.find({"phone": { "$exists": True }})
for doc in phones:
    print doc['phone']


# In[26]:

# Fix phone numbers
def format_phone(phone):
    # Remove all not meaning symbols:     
    phone = phone.encode('ascii','ignore').translate(None, '-_ ()')
    
    # Add country code '+1'
    if len(phone) == 10:
        phone = '+1' + phone
    
    # Add '+' if bare country code
    if len(phone) == 11:
        phone = '+' + phone
    
    # Add spaces for readability
    if len(phone) == 12:
        phone = phone[0:2] + ' ' + phone[2:5] + ' ' + phone[5:8] + ' ' + phone[8:]
    
    return phone


# In[18]:

# Update phone numbers
phones = db.everett.find({"phone": { "$exists": True }})
for doc in phones:
    new_phone = format_phone(doc["phone"])
    db.everett.update_one({'_id': doc['_id']}, {"$set": { 'phone': new_phone}})
    


# ## Cuisines

# In[19]:

# Amenities with cusisine
amenities = db.everett.aggregate([{"$match": {"cuisine": { "$exists": True }}},
        {"$group":{"_id":"$amenity", "count":{"$sum":1}}},
                                 {"$sort":{"count":-1}}])
print '| Amenity type | Count |'
for doc in amenities:
    print "| " + str(doc['_id']) + " | " + str(doc['count']) + " |" 


# In[20]:

# All Amenities of these types
all_amenities = db.everett.aggregate([{"$match": {"amenity": { "$in": ['restaurant', 'fast_food', 'cafe', 'pub']}}},
        {"$group":{"_id":"$amenity", "count":{"$sum":1}}},
                                 {"$sort":{"count":-1}}])
print '| Amenity type | Count |'
for doc in all_amenities:
    print "| " + str(doc['_id']) + " | " + str(doc['count']) + " |" 


# In[21]:

cousines = db.everett.aggregate([{"$match": {"cuisine": { "$exists": True }}},
                                 {"$match": {"amenity": { "$in": ['restaurant', 'fast_food', 'cafe', 'pub']}}},
                                 {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
                                 {"$sort":{"count":-1}}])
for doc in cousines:
    print doc


# In[22]:

amenities = db.everett.aggregate([{"$match": {"cuisine": { "$exists": True }}},
        {"$group":{"_id":"$amenity", "count":{"$sum":1}}},
                                 {"$sort":{"count":-1}}])
for doc in amenities:
    print doc


# In[23]:

cuisine_suffix = [
    '_restaurant',
    '_food' 
] 


# In[24]:

#Fix cuisine
def format_cuisine(cuisines):
    if not isinstance(cuisines, list):
        cuisines = [cuisines]
    
    out_cuisines = []
    for cuisine in cuisines:
        # Lowercase     
        cuisine = cuisine.encode('ascii','ignore').lower()

        # Remove spaces
        cuisine = cuisine.translate(None, ' ')
        
        # Remove suffixes 
        for suffix in cuisine_suffix:
            cuisine = cuisine.replace(suffix, '')

        # Replace separators to coma
        cuisine = cuisine.replace(';', ',')

        cuisine = cuisine.split(',')
        
        for el in cuisine:
            out_cuisines.append(el)
        
    return out_cuisines


# In[25]:

# Update cuisines
cousines = db.everett.aggregate([{"$match": {"cuisine": { "$exists": True }}},
                                 {"$match": {"amenity": { "$in": ['restaurant', 'fast_food', 'cafe', 'pub']}}}])
for doc in cousines:
    new_cuisine = format_cuisine(doc["cuisine"])
    db.everett.update_one({'_id': doc['_id']}, {"$set": { 'cuisine': new_cuisine}})
    


# ## Additional ideas
# ### Foursquare amenity data

# In[27]:

fs_client = foursquare.Foursquare(client_id=os.environ.get('FOURSQUARE_CLIENT_ID'),
                               client_secret=os.environ.get('FOURSQURE_CLIENT_SECRET'))


# In[39]:

def fs_venue(elem):
    ll = '{},{}'.format(elem['pos'][0], elem['pos'][1]) 
    query = elem['name']
    venues = fs_client.venues.search(params={"ll": ll, "query": query}).get("venues")
    if len(venues)  > 0 :
        return venues[0]
    else:
        return None


# In[42]:

filters = [{"$match": {"phone": { "$exists": False }, "name": { "$exists": True }}}]
amenities = db.everett.aggregate(filters)
count = 0
fixed_count = 0
for doc in amenities:
    fs = fs_venue(doc)
    count += 1
    if fs:
        phone = fs["contact"].get("phone")
        if phone:
            new_phone = format_phone(phone)
            db.everett.update_one({'_id': doc['_id']}, {"$set": { 'phone': new_phone}})
            fixed_count += 1
            print new_phone
print count
print fixed_count

