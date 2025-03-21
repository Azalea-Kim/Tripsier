/*
 Template Name: Drezoc - Responsive Bootstrap 4 Admin Dashboard
 Author: Myra Studio
 File: Dashboard
*/

$(function() {
  'use strict';
  if ($("#morris-bar-example").length) {
    Morris.Bar({
      element: 'morris-bar-example',
      barColors: ['#2e7ce4', '#00c2b2'],
      data: [
        {
          y: 'Beijing',
          a: 80,
          b: 100
        },
        {
          y: 'Shanghai',
          a: 110,
          b: 130
        },
        {
          y: 'Guangzhou',
          a: 90,
          b: 110
        },
      {
        y: 'Chengdu',
        a: 80,
        b: 100
      },
      {
        y: 'Chongqing',
        a: 110,
        b: 130
      },
      {
        y: 'Hong Kong',
        a: 90,
        b: 110
      },
    ],
      xkey: 'y',
      ykeys: ['a', 'b'],
      hideHover: 'auto',
      gridLineColor: '#eef0f2',
      resize: true,
      barSizeRatio: 0.4,
      labels: ['Accommodations', 'Attractions']
    });
  }
  if ($("#morris-donut-example").length) {
    Morris.Donut({
      element: 'morris-donut-example',
      resize: true,
      colors: ['#2e7ce4', '#00c2b2', '#df3554'],
      data: [{
          label: "Shanghai",
          value: 12
        },
        {
          label: "Beijing",
          value: 30
        },
        {
          label: "Guangzhou",
          value: 20
        }
      ]
    });
  }
});

$( document ).ready(function() {
    
  var DrawSparkline = function() {
      $('#sparkline1').sparkline([25, 23, 26, 24, 25, 32, 30, 24, 19], {
          type: 'line',
          width: "100%",
          height: '50',
          chartRangeMax: 35,
          lineColor: '#2e7ce4',
          fillColor: 'rgba(46, 124, 228, 0.3)',
          highlightLineColor: 'rgba(0,0,0,.1)',
          highlightSpotColor: 'rgba(0,0,0,.2)',
          maxSpotColor:false,
          minSpotColor: false,
          spotColor:false,
          lineWidth: 1
      });

      $('#sparkline2').sparkline([24, 25, 32, 30, 24, 19, 32, 35, 23], {
          type: 'line',
          width: "100%",
          height: '50',
          chartRangeMax: 35,
          lineColor: '#627898',
          fillColor: 'rgba(98, 120, 152, 0.3)',
          highlightLineColor: 'rgba(0,0,0,.1)',
          highlightSpotColor: 'rgba(0,0,0,.2)',
          maxSpotColor:false,
          minSpotColor: false,
          spotColor:false,
          lineWidth: 1
      });

      $('#sparkline3').sparkline([30, 24, 19, 32, 35, 23, 12, 25, 35], {
          type: 'line',
          width: "100%",
          height: '50',
          chartRangeMax: 35,
          lineColor: '#f1bf43',
          fillColor: 'rgba(241, 191, 67, 0.3)',
          highlightLineColor: 'rgba(0,0,0,.1)',
          highlightSpotColor: 'rgba(0,0,0,.2)',
          maxSpotColor:false,
          minSpotColor: false,
          spotColor:false,
          lineWidth: 1
      });

      $('#sparkline4').sparkline([23, 12, 25, 35, 23, 12, 25, 35], {
          type: 'line',
          width: "100%",
          height: '50',
          chartRangeMax: 35,
          lineColor: '#df3554',
          fillColor: 'rgba(223, 53, 84, 0.3)',
          highlightLineColor: 'rgba(0,0,0,.1)',
          highlightSpotColor: 'rgba(0,0,0,.2)',
          maxSpotColor:false,
          minSpotColor: false,
          spotColor:false,
          lineWidth: 1
      });
      
    };
  
  DrawSparkline();
  
  var resizeChart;

  $(window).resize(function(e) {
      clearTimeout(resizeChart);
      resizeChart = setTimeout(function() {
          DrawSparkline();
      }, 300);
  });
});
