document.addEventListener("DOMContentLoaded", function () {
    displaySearchResults();
})

function displaySearchResults() {
    const resultsContainer = document.getElementById('search-results');
    const results = JSON.parse(resultsContainer.dataset.results);

    console.log(results);

    if (results.length > 0) {
        results.forEach(result => {
            // Get result container
            const container = document.getElementById(`title-${result.id}`);
            // Update poster
            if (result.poster_path) {
                container.style.backgroundImage = `url(https://image.tmdb.org/t/p/w200${result.poster_path})`;
            }
            else {
                console.log(result.poster_path);
                console.log(defaultPoster);
                container.style.backgroundImage = `url(${defaultPoster})`; // defaultPoster is passed in search.html
            }
        });
    }
    // else is already handled in html via jinja2
}