import xml.etree.ElementTree as ET

def parse_queries(query_file):
    """Parse queries from the XML file and return a dictionary."""
    tree = ET.parse(query_file)
    root = tree.getroot()
    
    queries = {}
    for i, top in enumerate(root.findall("top"), start=1):
        if i > 225:
            break
        query_id = i
        query_text = top.find("title").text.strip()
        queries[query_id] = query_text

    return queries
