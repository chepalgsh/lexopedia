$('.lexopedia-header-search-bar-button-container .lexopedia-header-search-bar-button:first-child').on('click', function() {
  searchMeaning();
});

$('.lexopedia-header-search-bar-button-container .lexopedia-header-search-bar-button:last-child').on('click', function() {
  searchSpelling();
});

function searchSpelling() {
    var searchTerm = document.getElementById("lexopedia-header-search-bar-input").value;
    if (searchTerm.length < 2 || searchTerm.indexOf(" ") !== -1) {
      alert("Please enter search term with at least two characters and without spaces.");
      return false;
    }
    // show progress bar
    var progressbar = document.querySelector('#progressbar');
    progressbar.classList.add('active');
    $.ajax({
      url: "/search-spelling-matches/",
      type: "POST",
      data: {searchTerm: searchTerm}, // Add this line to send the searchTerm to the server
      success: function(data) {
        window.location.href = "/spelling-matches/" + searchTerm;
        progressbar.classList.remove('active');
      }
    });
    return true;
  }
  
  function searchMeaning() {
    var searchTerm = document.getElementById("lexopedia-header-search-bar-input").value;
    if (searchTerm.length < 2 || searchTerm.indexOf(" ") !== -1) {
      alert("Please enter search term with at least two characters and without spaces.");
      return false;
    }
    // show progress bar
    var progressbar = document.querySelector('#progressbar');
    progressbar.classList.add('active');
    $.ajax({
      url: "/search-meaning-matches/",
      type: "POST",
      data: {searchTerm: searchTerm}, // Add this line to send the searchTerm to the server
      success: function(data) {
        window.location.href = "/meaning-matches/" + searchTerm;
        progressbar.classList.remove('active');
      }
    });
    return true;
  }
  
  $(document).ready(function() {
    // When the user types in the search input
    $('.lexopedia-header-search-bar-input').on('input', function() {
      // Get the search term entered by the user
      var searchTerm = $(this).val();
      
      // Update the search buttons with the new search term
      $('.lexopedia-header-search-bar-button-container .lexopedia-header-search-bar-button:first-child p').text('Search "' + searchTerm + '" for meaning matches...');
      $('.lexopedia-header-search-bar-button-container .lexopedia-header-search-bar-button:last-child p').text('Search "' + searchTerm + '" for spelling matches...');
    });
  });
  
  const headerSearchInput = document.querySelector('.lexopedia-header-search-bar-input[type="text"]');
  const headerSearchButtons = document.querySelectorAll('.lexopedia-header-search-bar-button-container .lexopedia-header-search-bar-button');
  const headerMaxLength = headerSearchInput.getAttribute('maxlength');
  
  headerSearchInput.addEventListener('input', function() {
    if (this.value.length > headerMaxLength) {
      this.value = this.value.slice(0, headerMaxLength);
    }
  });

  headerSearchInput.addEventListener('focus', () => {
    var searchTerm = document.getElementById("lexopedia-header-search-bar-input").value;
    if (searchTerm != "") {
      headerSearchInput.style.borderTopLeftRadius = '5px';
      headerSearchInput.style.borderTopRightRadius = '5px';
      headerSearchInput.style.borderBottomLeftRadius = '0px';
      headerSearchInput.style.borderBottomRightRadius = '0px';
      headerSearchButtons.forEach(button => button.style.display = 'flex');
    }
  });
  
  headerSearchInput.addEventListener('blur', () => {
    setTimeout(() => {
      headerSearchInput.style.borderRadius = '5px';
      headerSearchButtons.forEach(button => button.style.display = 'none');
    }, 222);
  });

  headerSearchInput.addEventListener('input', () => {
    if (headerSearchInput.placeholder && headerSearchInput.value) {
      headerSearchInput.style.borderTopLeftRadius = '5px';
      headerSearchInput.style.borderTopRightRadius = '5px';
      headerSearchInput.style.borderBottomLeftRadius = '0px';
      headerSearchInput.style.borderBottomRightRadius = '0px';
      headerSearchButtons.forEach(button => button.style.display = 'flex');
    } else if (headerSearchInput.placeholder && !headerSearchInput.value) {
      headerSearchInput.style.borderRadius = '5px';
      headerSearchButtons.forEach(button => button.style.display = 'none');
    }
  });
  