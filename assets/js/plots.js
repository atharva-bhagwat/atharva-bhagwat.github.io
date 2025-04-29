function format_json(data){

  let formatted_data = [];
  
  const data_length = Object.keys(data.Incident_ID).length

  for(let itr = 0; itr < data_length; itr++){
    let row = {}
    let keys = Object.keys(data)
    for(let col=0; col < keys.length; col++){
      row[keys[col]] = data[keys[col]][itr]
    }
    formatted_data.push(row)
  }

  return formatted_data;
}

const incident = format_json(get_incident());
const weapon = format_json(get_weapon());
const shooter = format_json(get_shooter());
const usaGeo = get_usaGeo();
const stateAbMap = get_stateAb();

const textColor = "#a79e8b";
const width = 900;

function formatTime(value) {
    let quarterMap = {
      1: "Spring",
      2: "Summer",
      3: "Fall",
      4: "Winter",
    }
    return quarterMap[value];
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
    return ageMapping[value];
}

function colorize(colorList, htmlElement) {
  var container = document.getElementById(htmlElement);
  container.className = "swatch";

  for (var key in colorList) {
      var boxContainer = document.createElement("DIV");
      boxContainer.className = "swatch-col";
      var box = document.createElement("DIV");
      var label = document.createElement("SPAN");

      label.innerHTML = `  ${key}`;
      box.className = "box";
      box.style.backgroundColor = colorList[key];

      boxContainer.appendChild(box);
      boxContainer.appendChild(label);

      container.appendChild(boxContainer);
 }
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
    // setup margin
    const margin = {top: 20, right: 10, bottom: 60, left: 50};
    const visWidth = width - margin.left - margin.right;
    const visHeight = 550 - margin.top - margin.bottom;
  
    // define axis
    const x = d3.scaleLinear()
        .domain(q1_extend)
        .range([0, visWidth]);
  
    const y = d3.scaleLinear()
        .domain([0, q1_maxIncident]).nice()
        .range([visHeight, 0]);
  
    // define svg
    const svg = d3.select("#incident_over_time").append('svg')
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
              .attr('stroke-width', 0.4)
              .attr('fill-opacity', 0.2)
        )
      // axis label
      .append('text')
        .attr('x', visWidth / 2)
        .attr('y', 40)
        .attr('fill', textColor)
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
              .attr('stroke-width', 0.4)
              .attr('fill-opacity', 0.2)
        )
        .append('text')
          .attr("transform", "rotate(-90)")
          .attr("x", 0 - visHeight/2)
          .attr("dy", "-2.5em")
          .attr('fill', textColor)
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
        .attr('fill', textColor)
        .attr('x', visWidth / 2)
        .attr('y', -margin.top)
        .style("text-anchor", "middle")
        .text('Shooting incidents in US over the years');
}

