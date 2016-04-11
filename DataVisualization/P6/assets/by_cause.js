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
  var svg = d3.select("#by-cause .visualization")
    .append('svg')
    .attr('width', 960)
    .attr('height', 600);

  /* Initialize tooltip with info */
  var tip = d3.tip().attr('class', 'd3-tip').html(function(d) {
    return 'Group: ' + d.group + '<br> Cause: ' + d.name +
      '<br> Death: <strong>' + d.count +
      '</strong><br> IDC-10 Codes: ' + d.codes;
  });

  svg.call(tip);

  // Main draw function. Called, when data available
  var draw = function(data) {

    // Setup treemap layout
    var treemap = d3.layout.treemap()
      .size([960, 700])
      .value(function(d) {
        return d.count;
      });

    var position = function() {
      this.style("x", function(d) {
          return d.x;
        })
        .style("y", function(d) {
          return d.y;
        })
        .style("width", function(d) {
          return Math.max(0, d.dx - 1);
        })
        .style("height", function(d) {
          return Math.max(0, d.dy - 1);
        });
    }

    var drawNodes = function(data) {
      // Set colors for categories
      var color = d3.scale.ordinal()
        .domain(data.children.map(function(d) {
          return d.name;
        })).range(colorsList.slice(0, 26));

      // Clean before draw
      svg.selectAll("rect").remove();

      var node = svg.datum(data).selectAll("rect")
        .data(treemap.nodes);

      node.exit().remove();

      node.enter().append("svg:g")
        .call(position)
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)


      node.append("svg:rect")
        .call(position)
        .style("fill", function(d) {
          return color(d.name);
        })
        .style("fill-opacity", function(d) {
          return d.children ? 1 : 0;
        })
        .style("stroke", function(d) {
          return "#eee"
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
    .defer(d3.json, "./data/by_cause_all.json")
    .defer(d3.json, "./data/by_cause_female.json")
    .defer(d3.json, "./data/by_cause_male.json")
    .awaitAll(function(error, results) {
      if (error) throw error;
      draw(results);
    });

}, false);
