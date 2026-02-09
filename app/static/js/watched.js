document.addEventListener('DOMContentLoaded', function() {
    initTitleGridPage({
        gridId: 'titleGrid',
        filterBarSelector: '.title-filter-bar',
        moviesUrl: watchedMoviesUrl,
        seriesUrl: watchedSeriesUrl,
        similarUrl: similarTitlesUrl,
        recommendationsUrl: recommendationsUrl,
        titleBaseUrl: titleBaseUrl,
        defaultPosterUrl: defaultPosterUrl,
        cardClass: 'title-card',
        errorMessage: 'Failed to load your watched titles. Please try again.'
    });
});
