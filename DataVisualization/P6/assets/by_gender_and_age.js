document.addEventListener('DOMContentLoaded', function() {
  var svgByGenderAndAge = dimple.newSvg("#by-gender-and-age", 600, 500);
  d3.json("./data/by_gender_and_age.json", function(dataByGenderAndAge) {
    /**
     * Year switcher chart
     */
    // Create the switcher chart object
    var switcher = new dimple.chart(svgByGenderAndAge,
      dataByGenderAndAge);

    // Place the year switcher above main chart
    switcher.setBounds(50, 10, 500, 30);

    var y = switcher.addMeasureAxis("y", "Deaths");
    y.hidden = true;

    // Use sales for bar size and hide the axis
    var x = switcher.addCategoryAxis("x", "Year");

    // Add the bars to the indicator and add event handlers
    var sS = switcher.addSeries(null, dimple.plot.bar);
    sS.addEventHandler("click", switchYear);

    // Draw switcher
    switcher.draw();

    // Remove unused elements
    x.titleShape.remove();
    x.shapes.selectAll("line,path").remove();

    // Add some design
    // default colors
    var idleColor = "#ccc";
    var activeColor = "#99f";

    // Move labels inside
    x.shapes.selectAll("text")
      .attr("transform", "translate(0, -25)");

    // Set initial active color and switcher style
    sS.shapes
      .attr("rx", 5)
      .attr("ry", 5)
      .style("fill", function(d) {
        return (d.x === 2011 ? activeColor : idleColor)
      })
      .style("stroke", function() {
        "#eee"
      })
      .style("opacity", 0.4);

    /**
     * Main Chart
     */
    // Create Chart Object
    var chartByGenderAndAge = new dimple.chart(svgByGenderAndAge,
      dataByGenderAndAge);
    // Set Chart and Legend sizes
    chartByGenderAndAge.setBounds(50, 60, 500, 320);
    chartByGenderAndAge.addLegend(
      50, 450, 500, 100, "left");

    var y = chartByGenderAndAge.addCategoryAxis("x", ["Age Group",
      "Sex"
    ]);
    var x = chartByGenderAndAge.addMeasureAxis("y", ["Deaths"]);
    x.overrideMax = 200000;
    var s = chartByGenderAndAge.addSeries("Sex",
      dimple.plot.bar);
    s.interpolation = "step";

    // Setup right colors
    chartByGenderAndAge.defaultColors = [
      new dimple.color("#E05F4E"), // Set a red fill with a blue stroke
      new dimple.color("#26C7E0")
    ]

    // setup storyboard
    var onSwitchYear = function(e) {
      sS.shapes
        .transition()
        .style("fill", function(d) {
          return (String(d.x) === String(e) ? activeColor :
            idleColor)
        })
    }

    var genderAndAgeStoryboard = chartByGenderAndAge.setStoryboard(
      "Year", onSwitchYear);

    // On click on switcher
    function switchYear(e) {
      genderAndAgeStoryboard.goToFrame(String(e.xValue));
      genderAndAgeStoryboard.pauseAnimation();
    }

    chartByGenderAndAge.draw();
    // Remove labels
    genderAndAgeStoryboard.storyLabel.remove();

    // Disable animation
    genderAndAgeStoryboard.pauseAnimation();
  });
}, false);
