document.addEventListener("DOMContentLoaded", function () {
    // Remove padding from main
    document.querySelector("main").style.cssText += 'padding: 0px !important;';

    displayTitleInfo();
    setupUserActions();
    setupSeasonsDropdown();
});

function displayTitleInfo() {
    const container = document.getElementById("title-page");
    const result = JSON.parse(container.dataset.results || "{}");

    if (!result.id || !result.title) {
        return;
    }
    console.log(result);

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

/**
 * Check if user is authenticated before performing an action.
 * If not authenticated, redirects to login page.
 * @returns {boolean} - True if authenticated, false otherwise
 */
function requireAuth() {
    if (typeof isAuthenticated !== 'undefined' && isAuthenticated === "false") {
        // Redirect to login with current path as next parameter (relative path only)
        const currentPath = window.location.pathname;
        window.location.href = `${loginUrl}?next=${encodeURIComponent(currentPath)}`;
        return false;
    }
    return true;
}

function setupSeasonsDropdown() {
    const seasonsSection = document.getElementById("seasons-section");
    const seasonsHeader = document.getElementById("seasons-header");
    const seasonsDropdown = document.getElementById("seasons-dropdown");
    
    if (!seasonsSection || !seasonsHeader) return;
    
    // Toggle dropdown on header click
    seasonsHeader.addEventListener('click', () => {
        seasonsSection.classList.toggle('open');
    });
    
    // Handle "Add to Watched" link click - auto-open dropdown (for TV series)
    document.querySelectorAll('.toggle-watched-link').forEach(link => {
        link.addEventListener('click', (e) => {
            const isWatched = link.dataset.isWatched === 'true';
            
            // Only open dropdown if adding to watched (not removing)
            if (!isWatched) {
                // Small delay to allow scroll, then open dropdown
                setTimeout(() => {
                    if (!seasonsSection.classList.contains('open')) {
                        seasonsSection.classList.add('open');
                    }
                }, 100);
            }
        });
    });
    
    // Handle season selection
    document.querySelectorAll('.season-select-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            // Check if user is authenticated
            if (!requireAuth()) return;
            
            const seasonNumber = btn.dataset.season;
            const seriesId = btn.dataset.seriesId;
            const watchedLink = document.querySelector('.toggle-watched-link');
            const watchlistBtn = document.querySelector('.toggle-watchlist');
            
            try {
                const response = await fetch(tvProgressUpdateLastSeasonUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        series_id: seriesId,
                        season_number: parseInt(seasonNumber)
                    })
                });
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    const selectedSeasonNum = parseInt(seasonNumber);
                    
                    // Update all season items based on their season number
                    document.querySelectorAll('.season-item').forEach(item => {
                        const itemSeasonNum = parseInt(item.dataset.season);
                        const itemBtn = item.querySelector('.season-select-btn');
                        
                        if (itemSeasonNum < selectedSeasonNum) {
                            // Seasons before the selected one - mark as watched
                            item.classList.add('selected', 'watched-previous');
                            item.classList.remove('selected-current');
                            if (itemBtn) {
                                itemBtn.classList.add('selected');
                                itemBtn.innerHTML = '<i class="bi bi-check-circle-fill"></i> Watched';
                            }
                        } else if (itemSeasonNum === selectedSeasonNum) {
                            // The selected season - mark as current selection
                            item.classList.add('selected', 'selected-current');
                            item.classList.remove('watched-previous');
                            if (itemBtn) {
                                itemBtn.classList.add('selected');
                                itemBtn.innerHTML = '<i class="bi bi-check-circle-fill"></i> Last Watched';
                            }
                        } else {
                            // Seasons after the selected one - mark as not watched
                            item.classList.remove('selected', 'watched-previous', 'selected-current');
                            if (itemBtn) {
                                itemBtn.classList.remove('selected');
                                itemBtn.innerHTML = '<i class="bi bi-check-circle"></i> Select as Last Seen';
                            }
                        }
                    });
                    
                    // Update the watched link to show progress status
                    if (watchedLink) {
                        const totalSeasons = parseInt(watchedLink.dataset.totalSeasons) || 1;
                        
                        watchedLink.dataset.isWatched = 'true';
                        watchedLink.dataset.lastSeasonSeen = selectedSeasonNum.toString();
                        watchedLink.classList.remove('outlined');
                        watchedLink.classList.add('filled', 'active');
                        
                        // Check if all seasons are watched
                        if (selectedSeasonNum >= totalSeasons) {
                            // All seasons watched
                            watchedLink.innerHTML = '<i class="bi bi-check-circle-fill"></i><span class="btn-text-main">Watched</span>';
                        } else {
                            // Still in progress
                            watchedLink.innerHTML = `<i class="bi bi-check-circle-fill"></i><div style="padding-left: 8px;"><span class="btn-text-main">In Progress</span><span class="btn-text-sub">${selectedSeasonNum}/${totalSeasons} seasons</span></div>`;
                        }
                    }
                    
                    // Hide watchlist button with animation
                    if (watchlistBtn && !watchlistBtn.classList.contains('hidden')) {
                        watchlistBtn.classList.add('fade-out');
                        setTimeout(() => {
                            watchlistBtn.classList.add('hidden');
                            watchlistBtn.classList.remove('fade-out');
                            // Reset watchlist state when hidden
                            watchlistBtn.dataset.inWatchlist = 'false';
                            watchlistBtn.classList.remove('filled', 'active');
                            watchlistBtn.classList.add('outlined');
                            watchlistBtn.innerHTML = '<i class="bi bi-bookmark-plus"></i><span>Add to Watchlist</span>';
                        }, 300);
                    }
                    
                    // Show success feedback
                    showNotification(`Season ${seasonNumber} marked as last watched!`, 'success');
                } else {
                    showNotification(data.message || 'Failed to update season', 'error');
                }
            } catch (error) {
                console.error('Error updating last season seen:', error);
                showNotification('Error updating season. Please try again.', 'error');
            }
        });
    });
}

