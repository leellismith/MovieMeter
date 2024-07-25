document.addEventListener('DOMContentLoaded', function () {
    // Autocomplete functionality
    const queryInput = document.getElementById('query');
    const autocompleteList = document.getElementById('autocomplete-list');

    if (queryInput) {
        queryInput.addEventListener('input', function() {
            let query = this.value.trim();
            if (query.length < 2) {
                autocompleteList.innerHTML = '';
                return;
            }
            // Fetch autocomplete suggestions from the server
            fetch(`/autocomplete?query=${encodeURIComponent(query)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    // Populate autocomplete list with suggestions
                    let suggestions = data.map(title => 
                        `<div class="autocomplete-suggestion">${title}</div>`).join('');
                    autocompleteList.innerHTML = suggestions;

                    // Add click event listener to each suggestion
                    document.querySelectorAll('.autocomplete-suggestion').forEach(item => {
                        item.addEventListener('click', function () {
                            queryInput.value = this.innerText;
                            autocompleteList.innerHTML = '';
                        });
                    });
                })
                .catch(error => {
                    console.error('Error fetching autocomplete suggestions:', error);
                    autocompleteList.innerHTML = '<div class="autocomplete-error error-search">Unable to find the movie</div>';
                });
        });

        // Close autocomplete list when clicking outside of it
        document.addEventListener('click', function(e) {
            if (!e.target.classList.contains('autocomplete-suggestion') && e.target.id !== 'query') {
                autocompleteList.innerHTML = '';
            }
        });
    }

    // VANTA background effect
    if (typeof VANTA !== 'undefined') {
        VANTA.WAVES({
            el: '#vanta-bg',
            mouseControls: true,
            touchControls: true,
            gyroControls: false,
            scale: 1.00,
            scaleMobile: 1.00,
            color: 0x000000,
            waveSpeed: 0.40
        });
    }

    // Review button functionality
    const reviewButtons = document.querySelectorAll('.review-button');
    reviewButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.stopPropagation();
            const carouselItem = this.closest('.carousel-item');
            const movieId = carouselItem.getAttribute('data-movie-id');
            const movieTitleWithYear = carouselItem.querySelector('.carousel-caption h5').innerText;
            const movieTitle = movieTitleWithYear.split('(')[0].trim();
            const posterUrl = carouselItem.querySelector('img').src;

            // Redirect to the add review page with movie details as query parameters
            window.location.href = `/add_review?movieId=${movieId}&movieTitle=${encodeURIComponent(movieTitle)}&posterUrl=${encodeURIComponent(posterUrl)}`;
        });
    });
});

/**
 * Asks for confirmation before deleting a review.
 * @returns {boolean} - True if the user confirms, false otherwise.
 */
function confirmDelete() {
    return confirm("Are you sure you want to delete this review?"); // jshint ignore:line
}
