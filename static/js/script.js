document.getElementById('query').addEventListener('input', function() {
  let query = this.value;
  if (query.length < 2) {
      document.getElementById('autocomplete-list').innerHTML = '';
      return;
  }
  
  fetch(`/autocomplete?query=${query}`)
      .then(response => response.json())
      .then(data => {
          let suggestions = data.map(title => `<div class="autocomplete-suggestion">${title}</div>`).join('');
          document.getElementById('autocomplete-list').innerHTML = suggestions;

          document.querySelectorAll('.autocomplete-suggestion').forEach(item => {
              item.addEventListener('click', function() {
                  document.getElementById('query').value = this.innerText;
                  document.getElementById('autocomplete-list').innerHTML = '';
              });
          });
      });
});

// Close autocomplete suggestions when clicking outside
document.addEventListener('click', function(e) {
  if (!e.target.classList.contains('autocomplete-suggestion')) {
      document.getElementById('autocomplete-list').innerHTML = '';
  }
});

// jQuery code safely wrapped in noConflict mode
jQuery(document).ready(function($) {
  // Use $ safely within this function
  $('.sidenav').sidenav();
});