function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.title-notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = `title-notification ${type}`;
    notification.innerHTML = `
        <i class="bi bi-${type === 'success' ? 'check-circle-fill' : type === 'error' ? 'x-circle-fill' : 'info-circle-fill'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        padding: 15px 25px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 500;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        ${type === 'success' ? 'background: var(--greenColor); color: white;' : ''}
        ${type === 'error' ? 'background: var(--redColor); color: white;' : ''}
        ${type === 'info' ? 'background: var(--accentColor); color: var(--primaryColor);' : ''}
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function setupUserActions() {
    // Get title data from the page
    const container = document.getElementById("title-page");
    const result = JSON.parse(container.dataset.results || "{}");
    const mediaType = result.media_type; // "movie" or "tv"
    const titleId = result.id;

    // Toggle Watched Button (for movies)
    document.querySelectorAll('.toggle-watched').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            
            // Check if user is authenticated
            if (!requireAuth()) return;
            
            const id = btn.dataset.id || titleId;
            const isWatched = btn.dataset.isWatched === 'true';
            const watchlistBtn = document.querySelector('.toggle-watchlist');
            
            // Determine the correct endpoint based on current state and media type
            const endpoint = isWatched 
                ? (mediaType === 'tv' ? tvProgressRemoveUrl : movieSeenRemoveUrl)
                : (mediaType === 'tv' ? tvProgressAddUrl : movieSeenAddUrl);
            
            try {
                btn.disabled = true;
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: parseInt(id) })
                });
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    // Toggle the state
                    const newState = !isWatched;
                    btn.dataset.isWatched = newState.toString();
                    
                    // Update button appearance
                    if (newState) {
                        // Marked as watched
                        btn.classList.remove('outlined');
                        btn.classList.add('filled', 'active');
                        btn.innerHTML = '<i class="bi bi-check-circle-fill"></i><span>Watched</span>';
                        showNotification('Added to your watched list!', 'success');
                        
                        // Hide watchlist button with animation
                        if (watchlistBtn) {
                            watchlistBtn.classList.add('fade-out');
                            setTimeout(() => {
                                watchlistBtn.classList.add('hidden');
                                watchlistBtn.classList.remove('fade-out');
                                // Reset watchlist state when hidden
                                watchlistBtn.dataset.inWatchlist = 'false';
                                watchlistBtn.classList.remove('filled', 'active');
                                watchlistBtn.classList.add('outlined');
                                watchlistBtn.innerHTML = '<i class="bi bi-bookmark-plus"></i><span>Add to Watchlist</span>';
                            }, 300);
                        }
                    } else {
                        // Removed from watched
                        btn.classList.remove('filled', 'active');
                        btn.classList.add('outlined');
                        btn.innerHTML = '<i class="bi bi-check-circle"></i><span>Add to Watched</span>';
                        showNotification('Removed from your watched list', 'info');
                        
                        // Show watchlist button with animation
                        if (watchlistBtn) {
                            watchlistBtn.classList.remove('hidden');
                            watchlistBtn.classList.add('fade-in');
                            setTimeout(() => {
                                watchlistBtn.classList.remove('fade-in');
                            }, 300);
                        }
                    }
                } else {
                    showNotification(data.message || 'Failed to update', 'error');
                }
            } catch (error) {
                console.error('Error toggling watched:', error);
                showNotification('Error updating. Please try again.', 'error');
            } finally {
                btn.disabled = false;
            }
        });
    });

    // Toggle Watchlist Button
    document.querySelectorAll('.toggle-watchlist').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            
            // Check if user is authenticated
            if (!requireAuth()) return;
            
            const id = btn.dataset.id || titleId;
            const inWatchlist = btn.dataset.inWatchlist === 'true';
            
            // Determine the correct endpoint based on current state and media type
            const endpoint = inWatchlist 
                ? (mediaType === 'tv' ? tvWatchlistRemoveUrl : movieWatchlistRemoveUrl)
                : (mediaType === 'tv' ? tvWatchlistAddUrl : movieWatchlistAddUrl);
            
            try {
                btn.disabled = true;
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: parseInt(id) })
                });
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    // Toggle the state
                    const newState = !inWatchlist;
                    btn.dataset.inWatchlist = newState.toString();
                    
                    // Update button appearance
                    if (newState) {
                        btn.classList.remove('outlined');
                        btn.classList.add('filled', 'active');
                        btn.innerHTML = '<i class="bi bi-bookmark-fill"></i><span>In Watchlist</span>';
                        showNotification('Added to your watchlist!', 'success');
                    } else {
                        btn.classList.remove('filled', 'active');
                        btn.classList.add('outlined');
                        btn.innerHTML = '<i class="bi bi-bookmark-plus"></i><span>Add to Watchlist</span>';
                        showNotification('Removed from your watchlist', 'info');
                    }
                } else {
                    showNotification(data.message || 'Failed to update', 'error');
                }
            } catch (error) {
                console.error('Error toggling watchlist:', error);
                showNotification('Error updating. Please try again.', 'error');
            } finally {
                btn.disabled = false;
            }
        });
    });

    // Handle TV series watched link (scrolls to seasons and opens dropdown)
    document.querySelectorAll('.toggle-watched-link').forEach(link => {
        link.addEventListener('click', (e) => {
            // Check if user is authenticated
            if (!requireAuth()) {
                e.preventDefault();
                return;
            }
            
            const isWatched = link.dataset.isWatched === 'true';
            const watchlistBtn = document.querySelector('.toggle-watchlist');
            
            // If already watched, toggle off (remove from watched)
            if (isWatched) {
                e.preventDefault();
                
                const id = link.dataset.id || titleId;
                
                fetch(tvProgressRemoveUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: parseInt(id) })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update link appearance
                        link.dataset.isWatched = 'false';
                        link.dataset.lastSeasonSeen = '0';
                        link.classList.remove('filled', 'active');
                        link.classList.add('outlined');
                        link.innerHTML = '<i class="bi bi-check-circle"></i><span class=\"btn-text-main\">Add to Watched</span>';
                        showNotification('Removed from your watched list', 'info');
                        
                        // Reset all season items
                        document.querySelectorAll('.season-item').forEach(item => {
                            item.classList.remove('selected', 'watched-previous', 'selected-current');
                            const itemBtn = item.querySelector('.season-select-btn');
                            if (itemBtn) {
                                itemBtn.classList.remove('selected');
                                itemBtn.innerHTML = '<i class="bi bi-check-circle"></i> Select as Last Seen';
                            }
                        });
                        
                        // Show watchlist button with animation
                        if (watchlistBtn) {
                            watchlistBtn.classList.remove('hidden');
                            watchlistBtn.classList.add('fade-in');
                            setTimeout(() => {
                                watchlistBtn.classList.remove('fade-in');
                            }, 300);
                        }
                    } else {
                        showNotification(data.message || 'Failed to remove', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error removing from watched:', error);
                    showNotification('Error updating. Please try again.', 'error');
                });
            }
            // If not watched, the link will scroll to the seasons section (default behavior)
        });
    });
}