function plot2(){
  const incidentFilter = d3.filter(incident, d => d.Year >= 2000);
  const death_injuries_change = d3.rollups(incidentFilter , group => 
            ({
              "wounded" : d3.sum(group , d=>d.Victims_Wounded),
              "killed" : d3.sum(group , d=>d.Victims_Killed)
            }) , d=>d.Year)
        .map(data => ({
        "Year" : data[0],
        "Injuries" : data[1].wounded,
        "Deaths" : data[1].killed,
        "Total" : data[1].wounded + data[1].killed
        })).sort((a,b) => d3.ascending( a.Year , b.Year));
  const q2_maxValue = d3.max(death_injuries_change, d => d.Total);
  const q2_color = d3.scaleOrdinal()
      .domain(["Injuries", "Deaths"])
      .range(["#fed976", "#b10026"]);
    
  const q2_margin = ({top: 20, right: 10, bottom: 20, left: 50});
  const q2_height = 750; 

  const q2_visWidth = width - q2_margin.left - q2_margin.right;
  const q2_visHeight = q2_height - q2_margin.top - q2_margin.bottom;
  const svg = d3.select("#injuried_death_ratio").append('svg')
      .attr('width', width)
      .attr('height', q2_height);

  // sclaces and axis - 
  
  const q2_xScale = d3.scaleBand(death_injuries_change.map(d => d.Year),[q2_margin.left, width - q2_margin.right]).padding(0.2);
  const q2_yScale = d3.scaleLinear([ 0, q2_maxValue ],[ q2_visHeight, 0 ]);



  const q2_xAxis = d3.axisBottom(q2_xScale).tickSizeOuter(0);
  const q2_yAxis = d3.axisLeft(q2_yScale)

  const q2_stack = d3.stack().keys(["Injuries", "Deaths"])
  
  // Pass our data to the stack to generate the layer positions
  const chartData = q2_stack(death_injuries_change)
  
  const groups = svg.append('g')
    // Each layer of the stack goes in a group
    // the group contains that layer for all countries
    .selectAll('g')
    .data(chartData)
    .join('g')
      // rects in the same layer will all have the same color, so we can put it on the group
      // we can use the key on the layer's array to set the color
      .style('fill', (d,i) => q2_color(d.key))
  
  groups.selectAll('rect')
    // Now we place the rects, which are the children of the layer array
    .data(d => d)
    .join('rect')
      .attr('x', d => q2_xScale(d.data.Year))
      .attr('y', d => q2_yScale(d[1]))
      .attr('height', d => q2_yScale(d[0]) - q2_yScale(d[1]))
      .attr('width', q2_xScale.bandwidth())

  svg.append('g')
    .attr('transform', `translate(0,${q2_visHeight})`)
    .call(q2_xAxis)
    .call(g => g.selectAll('.domain').remove())
      // add a label for the x-axis
    .append('text')
      .attr('fill', textColor)
      .attr('font-family', 'sans-serif')
      .attr('x', q2_visWidth / 2)
      .style("font-size","12px")
      .style("text-anchor", "middle")
      .attr('y', 40)
      .text("Years");

  
  svg.append('g')
    .attr('transform', `translate(${ q2_margin.left },0)`)
    .call(q2_yAxis)
    .call(g => g.selectAll('.domain').remove())
    .append('text')
    .attr("transform", "rotate(-90)")
    .attr("x", 0 - q2_visHeight/2)
    .attr("dy", "-2.5em")
    .attr('fill', textColor)
    .attr('font-family', 'sans-serif')
    .style("text-anchor", "middle")
    .style("font-size","12px")
    .text('No. of Incidents');
}

const state_wise_count = d3.rollups(
    incident,
    group=> group.length,
    item => item.State
  ).sort((a,b)=>d3.descending(a[1],b[1]));

const vis4_Spike_Data = Object.fromEntries(state_wise_count.map(([k, v]) => [ stateAbMap[k], v ]));

function plot3(){
  // define margin
  const margin = ({top: 0, right: 20, bottom: 0, left: 50});
  const visWidth =  width - margin.top - margin.bottom;
  const visHeight = 700 - margin.top - margin.bottom;

  const projection =  d3.geoAlbersUsa().fitSize([visWidth -100, visHeight], usaGeo);
  const path = d3.geoPath().projection(projection);

  // Referenced from https://observablehq.com/@d3/spike-map
  const spike = (length, width = 8) => `M${-width / 2},0L0,${-length}L${width / 2},0`;

  const maxRate = d3.max(Object.values(vis4_Spike_Data));
  const length = d3.scaleLinear().domain([0, maxRate]).range([0, 150]);

    // Setup
  const svg = d3.select('#statewise').append('svg')
      .attr('width', visWidth + margin.left + margin.right)
      .attr('height', visHeight + margin.top + margin.bottom);

  const g = svg.append("g")
      .attr("transform", `translate(${margin.left}, ${margin.top})`);
  
  // Draw map
  g.selectAll("path")
    .data(usaGeo.features)
    .join("path")
      .attr("d", path)
      .attr("fill", "lightgrey")
      .attr("stroke", "white");

  // draw spikes 
  g.append("g")
      .attr("fill", "red" )
      .attr("fill-opacity", 0.2)
      .attr("stroke", "red")
    .selectAll("path")
    .data(usaGeo.features)
    .join("path") 
      .attr("transform", state => `translate(${path.centroid(state)})`)
      .attr("d", state => spike(length(vis4_Spike_Data[state.properties.NAME])));

  // Draw Legend   
  
// Referenced from https://observablehq.com/@d3/spike-map
  const legend = svg.append("g")
      .attr("fill", "#777")
      .attr("text-anchor", "middle")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
    .selectAll("g")
      .data(length.ticks(4).slice(1).reverse())
    .join("g")
    .attr('transform' , (d, i) => `translate(${width - i * 18},${600})` )

  legend.append("path")
      .attr("fill", "red")
      .attr("fill-opacity", 0.2)
      .attr("stroke", "red")
      .attr("d", d => spike(length(d)));

  legend.append("text")
      .attr("dy", "1.3em")
      .text(length.tickFormat(4, "s"));
}

