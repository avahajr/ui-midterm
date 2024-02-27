function doSearch(search_term) {
    console.log("searching for", search_term)
    if (isValidSearchTerm(search_term)) {
        $.ajax({
            url: '/search',
            type: "POST",
            // dataType: "json",
            contentType: 'application/json',
            data: JSON.stringify({search_term: search_term}),
            success: function (results) {
                $("#searchbar").val("");

                // display the template in results.
                $('body').html(results);
            },
            error: function (err) {
                console.error(this.error)
            }
        })
    }
    else {
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

})