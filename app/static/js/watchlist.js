// Watchlist page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tabs
    initializeTabs();
    
    // Initialize actions
    initializeActions();
    
    // Update counts
    updateCounts();
});

function initializeTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.dataset.tab;
            
            // Update active states
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(`${targetTab}-content`).classList.add('active');
        });
    });
}

function initializeActions() {
    // Mark as watched
    document.querySelectorAll('.mark-watched').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            const id = btn.dataset.id;
            
            try {
                const response = await fetch(`/watchlist/mark-watched/${id}`, { method: 'POST' });
                if (response.ok) {
                    const card = btn.closest('.watchlist-card');
                    card.style.transform = 'scale(0.9)';
                    card.style.opacity = '0';
                    setTimeout(() => {
                        card.remove();
                        updateCounts();
                        checkEmptyState();
                    }, 300);
                }
            } catch (error) {
                console.error('Error marking as watched:', error);
            }
        });
    });
    
    // Remove item
    document.querySelectorAll('.remove-item').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            if (!confirm('Are you sure you want to remove this item?')) return;
            
            const id = btn.dataset.id;
            
            try {
                const response = await fetch(`/watchlist/remove/${id}`, { method: 'POST' });
                if (response.ok) {
                    const card = btn.closest('.watchlist-card');
                    card.style.transform = 'scale(0.9)';
                    card.style.opacity = '0';
                    setTimeout(() => {
                        card.remove();
                        updateCounts();
                        checkEmptyState();
                    }, 300);
                }
            } catch (error) {
                console.error('Error removing item:', error);
            }
        });
    });
    
    // Edit rating
    document.querySelectorAll('.edit-rating').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            const id = btn.dataset.id;
            
            const rating = prompt('Rate this title (1-10):', '');
            if (rating === null) return;
            
            const numRating = parseFloat(rating);
            if (isNaN(numRating) || numRating < 1 || numRating > 10) {
                alert('Please enter a valid rating between 1 and 10');
                return;
            }
            
            try {
                const response = await fetch(`/watchlist/rate/${id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ rating: numRating })
                });
                if (response.ok) {
                    location.reload();
                }
            } catch (error) {
                console.error('Error rating item:', error);
            }
        });
    });
}

function updateCounts() {
    const toWatchCount = document.querySelectorAll('#to-watch-content .watchlist-card').length;
    const watchedCount = document.querySelectorAll('#watched-content .watchlist-card').length;
    
    document.getElementById('to-watch-count').textContent = toWatchCount;
    document.getElementById('watched-count').textContent = watchedCount;
}

function checkEmptyState() {
    const toWatchContent = document.getElementById('to-watch-content');
    const watchedContent = document.getElementById('watched-content');
    
    if (toWatchContent.querySelectorAll('.watchlist-card').length === 0) {
        const grid = toWatchContent.querySelector('.watchlist-grid');
        if (grid) {
            grid.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1;">
                    <i class="bi bi-bookmark-plus"></i>
                    <h3>Your watchlist is empty</h3>
                    <p>Start adding movies and TV shows you want to watch!</p>
                    <a href="/" class="btn-explore">
                        <i class="bi bi-search"></i> Explore Titles
                    </a>
                </div>
            `;
        }
    }
    
    if (watchedContent.querySelectorAll('.watchlist-card').length === 0) {
        const grid = watchedContent.querySelector('.watchlist-grid');
        if (grid) {
            grid.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1;">
                    <i class="bi bi-film"></i>
                    <h3>No watched titles yet</h3>
                    <p>Mark titles as watched to keep track of what you've seen!</p>
                    <a href="/" class="btn-explore">
                        <i class="bi bi-search"></i> Explore Titles
                    </a>
                </div>
            `;
        }
    }
}
