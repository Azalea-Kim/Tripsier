// This js file is to support drag and drop for planning

/**
       * 计算两个日期之间的天数
       *  date1  开始日期 yyyy-MM-dd
       *  date2  结束日期 yyyy-MM-dd
       *  如果日期相同 返回一天 开始日期大于结束日期，返回0
       */
var num = 0;
var global = 1;
let tabsCount = 0;
let startD;
let endD;
function  getDaysBetween(date1,date2){
    var  startDate = Date.parse(date1);
    var  endDate = Date.parse(date2);
    if (startDate>endDate){
        return 0;
    }
    if (startDate===endDate){
        return 1;
    }
    var days=(endDate - startDate)/(1*24*60*60*1000);
    days = days + 1;
    return  days;
}

function getTabs(){
    tabsCount++;
       $('#tabs').empty();
     var result = document.getElementById("demo").value;
     var results = result.split("-");
     var start = results[0].replace(" ","");
     var end = results[1].replace(" ","");
     start = start.split("/");
     end = end.split("/");

     var startDate = start[2] +"-"+ start[1] +"-"+ start[0];
     var endDate = end[2] +"-"+ end[1] +"-"+ end[0];
     console.log(startDate,endDate)
     startD = startDate;
     endD = endDate;
     var days = getDaysBetween(startDate,endDate);
    var tabs = $('#tabs').bootstrapDynamicTabs().addTab({
        title:'Tabs',
	    text:'',
        closable: false
      });

    for(var i = 1; i <= days; i++) {
        console.log('tab' + i.toString()+"-"+tabsCount.toString());
        tabs.addTab({
            title: 'Day'+i.toString(),
            id: 'tab' + i.toString()+tabsCount.toString(),

		    loadStyles: ['../static/css/test.css','../static/css/test2.css'],
            html: "<div class='example example--outside'>"+
              "<div class='drag-zone plan-item' id='tab-"+i+"-1'></div>"+
              "<p class='line_01'> Destination </p>"+
              "<div class='drag-zone plan-item' id='tab-"+i+"-2'></div>"+
              "<div class='drag-zone plan-item' id='tab-"+i+"-3'></div>"+
              "<div class='drag-zone plan-item' id='tab-"+i+"-4'></div>"+
              "<div class='drag-zone plan-item' id='tab-"+i+"-5'></div>"+
              "<div class='drag-zone plan-item' id='tab-"+i+"-6'></div>"+
              "</div>"

          })
    }

    getDestinations();

}

function getDestinations(){
    num = 0;
     $.ajax({
        url: "/destInfo",
        method: "POST",
        data: {
            "command": "Get destinations"
        },
        success: function (res) {
            var htmlStr = ""
            var destinations = res["destinations"]
            for (var i = 0; i < destinations.length; i++) {
                var name = destinations[i][0]
                var image_pace = "data:;base64," + (destinations[i][1])
                var info = destinations[i][2]
                // var score = destinations[i][3]
                // var price = destinations[i][4]
                var id = destinations[i][3]
                var country = destinations[i][4]
                var string =
                            "<div class='drag-zone' id='draggable-container-destination-"+id+"-"+global+"'>"+
                                "<div class='draggable-form' style='width: 80%' id='draggable-task-destination-"+ id +"-"+global+"' draggable='true'>" +
                                    "<div class='listing-item listing-item-3 mb-3 destination'>" +
                                        "<div class='listing-image'>" +
                                            `<img class='img-fluid' src="${image_pace}" alt='#'>` +
                                        "</div>" +
                                        "<div class='listing-details'>" +
                                            "<div class='listing-title d-flex justify-content-between'>" +
                                                "<h5 class='mb-0'>" +
                                                    "<a href='#' class='title mb-0'>"+name+"</a>" + "</h5>" +
                                                "<div class='country-flags'>" +
                                                    `<img class='img-fluid shadow-sm' src="/static/images/country-flags/${country}.jpg"` + " alt='#'>" +
                                                "</div>" +
                                            "</div>" +
                                            "<a href='#' class='listing-loaction'>" + "<i class='fa fa-location-dot'></i>" + info+ "</a>" +
                                            "<div class='listing-rating d-flex justify-content-between'>" +
                                                "<div class='d-flex'>" +
                                                    "<div class='rating'>" +
                                                        "<i class='fa-solid fa-star me-1 text-yellow'></i><span>"+5+"/ 5</span>" +
                                                    "</div>" +
                                                "</div>" +
                                            "</div>" +
                                        "</div>" +
                                    "</div>" +
                                "</div>" +
                            "</div>"
                htmlStr = htmlStr + string
                global++;
            }
            document.getElementById("displaylist").innerHTML = htmlStr
            drop();
        }
    })
}

