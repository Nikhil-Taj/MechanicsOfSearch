from whoosh.index import open_dir
from whoosh.qparser import QueryParser

# Open the index directory where Whoosh index is stored
ix = open_dir("index")

# Create a searcher object to query the index
with ix.searcher() as searcher:
    query = QueryParser("description", ix.schema).parse("car1")  # Search for 'car' in the image descriptions
    results = searcher.search(query)

    # Display the found results (image URL and description)
    if results:
        for result in results:
            print(f"Found image: {result['url']} - Description: {result['description']}")
    else:
        print("No results found for the query.")
