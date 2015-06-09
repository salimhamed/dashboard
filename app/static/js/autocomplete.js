$(document).ready(function() {
    // define web url
    var search_url = 'http://' + $SCRIPT_ROOT + '/search/_ta_remote/'
    var prefetch_url = 'http://' + $SCRIPT_ROOT + '/search/_ta_prefetch'

    // Set up "Bloodhound" Options
    var suggestion_class = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        sufficient: 5,
        prefetch: prefetch_url,
        remote: {
             url: search_url + '%QUERY',
             wildcard: "%QUERY"
         }
    });


    // Initialize Typeahead with Parameters
    $('.typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1,
    },
    {
        name: 'firm-company',
        display: 'name',
        limit: 10,
        source: suggestion_class
    });



    $(".fa.fa-plus").click(function(e){ window.location = "/create" })


});

// var bestPictures = new Bloodhound({
//   datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
//   queryTokenizer: Bloodhound.tokenizers.whitespace,
//   prefetch: '../data/films/post_1960.json',
//   remote: {
//     url: '../data/films/queries/%QUERY.json',
//     wildcard: '%QUERY'
//   }
// });
//
// $('#remote .typeahead').typeahead(null, {
//   name: 'best-pictures',
//   display: 'value',
//   source: bestPictures
// });
