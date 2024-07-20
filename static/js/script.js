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
        el: 'html',  // Apply the effect to the entire body
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: window.innerHeight,
        minWidth: window.innerWidth,
        scale: 1,
        scaleMobile: 1,
        color: 0x000000,  // Background color in hexadecimal (black)
        waveSpeed: 0.40
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    const carouselItems = document.querySelectorAll('.carousel-item');

    carouselItems.forEach(item => {
        item.addEventListener('click', function () {
            const movieId = this.getAttribute('data-movie-id');
            const movieTitle = this.querySelector('h5').innerText;
            const posterUrl = this.querySelector('img').src;
            // Redirect to the add_review page with the selected movie details
            window.location.href = `/add_review?movieId=${movieId}&movieTitle=${encodeURIComponent(movieTitle)}&posterUrl=${encodeURIComponent(posterUrl)}`;
        });
    });
});
