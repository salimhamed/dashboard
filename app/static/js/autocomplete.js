$(document).ready(function() {
    // define web url
    var search_url = 'http://' + $SCRIPT_ROOT
    var prefetch_url = 'http://' + $SCRIPT_ROOT

    // Set up "Bloodhound" Options
    var suggestion_class = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('vval'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,

        prefetch: {
            url: search_url + '/_search_prefetch',
            filter: function(x) {
                return $.map(x.results, function(item) {
                    return {vval: item.name, vid: item.id};

                });
            }
        },

        remote: {
             url: search_url + '/_search?query=%QUERY',
             filter: function(x) {
                console.log(x)
                 return $.map(x.results, function(item) {
                     return {vval: item.name, vid: item.id};
                 });
             },
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
        name: 'vval',
        displayKey: 'vval',
        limit: 10,
        source: suggestion_class
    });

});