const num_states = 5;
const filtered_incident = incident.filter(i => i.Year >=2000);
const top_state_data = d3.rollups(
    filtered_incident ,
    group=>group,
    item => item.State
  ).sort((a,b)=>d3.descending(a[1].length,b[1].length))
  .slice(0,num_states);
const bottom_state_data = d3.rollups(
    filtered_incident,
    group=>group,
    item => item.State
  ).sort((a,b)=>d3.ascending(a[1].length,b[1].length))
  .slice(0,num_states);

function plot4(){
  const state_data = d3.rollups(
      incident ,
      group=>group,
      item => item.State
    ).sort((a,b)=>d3.descending(a[1].length,b[1].length));
  const state_names = state_data.map(a=>a[0]);
  const heatmap_plot_data = state_data
    .flatMap(s=>d3.rollups(
      s[1],
      group=>group.length,
      item=>item.Year)
      .sort((a,b)=>d3.ascending(a[0],b[0]))
      .map(
        arr=>({
          state:s[0],
          year:arr[0],
          total:arr[1]
        })
      ));

  const heatmap_color = d3.scaleSequential()
    .domain(d3.extent(heatmap_plot_data, d => d.total))
    .interpolator(d3.interpolateOrRd);

  Legend(heatmap_color, '#heatmap_legend', {title: 'State-wise Incident Distribution', width: width});

  // margin
  const margin = ({top: 55, bottom: 20, left: 30, right: 50});
  const visWidth = width - margin.left - margin.right;
  const visHeight = 800 - margin.top - margin.bottom;
  // const visHeight = (state_names.length*12) - margin.top - margin.bottom;


  // Setup
  const svg = d3.select('#heatmap').append('svg')
      .attr('width', visWidth + margin.left + margin.right)
      .attr('height', visHeight + margin.top + margin.bottom);

  const g = svg.append("g")
      .attr('transform', `translate(${margin.left}, ${margin.top})`);
  
// Define x axis
  const x = d3.scaleBand()
    .range([0, visWidth])
    .domain(d3.range(1970 ,2023))
    .padding(0.2)
  
  const xAxis = d3.axisTop(x)
  
  g.append('g')
    .attr('transform', `translate(0,0)`)
    .call(xAxis)
    .selectAll("text")
        .attr("transform","rotate(-90)")
        .style("text-anchor", "mid")
        .attr("dx", "1.75em")
        .attr("dy", "1.35em")
  
  // Define y-axis
  const y = d3.scaleBand()
		.domain(state_names)
    .range([0, visHeight - 30])
		.padding(0.2)
  
  const yAxis = d3.axisLeft(y)
  
	g.append('g').call(yAxis)
    
	// draw rectangles
	g.selectAll('rect')
		.data(heatmap_plot_data)
		.enter()
    .append('rect')
			.attr('x', d => x(d.year))
			.attr('y', d => y(d.state))
			.attr('width', x.bandwidth())
			.attr('height', y.bandwidth())
			.attr('fill', d => heatmap_color(d.total))
      .on('mouseenter', mouseEnter)
      .on('mouseleave', mouseLeave);

  const tooltip = g.append('g')
      .attr('visibility', 'hidden');
  
  const tooltipHeight = 16;
  
  const tooltipRect = tooltip.append('rect')
      .attr('fill', '#101417')
      .attr('rx', 5)
      .attr('height', tooltipHeight);
  
  const amountText = tooltip.append('text')
      .attr('fill', 'white')
      .attr('font-family', 'sans-serif')
      .attr('font-size', 12)
      .attr('y', 2)
      .attr('x', 3)
      .attr('dominant-baseline', 'hanging')

   function mouseEnter(event, d) {
    d3.select(this)
        .attr('stroke', '#101417');

    amountText.text(`${d.state}, ${d.year} : ${d.total}`)
    
    const labelWidth = amountText.node().getComputedTextLength();

    tooltipRect.attr('width', labelWidth+10);
    tooltipRect.attr('text-align', 'center');

    tooltip
      .attr('transform', `translate(${visWidth-75},-50)`)
      .attr('visibility', 'visible');
  }

  function mouseLeave(event, d) {
    d3.select(this)
        .attr('stroke', "");
    
    tooltip
        .attr('visibility', 'hidden');
  }
}

