/**
 * Search Page Filter Logic
 * Handles filtering, sorting, and display of search results
 */

document.addEventListener("DOMContentLoaded", function () {
    initSearchFilters();
});

function initSearchFilters() {
    const filterToggleBtn = document.getElementById('filterToggleBtn');
    const filterDropdown = document.getElementById('filterDropdown');
    const resetFiltersBtn = document.getElementById('resetFilters');
    const resultsGrid = document.getElementById('resultsGrid');
    const resultCount = document.getElementById('resultCount');
    const activeFiltersDisplay = document.getElementById('activeFilters');

    if (!filterToggleBtn || !filterDropdown || !resultsGrid) return;

    // Store original cards for filtering
    const allCards = Array.from(resultsGrid.querySelectorAll('.result-card'));
    
    // Load filter state from sessionStorage (set by navbar) or use defaults
    let savedState = JSON.parse(sessionStorage.getItem('navbarFilterState'));
    let filterState = savedState || {
        quickFilter: 'relevant',
        sortBy: 'popularity',
        sortOrder: 'desc',
        genres: ['all'],
        mediaType: 'all'
    };
    // Ensure mediaType exists for older saved states
    if (!filterState.mediaType) filterState.mediaType = 'all';

    // Apply saved state to UI
    applyStateToUI();

    // Toggle dropdown
    filterToggleBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        filterDropdown.classList.toggle('open');
        filterToggleBtn.classList.toggle('active');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!filterDropdown.contains(e.target) && !filterToggleBtn.contains(e.target)) {
            filterDropdown.classList.remove('open');
            filterToggleBtn.classList.remove('active');
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && filterDropdown.classList.contains('open')) {
            filterDropdown.classList.remove('open');
            filterToggleBtn.classList.remove('active');
        }
    });

    // Quick filter buttons
    filterDropdown.querySelectorAll('.quick-filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            filterDropdown.querySelectorAll('.quick-filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            filterState.quickFilter = this.dataset.filter;
            applyFilters();
        });
    });

    // Sort buttons
    filterDropdown.querySelectorAll('.sort-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            filterDropdown.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            filterState.sortBy = this.dataset.sort;
            filterState.sortOrder = this.dataset.order;
            applyFilters();
        });
    });

    // Genre buttons (multi-select)
    filterDropdown.querySelectorAll('.genre-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const genre = this.dataset.genre;
            
            if (genre === 'all') {
                // Select only "All"
                filterDropdown.querySelectorAll('.genre-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                filterState.genres = ['all'];
            } else {
                // Deselect "All" and toggle this genre
                filterDropdown.querySelector('.genre-btn[data-genre="all"]').classList.remove('active');
                this.classList.toggle('active');
                
                // Update genres array
                const activeGenres = Array.from(filterDropdown.querySelectorAll('.genre-btn.active:not([data-genre="all"])'))
                    .map(b => b.dataset.genre);
                
                if (activeGenres.length === 0) {
                    // If no genres selected, select "All"
                    filterDropdown.querySelector('.genre-btn[data-genre="all"]').classList.add('active');
                    filterState.genres = ['all'];
                } else {
                    filterState.genres = activeGenres;
                }
            }
            applyFilters();
        });
    });

    // Media type buttons
    filterDropdown.querySelectorAll('.media-type-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            filterDropdown.querySelectorAll('.media-type-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            filterState.mediaType = this.dataset.type;
            applyFilters();
        });
    });

    // Reset filters
    resetFiltersBtn.addEventListener('click', function() {
        // Reset state
        filterState = {
            quickFilter: 'relevant',
            sortBy: 'popularity',
            sortOrder: 'desc',
            genres: ['all'],
            mediaType: 'all'
        };

        // Reset UI and apply
        applyStateToUI();
        applyFilters();
        
        // Also clear navbar filter state
        sessionStorage.removeItem('navbarFilterState');
    });

    // Apply state to UI function
    function applyStateToUI() {
        // Quick filters
        filterDropdown.querySelectorAll('.quick-filter-btn').forEach(b => b.classList.remove('active'));
        const quickBtn = filterDropdown.querySelector(`.quick-filter-btn[data-filter="${filterState.quickFilter}"]`);
        if (quickBtn) quickBtn.classList.add('active');

        // Sort buttons
        filterDropdown.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
        const sortBtn = filterDropdown.querySelector(`.sort-btn[data-sort="${filterState.sortBy}"][data-order="${filterState.sortOrder}"]`);
        if (sortBtn) sortBtn.classList.add('active');

        // Genre buttons
        filterDropdown.querySelectorAll('.genre-btn').forEach(b => b.classList.remove('active'));
        if (filterState.genres.includes('all')) {
            const allBtn = filterDropdown.querySelector('.genre-btn[data-genre="all"]');
            if (allBtn) allBtn.classList.add('active');
        } else {
            filterState.genres.forEach(g => {
                const gBtn = filterDropdown.querySelector(`.genre-btn[data-genre="${g}"]`);
                if (gBtn) gBtn.classList.add('active');
            });
        }

        // Media type buttons
        filterDropdown.querySelectorAll('.media-type-btn').forEach(b => b.classList.remove('active'));
        const mediaTypeBtn = filterDropdown.querySelector(`.media-type-btn[data-type="${filterState.mediaType || 'all'}"]`);
        if (mediaTypeBtn) mediaTypeBtn.classList.add('active');
    }

    // Apply filters function
    function applyFilters() {
        let filteredCards = [...allCards];

        // 1. Apply quick filter
        if (filterState.quickFilter === 'relevant') {
            filteredCards = filteredCards.filter(card => {
                const popularity = parseFloat(card.dataset.popularity) || 0;
                const releaseYear = parseInt(card.dataset.release) || 0;
                const hasBackdrop = card.dataset.backdrop && card.dataset.backdrop !== '';
                
                // Relevant: popularity > 5, released after 1950, has backdrop image
                return popularity > 5 && releaseYear >= 1950 && hasBackdrop;
            });
        }

        // 2. Apply media type filter
        if (filterState.mediaType && filterState.mediaType !== 'all') {
            filteredCards = filteredCards.filter(card => {
                return card.dataset.type === filterState.mediaType;
            });
        }

        // 3. Apply genre filter
        if (!filterState.genres.includes('all')) {
            filteredCards = filteredCards.filter(card => {
                const cardGenres = JSON.parse(card.dataset.genres || '[]').map(String);
                return filterState.genres.some(genre => cardGenres.includes(genre));
            });
        }

        // 4. Sort
        filteredCards.sort((a, b) => {
            let aVal, bVal;

            switch (filterState.sortBy) {
                case 'popularity':
                    aVal = parseFloat(a.dataset.popularity) || 0;
                    bVal = parseFloat(b.dataset.popularity) || 0;
                    break;
                case 'vote_average':
                    aVal = parseFloat(a.dataset.vote) || 0;
                    bVal = parseFloat(b.dataset.vote) || 0;
                    break;
                case 'title':
                    aVal = a.dataset.title.toLowerCase();
                    bVal = b.dataset.title.toLowerCase();
                    if (filterState.sortOrder === 'asc') {
                        return aVal.localeCompare(bVal);
                    } else {
                        return bVal.localeCompare(aVal);
                    }
                case 'release_date':
                    aVal = parseInt(a.dataset.release) || 0;
                    bVal = parseInt(b.dataset.release) || 0;
                    break;
                default:
                    return 0;
            }

            if (filterState.sortBy !== 'title') {
                return filterState.sortOrder === 'desc' ? bVal - aVal : aVal - bVal;
            }
        });

        // 5. Update DOM
        // Hide all cards first
        allCards.forEach(card => {
            card.style.display = 'none';
            card.style.order = '';
        });

        // Show and order filtered cards
        filteredCards.forEach((card, index) => {
            card.style.display = 'flex';
            card.style.order = index;
        });

        // Update result count
        if (resultCount) {
            resultCount.textContent = filteredCards.length;
        }

        // Update active filters display
        updateActiveFiltersDisplay();
    }

    // Genre ID to name mapping
    const genreNames = {
        '28': 'Action', '12': 'Adventure', '16': 'Animation', '35': 'Comedy',
        '80': 'Crime', '99': 'Documentary', '18': 'Drama', '10751': 'Family',
        '14': 'Fantasy', '36': 'History', '27': 'Horror', '10402': 'Music',
        '9648': 'Mystery', '10749': 'Romance', '878': 'Sci-Fi', '53': 'Thriller',
        '10752': 'War', '37': 'Western'
    };

    function updateActiveFiltersDisplay() {
        if (!activeFiltersDisplay) return;

        const tags = [];

        // Quick filter tag
        if (filterState.quickFilter === 'relevant') {
            tags.push('<span class="active-filter-tag"><i class="bi bi-fire"></i> Relevant Only</span>');
        }

        // Media type tag
        if (filterState.mediaType && filterState.mediaType !== 'all') {
            const typeLabel = filterState.mediaType === 'movie' ? 'Movies' : 'Series';
            const typeIcon = filterState.mediaType === 'movie' ? 'film' : 'tv';
            tags.push(`<span class="active-filter-tag"><i class="bi bi-${typeIcon}"></i> ${typeLabel}</span>`);
        }

        // Sort tag
        const sortLabels = {
            'popularity-desc': 'Popular',
            'vote_average-desc': 'Rating ↓',
            'vote_average-asc': 'Rating ↑',
            'title-asc': 'A-Z',
            'title-desc': 'Z-A',
            'release_date-desc': 'Newest',
            'release_date-asc': 'Oldest'
        };
        const sortKey = `${filterState.sortBy}-${filterState.sortOrder}`;
        if (sortLabels[sortKey] && sortKey !== 'popularity-desc') {
            tags.push(`<span class="active-filter-tag"><i class="bi bi-sort-down"></i> ${sortLabels[sortKey]}</span>`);
        }

        // Genre tags
        if (!filterState.genres.includes('all')) {
            filterState.genres.forEach(genreId => {
                const name = genreNames[genreId] || genreId;
                tags.push(`<span class="active-filter-tag"><i class="bi bi-tag"></i> ${name}</span>`);
            });
        }

        activeFiltersDisplay.innerHTML = tags.join('');
    }

    // Apply initial filters (relevant by default)
    applyFilters();
}
