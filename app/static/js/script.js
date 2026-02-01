
document.addEventListener("DOMContentLoaded", function () {
    leftButtonsDrop();
    initSearchOverlay();
    initNotificationDropdown();
    initNavbarFilterDropdown();
    initSearchValidation();
});

function leftButtonsDrop() {
    const dropdowns = document.querySelectorAll(".dropdown-watch");
    
    dropdowns.forEach((dropdown) => {
        const button = dropdown.querySelector(".dropdown-button");
        
        button.addEventListener("click", function (event) {
            event.stopPropagation(); //Evita que se feche automaticamente
            //Altera o estado atual
            dropdown.classList.toggle("open");
        });
    });
    // Fechar dropdowns ao clicar fora
    document.addEventListener("click", function (event) {
        dropdowns.forEach((dropdown) => {
            if (dropdown.contains(event.target)) {
                dropdown.classList.remove("open");
                sessionStorage.setItem("leftButtonsDrop", false);
            }
        })
    });
}

function initSearchOverlay() {
    const searchToggleBtn = document.querySelector('.search-toggle-btn');
    const searchOverlay = document.querySelector('.search-overlay');
    const searchOverlayClose = document.querySelector('.search-overlay-close');
    const searchOverlayInput = document.querySelector('.search-overlay-input');

    if (!searchToggleBtn || !searchOverlay) return;

    // Open search overlay
    searchToggleBtn.addEventListener('click', function() {
        searchOverlay.classList.add('active');
        setTimeout(() => {
            searchOverlayInput.focus();
        }, 100);
    });

    // Close search overlay
    if (searchOverlayClose) {
        searchOverlayClose.addEventListener('click', function() {
            searchOverlay.classList.remove('active');
        });
    }

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
            searchOverlay.classList.remove('active');
        }
    });

    // Submit on Enter
    if (searchOverlayInput) {
        searchOverlayInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                this.closest('form').submit();
            }
        });
    }
}

function initNotificationDropdown() {
    const notificationBtn = document.querySelector('.notification-btn');
    const notificationDropdown = document.querySelector('.notification-dropdown');
    const notificationTabs = document.querySelectorAll('.notification-tab');

    if (!notificationBtn || !notificationDropdown) return;

    // Toggle dropdown on button click
    notificationBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        notificationDropdown.classList.toggle('open');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!notificationDropdown.contains(e.target) && !notificationBtn.contains(e.target)) {
            notificationDropdown.classList.remove('open');
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && notificationDropdown.classList.contains('open')) {
            notificationDropdown.classList.remove('open');
        }
    });

    // Tab switching
    notificationTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            notificationTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.dataset.filter;
            filterNotifications(filter);
        });
    });
}

function filterNotifications(filter) {
    const notificationItems = document.querySelectorAll('.notification-item');
    const emptyState = document.querySelector('.notification-empty');
    
    let visibleCount = 0;
    
    notificationItems.forEach(item => {
        if (filter === 'all') {
            item.style.display = 'flex';
            visibleCount++;
        } else if (filter === 'new' && item.classList.contains('unread')) {
            item.style.display = 'flex';
            visibleCount++;
        } else {
            item.style.display = 'none';
        }
    });
    
    // Show empty state if no notifications visible
    if (emptyState) {
        emptyState.style.display = visibleCount === 0 ? 'flex' : 'none';
    }
}

/**
 * Navbar Filter Dropdown
 * Handles filter selection in the search bar
 */
