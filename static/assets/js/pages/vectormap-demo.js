/*
 Template Name: Drezoc - Responsive Bootstrap 4 Admin Dashboard
 Author: Myra Studio
 File: Vector Map
*/
var latlng;


(function($) {
  'use strict';
  $(function() {
      var path = window.location.href
      var list_id = path.split("/")
      var id = parseInt(list_id[list_id.length-1])
      var name
      var coord
      var latlng_coord
      var lat_list
      var listener = 0

  $.ajax({
      type: "POST",//method is post
      url: "/admin/destination/detail/" + id + "/coord",//the url of the backend to receive the parameters
      //增加一个休眠程序
      success: function (data) {
        name = data['name']
        coord = data['coord']
        lat_list = coord.split(",")
        latlng_coord = [parseInt(lat_list[0]),parseInt(lat_list[1])]
        draw_map()
      }
    })


    function draw_map() {
        if ($("#world-map-markers").length) {
            $('#world-map-markers').vectorMap({
                map: 'world_mill_en',
                scaleColors: ['#df3554', '#df3554'],
                normalizeFunction: 'polynomial',
                hoverOpacity: 0.7,
                hoverColor: false,
                regionStyle: {
                    initial: {
                        fill: '#2e7ce4'
                    }
                },
                markerStyle: {
                    initial: {
                        r: 9,
                        'fill': '#df3554',
                        'fill-opacity': 0.9,
                        'stroke': '#fff',
                        'stroke-width': 7,
                        'stroke-opacity': 0.4
                    },

                    hover: {
                        'stroke': '#fff',
                        'fill-opacity': 1,
                        'stroke-width': 1.5
                    }
                },
                backgroundColor: 'transparent',
                markers: [
                    {
                        latLng: latlng_coord,
                        name: name
                    }]
            });
        }
    }

  });
})(jQuery);