
document.addEventListener("DOMContentLoaded", function () {
    leftButtonsDrop();
    initSearchOverlay();
    initNotificationDropdown();
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