function initNavbarFilterDropdown() {
    const filterBtn = document.getElementById('navbarFilterBtn');
    const filterDropdown = document.getElementById('navbarFilterDropdown');
    const resetBtn = document.getElementById('navbarResetFilters');

    if (!filterBtn || !filterDropdown) return;

    // Store filter state in sessionStorage for persistence
    let filterState = JSON.parse(sessionStorage.getItem('navbarFilterState')) || {
        quickFilter: 'relevant',
        sortBy: 'popularity',
        sortOrder: 'desc',
        genres: ['all']
    };

    // Apply saved state to UI
    applyStateToUI();

    // Toggle dropdown
    filterBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        filterDropdown.classList.toggle('open');
        filterBtn.classList.toggle('active');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!filterDropdown.contains(e.target) && !filterBtn.contains(e.target)) {
            filterDropdown.classList.remove('open');
            filterBtn.classList.remove('active');
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && filterDropdown.classList.contains('open')) {
            filterDropdown.classList.remove('open');
            filterBtn.classList.remove('active');
        }
    });

    // Quick filter buttons
    filterDropdown.querySelectorAll('.quick-filter-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            filterDropdown.querySelectorAll('.quick-filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            filterState.quickFilter = this.dataset.filter;
            saveState();
        });
    });

    // Sort buttons
    filterDropdown.querySelectorAll('.sort-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            filterDropdown.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            filterState.sortBy = this.dataset.sort;
            filterState.sortOrder = this.dataset.order;
            saveState();
        });
    });

    // Genre buttons
    filterDropdown.querySelectorAll('.genre-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const genre = this.dataset.genre;
            
            if (genre === 'all') {
                filterDropdown.querySelectorAll('.genre-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                filterState.genres = ['all'];
            } else {
                filterDropdown.querySelector('.genre-btn[data-genre="all"]').classList.remove('active');
                this.classList.toggle('active');
                
                const activeGenres = Array.from(filterDropdown.querySelectorAll('.genre-btn.active:not([data-genre="all"])'))
                    .map(b => b.dataset.genre);
                
                if (activeGenres.length === 0) {
                    filterDropdown.querySelector('.genre-btn[data-genre="all"]').classList.add('active');
                    filterState.genres = ['all'];
                } else {
                    filterState.genres = activeGenres;
                }
            }
            saveState();
        });
    });

    // Reset button
    if (resetBtn) {
        resetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            filterState = {
                quickFilter: 'relevant',
                sortBy: 'popularity',
                sortOrder: 'desc',
                genres: ['all']
            };
            applyStateToUI();
            saveState();
        });
    }

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
            filterDropdown.querySelector('.genre-btn[data-genre="all"]').classList.add('active');
        } else {
            filterState.genres.forEach(g => {
                const gBtn = filterDropdown.querySelector(`.genre-btn[data-genre="${g}"]`);
                if (gBtn) gBtn.classList.add('active');
            });
        }
    }

    function saveState() {
        sessionStorage.setItem('navbarFilterState', JSON.stringify(filterState));
        
        // Update filter button appearance based on whether non-default filters are active
        const isDefault = filterState.quickFilter === 'relevant' && 
                          filterState.sortBy === 'popularity' && 
                          filterState.sortOrder === 'desc' && 
                          filterState.genres.includes('all');
        
        if (!isDefault) {
            filterBtn.style.background = 'var(--accentColor)';
            filterBtn.style.color = 'var(--primaryColor)';
        } else {
            filterBtn.style.background = '';
            filterBtn.style.color = '';
        }
    }
}
/**
 * Search Input Validation
 * Provides visual feedback for search input validation
 */
function initSearchValidation() {
    const MIN_LENGTH = 3;
    const MAX_LENGTH = 100;

    // Main search form
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    
    if (searchForm && searchInput) {
        setupValidation(searchForm, searchInput);
    }

    // Overlay search form
    const overlayForm = document.querySelector('.search-overlay-form');
    const overlayInput = document.querySelector('.search-overlay-input');
    
    if (overlayForm && overlayInput) {
        setupValidation(overlayForm, overlayInput);
    }

    function setupValidation(form, input) {
        // Real-time validation on input
        input.addEventListener('input', function() {
            const value = this.value.trim();
            
            if (value.length > 0 && value.length < MIN_LENGTH) {
                this.classList.add('invalid');
                form.classList.add('show-error');
            } else {
                this.classList.remove('invalid');
                form.classList.remove('show-error');
            }
        });

        // Validate on blur
        input.addEventListener('blur', function() {
            form.classList.remove('show-error');
        });

        // Prevent form submission if invalid
        form.addEventListener('submit', function(e) {
            const value = input.value.trim();
            
            if (value.length === 0) {
                e.preventDefault();
                input.classList.add('invalid');
                form.classList.add('show-error');
                input.focus();
                
                // Update tooltip message
                const tooltip = form.querySelector('.search-error-tooltip');
                if (tooltip) {
                    tooltip.textContent = 'Please enter a search term';
                }
                
                // Hide error after 3 seconds
                setTimeout(() => {
                    form.classList.remove('show-error');
                }, 3000);
                return;
            }
            
            if (value.length < MIN_LENGTH) {
                e.preventDefault();
                input.classList.add('invalid');
                form.classList.add('show-error');
                input.focus();
                
                // Update tooltip message
                const tooltip = form.querySelector('.search-error-tooltip');
                if (tooltip) {
                    tooltip.textContent = `Please enter at least ${MIN_LENGTH} characters`;
                }
                
                // Hide error after 3 seconds
                setTimeout(() => {
                    form.classList.remove('show-error');
                }, 3000);
                return;
            }
            
            if (value.length > MAX_LENGTH) {
                e.preventDefault();
                input.classList.add('invalid');
                form.classList.add('show-error');
                
                // Update tooltip message
                const tooltip = form.querySelector('.search-error-tooltip');
                if (tooltip) {
                    tooltip.textContent = `Search term is too long (max ${MAX_LENGTH} characters)`;
                }
                
                // Hide error after 3 seconds
                setTimeout(() => {
                    form.classList.remove('show-error');
                }, 3000);
                return;
            }
            
            // Valid - remove any error states
            input.classList.remove('invalid');
            form.classList.remove('show-error');
        });
    }
}