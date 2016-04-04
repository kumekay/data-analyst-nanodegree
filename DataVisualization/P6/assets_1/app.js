document.addEventListener('DOMContentLoaded', function() {
  var svgByGenderAndAge = dimple.newSvg("#by-gender-and-age", 800, 600);
  d3.json("./data/by_gender_and_age.json", function(dataByGenderAndAge) {
    dataByGenderAndAge = dimple.filterData(dataByGenderAndAge, "Owner", [
      "Aperture", "Black Mesa"
    ]);
    var chartByGenderAndAge = new dimple.chart(svgByGenderAndAge,
      dataByGenderAndAge);
    chartByGenderAndAge.setBounds(70, 30, 340, 330);
    var x = chartByGenderAndAge.addCategoryAxis("x", ["Owner", "Month"]);
    x.addGroupOrderRule("Date");
    chartByGenderAndAge.addPctAxis("y", "Unit Sales");
    var s = chartByGenderAndAge.addSeries("SKU", dimple.plot.area);
    s.lineWeight = 1;
    s.barGap = 0.05;
    chartByGenderAndAge.addLegend(430, 20, 100, 300, "left");
    chartByGenderAndAge.draw();
  });
}, false);
