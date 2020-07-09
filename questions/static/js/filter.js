/* Search function for filtering through questions.
 * https://www.w3schools.com/jquery/jquery_filters.asp
 */

$(document).ready(function(){
  $(".search-bar").on("keyup", function() { // When type, dynamically search
    var value = $(this).val().toLowerCase();
    $(".question-list-item").filter(function() {
      // If doesn't match, hide it.
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

/*
 * Once the question's fully loaded, add on all the categories it has.
 */
