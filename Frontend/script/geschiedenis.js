const setchart = function() {
  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end

  var chart = am4core.create('c-chart', am4charts.XYChart);
  chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

  chart.data = [
    {
      country: 'USA',
      visits: 237
    },
    {
      country: 'China',
      visits: 1882
    },
    {
      country: 'Japan',
      visits: 1809
    },
    {
      country: 'Germany',
      visits: 1322
    },
    {
      country: 'UK',
      visits: 1122
    },
    {
      country: 'France',
      visits: 1114
    },
    {
      country: 'India',
      visits: 984
    },
    {
      country: 'Spain',
      visits: 711
    },
    {
      country: 'Netherlands',
      visits: 665
    },
    {
      country: 'Russia',
      visits: 580
    },
    {
      country: 'South Korea',
      visits: 443
    },
    {
      country: 'Canada',
      visits: 441
    }
  ];

  var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
  categoryAxis.renderer.grid.template.location = 0;
  categoryAxis.dataFields.category = 'country';
  categoryAxis.renderer.minGridDistance = 40;
  categoryAxis.fontSize = 11;

  var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
  valueAxis.min = 0;
  valueAxis.max = 2000;
  valueAxis.strictMinMax = true;
  valueAxis.renderer.minGridDistance = 30;

  /*
    // this is exactly the same, but with events
    axisBreak.events.on("over", function() {
      axisBreak.animate(
        [{ property: "breakSize", to: 1 }, { property: "opacity", to: 0.1 }],
        1500,
        am4core.ease.sinOut
      );
    });
    axisBreak.events.on("out", function() {
      axisBreak.animate(
        [{ property: "breakSize", to: 0.005 }, { property: "opacity", to: 1 }],
        1000,
        am4core.ease.quadOut
      );
    });*/

  var series = chart.series.push(new am4charts.ColumnSeries());
  series.dataFields.categoryX = 'country';
  series.dataFields.valueY = 'visits';
  series.columns.template.tooltipText = '{valueY.value}';
  series.columns.template.tooltipY = 0;
  series.columns.template.strokeOpacity = 0;

  // as by default columns of the same series are of the same color, we add adapter which takes colors from chart.colors color set
  series.columns.template.adapter.add('fill', function(fill, target) {
    return chart.colors.getIndex(target.dataItem.index);
  });
}; // end am4core.ready()

const maak_chart = function(geschiedenis) {
  console.log(geschiedenis);
  let dagen = [];
  let gegevens = [];
  for (dag of geschiedenis) {
    //unshift om de volgorde om te draaien
    dagen.unshift(dag.datum);
    gegevens.unshift(dag.minuten);
  }
  console.log(dagen);

  var ctx = document.querySelector('.c-chart');
  var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'bar',

    // The data for our dataset
    data: {
      labels: dagen,
      datasets: [
        {
          label: 'Aantal gespeelde Minuten',
          backgroundColor: '#38beff',
          borderColor: '#02002e',
          data: gegevens
        }
      ]
    },

    // Configuration options go here
    options: {}
  });
};

const init = function() {
  console.log('Dom geladen');
  //setchart();
  //handleData(endpoint + 'geschiedenis', maak_chart);
  socket.emit('getgeschiedenis');
  socket.on('setgeschiedenis', function(geschiedenisdata) {
    console.log(geschiedenisdata);
    maak_chart(geschiedenisdata);
  });
  console.log(localStorage.getItem('userid'));
};
console.log(localStorage.getItem('allow'));
if (localStorage.getItem('allow') != 'true') {
  console.log('redirect now');
  window.location.replace('index.html');
}

document.addEventListener('DOMContentLoaded', init);
