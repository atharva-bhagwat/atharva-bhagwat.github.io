console.log("Active");
var svg1 = d3.select("#svg1");
svg1.append("circle")
       .attr("cx",100)
       .attr("cy", 100)
       .attr("r", 90)
       .attr("fill", "red");