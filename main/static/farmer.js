
function doSearch() {
    console.log("search")
}

$(document).ready(function(){

    $("#searchbtn").click(function (e) {
        doSearch();
    })
    $("#searchbar").submit(function(e){
        doSearch();
    })

})