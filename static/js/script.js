document.getElementById('query').addEventListener('input', function() {
  let query = this.value.trim();
  if (query.length < 2) {
      document.getElementById('autocomplete-list').innerHTML = '';
      return;
  }
  
  fetch(`/autocomplete?query=${query}`)
      .then(response => {
          if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
          }
          // Additional logging to capture the response before parsing
          return response.text().then(text => {
              try {
                  return JSON.parse(text);
              } catch (err) {
                  console.error('Response is not valid JSON:', text);
                  throw new Error('Response is not valid JSON');
              }
          });
      })
      .then(data => {
          let suggestions = data.map(title => `<div class="autocomplete-suggestion">${title}</div>`).join('');
          document.getElementById('autocomplete-list').innerHTML = suggestions;

          document.querySelectorAll('.autocomplete-suggestion').forEach(item => {
              item.addEventListener('click', function () {
                  document.getElementById('query').value = this.innerText;
                  document.getElementById('autocomplete-list').innerHTML = '';
              });
          });
      })
      .catch(error => {
          console.error('Error fetching autocomplete suggestions:', error);
          document.getElementById('autocomplete-list').innerHTML = '<div class="autocomplete-error">Unable to find the movie</div>';
      });
  });

// Close autocomplete suggestions when clicking outside
document.addEventListener('click', function(e) {
    if (!e.target.classList.contains('autocomplete-suggestion') && e.target.id !== 'query') {
        document.getElementById('autocomplete-list').innerHTML = '';
    }
});

// jQuery code safely wrapped in noConflict mode
jQuery(document).ready(function($) {
  // Use $ safely within this function
  $('.sidenav').sidenav();
});

