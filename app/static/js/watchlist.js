document.addEventListener('DOMContentLoaded', function() {
    initTitleGridPage({
        gridId: 'titleGrid',
        filterBarSelector: '.title-filter-bar',
        moviesUrl: watchlistMoviesUrl,
        seriesUrl: watchlistSeriesUrl,
        similarUrl: similarTitlesUrl,
        recommendationsUrl: recommendationsUrl,
        titleBaseUrl: titleBaseUrl,
        defaultPosterUrl: defaultPosterUrl,
        cardClass: 'title-card',
        errorMessage: 'Failed to load your watchlist. Please try again.'
    });
});
