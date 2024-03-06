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

async function validateEntry() {
    $(".warning").empty();

    let checkboxes = $('input[name="days"]:checked')
    let selectedDays = checkboxes.map(function () {
        return this.value;
    }).get();

    // check if the address is valid & retrieve lat, lng
    let zip = $("#zip").val();
    let street_address = $("#street_address").val()
    let [lat, lng] = [null, null]
    const apiKey = "AhCY625KQxZJyShmnHRlfjMuPw_dKcblIGFwahIKbuSn1iy0zkMHaLi0Ic9YbUzH";
    // call to validate the address & geolocate

    let isValid = true;

    // validation
    let summary = $("#summary").val()
    if (summary.trim() === '') {
        $(`#summary_warning`).append("Field cannot be empty.")
        $("#summary").focus().empty();
        isValid = false
    }

    let vendors = $("#vendors_list").val()
    if (vendors.trim() === '') {
        $(`#vendors_list_warning`).append("Field cannot be empty.")
        $("#vendors_list").focus().empty();
        isValid = false
    }
    let year_round = $('input[name="year_round"]:checked').val();
    if (year_round !== "true" && year_round !== "false") {
        $("#yearRoundWarning").append("Please select a value.");
        $("#year_round_true").focus()
        isValid = false
    }
    if (selectedDays.length === 0) {
        $('#daysWarning').append("Market must have at least one day.")
        $("#day_sunday").focus()
        isValid = false
    }

    let image = $("#image").val()
    if (image.trim() === '') {
        $(`label[for=image].warning`).append("Field cannot be empty.");
        $('#image').focus().empty();
        isValid = false

    }
    if (street_address.trim() === '') {
        $("label[for=street_address].warning").append("Field cannot be empty.")
        $('#street_address').focus().empty();
        isValid = false
    }
    if (isNaN(Number(zip))) {
        $("#zipWarning").append("Zipcode must be a number");
        $('#zip').focus();
        isValid = false
    } else if (isValid) {

        await $.ajax({
                url: `http://dev.virtualearth.net/REST/v1/Locations?key=${apiKey}&locality=New York City&adminDistrict=NY&addressLine=${street_address}&postalCode=${zip}`,
                type: "GET",
                dataType: 'json',
                success: function (data) {
                    [lat, lng] = data['resourceSets'][0]['resources'][0]['point']['coordinates']
                },
                error: function (e) {
                    console.error("Error:", e)
                }
            }
        )
        if (lat === null) {
            $("label[for=street_address].warning").append("Could not find matching address.")
            $('#street_address').focus();
            isValid = false
        }
    }

    let market_name = $("#market_name").val();
    if (market_name.trim() === '') {
        $(`label[for=market_name].warning`).append("Field cannot be empty.");
        $("#market_name").focus().val("");
        isValid = false
    }

    if (isValid) {
        let newEntry = {
            market_name: market_name,
            borough: $("#borough").val(),
            image: image,
            street_address: street_address,
            zip: Number(zip),
            latitude: Number(lat),
            longitude: Number(lng),
            days: selectedDays,
            vendors_list: vendors.split(", "),
            year_round: year_round,
            summary: summary,
        };
        console.log('Validation successful. Adding entry:', newEntry);
        $.ajax({
            url: '/add',
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(newEntry),
            success: function (data) {
                console.log("successfully submitted", data)
                // clear all data fields
                $("#add_market")[0].reset();
                $("#market_name").focus();
            },
            error: function (e) {
                console.error("while input was valid, there was an error adding new market:", e)
            }
        });
    } else {
        console.error('something was wrong with the input.')
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

    $("#submit-form").click(function (e) {
        e.preventDefault();
        validateEntry();
    })

})