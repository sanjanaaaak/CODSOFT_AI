import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# Sample movie dataset
movies_data = {
    "MovieID": [1, 2, 3, 4, 5],
    "Title": [
        "The Matrix",
        "Inception",
        "Interstellar",
        "The Dark Knight",
        "The Avengers"
    ],
    "Genre": [
        "Action Sci-Fi",
        "Sci-Fi Thriller",
        "Sci-Fi Drama",
        "Action Thriller",
        "Action Superhero"
    ]
}

# Load dataset into a DataFrame
movies_df = pd.DataFrame(movies_data)

# Step 1: Convert Genres into TF-IDF feature vectors
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(movies_df["Genre"])

# Step 2: Compute similarity using Cosine Similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Step 3: Recommendation function with enhanced search
def recommend_movies(movie_title, movies_df, cosine_sim):
    # Check if the movie is in the dataset (case-insensitive)
    close_matches = get_close_matches(movie_title, movies_df["Title"], n=1, cutoff=0.5)
    
    if not close_matches:
        return f"No similar movies found for '{movie_title}'. Please check the title and try again."
    
    # Use the closest match as the input movie title
    matched_title = close_matches[0]
    
    # Find the index of the matched movie title
    movie_idx = movies_df[movies_df["Title"] == matched_title].index[0]
    
    # Get similarity scores for the movie with all others
    similarity_scores = list(enumerate(cosine_sim[movie_idx]))

    # Sort the movies based on similarity scores in descending order
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top 5 similar movies (excluding the input movie)
    recommended_indices = [idx for idx, score in sorted_scores[1:6]]

    # Return the matched title and recommended movies
    recommendations = movies_df["Title"].iloc[recommended_indices].tolist()
    return matched_title, recommendations

# User interaction
print("Welcome to the Movie Recommendation System!")
user_movie = input("Enter a movie title: ")

# Get recommendations
result = recommend_movies(user_movie, movies_df, cosine_sim)

if isinstance(result, tuple):
    matched_title, recommendations = result
    print(f"\nMatched Movie: {matched_title}")
    print("Recommended Movies:")
    for movie in recommendations:
        print(f"- {movie}")
else:
    print(result)
