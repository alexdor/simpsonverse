import * as d3 from "d3";

import { options, randomLog } from "./helpers";

const w = 600;
const h = 800;
const forceSimulation = (nodes, links, small) => {
  const forceD3 = d3
    .forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id))
    .force("charge", d3.forceManyBody().strength(-80));
  small
    ? forceD3
        .force("charge", d3.forceManyBody().strength(-310))
        .force("center", d3.forceCenter())
    : forceD3.force("x", d3.forceX()).force("y", d3.forceY());
  return forceD3;
};

const drag = simulation => {
  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

  return d3
    .drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);
};

const color = (() => {
  const scale = d3.scaleOrdinal(d3.schemeCategory10);
  return d => scale(d.group);
})();

export const drawChart = (id, data, small) => {
  const links = data.elements.edges.map(d => Object.create(d.data));
  const nodes = data.elements.nodes.map(d => Object.create(d.data));

  const svg = d3
    .select(id)
    .append("div")
    .classed("svg-container", true) //container class to make it responsive
    .append("svg")
    // .attr("style", `left: calc(50vw - ${w / 2}px)`)
    //responsive SVG needs these 2 attributes and no width and height attr
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", `0 0 ${w} ${h}`)
    // .call(
    //   d3.zoom().on("zoom", function() {
    //     svg.attr("transform", d3.event.transform);
    //   })
    // )
    //class to make it responsive
    .classed("svg-content-responsive", true);

  const link = svg
    .append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(links)
    .enter()
    .append("line")
    .attr("stroke-width", d => randomLog(d.value));
  const ticked = () => {
    link
      .attr("x1", d => w + d.source.x)
      .attr("y1", d => h / 2 + d.source.y / 2)
      .attr("x2", d => w + d.target.x)
      .attr("y2", d => h / 2 + d.target.y / 2);
    node.attr("cx", d => w + d.x).attr("cy", d => h / 2 + d.y / 2);
  };
  const simulation = forceSimulation(nodes, links, small).on("tick", ticked);
  const node = svg
    .append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 0.7)
    .selectAll("circle")
    .data(nodes)
    .enter()
    .append("circle")
    .attr("r", d => Math.sqrt(d.degree * 2))
    .attr("fill", color)
    .call(drag(simulation));
  node.append("title").text(d => d.name);
};

export const drawBar = (id, dat) => {
  const data = dat.map((d, i) => ({ value: d * 100, date: options[i].value }));
  const svg = d3
    .select(id)
    .append("div")
    .classed("svg-container", true) //container class to make it responsive
    .append("svg");
  // const margin = { top: 20, right: 20, bottom: 30, left: 40 };
  // const width = +svg.attr("width") - margin.left - margin.right;
  // const height = +svg.attr("height") - margin.top - margin.bottom;
  const yAxis = g =>
    g
      .attr("transform", `translate(0,0)`)
      // .call(d3.axisLeft(0))
      .call(g => g.select(".domain").remove())
      .call(g =>
        g
          .select(".tick:last-of-type text")
          .clone()
          .attr("x", 3)
          .attr("text-anchor", "start")
          .attr("font-weight", "bold")
          .text(data.y)
      );

  // const xAxis = g =>
  //   g.attr("transform", `translate(0,${h})`).call(
  //     d3
  //       .axisBottom(0)
  //       .ticks(w / 80)
  //       .tickSizeOuter(0)
  //   );

  const xAxis = g => g.attr("transform", `translate(0,${h})`);
  // .call(
  //   d3
  //     // .axisBottom(x)
  //     .ticks(w / 80)
  //     .tickSizeOuter(0)
  // );

  // const x = d3.scaleTime().range([0, w]);
  // const y = d3.scaleLinear().range([h, 0]);

  svg.append("g").call(xAxis);

  svg.append("g").call(yAxis);

  const line = d3
    .line()
    .defined(d => !isNaN(d.value))
    .x(d => {
      console.log("====================================");
      console.log(d);
      console.log("====================================");
      return d.date;
    })
    .y(d => {
      console.log("====================================");
      console.log(d);
      console.log("====================================");
      return d.value;
    });
  svg
    .append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .attr("stroke-linejoin", "round")
    .attr("stroke-linecap", "round")
    .attr("d", line);

  // const g = svg
  //   .append("g")
  //   .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // g.append("g")
  //   .attr("class", "axis axis--x")
  //   .attr("transform", "translate(0," + h + ")")
  //   .call(d3.axisBottom(x));
  // g.append("g")
  //   .attr("class", "axis axis--y")
  //   .call(
  //     d3
  //       .axisLeft(y)
  //       .ticks(6)
  //       .tickFormat(function(d) {
  //         return parseInt(d / 100) + "k";
  //       })
  //   )
  //   .append("text")
  //   .attr("class", "axis-title")
  //   .attr("transform", "rotate(-90)")
  //   .attr("y", 6)
  //   .attr("dy", ".71em")
  //   .style("text-anchor", "end")
  //   .attr("fill", "#5D6971")
  //   .text("Population)");

  // g.append("path")
  //   .datum(data)
  //   .attr("class", "line")
  //   .attr("fill", "none")
  //   .attr("stroke", "steelblue")
  //   .attr("stroke-width", 1.5)
  //   .attr("stroke-linejoin", "round")
  //   .attr("stroke-linecap", "round")
  //   .attr("d", line);

  // const focus = g
  //   .append("g")
  //   .attr("class", "focus")
  //   .style("display", "none");
  // focus
  //   .append("line")
  //   .attr("class", "x-hover-line hover-line")
  //   .attr("y1", 0)
  //   .attr("y2", h);
  // focus
  //   .append("line")
  //   .attr("class", "y-hover-line hover-line")
  //   .attr("x1", w)
  //   .attr("x2", w);
  // focus.append("circle").attr("r", 7.5);
  // focus
  //   .append("text")
  //   .attr("x", 15)
  //   .attr("dy", ".31em");
  // svg
  //   .append("rect")
  //   .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
  //   .attr("class", "overlay")
  //   .attr("width", w)
  //   .attr("height", h)
  //   .on("mouseover", function() {
  //     focus.style("display", null);
  //   })
  //   .on("mouseout", function() {
  //     focus.style("display", "none");
  //   });
  // .on("mousemove", mousemove);
  // function mousemove() {
  //   let x0 = x.invert(d3.mouse(this)[0]),
  //     i = bisectDate(data, x0, 1),
  //     d0 = data[i - 1],
  //     d1 = data[i],
  //     d = x0 - d0.year > d1.year - x0 ? d1 : d0;
  //   focus.attr(
  //     "transform",
  //     "translate(" + x(d.year) + "," + y(d.value) + ")"
  //   );
  //   focus.select("text").text(function() {
  //     return d.value;
  //   });
  //   focus.select(".x-hover-line").attr("y2", height - y(d.value));
  //   focus.select(".y-hover-line").attr("x2", width + width);
  // }
};
