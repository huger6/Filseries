/**
 * Watched Page JavaScript
 * Handles infinite scroll, filtering, and sorting
 */

document.addEventListener('DOMContentLoaded', function() {
    initWatchedPage();
});

function initWatchedPage() {
    const watchedGrid = document.getElementById('watchedGrid');
    const filterBar = document.querySelector('.watched-filter-bar');
    const loadMoreTrigger = document.getElementById('loadMoreTrigger');
    const emptyState = document.getElementById('emptyState');
    const endOfResults = document.getElementById('endOfResults');
    const resultsCount = document.getElementById('resultsCount');
    
    if (!watchedGrid) return;

    // State
    let state = {
        mediaType: 'all', // 'all', 'movie', 'tv'
        sortBy: 'updated_at',
        sortOrder: 'desc',
        isLoading: false,
        hasMore: true,
        lastId: null,
        lastDate: null,
        totalLoaded: 0,
        allTitles: [] // Store all loaded titles for client-side filtering/sorting
    };

    // Sticky filter bar shadow on scroll
    if (filterBar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                filterBar.classList.add('scrolled');
            } else {
                filterBar.classList.remove('scrolled');
            }
        });
    }

    // Media type filter buttons
    document.querySelectorAll('.media-type-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.media-type-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            state.mediaType = this.dataset.type;
            applyFiltersAndSort();
        });
    });

    // Sort dropdown
    const sortBtn = document.getElementById('sortBtn');
    const sortDropdown = document.getElementById('sortDropdown');
    
    if (sortBtn && sortDropdown) {
        sortBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            sortDropdown.classList.toggle('open');
            sortBtn.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!sortDropdown.contains(e.target) && !sortBtn.contains(e.target)) {
                sortDropdown.classList.remove('open');
                sortBtn.classList.remove('active');
            }
        });

        document.querySelectorAll('.sort-option').forEach(option => {
            option.addEventListener('click', function() {
                document.querySelectorAll('.sort-option').forEach(o => o.classList.remove('active'));
                this.classList.add('active');
                
                state.sortBy = this.dataset.sort;
                state.sortOrder = this.dataset.order;
                
                // Update button text
                const sortLabel = document.getElementById('sortLabel');
                if (sortLabel) {
                    sortLabel.textContent = this.textContent.trim();
                }
                
                sortDropdown.classList.remove('open');
                sortBtn.classList.remove('active');
                
                applyFiltersAndSort();
            });
        });
    }

    // Infinite scroll with Intersection Observer
    if (loadMoreTrigger) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !state.isLoading && state.hasMore) {
                    loadMoreTitles();
                }
            });
        }, {
            rootMargin: '200px' // Start loading before reaching the trigger
        });
        
        observer.observe(loadMoreTrigger);
    }

    // Initial load - load both movies and series
    loadInitialData();

    async function loadInitialData() {
        state.isLoading = true;
        showLoadingState();

        try {
            // Load movies and series in parallel
            const [moviesResponse, seriesResponse] = await Promise.all([
                fetchTitles('movie'),
                fetchTitles('tv')
            ]);

            // Combine and store all titles
            const movies = moviesResponse.results || [];
            const series = seriesResponse.results || [];
            
            state.allTitles = [...movies, ...series];
            state.hasMore = moviesResponse.has_more || seriesResponse.has_more;
            
            // Track pagination cursors separately
            state.moviesCursor = getLastCursor(movies);
            state.seriesCursor = getLastCursor(series);
            state.moviesHasMore = moviesResponse.has_more;
            state.seriesHasMore = seriesResponse.has_more;
            
            state.totalLoaded = state.allTitles.length;
            
            applyFiltersAndSort();
            
        } catch (error) {
            console.error('Error loading initial data:', error);
            showError();
        } finally {
            state.isLoading = false;
        }
    }

    async function loadMoreTitles() {
        if (state.isLoading || !state.hasMore) return;
        
        state.isLoading = true;
        showLoadingMore();

        try {
            const requests = [];
            
            // Load more movies if needed
            if (state.moviesHasMore) {
                requests.push(fetchTitles('movie', state.moviesCursor));
            }
            
            // Load more series if needed
            if (state.seriesHasMore) {
                requests.push(fetchTitles('tv', state.seriesCursor));
            }

            if (requests.length === 0) {
                state.hasMore = false;
                hideLoadingMore();
                return;
            }

            const responses = await Promise.all(requests);
            
            let newTitles = [];
            let responseIndex = 0;
            
            if (state.moviesHasMore && responseIndex < responses.length) {
                const moviesResponse = responses[responseIndex++];
                const movies = moviesResponse.results || [];
                newTitles = [...newTitles, ...movies];
                state.moviesCursor = getLastCursor(movies);
                state.moviesHasMore = moviesResponse.has_more;
            }
            
            if (state.seriesHasMore && responseIndex < responses.length) {
                const seriesResponse = responses[responseIndex++];
                const series = seriesResponse.results || [];
                newTitles = [...newTitles, ...series];
                state.seriesCursor = getLastCursor(series);
                state.seriesHasMore = seriesResponse.has_more;
            }
            
            // Add new titles to our collection
            state.allTitles = [...state.allTitles, ...newTitles];
            state.totalLoaded = state.allTitles.length;
            state.hasMore = state.moviesHasMore || state.seriesHasMore;
            
            applyFiltersAndSort();
            
        } catch (error) {
            console.error('Error loading more titles:', error);
        } finally {
            state.isLoading = false;
            hideLoadingMore();
        }
    }

    async function fetchTitles(mediaType, cursor = null) {
        const endpoint = mediaType === 'movie' ? watchedMoviesUrl : watchedSeriesUrl;
        
        const body = { limit: 30 };
        if (cursor) {
            body.last_id = cursor.id;
            body.last_date = cursor.date;
        }

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch ${mediaType}`);
        }

        return response.json();
    }

    function getLastCursor(titles) {
        if (!titles || titles.length === 0) return null;
        const last = titles[titles.length - 1];
        return {
            id: last.id,
            date: last.updated_at
        };
    }

    function applyFiltersAndSort() {
        let filtered = [...state.allTitles];
        
        // Filter by media type
        if (state.mediaType !== 'all') {
            filtered = filtered.filter(t => t.media_type === state.mediaType);
        }
        
        // Sort
        filtered.sort((a, b) => {
            let valA, valB;
            
            switch (state.sortBy) {
                case 'updated_at':
                    valA = new Date(a.updated_at || 0);
                    valB = new Date(b.updated_at || 0);
                    break;
                case 'title':
                    valA = (a.title || '').toLowerCase();
                    valB = (b.title || '').toLowerCase();
                    break;
                case 'user_rating':
                    valA = a.user_rating || 0;
                    valB = b.user_rating || 0;
                    break;
                case 'vote_average':
                    valA = a.vote_average || 0;
                    valB = b.vote_average || 0;
                    break;
                case 'release_date':
                    valA = a.release_date || '0';
                    valB = b.release_date || '0';
                    break;
                default:
                    valA = new Date(a.updated_at || 0);
                    valB = new Date(b.updated_at || 0);
            }
            
            if (state.sortOrder === 'desc') {
                return valA > valB ? -1 : valA < valB ? 1 : 0;
            } else {
                return valA < valB ? -1 : valA > valB ? 1 : 0;
            }
        });
        
        renderTitles(filtered);
        updateResultsCount(filtered.length);
    }

    function renderTitles(titles) {
        if (!watchedGrid) return;
        
        if (titles.length === 0) {
            watchedGrid.innerHTML = '';
            if (emptyState) emptyState.style.display = 'flex';
            if (endOfResults) endOfResults.style.display = 'none';
            return;
        }
        
        if (emptyState) emptyState.style.display = 'none';
        
        const html = titles.map(title => createTitleCard(title)).join('');
        watchedGrid.innerHTML = html;
        
        // Show/hide end of results
        if (endOfResults) {
            endOfResults.style.display = state.hasMore ? 'none' : 'flex';
        }
    }

    function createTitleCard(title) {
        const posterUrl = title.poster_path 
            ? `https://image.tmdb.org/t/p/w500${title.poster_path}` 
            : defaultPosterUrl;
        
        const mediaTypeLabel = title.media_type === 'tv' ? 'TV' : 'Movie';
        const mediaTypeBadgeClass = title.media_type === 'tv' ? 'badge-tv' : 'badge-movie';
        
        const year = title.release_date || 'N/A';
        const userRating = title.user_rating ? `<span class="card-user-rating"><i class="bi bi-star-fill"></i> ${title.user_rating.toFixed(1)}</span>` : '';
        const ratingBadge = title.user_rating ? `<span class="badge badge-rating"><i class="bi bi-star-fill"></i> ${title.user_rating.toFixed(1)}</span>` : '';
        
        // For series, show progress if available
        let progressInfo = '';
        if (title.media_type === 'tv' && title.last_season_seen) {
            progressInfo = `<span class="card-progress">S${title.last_season_seen}</span>`;
        }
        
        return `
            <div class="watched-card" data-id="${title.id}" data-type="${title.media_type}">
                <a href="${titleBaseUrl}/${title.media_type}/${title.id}" class="card-link">
                    <div class="card-poster">
                        <img src="${posterUrl}" alt="${title.title}" loading="lazy" class="poster-img${!title.poster_path ? ' default-poster' : ''}">
                        <div class="card-badges">
                            <span class="badge ${mediaTypeBadgeClass}">${mediaTypeLabel}</span>
                            ${ratingBadge}
                        </div>
                        <div class="card-info">
                            <h4 class="card-title">${escapeHtml(title.title)}</h4>
                            <div class="card-meta">
                                <span class="card-year">${year}</span>
                                ${progressInfo}
                                ${userRating}
                            </div>
                        </div>
                    </div>
                </a>
            </div>
        `;
    }

    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function updateResultsCount(count) {
        if (resultsCount) {
            resultsCount.innerHTML = `<span>${count}</span> title${count !== 1 ? 's' : ''}`;
        }
    }

    function showLoadingState() {
        if (watchedGrid) {
            watchedGrid.innerHTML = Array(12).fill(0).map(() => `
                <div class="skeleton-card">
                    <div class="skeleton-poster"></div>
                </div>
            `).join('');
        }
        if (emptyState) emptyState.style.display = 'none';
    }

    function showLoadingMore() {
        if (loadMoreTrigger) {
            loadMoreTrigger.classList.add('loading');
            loadMoreTrigger.innerHTML = '<div class="loading-spinner"></div>';
        }
    }

    function hideLoadingMore() {
        if (loadMoreTrigger) {
            loadMoreTrigger.classList.remove('loading');
            loadMoreTrigger.innerHTML = '';
        }
    }

    function showError() {
        if (watchedGrid) {
            watchedGrid.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1;">
                    <i class="bi bi-exclamation-triangle"></i>
                    <h3>Something went wrong</h3>
                    <p>Failed to load your watched titles. Please try again.</p>
                    <button class="btn-explore" onclick="location.reload()">
                        <i class="bi bi-arrow-clockwise"></i> Retry
                    </button>
                </div>
            `;
        }
    }

    // ================================
    // Carousels: Similar & Recommendations
    // ================================
    
    initCarousels();
    
    function initCarousels() {
        loadSimilarTitles();
        loadRecommendations();
        setupCarouselControls();
    }

    async function loadSimilarTitles() {
        const section = document.getElementById('similarSection');
        const track = document.getElementById('similarTrack');
        
        if (!section || !track) {
            console.error('Similar section elements not found');
            return;
        }
        
        // Show section with loading skeletons
        section.style.display = 'block';
        track.innerHTML = Array(8).fill(0).map(() => '<div class="skeleton-card"></div>').join('');
        
        try {
            const response = await fetch(similarTitlesUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            if (!response.ok) {
                console.error('Similar titles response not ok:', response.status);
                throw new Error('Failed to fetch similar titles');
            }
            
            const data = await response.json();
            console.log('Similar titles data:', data);
            
            if (data.success && data.results && data.results.length > 0) {
                renderCarouselCards(track, data.results);
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        } catch (error) {
            console.error('Error loading similar titles:', error);
            section.style.display = 'none';
        }
    }

    async function loadRecommendations() {
        const section = document.getElementById('recommendationsSection');
        const track = document.getElementById('recommendationsTrack');
        
        if (!section || !track) {
            console.error('Recommendations section elements not found');
            return;
        }
        
        // Show section with loading skeletons
        section.style.display = 'block';
        track.innerHTML = Array(8).fill(0).map(() => '<div class="skeleton-card"></div>').join('');
        
        try {
            const response = await fetch(recommendationsUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            if (!response.ok) {
                console.error('Recommendations response not ok:', response.status);
                throw new Error('Failed to fetch recommendations');
            }
            
            const data = await response.json();
            console.log('Recommendations data:', data);
            
            if (data.success && data.results && data.results.length > 0) {
                renderCarouselCards(track, data.results);
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        } catch (error) {
            console.error('Error loading recommendations:', error);
            section.style.display = 'none';
        }
    }

    function renderCarouselCards(track, titles) {
        const html = titles.map(title => {
            const posterUrl = title.poster_path 
                ? `https://image.tmdb.org/t/p/w500${title.poster_path}` 
                : defaultPosterUrl;
            
            const year = title.release_date ? title.release_date.substring(0, 4) : 'N/A';
            const rating = title.vote_average ? title.vote_average.toFixed(1) : 'N/A';
            const mediaType = title.media_type || 'movie';
            
            return `
                <a href="${titleBaseUrl}/${mediaType}/${title.id}" class="carousel-card">
                    <div class="card-poster">
                        <img src="${posterUrl}" alt="${escapeHtml(title.title)}" loading="lazy" class="poster-img${!title.poster_path ? ' default-poster' : ''}">
                        <div class="card-overlay"></div>
                        <div class="card-info">
                            <h4 class="card-title">${escapeHtml(title.title)}</h4>
                            <div class="card-meta">
                                <span class="card-year">${year}</span>
                                <span class="card-rating"><i class="bi bi-star-fill"></i> ${rating}</span>
                            </div>
                        </div>
                    </div>
                </a>
            `;
        }).join('');
        
        track.innerHTML = html;
    }

    function setupCarouselControls() {
        document.querySelectorAll('.carousel-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const carouselName = this.dataset.carousel;
                const track = document.getElementById(`${carouselName}Track`);
                
                if (!track) return;
                
                const scrollAmount = 350;
                const direction = this.classList.contains('prev-btn') ? -1 : 1;
                
                track.scrollBy({
                    left: scrollAmount * direction,
                    behavior: 'smooth'
                });
            });
        });
    }
}
