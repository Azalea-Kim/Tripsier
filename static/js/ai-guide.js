$(function() {
    $("#ask-ai-btn").click(function () {
        if (this.style.bottom === "50px"){
            this.style.background = "black";
            this.style.color = "white";
            this.style.bottom = "0";
            $("#ask-ai-container").css("bottom", "-50px");
        }else{
            this.style.bottom = "50px";
            this.style.color = "black";
            this.style.background = "linear-gradient(270deg, rgba(2, 29, 78, 0.681) 0%, rgba(31, 215, 232, 0.873) 60%)";
            $("#ask-ai-container").css("bottom", "0");
        }
    });

    $("#ai-search-btn").click(function () {

        $("#ai-response-container").css("visibility", "visible");
    })

    $("#close-response-btn").click(function (){
        $("#ai-response-container").css("visibility", "hidden");
    });
});