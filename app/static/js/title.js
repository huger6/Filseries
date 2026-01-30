document.addEventListener("DOMContentLoaded", function () {
    // Remove padding from main
    document.querySelector("main").style.cssText += 'padding: 0px !important;';

    displayTitleInfo();
    setupUserActions();
});

function displayTitleInfo() {
    const container = document.getElementById("title-page");
    const result = JSON.parse(container.dataset.results || "{}");

    if (!result.id || !result.title) {
        return;
    }

    // Poster
    const poster = document.getElementById("title-poster");
    if (poster) {
        if (result.poster_path) {
            poster.style.backgroundImage = `url(https://image.tmdb.org/t/p/w500${result.poster_path})`;
        } else if (typeof defaultPoster !== 'undefined') {
            poster.style.backgroundImage = `url(${defaultPoster})`;
        }
    }

    // Backdrop
    const backdrop = document.getElementById("title-backdrop");
    if (backdrop) {
        if (result.backdrop_path) {
            backdrop.style.backgroundImage = `url(https://image.tmdb.org/t/p/original${result.backdrop_path})`;
        } else if (typeof defaultBackground !== 'undefined') {
            backdrop.style.backgroundImage = `url(${defaultBackground})`;
        }
    }
}

function setupUserActions() {
    // Add to watched
    document.querySelectorAll('.add-to-watched').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const id = btn.dataset.id;
            try {
                const response = await fetch(`/watchlist/add-watched/${id}`, { method: 'POST' });
                if (response.ok) {
                    btn.innerHTML = '<i class="bi bi-check-circle-fill"></i> Added!';
                    btn.disabled = true;
                    btn.classList.remove('primary');
                    btn.style.background = 'var(--greenColor)';
                    setTimeout(() => location.reload(), 1000);
                }
            } catch (error) {
                console.error('Error adding to watched:', error);
            }
        });
    });

    // Add to watchlist
    document.querySelectorAll('.add-to-watchlist').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const id = btn.dataset.id;
            try {
                const response = await fetch(`/watchlist/add/${id}`, { method: 'POST' });
                if (response.ok) {
                    btn.innerHTML = '<i class="bi bi-bookmark-fill"></i> Added!';
                    btn.disabled = true;
                    btn.style.borderColor = '#ffc107';
                    btn.style.color = '#ffc107';
                    setTimeout(() => location.reload(), 1000);
                }
            } catch (error) {
                console.error('Error adding to watchlist:', error);
            }
        });
    });

    // Remove from watched
    document.querySelectorAll('.remove-watched').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            if (confirm('Are you sure you want to remove this from your watched list?')) {
                try {
                    const response = await fetch(`/watchlist/remove-watched`, { method: 'POST' });
                    if (response.ok) {
                        location.reload();
                    }
                } catch (error) {
                    console.error('Error removing from watched:', error);
                }
            }
        });
    });

    // Remove from watchlist
    document.querySelectorAll('.remove-to-watch').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            if (confirm('Are you sure you want to remove this from your watchlist?')) {
                try {
                    const response = await fetch(`/watchlist/remove`, { method: 'POST' });
                    if (response.ok) {
                        location.reload();
                    }
                } catch (error) {
                    console.error('Error removing from watchlist:', error);
                }
            }
        });
    });
}