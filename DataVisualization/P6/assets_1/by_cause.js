document.addEventListener('DOMContentLoaded', function() {
  // List of colors for categories.
  // We cannot use builtin because we have more than 20 categories
  var colorsList = ["#0cc402", "#fd0903", "#7a6b52", "#fd08a8", "#e39a03",
    "#0eb6e7", "#12bc8b", "#bd3aff", "#d393d1", "#c23c4d", "#6f8805",
    "#a840b3", "#e6956a", "#4f6bad", "#107a76", "#bd4702", "#a0a5b8",
    "#96b177", "#8c670d", "#029630", "#9b596e", "#fe6fa8", "#ff094b",
    "#ff08e2", "#b88dff", "#307b45", "#8662fe", "#08a1ff", "#baaa04",
    "#7bba04", "#f60b75", "#fe76de", "#ed8e96", "#ff725b", "#fe7b02",
    "#0ebcb7", "#af4689", "#bda853"
  ];

  // container for visualization
  var div = d3.select("#by-cause .visualization");

  // Main draw function. Called, when data available
  var draw = function(data) {

    // Setup treemap layout
    var treemap = d3.layout.treemap()
      .size([960, 700])
      .value(function(d) {
        return d.count;
      });

    var position = function() {
      this.style("left", function(d) {
          return d.x + "px";
        })
        .style("top", function(d) {
          return d.y + "px";
        })
        .style("width", function(d) {
          return Math.max(0, d.dx - 1) + "px";
        })
        .style("height", function(d) {
          return Math.max(0, d.dy - 1) + "px";
        });
    }

    var drawNodes = function(data) {
      // Set colors for categories
      var color = d3.scale.ordinal()
        .domain(data.children.map(function(d) {
          return d.name;
        })).range(colorsList.slice(0, 26));

      var node = div.html("").datum(data).selectAll(".node")
        .data(treemap.nodes);

      node.exit().remove();

      node.enter().append("div")
        .attr("class", "node")
        .call(position)
        .style("background", function(d) {
          return d.children ? color(d.name) : null;
        })
        .text(function(d) {
          return d.children ? null : d.name;
        });
    };

    // Draw initial F+M data
    drawNodes(data[0]);

    // Data switcher
    d3.selectAll("input").on("change", function change() {
      drawNodes(data[this.value]);
    });
  }

  // Download all necessary data files
  var q = d3_queue.queue()
    .defer(d3.json, "./data_v1/by_cause_all.json")
    .defer(d3.json, "./data_v1/by_cause_female.json")
    .defer(d3.json, "./data_v1/by_cause_male.json")
    .awaitAll(function(error, results) {
      if (error) throw error;
      draw(results);
    });

}, false);
