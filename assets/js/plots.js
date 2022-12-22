const incident = d3.csv("assets/js/data_files/incident.csv");
const weapon = d3.csv("assets/js/data_files/weapon_state.csv");
const shooter = d3.csv("assets/js/data_files/shooter.csv");
const usaGeo = get_usaGeo();
const stateAbMap = get_stateAb();

console.log(incident);

function formatTime(value) {
    if(mode === "Over months"){
      let monthMap = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sept",
        10: "Oct",
        11: "Nov",
        12: "Dec"
      }
      return monthMap[value]
    } else {
      let quarterMap = {
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter",
      }
      return quarterMap[value]
    }
}

function formatAge(value) {
    const ageMapping = {
      1: "0-12",
      2: "13-17",
      3: "18-21",
      4: "22-30",
      5: "31-50",
      6: "50+"
    }
    return ageMapping[value]  
}

function plot1(){
    const q1_change_over_year = d3.rollups(incident , v=>v.length, d=>d.Year)
    .map( data => ({
    "Year": data[0],
    "Count": data[1]
    }) )
    .sort((a,b) => d3.ascending(a.Year , b.Year));

    const q1_years = d3.map(q1_change_over_year , d=>d.Year);
    const q1_extend = d3.extent(q1_years);
    const q1_maxIncident = d3.max(d3.map(q1_change_over_year , d=>d.Count));
    console.log(q1_extend);
    // setup margin
    const margin = {top: 20, right: 10, bottom: 60, left: 50};
    const visWidth = 1152 - margin.left - margin.right;
    const visHeight = 600 - margin.top - margin.bottom;
  
    // define axis
    const x = d3.scaleLinear()
        .domain(q1_extend)
        .range([0, visWidth]);
  
    const y = d3.scaleLinear()
        .domain([0, q1_maxIncident]).nice()
        .range([visHeight, 0]);
  
  
    // define svg
      const svg = d3.create('svg')
        .attr('width', visWidth + margin.left + margin.right)
        .attr('height', visHeight + margin.top + margin.bottom);
    
    const g = svg.append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);
  
  
   // line generator
    const line = d3.line()
        .curve(d3.curveBundle)
        .x(d => x(d.Year))
        .y(d => y(d.Count));
  
    // axes
    const xAxis = d3.axisBottom(x).ticks(10).tickFormat(d3.format("d"));
    const yAxis = d3.axisLeft(y);
  
  
    // draw axes and grids
  
    // x-axis and verical grid lines
    g.append('g')
        .attr('transform', `translate(0,${visHeight})`)
        .call(xAxis)
        .call(
          // clone the axis tick marks to create the grid lines
          g => g.selectAll('.tick > line').clone()
              .attr('y1', 0)
              .attr('y2', -visHeight)
              .attr('stroke', 'lightgray')
              .attr('stroke-width', 0.5)
        )
      // axis label
      .append('text')
        .attr('x', visWidth / 2)
        .attr('y', 40)
        .attr('fill', 'black')
        .attr('font-size', '15px')
        .attr('text-anchor', 'center')
        .text('Years');
  
    // y-axis and horizontal grid lines
    g.append('g')
        .call(yAxis)
        .call(
          // clone the axis tick marks to create the grid lines
          g => g.selectAll('.tick > line')
            // skip the first tick mark, since that's the baseline
            // of the x-axis
            .filter((d, i) => i !== 0).clone()
              .attr('x1', 0)
              .attr('x2', visWidth)
              .attr('stroke', 'lightgrey')
              .attr('stroke-width', 0.5)
        ).append('text')
          .attr("transform", "rotate(-90)")
          .attr("x", 0 - visHeight/2)
          .attr("dy", "-2.5em")
          .attr('fill', 'black')
          .attr('font-family', 'sans-serif')
          .style("text-anchor", "middle")
          .style("font-size","15px")
         .text('No. of Incidents');
  
    //draw line
    g.append('g')
      .selectAll('path')
      .data(q1_change_over_year)
      .join('path')
        .attr("d", d =>line(q1_change_over_year))
        .attr('fill', 'none')
        .attr('stroke', "red")
        .attr('stroke-width', 1.5)
        .attr("stroke-linecap", "round")
        .attr("stroke-linejoin", "round");
  
    // add title
       g.append('text')
        .attr('font-size', '15px')
        .attr('dominant-baseline', 'hanging')
        .attr('x', visWidth / 2 - 120)
        .attr('y', -margin.top)
        .text('Shooting incidents in US over the years');

  return svg.node();
}
  