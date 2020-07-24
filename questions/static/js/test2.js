

// variable that keeps all the filter information

var send_data = {};

$(document).ready(function () {
  // reset all parameters on page load
  resetFilters();

  // bring all the data without any filters.
  getAPIData();

  // get all categories from database via ajax call.
  getCategories();

  // sort the data according to price/points

  // on selecting the category option
  $('#categories').on('change', function () {

    // update the selected country
    if(this.value == 'all')
      send_data['categories'] = '';
    else
      send_data['categories'] = this.value;

      // Get the new data.
      getAPIData();
  });


  $('#sort_by').on('change', function () {
    send_data['sort_by'] = this.value;
    getAPIData();
  });

  $('#post_in').on('change', function(){
    send_data['post_in'] = this.value;
    getAPIData();
  });

  // display the results after reseting the filters

  $("#display_all").click(function(){
    resetFilters();
    getAPIData();
  });
});


/**
    Function that resets all the filters
**/
function resetFilters() {
  $("#categories").val("all");
  $("#sort_by").val("none");
  $("#post_in").val("none");

  send_data['categories'] = '';
  send_data['sort_by'] = '';
  send_data['post_in'] = '';
}

/**.
    Utility function to showcase the api data
    we got from backend to the table content
**/
function putTableData(result) {
  // creating table row for each result and

  // pushing to the html cntent of table body of listing table

  let row;
  if(result.results.length > 0){
    $("#no_results").hide();
    $("#list_data").show();
    $("#listing").html("");
    $.each(result.results, function (a, b) {
      row = "<tr>" +
               "<td title=\"" + b.subject + "\">" + b.subject.slice(0, 50) +
               "..." +
               "</td>" +
               "<td title=\"" + b.content + "\">" + b.content.slice(0, 60) +
               "..." +
               "</td>" +
               "<td>" + b.category + "</td>" +
             "</tr>";
            $("#listing").append(row);
    });
  }
  else{
    // if no result found for the given filter, then display no result

    $("#no_results h5").html("No results found");
    $("#list_data").hide();
    $("#no_results").show();
  }

  // setting previous and next page url for the given result

  let prev_url = result["previous"];
  let next_url = result["next"];
  // disabling-enabling button depending on existence of next/prev page.

  if (prev_url === null) {
    $("#previous").addClass("disabled");
    $("#previous").prop('disabled', true);
  } else {
    $("#previous").removeClass("disabled");
    $("#previous").prop('disabled', false);
  }
  if (next_url === null) {
    $("#next").addClass("disabled");
    $("#next").prop('disabled', true);
  } else {
    $("#next").removeClass("disabled");
    $("#next").prop('disabled', false);
  }
  // setting the url

  $("#previous").attr("url", result["previous"]);
  $("#next").attr("url", result["next"]);
  // displaying result count

  $("#result-count span").html(result["count"]);
}

function getAPIData() {
    let url = $('#list_data').attr("url")
    $.ajax({
        method: 'GET',
        url: url,
        data: send_data,
        beforeSend: function(){
            $("#no_results h5").html("Loading data...");
        },
        success: function (result) {
            putTableData(result);
        },
        error: function (response) {
            $("#no_results h5").html("Something went wrong");
            $("#list_data").hide();
        }
    });
}

$("#next").click(function () {
    // load the next page data and

    // put the result to the table body

    // by making ajax call to next available url

    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (result) {
            putTableData(result);
        },
        error: function(response){
            console.log(response);
        }
    });
})

$("#previous").click(function () {
    // load the previous page data and

    // put the result to the table body

    // by making ajax call to previous available url

    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (result) {
            putTableData(result);
        },
        error: function(response){
            console.log(response)
        }
    });
})

function getCategories() {
  // fill the options of countries by making ajax call
  // obtain the url from the countries select input attribute

  let url = $("#categories").attr("url");

  // makes request to getCountries(request) method in views

  $.ajax({
    method: 'GET',
    url: url,
    data: {},
    success: function (result) {

      categories_option="<option value='all' selected>All Categories</option>";
      $.each(result["categories"], function (a, b) {
          categories_option += "<option>" + b + "</option>"
      });
      $("#categories").html(categories_option);
    },
    error: function(response){
      console.log(response)
    }
  });
}
