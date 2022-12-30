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

function colorize(colorList, htmlElement) {
  var container = document.getElementById(htmlElement);

  for (var key in colorList) {
      var boxContainer = document.createElement("DIV");
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
              .attr('stroke-width', 0.5)
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
              .attr('stroke-width', 0.5)
        ).append('text')
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

function getAgeBin(){
    const res = {}
    shooter.forEach(row=>{
      const age = row.Age
      let key = ''
      if(Number.isInteger(age)){
        if(age>=0 && age < 13){ // mior child
          key = 1  // 0-12
        }
        if(age>=13 && age < 18){
          key = 2 // 13-17
        }
        if(age>=18 && age < 22){
          key = 3 // 18-21
        }
        if(age>=22 && age < 31) {
          key = 4 // 22-30
        }
        if(age>=31 && age < 51) {
          key = 5 // 31-50
        }
        if(age>=51 ) {
          key = 6 // 50+
        }
      }
      // if(!key) key = age
      if(key) {
        if(res[key]) res[key].push(row)
        else res[key] = [row]    
      }
    })
    const age_bin_disbn = []
    Object.keys(res).forEach(b=>{
      console.log(b,res[b])
      const val = d3.rollup(res[b],group=>group.length,item=>item.Gender||"Unknown")
      age_bin_disbn.push([b,val])
    })
    return age_bin_disbn;
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

function plot4(){
  const num_states = 5;
  const filtered_incident = incident.filter(i => i.Year >=2000);
  const top_state_data = d3.rollups(
      filtered_incident ,
      group=>group,
      item => item.State
    ).sort((a,b)=>d3.descending(a[1].length,b[1].length))
    .slice(0,num_states);
  const state_data = d3.rollups(
      incident ,
      group=>group,
      item => item.State
    ).sort((a,b)=>d3.descending(a[1].length,b[1].length));
  const top_state_wise_count_dsbn = top_state_data
    .map(s=>({
      state: s[0],
      counts: d3.rollups(
        s[1],
        group=>group.length,
        item=>item.Year)
      .sort((a,b)=>d3.ascending(a[0],b[0]))
      .map(arr=>({year:arr[0],total:arr[1]})) 
    }));
  const state_wise_count_dsbn = state_data
    .map(s=>({
      state: s[0],
      counts: d3.rollups(
        s[1],
        group=>group.length,
        item=>item.Year)
      .sort((a,b)=>d3.ascending(a[0],b[0]))
      .map(arr=>({year:arr[0],total:arr[1]})) 
    }));
  const top_state_names = top_state_data.map(a=>a[0]);
  const state_names = state_data.map(a=>a[0]);
  const bottom_state_data = d3.rollups(
      filtered_incident,
      group=>group,
      item => item.State
    ).sort((a,b)=>d3.ascending(a[1].length,b[1].length))
    .slice(0,num_states);
  const bottom_state_names = bottom_state_data.map(a=>a[0]);
  const minYear = 1970;
  const maxYear = 2022;
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
  const start_year_heatmap = 2000;
  const count_extent = d3.extent(heatmap_plot_data, d => d.total);
  const top_count_extent = d3.extent(top_heatmap_plot_data, d => d.total);
  const top_heatmap_color = d3.scaleSequential()
    .domain(d3.extent(top_heatmap_plot_data, d => d.total))
    .interpolator(d3.interpolateOrRd);
  const heatmap_color = d3.scaleSequential()
    .domain(d3.extent(heatmap_plot_data, d => d.total))
    .interpolator(d3.interpolateOrRd);

  const plot_legend = d3.select('#heatmap_legend').append(legend({
    color: heatmap_color,
    width: width,
    title: 'State-wise Incident Distribution'
  }));

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
      .attr('fill', 'black')
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
    console.log("qwer",d);
    d3.select(this)
        .attr('stroke', 'black');

    amountText.text(`${d.state},${d.year} : ${d.total}`)
    
    const labelWidth = amountText.node().getComputedTextLength();

    tooltipRect.attr('width', labelWidth+10);
    tooltipRect.attr('text-align', 'center');

    const xPos = x(d.year) - 5;
    const yPos = y(d.state) - 5;

    tooltip
      // .attr('transform', `translate(${visHeight},${visWidth+20})`)
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