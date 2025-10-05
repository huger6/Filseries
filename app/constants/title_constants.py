MIN_TITLE_LENGTH = 2
MAX_TITLE_LENGTH = 101
MIN_LIM_PER_PAGE = 6
LIMIT_PER_PAGE = 36

TITLE_TYPE_DEFAULT = [
    "movie",      
    "tvSeries",   
    "tvMiniSeries",  
    "tvMovie",      
    #"documentary",   #Será mantido
]
#Filters must be ready to be called in query
SORT_BY_FILTERS = [
    "t.primaryTitle", #Default
    "t.startYear",
    "t.genres",
    "r.averageRating"
]
SORT_BY_ORDERS = [
    "ASC", #Default
    "DESC"
]
GENRES_ALLOWED = {
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Sci-Fi", "Thriller", "War", "Western"
}
#Documentary type was removed
GENRES_DEFAULT = {
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Drama",
    "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Sci-Fi", "Thriller", "War", "Western"
}