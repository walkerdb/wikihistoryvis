$(document).ready(function() {
    console.log("ready!");

    $("form").on("submit", function(){
        console.log("the form has been submitted");

        var web_link = $('input[name="article_name"]').val();
        console.log(web_link);

        $.getJSON('')

    });
});