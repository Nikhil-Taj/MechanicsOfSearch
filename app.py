from flask import Flask, render_template, request
from image_search_indexer import SearchEngineIndexer

# Initialize Flask app FIRST
app = Flask(__name__)

# Then initialize your search indexer
indexer = SearchEngineIndexer("image_data.json")
indexer.build_index()  # Build the index at startup

# Now you can define routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    
    # Get matching URLs from indexer
    matched_urls = indexer.search(query)
    
    # Fetch full image data for these URLs
    results = []
    image_data = indexer.load_image_data()
    url_set = set(matched_urls)
    
    for image in image_data:
        if image['url'] in url_set:
            results.append(image)
            if len(results) == len(matched_urls):
                break
    
    print(f"Query: '{query}' returned {len(results)} results")
    return render_template('results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)