function plot5(){
  const top_state_names = top_state_data.map(a=>a[0]);
  const start_year_heatmap = 2000;
  const top_heatmap_plot_data = top_state_data
    .flatMap(s=>d3.rollups(
      s[1],
      group=>group.length,
      item=>item.Year)
      .sort((a,b)=>d3.ascending(a[0],b[0]))
      .map(
        arr=>({
          state:s[0],
          year:arr[0],
          total:arr[1]
        })
      ));
  const top_heatmap_color = d3.scaleSequential()
    .domain(d3.extent(top_heatmap_plot_data, d => d.total))
    .interpolator(d3.interpolateOrRd);

  Legend(top_heatmap_color, '#heatmap_small_legend', {title: 'State-wise Incident Distribution from year 2000', width: width});

  // margin
  const margin = ({top: 55, bottom: 20, left: 25, right: 0});
  const visWidth = 900 - margin.left - margin.right;
  const visHeight = (top_state_names.length*40) - margin.top - margin.bottom;


  // Setup
  const svg = d3.select('#heatmap_small').append('svg')
      .attr('width', visWidth + margin.left + margin.right)
      .attr('height', visHeight + margin.top + margin.bottom);

  const g = svg.append("g")
      .attr('transform', `translate(${margin.left}, ${margin.top})`);
  
// Define x axis
  const x = d3.scaleBand()
    .range([0, visWidth])
    .domain(d3.range(start_year_heatmap ,2023))
    .padding(0.2)
  
  const xAxis = d3.axisTop(x)
  
  g.append('g')
    .attr('transform', `translate(0,0)`)
    .call(xAxis)
    .selectAll("text")
        .attr("transform","rotate(-90)")
        .style("text-anchor", "mid")
        .attr("dx", "1.75em")
        .attr("dy", "1.35em")
  
  // Define y-axis
  const y = d3.scaleBand()
		.domain(top_state_names)
    .range([0, visHeight - 30])
		.padding(0.2)
  
  const yAxis = d3.axisLeft(y)
  
	g.append('g').call(yAxis)
    
	// draw rectangles
	g.selectAll('rect')
		.data(top_heatmap_plot_data)
		.enter()
    .append('rect')
			.attr('x', d => x(d.year))
			.attr('y', d => y(d.state))
			.attr('width', x.bandwidth())
			.attr('height', y.bandwidth())
			.attr('fill', d => top_heatmap_color(d.total))
      .on('mouseenter', mouseEnter)
      .on('mouseleave', mouseLeave);

  const tooltip = g.append('g')
      .attr('visibility', 'hidden');
  
  const tooltipHeight = 16;
  
  const tooltipRect = tooltip.append('rect')
      .attr('fill', '#101417')
      .attr('rx', 5)
      .attr('height', tooltipHeight);
  
  const amountText = tooltip.append('text')
      .attr('fill', 'white')
      .attr('font-family', 'sans-serif')
      .attr('font-size', 12)
      .attr('y', 2)
      .attr('x', 3)
      .attr('dominant-baseline', 'hanging')
      .style("text-anchor", "mid");

  function mouseEnter(event, d) {
    d3.select(this)
        .attr('stroke', '#101417');

    amountText.text(`${d.state}, ${d.year} : ${d.total}`)
    
    const labelWidth = amountText.node().getComputedTextLength();

    tooltipRect.attr('width', labelWidth+10);
    tooltipRect.attr('text-align', 'center');

    tooltip
      .attr('transform', `translate(${visWidth-100},-50)`)
      .attr('visibility', 'visible');
  }

  function mouseLeave(event, d) {
    d3.select(this)
        .attr('stroke', "");
    
    tooltip
        .attr('visibility', 'hidden');
  }
}

