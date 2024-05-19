

from flask import Flask, request, jsonify
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)


reviews = pd.read_csv('/Users/thabochesane/Desktop/path2/reviews.csv')
x = pd.read_csv('/Users/thabochesane/Desktop/path2/x.csv', index_col=0)

# Precomputed cosine similarity matrix
cosine_sim = cosine_similarity(x)

def recommendBooks(userID):
    # Get the index of the user in the user-item matrix
    index = x.index.get_loc(userID)
    similar_books = list(enumerate(cosine_sim[index]))
    similar_books = sorted(similar_books, key=lambda x: x[1], reverse=True)[1:4]

    userData = []
    for n in similar_books:
        df = reviews[reviews['UserId'] == x.index[n[0]]].sort_values(by='Review', ascending=False)
        listOfUserBooks = list(reviews[reviews['UserId'] == userID]['BookTitle'])
        df = df[~df['BookTitle'].isin(listOfUserBooks)]
        df = df[df['Review'].isin([4.0, 5.0])]
        userData.extend(list(df.head()['BookTitle']))
        userData = list(set(userData))

    return userData

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    try:
        recommendations = recommendBooks(user_id)
        return jsonify({'recommended_books': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
