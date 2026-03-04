import re

def parse_query(query):

    q = query.lower()

    data = {}

    # bedrooms
    bhk = re.search(r'(\d+)\s*(bhk|bedroom)', q)
    if bhk:
        data["bedrooms"] = int(bhk.group(1))

    # price crore
    crore = re.search(r'(\d+)\s*crore', q)
    if crore:
        data["max_price"] = int(crore.group(1)) * 10000000

    # price lakh
    lakh = re.search(r'(\d+)\s*lakh', q)
    if lakh:
        data["max_price"] = int(lakh.group(1)) * 100000

    # location
    location = re.search(r'in\s+([a-zA-Z ]+)', q)
    if location:
        data["location"] = location.group(1).strip()

    # parking
    if "parking" in q:
        data["parking"] = True

    # cheap / luxury
    if "cheap" in q:
        data["sort"] = "cheap"

    if "luxury" in q:
        data["sort"] = "luxury"

    # land area
    land = re.search(r'(\d+)\s*(sqft|square)', q)
    if land:
        data["land"] = int(land.group(1))

    data["keywords"] = q.split()

    return data