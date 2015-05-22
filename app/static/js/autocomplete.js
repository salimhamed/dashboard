$(document).ready(function() {

    // define web url
    var search_url = 'http://' + $SCRIPT_ROOT + '/search/_typeahead/'
    var prefetch_url = 'http://' + $SCRIPT_ROOT + '/search/_typeahead/prefetch'

    //Set up "Bloodhound" Options
    var suggestion_class = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('vval'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,

        // prefetch: {
        //     url: prefetch_url,
        //     filter: function(x) {
        //         return $.map(x.results, function(item) {
        //             return {vval: item.name};
        //         });
        //     }
        // },

        remote: {
             url: search_url + '%QUERY',
             filter: function(x) {
                 return $.map(x.results, function(item) {
                     return {vval: item.name};
                 });
             },
             wildcard: "%QUERY",
         }
    });

    // Initialize Typeahead with Parameters
    $('#bloodhound .typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'vval',
        displayKey: 'vval',
        limit: 10,
        source: suggestion_class
    });

});
