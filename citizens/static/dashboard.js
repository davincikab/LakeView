$(function(){ 
  var data;
  var condition;
  
  //  Write a promise to fetch the data in parallel
    // var this_data = getData();
    // var other_data = otherData();

    // var myPromise = new Promise.all([this_data,other_data]);
  // Blablablabla

$.getJSON('/static/data.geojson')
    .done(function(res){
      data = res.features;

      // Extract categories
      condition = processData(data)

      // Counts
      updateTables(data,'one');
      updateCount(data, 'one','dough-drains');

      // Data cleaning
      cleanConditionData(data,'drain-condition');
      cleanCulvertMaterial(data,'drain-materials');
    }).fail(function (){
      console.log("Failed to load the data");
});

$.getJSON('/static/data.geojson')
    .done(function(res){
      data = res.features;

      // Extract categories
      condition = processData(data)

      // Counts
      updateTables(data,'three');
      updateCount(data, 'three','dough-network');

      // Data cleaning
      cleanConditionData(data,'network-condition');
      cleanCulvertMaterial(data,'network-materials');
    }).fail(function (){
      console.log("Failed to load the data");
});

function getResourceData(){

}

function getZoneData(){

}

function processData(data){
  // console.log(data);
  return {
    condition:[...new Set(Object.values(data.map(k => k.properties.Condition)))],
    time: [...new Set(Object.values(data.map(k=> k.properties.InspectionDate)))]
  };
}

function updateTables(data,id){
  let div = document.querySelectorAll('#list');
  data = data.filter(datum => datum.properties.Condition == "Uknown");
  // console.log(div);
  for(let datum of data){
    let str = `<p class="border-bottom">${datum.properties.name} <strong>::</strong><span class="text-gold ml-2" data-content="${datum.geometry.coordinates}" onClick="listenEvent(this)">${datum.properties.Notes}</span></p>`;
    div[0].innerHTML += str;
    div[1].innerHTML += str;
  }
  
}

function updateCount(data, id, plotId){
  // Inspection date 
  var recentInspection = new Date('2019/11/14 12:28:09');
  var inspectedCrossdrains = data.filter( datum => new Date(datum.properties.InspectionDate)>recentInspection).length;
  var verifiedCrossDrains = data.filter( datum => new Date(datum.properties.InspectionDate)<recentInspection).length;;

  var elements = $(`div#${id}`).find('h2');
  $(elements[0]).html(` ${inspectedCrossdrains}`);
  $(elements[1]).html(`<i class="fa fa-tint"></i> ${verifiedCrossDrains}`);

  plotPie([['Inspected',(inspectedCrossdrains*100/data.length)],['Verified',(verifiedCrossDrains*100/data.length)]],plotId);
  
}

// Reuse the two function even on culvert(Drainage) network data
function cleanConditionData(data,id){
  var dataPlot = [];
  for(let cond of condition.condition){
    dataPlot.push(
      data.filter(datum => datum.properties.Condition == cond).length
    );
  }

  // console.log(dataPlot);
  plot_data([{name:'Condition',data:dataPlot,colorByPoint:true}],'column',id, condition.condition,'');
}

function cleanCulvertMaterial(data,id){
  var dataPlot = [];
  for(let cond of condition.condition){
    dataPlot.push(data.filter(datum=> datum.properties.Condition == cond).length
    );
  }

  plot_data([{name:'Materials',data:dataPlot,colorByPoint:true}],'bar',id, condition.condition,'');
}

function plot_data(data, type, id, category, title){
  // Column plots
  areacolors = (function(){
      let colors= ['#d73027','#f46d43'];
      return colors
  }());

  function getColor(condition){
    return condition== "Excellent"?'#003300':condition== "Very Good"?'#006600':condition== "Good"?'#009900':condition== "Fair"?'#99CC00':condition== "Poor"?'#FF6600':condition== "Unknown"?'#FF3300':'#FF0000';
  }

  let colors =category.map(k=> getColor(k));

  let xAxis;
  let series;

  if (type != "line") {
    // Check plot type
    xAxis = [{
        categories: category,
        labels: {
            step: 0
        },
        legend:false
    }];

    series = {
          label: {
              connectorAllowed: false,
          },
          stacking: 'normal',
      }
  }else{
    xAxis = [{
      crosshair:true,
    }
  ];

    series = {
          label: {
              connectorAllowed: false,
          },
          pointStart: 2015
      }
  }


    // Column plots
    Highcharts.chart(id, {
        chart: {
            backgroundColor:'#202020',
            type: type
        },
        legend: {
            enabled: false
        },
        credits:{
          enabled:false
        },
        title: {
            text: `${title} `
        },
        xAxis:xAxis,
        yAxis: {
            // min: 0,
            title: {
                text: null
            },labels: {
                formatter: function () {
                    return Math.abs(this.value) + '';
                }
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
         series: series
       },
        series: data,
        responsive: {
          rules: [{
              condition: {
              maxWidth: 500
            },
            chartOptions: {
            legend: {
              layout: 'horizontal',
              align: 'center',
              verticalAlign: 'bottom'
            }
        }
        }]
      }
    });
}

function plotPie(data,id, title){
  // console.log(data);
  Highcharts.chart(id, {
    chart: {
        backgroundColor: '#202020',
        plotBorderWidth: 0,
        plotShadow: false
    },
    credits:{
      enabled:false
    },
    title: {
        text: data[0][1] +"%",
        align: 'center',
        verticalAlign: 'middle',
        y: 40
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: false,
                distance: -50,
                style: {
                    fontWeight: 'bold',
                    color: 'white'
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '75%'],
            size: '110%',
            colors: ['#99FF00','#CC9900']
        },
        series:{
          colors:['red']
        }
    },
    series: [{
        type: 'pie',
        name: '',
        innerSize: '70%',
        data: data
    }]
  });
}

});
