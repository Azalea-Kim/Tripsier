function sendReviewAccommodation(sender_id,accommodation_id) {
    //Input A sender's id and then to the backend
     $.ajax({
         type: "POST",//method is post
         url: "/reviewReceiveAccommodation" ,//the url of the backend to receive the parameters
         data: $('#review_form').serialize()+"&sender_id="+sender_id+"&accommodation_id="+accommodation_id,
         success: function (data) {
             sender = data.sender_name
             content = data.content
             time = getTime()
             $('#review-area').append("<div>\n" +
                 "            <p>Content:" + content + " </p>\n" +
                 "            <p>Sender:"+ sender +"</p>\n" +
                 "        </div>")
         }
     })
}

function sendReviewAttraction(sender_id,attraction_id) {
    //Input A sender's id and then to the backend
     $.ajax({
         type: "POST",//method is post
         url: "/reviewReceiveAttraction" ,//the url of the backend to receive the parameters
         data: $('#review_form').serialize()+"&sender_id="+sender_id+"&attraction_id="+attraction_id,
         success: function (data) {
             sender_name = data.sender_name
             sender_avatar = data.sender_avatar
             content_chat = data.content
             sender_rate = data.rate
             console.log(data)

             var str_part_1 = "<div class=\"d-block d-md-flex mb-4\">\n" +
                 "                            <div class=\"avatar mb-3\">\n" +
                 `                              <img src = \"data:;base64,${sender_avatar}\" class=\"rounded-circle img-fluid\" alt=\"...\">\n` +
                 "                            </div>\n" +
                 "                            <div class=\"p-4 border border-radius-sm ms-0 ms-md-3\">\n" +
                 "                              <div class=\"d-flex align-items-center\">\n" +
                 `                                <h6 class=\"mt-0\">${sender_name}</h6>\n` +
                 "                                <div class=\"d-flex ms-auto mb-3\">\n" +
                 `                                  <span class=\"px-2 border text-success border-radius-sm d-inline-block me-2\">${sender_rate}</span>\n` +
                 "                                  <ul class=\"list-unstyled d-flex mb-0\">\n" +
                 "\n"

             var str_star_1 =

                 "                                    <li><i class=\"fas fa-star text-warning\"></i></li>\n" +
                 "\n"

             var str_star_2 =

                 "                                    <li><i class=\"far fa-star text-light\"></i></li>\n" +
                 "\n"

             var str_part_2 =

                 "                                  </ul>\n" +
                 "                                </div>\n" +
                 "                              </div>\n" +
                 `                              <p>${content_chat}</p>\n` +
                 "                              <div class=\" d-flex flex-wrap\">\n" +
                 "                              </div>\n" +
                 "                            </div>\n" +
                 "                          </div>"

             var score_str = ""

             for(var i = 0; i < sender_rate; i++){
                 score_str += str_star_1
             }

             for(var i = 0; i< 5 - sender_rate; i++){
                 score_str += str_star_2
             }

             var final_str = str_part_1 + score_str + str_part_2

             $('#review-area').append(final_str)


             // $('#review-area').append("<div class=\"d-block d-md-flex mb-4\">\n" +
             //     "                            <div class=\"avatar mb-3\">\n" +
             //     `                              <img src = \"data:;base64,${sender_avatar}\" class=\"rounded-circle img-fluid\" alt=\"...\">\n` +
             //     "                            </div>\n" +
             //     "                            <div class=\"p-4 border border-radius-sm ms-0 ms-md-3\">\n" +
             //     "                              <div class=\"d-flex align-items-center\">\n" +
             //     `                                <h6 class=\"mt-0\">${sender_name}</h6>\n` +
             //     "                                <div class=\"d-flex ms-auto mb-3\">\n" +
             //     `                                  <span class=\"px-2 border text-success border-radius-sm d-inline-block me-2\">${sender_rate}</span>\n` +
             //     "                                  <ul class=\"list-unstyled d-flex mb-0\">\n" +
             //     "\n" +
             //     `                                       {% for i in range(0,${sender_rate}) %}\n` +
             //     "                                    <li><i class=\"fas fa-star text-warning\"></i></li>\n" +
             //     "                                      {% endfor %}\n" +
             //     "\n" +
             //     `                                      {% for i in range(0,5-${sender_rate}) %}\n` +
             //     "                                    <li><i class=\"far fa-star text-light\"></i></li>\n" +
             //     "                                      {% endfor %}\n" +
             //     "\n" +
             //     "                                  </ul>\n" +
             //     "                                </div>\n" +
             //     "                              </div>\n" +
             //     `                              <p>${content_chat}</p>\n` +
             //     "                              <div class=\" d-flex flex-wrap\">\n" +
             //     "                                <a class=\"bg-light text-dark border-radius-sm px-2 py-1 font-sm mb-2 mb-sm-0\" href=\"#\"> <i class=\"fas fa-reply pe-1\"></i> Reply Review </a>\n" +
             //     "                                <a class=\"bg-success-soft text-success border-radius-sm px-2 py-1 ms-3 font-sm mb-2 mb-sm-0\" href=\"#\"> <i class=\"far fa-thumbs-up pe-1\"></i> 56 Votes</a>\n" +
             //     "                                <a class=\"bg-danger-soft text-danger border-radius-sm px-2 py-1 ms-3 mb-2 mb-sm-0 font-sm\" href=\"#\"> <i class=\"far fa-thumbs-down pe-1\"></i> 06</a>\n" +
             //     "                              </div>\n" +
             //     "                            </div>\n" +
             //     "                          </div>")
         }
     })
}

function sendReviewWithOutAjax(){
    alert("You've send the review successfully!")
}

function getTime(){
    var myDate = new Date;
        var hour = myDate.getHours()
        var minute = myDate.getMinutes()

        if(parseInt(minute)<10){
            minute = "0" + minute
        }

        var str_time = hour.toString() + ":" + minute.toString()
        var pm_or_ar


        if(hour <= 12 && hour >= 0){
            pm_or_ar = "PM"
        }else{
            pm_or_ar = "AM"
        }
        return str_time+" "+pm_or_ar
}