const unique_weapons = Array.from(new Set(weapon.map(d => (d.Weapon_Type === "unknown") ? "Unknown" : d.Weapon_Type)));
const top_state_names = top_state_data.map(a=>a[0]);
const topStates = d3.filter(weapon, d => top_state_names.slice(0,5).includes(d.State));
const topWeaponState = d3.rollups(
    topStates,
    g => g.reduce((valueCount, current) => {
      const count = valueCount[current.Weapon_Type] ?? 0;
      valueCount[current.Weapon_Type] = count + 1;
      return valueCount;
    }, {}),
    d => d.State
  ).map(data => ({
    "State" : data[0],
    "unknown" : data[1].unknown ?? 0,
    "Handgun" : data[1].Handgun ?? 0,
    "Other": data[1].Other ?? 0,
    "Rifle": data[1].Rifle ?? 0,
    "Multiple Handguns": data[1]["Multiple Handguns"] ?? 0,
    "Multiple Rifles": data[1]["Multiple Rifles"] ?? 0,
    "Shotgun": data[1].Shotgun ?? 0
  })).sort((a,b) => d3.ascending(a.State, b.State));
const bottom_state_names = bottom_state_data.map(a=>a[0]);
const bottomStates = d3.filter(weapon, d => bottom_state_names.slice(0,5).includes(d.State));
const bottomWeaponState = d3.rollups(
    bottomStates,
    g => g.reduce((valueCount, current) => {
      const count = valueCount[current.Weapon_Type] ?? 0;
      valueCount[current.Weapon_Type] = count + 1;
      return valueCount;
    }, {}),
    d => d.State
  ).map(data => ({
    "State" : data[0],
    "unknown" : data[1].unknown ?? 0,
    "Handgun" : data[1].Handgun ?? 0,
    "Other": data[1].Other ?? 0,
    "Rifle": data[1].Rifle ?? 0,
    "Multiple Handguns": data[1]["Multiple Handguns"] ?? 0,
    "Multiple Rifles": data[1]["Multiple Rifles"] ?? 0,
    "Shotgun": data[1].Shotgun ?? 0
  })).sort((a,b) => d3.ascending(a.State, b.State));
const q5_height = 250;
const q5_margin = ({top:100, bottom:0, left:100, right:20});
const q5_visWidth = width - q5_margin.left - q5_margin.right;
const q5_visHeight = q5_height - q5_margin.top - q5_margin.bottom;
const q5_cols = 5;
const q5_rows = 1;
const grid = d3.cross(d3.range(q5_rows), d3.range(q5_cols), (row, col) => ({row, col}));
const topData = d3.zip(Array.from(topWeaponState), grid).map(
    ([data, {row, col}]) => ({
      data,
      row,
      col
    })
  ).map(d => ({
    "State" : d.data.State,
    "values": [
      ({"State" : d.data.State, "weapon": "Unknown", "count": d.data.unknown, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Handgun", "count": d.data.Handgun, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Other", "count": d.data.Other, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Rifle", "count": d.data.Rifle, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Multiple Handguns", "count": d.data["Multiple Handguns"], "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Multiple Rifles", "count": d.data["Multiple Rifles"], "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Shotgun", "count": d.data.Shotgun, "row": d.row, "col": d.col})
    ],
    "row": d.row,
    "col": d.col
  }));
const bottomData = d3.zip(Array.from(bottomWeaponState), grid).map(
    ([data, {row, col}]) => ({
      data,
      row,
      col
    })
  ).map(d => ({
    "State" : d.data.State,
    "values": [
      ({"State" : d.data.State, "weapon": "Unknown", "count": d.data.unknown, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Handgun", "count": d.data.Handgun, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Other", "count": d.data.Other, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Rifle", "count": d.data.Rifle, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Multiple Handguns", "count": d.data["Multiple Handguns"], "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Multiple Rifles", "count": d.data["Multiple Rifles"], "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Shotgun", "count": d.data.Shotgun, "row": d.row, "col": d.col})
    ],
    "row": d.row,
    "col": d.col
  }));
const q5_row = d3.scaleBand()
  .domain(d3.range(q5_rows))
  .range([0, q5_visHeight]);
const q5_col = d3.scaleBand()
  .domain(d3.range(q5_cols))
  .range([0, q5_visWidth])
  .paddingInner(0.2);
const q5_colorScale = d3.scaleOrdinal()
  .domain(unique_weapons)
  .range(['lightgray','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#e41a1c']);
const q5_angleGenerator = d3.pie()
  .value(d => d.count);
const q5_arcGenerator = d3.arc()
  .innerRadius(0)
  .outerRadius(80);

