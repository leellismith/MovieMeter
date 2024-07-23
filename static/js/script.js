document.addEventListener('DOMContentLoaded', function () {
    const queryInput = document.getElementById('query');
    const autocompleteList = document.getElementById('autocomplete-list');

    queryInput.addEventListener('input', function() {
        let query = this.value.trim();
        if (query.length < 2) {
            autocompleteList.innerHTML = '';
            return;
        }

        fetch(`/autocomplete?query=${encodeURIComponent(query)}`)  // Ensures proper URL encoding
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();  // Parse response as JSON directly
            })
            .then(data => {
                let suggestions = data.map(title => 
                    `<div class="autocomplete-suggestion">${title}</div>`).join('');
                autocompleteList.innerHTML = suggestions;

                document.querySelectorAll('.autocomplete-suggestion').forEach(item => {
                    item.addEventListener('click', function () {
                        queryInput.value = this.innerText;
                        autocompleteList.innerHTML = '';
                    });
                });
            })
            .catch(error => {
                console.error('Error fetching autocomplete suggestions:', error);
                autocompleteList.innerHTML = '<div class="autocomplete-error">Unable to find the movie</div>';
            });
    });

    // Close autocomplete suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.classList.contains('autocomplete-suggestion') && e.target.id !== 'query') {
            autocompleteList.innerHTML = '';
        }
    });

});

document.addEventListener('DOMContentLoaded', function() {
    VANTA.WAVES({
        el: '#vanta-bg',  // Apply the bg effect to the canvas
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        scale: 1.00,
        scaleMobile: 1.00,
        color: 0x000000,  // Background color in hexadecimal (black)
        waveSpeed: 0.40
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    const reviewButtons = document.querySelectorAll('.review-button');

    reviewButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.stopPropagation();  // Prevent carousel item click event
            const carouselItem = this.closest('.carousel-item');
            const movieId = carouselItem.getAttribute('data-movie-id');
            const movieTitleWithYear = carouselItem.querySelector('.carousel-caption h5').innerText;
            const movieTitle = movieTitleWithYear.split('(')[0].trim();
            const posterUrl = carouselItem.querySelector('img').src;

            // Redirect to the add_review page with the selected movie details
            window.location.href = `/add_review?movieId=${movieId}&movieTitle=${encodeURIComponent(movieTitle)}&posterUrl=${encodeURIComponent(posterUrl)}`;
        });
    });
});

function confirmDelete() {
    return confirm("Are you sure you want to delete this review?");
}
