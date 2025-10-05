document.addEventListener("DOMContentLoaded", function () {
    displaySearchResults();
})

function displaySearchResults() {
    const container = document.getElementById("main-content");
    const results = JSON.parse(container.dataset.results);

    if (results.length  > 0) {
        const grid = document.createElement("div");
        grid.classList.add("grid");

        results.forEach(result => {
            //Data verification
            if (!result.tconst || !result.primaryTitle) {
                return;
            }
            
            if (result.startYear === "\\N") {
                result.startYear = "n/a";
            }
            
            if (result.averageRating === null) {
                result.averageRating = "n/a";
            }

            if (result.situation === null) {
                situationClass = "title-not-marked";
            }
            else if (result.situation === "watched") {
                situationClass = "title-watched";
            }
            else if (result.situation === "to_watch") {
                situationClass = "title-to-watch";
            }


            const div = document.createElement("a");
            div.id = result.tconst;
            div.setAttribute("href", `/title?id=${result.tconst}`);
            div.classList.add("search-result");

            //Image
            if (result.poster_path) {
                div.style.backgroundImage = `url(https://image.tmdb.org/t/p/w500/${result.poster_path})`;
            }
            else {
                div.style.backgroundImage = `url(/static/img/defaultPoster.svg)`;

            }
            div.style.backgroundPosition = "center";
            div.style.backgroundRepeat = "no-repeat";
            //Img-label
            div.setAttribute("aria-label", `${result.primaryTitle}`);

            div.innerHTML = `
                <div class="${situationClass}"></div>
                <span class="primaryTitle">${result.primaryTitle}</span>
                <div class="bottomRow">
                    <span class="startYear">${result.startYear}</span>
                    <span class="averageRating">
                        <i class="fa fa-star-o" aria-hidden="true"></i>
                        ${result.averageRating}
                    </span>
                </div>
            `;

            grid.appendChild(div);
        });
        container.appendChild(grid);
    } 
    else {
        container.innerHTML = `<p>Não há resultados para a pesquisa</p>`;
    }
}