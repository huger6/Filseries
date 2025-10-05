document.addEventListener("DOMContentLoaded", function () {
    displayTitleInfo();
})

function displayTitleInfo() {
    //Padding adjustment
    const content = document.querySelector(".content");
    content.style.padding = "0px";

    const container = document.getElementById("title-info");
    const results = JSON.parse(container.dataset.results);

    if (results.length  > 0) {
        let result = results[0];

        if (!result.tconst || !result.primaryTitle) {
            container.innerHTML = `<p>Oops, the title does not exist!</p>`;
            return;
        }
        
        if (result.startYear === "\\N") {
            result.startYear = "n/a";
        }

        if (result.endYear === "\\N") {
            years = result.startYear;
        }
        else {
            years = `${result.startYear} - ${result.endYear}`;
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

        if (result.overview === null) {
            result.overview = "n/a";
        }

        if (result.backdrop_path) {
            container.style.setProperty("--bg-image", `url(https://image.tmdb.org/t/p/w500/${result.backdrop_path})`);
        }
        else {
            container.style.setProperty("--bg-image", `url(/static/img/background.jpeg)`);
            container.style.setProperty("--bg-size", `110%`);
        }

        const poster = document.createElement("img");
        poster.classList.add("poster");
        if (result.poster_path) {
            poster.src = `https://image.tmdb.org/t/p/w500/${result.poster_path}`;
        }
        else {
            poster.src = `/static/img/defaultPoster.svg`;
        }
        poster.alt = `${result.primaryTitle} Poster`;

        genres = styleGenres(result.genres);
        
        const info = document.createElement("div");
        info.classList.add("title-text");
        info.innerHTML = `
            <div id="info-primaryTitle">${result.primaryTitle}</div>
            <div id="info-row-details">
                <div id="info-years">${years}</div>
                <div id="info-runtime">
                    <i class="fa fa-clock-o" aria-hidden="true"></i>  ${convertMinutesToHourSchema(result.runtimeMinutes)}
                </div>
                <div id="info-rating">
                    <i class="fa fa-star" aria-hidden="true"></i>  ${result.averageRating}
                </div>
            </div>
            <div id="info-genres">
                ${genres}
            </div>
            <div id="info-overview">${result.overview}</div>
            `

        container.appendChild(poster);
        styleGenres(result.genres);
        container.appendChild(info);
    } 
    else {
        container.innerHTML = `<p>Oops, the title does not exist!</p>`;
    }
}

function convertMinutesToHourSchema(minutes) {
    if (!minutes) return "n/a";

    let hours = Math.floor(minutes / 60);
    let min = minutes % 60;

    if (!hours && !min) {
        return "0min";
    }

    if (!hours) return `${min}min`;
    if (!min) return `${hours}h`;

    return `${hours}h ${min}min`
}

function styleGenres(genres) {
    if (!genres || typeof genres !== "string") {
        return "";
    }

    const genresArray = genres.split(",").map(g => g.trim());

    // Creates an HTML string
    const genresHTML = genresArray.map(genre => `<div class="genre">${genre}</div>`).join("");

    console.log(genresHTML);
    return genresHTML;  
}