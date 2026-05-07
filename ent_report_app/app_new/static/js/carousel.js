// Carousel scroll function
function scrollCarousel(direction) {
    const carousel = document.querySelector('.carousel-container');
    if (!carousel) return;
    
    const scrollAmount = 350; // Width of card + gap
    carousel.scrollBy({
        left: direction * scrollAmount,
        behavior: 'smooth'
    });
}

// Auto scroll testimonials every 5 seconds
let autoScrollInterval = setInterval(() => {
    const carousel = document.querySelector('.carousel-container');
    if (carousel) {
        const maxScroll = carousel.scrollWidth - carousel.clientWidth;
        if (carousel.scrollLeft >= maxScroll) {
            carousel.scrollTo({ left: 0, behavior: 'smooth' });
        } else {
            scrollCarousel(1);
        }
    }
}, 5000);

// Pause auto-scroll on hover
document.addEventListener('mouseover', (e) => {
    if (e.target.closest('.testimonials-carousel')) {
        clearInterval(autoScrollInterval);
    }
});

document.addEventListener('mouseout', (e) => {
    if (e.target.closest('.testimonials-carousel')) {
        autoScrollInterval = setInterval(() => {
            const carousel = document.querySelector('.carousel-container');
            if (carousel) {
                const maxScroll = carousel.scrollWidth - carousel.clientWidth;
                if (carousel.scrollLeft >= maxScroll) {
                    carousel.scrollTo({ left: 0, behavior: 'smooth' });
                } else {
                    scrollCarousel(1);
                }
            }
        }, 5000);
    }
});
