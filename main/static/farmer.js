// https://geocode.maps.co/search?q=&api_key=65e7561c5c34f657560788tpg3c734f

function doSearch(search_term) {
    console.log("searching for", search_term)
    if (isValidSearchTerm(search_term)) {
        $.ajax({
            url: '/search/' + search_term, type: "GET",

            data: JSON.stringify({search_term: search_term}), success: function (results) {
                $("#searchbar").val("");

                // display the template in results.
                $('body').html(results);

                // modify browser history so that reloading the page doesn't lose the query
                history.pushState({page: "search results for'" + search_term + "'"}, "", "/search/" + search_term)
            }, error: function (err) {
                console.error(this.error)
            }
        })
    } else {
        console.error("invalid search term: all whitespace. please try again.")
    }
}

function isValidSearchTerm(search_term) {
    if (search_term.trim() === '') {
        $("#searchbar").focus()
        $("#searchbar").val("")
        return false
    }
    return true
}


function validateEntry() {
    let checkboxes = $('input[name="days"]:checked')
    let selectedDays = checkboxes.map(function () {
        return this.value;
    }).get();
    let newEntry = {
        market_name: $("#market_name").val(),
        borough: $("#borough").val(),
        image: $("#image").val(),
        street_address: $("#street_address").val(),
        latitude: 0,
        longitude: 0,
        days: selectedDays,
        vendors_list: $("#vendors").val().split(", "),
        year_round: $('input[name="year_round"]:checked').val(),
        summary: $("#summary").val()
    };
    let errors = {};
    console.log(newEntry)

    for (let prop in newEntry) {
        if (newEntry.hasOwnProperty(prop)) {
            let value = newEntry[prop];
            let dataType = typeof value;

            // Validate data types
            switch (prop) {
                case 'latitude':
                case 'longitude':
                    // Validate numeric values for latitude and longitude
                    if (dataType !== 'number') {
                        errors[prop] = 'Should be a numeric value.';
                    }
                    break;
                case 'year_round':
                    // Validate boolean value for year_round
                    if (!(newEntry["year_round"] === 'true' || newEntry['year_round'] === 'false')) {
                        errors[prop] = 'Should be a boolean value.';
                    }
                    break;
                // Add additional cases for other properties if needed
            }
        }
    }

    // Output errors or do something with them
    if (Object.keys(errors).length > 0) {
        console.error('Validation errors:', errors);
        // Handle errors as needed
    } else {
        console.log('Validation successful. Do something with the entry:', newEntry);
        $.ajax({
            url: '/add',
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(newEntry),
            success: function (data) {
                console.log("successfully submitted", data)
                // clear all data fields


            },
            error: function (e) {
                console.error("while input was valid, there was an error adding new market:", e)
            }
        });
    }
}

$(document).ready(function () {

    $("#searchbtn").click(function (e) {
        e.preventDefault();
        let searchTerm = $("#searchbar").val();
        doSearch(searchTerm);

    })
    $("#searchbar").submit(function (e) {
        e.preventDefault();
        let searchTerm = $("#searchbar").val();
        doSearch(searchTerm);
    })

    $("#submit-form").click(function(e) {
        e.preventDefault();
        console.log("submit")
        validateEntry();
    })

})