function getAttractions(desid) {
     $.ajax({
        url: "/destInfo",
        method: "POST",
        data: {
            "command": "Get attractions",
            "destination": desid
        },
        success: function (res) {
            var htmlStr = ""
            var attractions = res["attractions"]
            for (var i = 0; i < attractions.length; i++) {
                var name = attractions[i][0]
                var image_pace = "data:;base64," + (attractions[i][1])
                var info = attractions[i][2]
                var score = attractions[i][3]
                var price = attractions[i][4]
                var id = attractions[i][5]
                var country = attractions[i][6]
                var string =
                            "<div class='drag-zone' id='draggable-container-attraction-"+id+"-"+global+"'>"+
                                "<div class='draggable-form' style='width: 80%' id='draggable-task-attraction-"+ id +"-"+global+"' draggable='true'>" +
                                    "<div class='listing-item listing-item-3 mb-3 attraction'>" +
                                        "<div class='listing-image'>" +
                                            `<img class='img-fluid' src="${image_pace}" alt='#'>` +
                                        "</div>" +
                                        "<div class='listing-details'>" +
                                            "<div class='listing-title d-flex justify-content-between'>" +
                                                "<h5 class='mb-0'>" +
                                                    "<a href='#' class='title mb-0'>"+name+"</a>" + "</h5>" +
                                                "<div class='country-flags'>" +
                                                    `<img class='img-fluid shadow-sm' src= "/static/images/country-flags/${country}.jpg" alt='#'>` +
                                                "</div>" +
                                            "</div>" +
                                            "<a href='#' class='listing-loaction'>" + "<i class='fa fa-location-dot'></i> The Location : " + info+ "</a>" +
                                            "<div class='listing-rating d-flex justify-content-between'>" +
                                                "<div class='d-flex'>" +
                                                    "<div class='rating'>" +
                                                        "<i class='fa-solid fa-star me-1 text-yellow'></i><span>"+score+"/ 5</span>" +
                                                    "</div>" +
                                                "</div>" +
                                                "<div class='price'>" +
                                                    "<span class='text-decoration-line-through'>$899</span>"+price+
                                                "</div>" +
                                            "</div>" +
                                        "</div>" +
                                    "</div>" +
                                "</div>" +
                            "</div>"
                htmlStr = htmlStr + string
            }
            document.getElementById("displaylist").innerHTML = htmlStr
            drop();
        }
    })
}

function drop(){


    for (const draggableElement of document.querySelectorAll(".draggable-form")){
        // add dragstart event listener (in here, transfer data)
        draggableElement.addEventListener("dragstart", function (e) {
        e.dataTransfer.setData("text", draggableElement.id + "," + draggableElement.parentElement.id)
        })
    }

    // 每个drop zone添加dropover & drop事件监听器
    for (const dropZone of document.querySelectorAll(".drag-zone")){

        dropZone.addEventListener("dragover", e => {
            e.preventDefault();
            dropZone.classList.add("drop-zone-over")
            // alert(1)

        })

        dropZone.addEventListener("dragleave", e=> {
            e.preventDefault();
            dropZone.classList.remove("drop-zone-over");
            dropZone.style.height = height+"px"
            // alert(2)

        })


        dropZone.addEventListener("drop", e => {
            e.preventDefault();
            const data = e.dataTransfer.getData("text").split(",");
            const draggedElement = document.getElementById(data[0]);
            const children = dropZone.children
            var list = draggedElement.id.split("-");
            var type = list[2];
            var desid = list[3];


            if (children.item(0) === null){
                dropZone.appendChild(draggedElement)
                if(num == 0 && type == "destination"){
                    getAttractions(desid);
                    // alert(3)
                    num = 1;
                }
            }else{

                const swapDraggableElement = document.getElementById(children.item(0).id)
                const swapZone = document.getElementById(data[1]);
                swapZone.appendChild(swapDraggableElement)
                dropZone.appendChild(draggedElement)

            }

            if(dropZone.id === "trash-can"){
                num = 0;
                if(type === "destination"){
                    getDestinations();
                }
                var parent = dropZone.parentNode;
                parent.innerHTML="<div class='drag-zone trash-can' id='trash-can' style='height: 50px;'>🗑</div>"

            }else{
                dropZone.classList.remove("drop-zone-over");
            }

        })
    }
}

function submit(){

    var text = "";
    var tabNum = (document.querySelectorAll('.tab-pane')).length - 1;
    
    for (var i = 1; i <= tabNum; i ++){
        // text = text + i +":";
        destination="";
        attraction="";
        accommodation = "";
        var tab = document.getElementById('tab' + i.toString()+tabsCount.toString()).firstChild;
        planNodes = tab.children;
        console.log(planNodes);
        for (var t = 1; t < planNodes.length; t++){ 
            planNode = document.getElementById('tab-'+i+'-'+t);
            console.log(planNode.childNodes.length);
            if(planNode.childNodes.length !=0 ){
                
                list = (planNode.firstChild.id.split('-'));
                type = list[2];
                id = list[3];
                console.log(type);
                // if(type == "destination"){
                //     destination = id +";";
                // }
                if(type == "attraction"){
                    attraction = attraction + "attr"  + id +",";
                }
                if(type == "accommodation"){
                    accommodation = "acc" + accommodation + id +",";
                }
            }
        }
        text = text + accommodation + attraction + "||";
    }



    var dex1 = text.lastIndexOf("||");
    text = text.substring(0,dex1);
    var dex2 = text.lastIndexOf(",");
    text = text.substring(0,dex2);
    text = startD+","+endD +"||"+ text;
    console.log("submit text:"+text)

    $.ajax({
        url: "/tabs",
        method: "POST",
        data: {
            "text": text

        },
        success: function (res) {
            alert("Submit Successfully!");
        }
   })
}
