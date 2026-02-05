// Home page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize hero backdrop
    initializeHeroBackdrop();
    
    // Initialize sliders
    initializeSliders();
    
    // Initialize scroll indicators
    initializeScrollIndicators();
    
    // Initialize Explore Titles button
    initializeExploreTitlesBtn();
});

function initializeExploreTitlesBtn() {
    const exploreTitlesBtn = document.getElementById('explore-titles-btn');
    const searchOverlay = document.querySelector('.search-overlay');
    const searchOverlayInput = document.querySelector('.search-overlay-input');
    const desktopSearchInput = document.querySelector('.search-form .search-input');
    
    if (!exploreTitlesBtn) return;
    
    exploreTitlesBtn.addEventListener('click', function() {
        // Check if we're on mobile (search overlay is visible) or desktop
        const isMobile = searchOverlay && window.getComputedStyle(searchOverlay).display !== 'none';
        
        if (isMobile) {
            // Mobile: open the search overlay
            searchOverlay.classList.add('active');
            if (searchOverlayInput) {
                setTimeout(() => {
                    searchOverlayInput.focus();
                }, 100);
            }
        } else if (desktopSearchInput) {
            // Desktop: focus the search input in navbar
            desktopSearchInput.focus();
            // Scroll to top to ensure navbar is visible
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
}

function initializeHeroBackdrop() {
    const heroBackdrop = document.getElementById('hero-backdrop');
    const trendingSlider = document.getElementById('trending-slider');
    
    if (heroBackdrop && trendingSlider) {
        try {
            const results = JSON.parse(trendingSlider.dataset.results || '[]');
            if (results.length > 0) {
                const baseImageUrl = 'https://image.tmdb.org/t/p/original';
                let currentIndex = 0;
                
                // Set initial backdrop
                const setBackdrop = (index) => {
                    const item = results[index];
                    if (item && item.backdrop_path) {
                        heroBackdrop.style.backgroundImage = `url(${baseImageUrl}${item.backdrop_path})`;
                    }
                };
                
                setBackdrop(currentIndex);
                
                // Rotate backdrop every 8 seconds
                setInterval(() => {
                    currentIndex = (currentIndex + 1) % Math.min(results.length, 10);
                    heroBackdrop.style.opacity = '0';
                    setTimeout(() => {
                        setBackdrop(currentIndex);
                        heroBackdrop.style.opacity = '1';
                    }, 500);
                }, 8000);
            }
        } catch (e) {
            console.error('Error parsing trending results:', e);
        }
    }
}

function initializeSliders() {
    // Slider navigation
    document.querySelectorAll('.slider-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const sliderId = this.dataset.slider;
            const slider = document.getElementById(`${sliderId}-slider`);
            
            if (slider) {
                const cardWidth = 220; // card width + gap
                const scrollAmount = cardWidth * 3;
                
                if (this.classList.contains('prev-btn')) {
                    slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
                } else {
                    slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
                }
            }
        });
    });

    // Touch/swipe support for sliders
    const sliders = document.querySelectorAll('.slider');
    sliders.forEach(slider => {
        let isDown = false;
        let startX;
        let scrollLeft;

        slider.addEventListener('mousedown', (e) => {
            isDown = true;
            slider.style.cursor = 'grabbing';
            startX = e.pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
        });

        slider.addEventListener('mouseleave', () => {
            isDown = false;
            slider.style.cursor = 'grab';
        });

        slider.addEventListener('mouseup', () => {
            isDown = false;
            slider.style.cursor = 'grab';
        });

        slider.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - slider.offsetLeft;
            const walk = (x - startX) * 2;
            slider.scrollLeft = scrollLeft - walk;
        });
    });
}

function initializeScrollIndicators() {
    const sliderWrappers = document.querySelectorAll('.slider-wrapper');
    
    sliderWrappers.forEach(wrapper => {
        const slider = wrapper.querySelector('.slider');
        const leftBtn = wrapper.querySelector('.scroll-indicator.scroll-left');
        const rightBtn = wrapper.querySelector('.scroll-indicator.scroll-right');
        
        if (!slider) return;
        
        // Update scroll indicators based on scroll position
        function updateScrollIndicators() {
            const canScrollLeft = slider.scrollLeft > 10;
            const canScrollRight = slider.scrollLeft < (slider.scrollWidth - slider.clientWidth - 10);
            
            wrapper.classList.toggle('can-scroll-left', canScrollLeft);
            wrapper.classList.toggle('can-scroll-right', canScrollRight);
        }
        
        // Initial check
        updateScrollIndicators();
        
        // Update on scroll
        slider.addEventListener('scroll', updateScrollIndicators);
        
        // Update on window resize
        window.addEventListener('resize', updateScrollIndicators);
        
        // Click handlers for mobile scroll buttons
        if (leftBtn) {
            leftBtn.addEventListener('click', () => {
                const cardWidth = 170; // approximate card width on mobile
                slider.scrollBy({ left: -cardWidth * 2, behavior: 'smooth' });
            });
        }
        
        if (rightBtn) {
            rightBtn.addEventListener('click', () => {
                const cardWidth = 170;
                slider.scrollBy({ left: cardWidth * 2, behavior: 'smooth' });
            });
        }
    });
}
