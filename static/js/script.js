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
                let suggestions = data.map(title => `<div class="autocomplete-suggestion">${title}</div>`).join('');
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