const top_state_killed_data = top_state_data.map(s=>{
  const only_deaths = s[1].filter(i=> i.Victims_Killed > 0)
  return [s[0],only_deaths]
});

const topFiveIncident = d3.filter(incident, d => top_state_names.includes(d.State))
  .map(d => ({"Incident_ID": d.Incident_ID, "Victims_Killed": d.Victims_Killed, "Victims_Wounded": d.Victims_Wounded}));
const topFiveWeapon = d3.filter(weapon, d => top_state_names.includes(d.State))
  .map(d => ({"Incident_ID": d.Incident_ID, "Weapon_Type": d.Weapon_Type, "State": d.State}));
const dataset = topFiveWeapon.map(d => ({
    Incident_ID: d.Incident_ID,
    Weapon_Type: d.Weapon_Type,
    Victims_Killed: topFiveIncident.filter(i => i.Incident_ID === d.Incident_ID).map(i => i.Victims_Killed)[0],
    Victims_Wounded: topFiveIncident.filter(i => i.Incident_ID === d.Incident_ID).map(i => i.Victims_Wounded)[0],
    State: d.State
  }));
const datasetRollup = d3.rollups(
    dataset,
    g => g.reduce((valueCount, current) => {
      const count = valueCount[current.Weapon_Type] ?? 0;
      valueCount[current.Weapon_Type] = count + current.Victims_Killed;
      return valueCount
    }, {}),
    d => d.State,
  ).map(data => ({
    "State": data[0],
    "unknown" : data[1].unknown ?? 0,
    "Handgun" : data[1].Handgun ?? 0,
    "Other": data[1].Other ?? 0,
    "Rifle": data[1].Rifle ?? 0,
    "Multiple Handguns": data[1]["Multiple Handguns"] ?? 0,
    "Multiple Rifles": data[1]["Multiple Rifles"] ?? 0,
    "Shotgun": data[1].Shotgun ?? 0
  })).sort((a,b) => d3.ascending(a.State, b.State));
