import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

def recommend_movies(data, movie_title):
    # Ensure the movie title is case-insensitive by converting all to lowercase
    data['title'] = data['title'].str.lower()
    movie_title = movie_title.lower()
    
    # Check if the movie is in the dataset
    if movie_title not in data['title'].values:
        return f"Movie titled '{movie_title}' not found in the dataset."
    
    # Get the genres of the movie provided by the user
    user_movie_genres = data[data['title'] == movie_title]['genre'].values[0]
    if pd.isna(user_movie_genres):
        return "The movie has no genre listed, can't recommend similar movies."
    
    user_movie_genres = user_movie_genres.split(',')
    
    # Filter the dataset to find movies with the same genre
    recommendations = data[data['genre'].apply(lambda x: any(genre.strip() in (x or '').split(',') for genre in user_movie_genres) if isinstance(x, str) else False)]
    
    # Sort the recommendations by popularity and avoid recommending the same movie
    recommendations = recommendations[recommendations['title'] != movie_title].sort_values(by='popularity', ascending=False)
    
    # Return the top 5 recommendations
    return recommendations[['title', 'genre', 'popularity']].head(5)

def main():
    # Load the movie dataset
    data = load_data("dataset.csv")
    
    # Ask user for a movie title
    movie_title = input("Enter a movie title to get recommendations: ")
    
    # Get recommendations
    result = recommend_movies(data, movie_title)
    
    if isinstance(result, str):
        print(result)
    else:
        print("Recommended Movies:")
        print(result)

if __name__ == "__main__":
    main()
