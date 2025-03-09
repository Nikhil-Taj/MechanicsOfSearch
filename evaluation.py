import xml.etree.ElementTree as ET

def parse_queries(query_file):
    """
    Parse queries from the given XML file.
    Returns a dictionary mapping query IDs to query text.
    """
    tree = ET.parse(query_file)
    root = tree.getroot()
    
    queries = {}
    # Each query is in a <top> element
    for top in root.findall("top"):
        query_id = top.find("num").text.strip()
        query_text = top.find("title").text.strip()
        queries[query_id] = query_text
    return queries

if __name__ == "__main__":
    # Test the parser with the provided XML file path
    queries = parse_queries("data/cran.qry.xml")
    for qid, text in queries.items():
        print(f"Query {qid}: {text}")