const grid_dataset = d3.cross(d3.range(q5_rows), d3.range(q5_cols), (row, col) => ({row, col}));
const weaponDeath = d3.zip(Array.from(datasetRollup), grid).map(
    ([data, {row, col}]) => ({
      data,
      row,
      col
    })
  ).map(d => ({
    "State" : d.data.State,
    "values": [
      ({"State" : d.data.State, "weapon": "Unknown", "count": d.data.unknown, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Handgun", "count": d.data.Handgun, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Other", "count": d.data.Other, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Rifle", "count": d.data.Rifle, "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Multiple Handguns", "count": d.data["Multiple Handguns"], "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Multiple Rifles", "count": d.data["Multiple Rifles"], "row": d.row, "col": d.col}),
      ({"State" : d.data.State, "weapon": "Shotgun", "count": d.data.Shotgun, "row": d.row, "col": d.col})
    ],
    "row": d.row,
    "col": d.col
  }));

function plot678(){
  generatePies(topData, '#piechart_high');
  generatePies(bottomData, '#piechart_low');
  generatePies(weaponDeath, '#killed_vs_weapon');
}

function generatePies(data, divName) {
  const svg = d3.select(divName).append('svg')
    .attr('width', width)
    .attr('height', q5_height);

  const g = svg.append('g')
    .attr('transform', `translate(${q5_margin.left}, ${q5_margin.top})`);

  const pieGroups = svg.append('g')
    .attr('transform', `translate(${q5_margin.left}, ${q5_margin.top})`);

  const pieCharts = pieGroups.selectAll('g')
    .data(data)
    .join('g')
      .attr('transform', d => `translate(${q5_col(d.col)}, ${q5_row(d.row)})`);

  pieCharts.selectAll('path')
    .data(d => q5_angleGenerator(d.values))
    .join('path')
      .attr('d', d => q5_arcGenerator(d))
      .attr('fill', d => q5_colorScale(d.data.weapon))
      .on('mouseenter', mouseEnter)
      .on('mouseleave', mouseLeave);

  const textGroups = svg.append('g')
    .attr('transform', `translate(${q5_margin.left}, ${q5_margin.top})`);

  const textBoxes = textGroups.selectAll('g')
    .data(data)
    .join('g')
      .attr('transform', d => `translate(${q5_col(d.col)}, ${q5_row(d.row) - 95})`)
    .append('text')
      .text(d => stateAbMap[d.State])
      .attr('font-family', 'sans-serif')
      .attr('fill', 'white')
      .attr('text-anchor', 'middle')
      .attr('font-size', 12)
      .attr('dominant-baseline', 'hanging');

  const tooltip = g.append('g')
      .attr('visibility', 'hidden');
  
  const tooltipHeight = 16;
  
  const tooltipRect = tooltip.append('rect')
      .attr('fill', '#101417')
      .attr('rx', 5)
      .attr('height', tooltipHeight);
  
  const amountText = tooltip.append('text')
      .attr('fill', 'white')
      .attr('font-family', 'sans-serif')
      .attr('font-size', 12)
      .attr('y', 2)
      .attr('x', 3)
      .attr('dominant-baseline', 'hanging')

  function mouseEnter(event, d) {
    d3.select(this)
        .attr('stroke', '#101417');

    amountText.text(`${d.data.weapon}: ${d.data.count}`)
    
    const labelWidth = amountText.node().getComputedTextLength();

    tooltipRect.attr('width', labelWidth + 6);

    const xPos = q5_col(d.data.col) - 35;
    const yPos = q5_row(d.data.row) + 95;

    tooltip
      .attr('transform', `translate(${xPos},${yPos})`)
      .attr('visibility', 'visible');
  }

  function mouseLeave(event, d) {
    d3.select(this)
        .attr('stroke', "");
    
    tooltip
        .attr('visibility', 'hidden');
  }
}

function getAgeBin(){
  let res = {};
  shooter.forEach(row=>{
    const age = parseInt(row.Age);
    var key = '';
    if(Number.isInteger(age)){
      if(age>=0 && age < 13){// mior child
        key = 1; // 0-12
      }
      if(age>=13 && age < 18){
        key = 2; // 13-17
      }
      if(age>=18 && age < 22){
        key = 3; // 18-21
      }
      if(age>=22 && age < 31) {
        key = 4; // 22-30
      }
      if(age>=31 && age < 51) {
        key = 5; // 31-50
      }
      if(age>=51 ) {
        key = 6; // 50+
      }
    }
    if(res[key]) res[key].push(row)
    else res[key] = [row]
  });
  let age_bin_disbn = [];
  Object.keys(res).forEach(b=>{
    const val = d3.rollup(res[b],group=>group.length,item=>item.Gender||"Unknown")
    age_bin_disbn.push([b,val])
  })
  return age_bin_disbn;
}

function plot9(){
  const age_group_dsbn = getAgeBin();
  const ageRanges = d3.map(age_group_dsbn, d => d[0]);
  const genders = ["Unknown", "Male", "Female", "Transgender"];
  const q3_maxValue = d3.max(
      age_group_dsbn,
      ([ageRange, genderCount]) => d3.max(genderCount, ([gender, count]) => count)
    );
  const q3_color = d3.scaleOrdinal()
    .domain(genders)
    .range(d3.schemeCategory10);

  //setup 
  const q3_margin = ({top: 10, bottom: 50,left: 85, right: 10});
  const q3_height = 800;
  const q3_visWidth = width - q3_margin.left - q3_margin.right;
  const q3_visHeight = q3_height - q3_margin.top - q3_margin.bottom;

  // scales and axes
  const q3_group = d3.scaleBand()
  .domain(ageRanges)
  .range([0, q3_visWidth])
  .padding(0.1);

  const q3_barX = d3.scaleBand()
  .domain(genders)
  .range([0, q3_group.bandwidth()])
  .padding(0.1);

  const q3_y = d3.scaleLinear()
  .domain([0, q3_maxValue]).nice()
  .range([q3_visHeight, 0]);

  const q3_xAxis = d3.axisBottom(q3_group)
  .tickFormat(formatAge);;

  const q3_yAxis = d3.axisLeft(q3_y);
  
  const svg = d3.select('#age').append('svg')
    .attr('width', width)
    .attr('height', q3_height);

  const g = svg.append('g')
    .attr('transform', `translate(${q3_margin.left}, ${q3_margin.top})`)

  const groups = g.selectAll('g')
    .data(age_group_dsbn)
    .join('g')
      .attr('transform', ([ageRange, genderCount]) => `translate(${q3_group(ageRange)})`)

  groups.selectAll('rect')
    .data(([ageRange, genderCount]) => genderCount)
    .join('rect')
      .attr('x', ([gender, count]) => q3_barX(gender))
      .attr('y', ([gender, count]) => q3_y(count))
      .attr('width', ([gender, count]) => q3_barX.bandwidth())
      .attr('height', ([gender, count]) => q3_visHeight - q3_y(count))
      .attr('fill', ([gender, count]) => q3_color(gender))

  g.append('g')
    .attr('transform', `translate(0,${q3_visHeight})`)
    .call(q3_xAxis)
    .call(g => g.selectAll('.domain').remove())
   .append('text')
      .attr('x', q3_visWidth / 2)
      .attr('y', 30)
      .attr('dominant-baseline', 'hanging')
      .attr('text-align', 'middle')
      .attr('fill', 'white')
      .text('Age Range');
  
 g.append('g')
    .call(q3_yAxis)
    .call(g => g.selectAll('.domain').remove())
  .append('text')
    .attr('x', -50)
    .attr('y', q3_visHeight / 2)
    .attr('dominant-baseline', 'middle')
    .attr('text-align', 'end')
    .attr('fill', 'white')
    .text('Count');
}

function plot10(){
  const q6_data = d3.rollups(
      incident,
      g => g.reduce((valueCount, current) => {
        const count = valueCount[current.Quarter] ?? 0;
        valueCount[current.Quarter] = count + 1;
        return valueCount;
      }, {}),
      d => d.Year
    ).map(d => ({
      "year": d[0],
      "values": [
        ({"time": 1, "count": d[1].Spring ?? 0}),
        ({"time": 2, "count": d[1].Summer ?? 0}),
        ({"time": 3, "count": d[1].Fall ?? 0}),
        ({"time": 4, "count": d[1].Winter ?? 0})
      ]
    })).sort((a,b) => d3.ascending(a.year, b.year));
  const q6_height = 700;
  const q6_margin = ({top: 30, right: 30, bottom: 20, left: 40});
  const q6_visWidth = width - q6_margin.left - q6_margin.right;
  const q6_visHeight = q6_height - q6_margin.top - q6_margin.bottom;
  const q6_years = q6_data.map(d => d.year);
  const q6_xData = d3.extent(d3.map(q6_data[0].values, d => d.time));
  const q6_x = d3.scaleLinear()
    .domain(q6_xData)
    .range([0, q6_visWidth]);
  const q6_maxValue = d3.max(q6_data, d => d3.max(d.values, d => d.count));
  const q6_y = d3.scaleLinear()
    .domain([0, q6_maxValue])
    .range([q6_visHeight, 0])
    .nice();
  const q6_color = d3.scaleOrdinal()
    .domain(q6_years.slice(q6_years.length - 5, q6_years.length))
    .range(d3.schemeCategory10)
    .unknown("lightgray");
  const q6_line = d3.line()
    .x(d => q6_x(d.time))
    .y(d => q6_y(d.count));
  const q6_xAxis = d3.axisBottom(q6_x)
    .tickFormat(formatTime);
  const q6_yAxis = d3.axisLeft(q6_y);
  
  const svg = d3.select('#trend').append('svg')
    .attr('width', width)
    .attr('height', q6_height);

  const g = svg.append('g')
      .attr('transform', `translate(${q6_margin.left}, ${q6_margin.top})`);

  g.append('g')
      .attr('transform', `translate(0,${q6_visHeight})`)
      .call(q6_xAxis)
      .call(g => g.select('.domain').remove());

  let titleText = "quarters";
  
  g.append('g')
      .call(q6_yAxis)
      .call(g => g.select('.domain').remove())
    .append('text')
      .attr('fill', 'white')
      .attr('text-anchor', 'start')
      .attr('dominant-baseline', 'hanging')
      .attr('font-weight', 'bold')
      .attr('y', -q6_margin.top + 5)
      .attr('x', -q6_margin.left)
      .text(`Number of incidents over ${titleText}`)

  const linesGroup = g.append('g');
  
  linesGroup.selectAll('path')
    .data(q6_data)
    .join('path')
      .attr('stroke', d => q6_color(d.year))
      .attr('fill', 'None')
      .attr('stroke-width', 2)
      .attr('d', d => q6_line(d.values))
}