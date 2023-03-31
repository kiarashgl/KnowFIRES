<template>
  <div>
    <div id="ranking"></div>
    {{ rankings }}
  </div>
</template>

<script>
import * as d3 from 'd3'

export default {
  name: "Ranking",
  props: {
    rankings: Array
  },
  watch: {
    rankings: function (oldVal, newVal) {
      const topK = this.rankings[0].length
      var margin = {top: 30, right: 50, bottom: 10, left: 50},
          width = 460 - margin.left - margin.right,
          height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
      var svg = d3.select("#ranking")
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

      const y = d3.scaleLinear()
          .domain([1, topK])
          .range([0, height])

      var chartData = {}
      // console.log("ALIAAA")
      // console.log(this.rankings[0])
      this.rankings[0].forEach(item => {
        chartData[item[0]] = [0, 0]
      })
      this.rankings[1].forEach(item => {
        chartData[item[0]] = [0, 0]
      })
      this.rankings.forEach((item, index) => {
        Object.entries(item).forEach((ii, jj) => {
          chartData[ii[1][0]][+index] = jj + 1
        })
        // chartData[item]
        // console.log(item);
      })
      console.log(chartData);

      svg
          .selectAll("myPath")
          .data(chartData)
          .enter()
          .append("path")
          // .attr("class", function (d) { return "line " + d.Species } ) // 2 class for each line: 'line' and the group name
          .attr("d", d3.line()
              .x(function(d) { return 10 })
              .y(function(d) {
                console.log(d);
                return 20 }))
          .style("fill", "none" )
          // .style("stroke", function(d){ return( color(d.Species))} )
          .style("opacity", 0.5)

      // // Draw the axis:
      // svg.selectAll("myAxis")
      //     // For each dimension of the dataset I add a 'g' element:
      //     // .data(dimensions).enter()
      //     .append("g")
      //     .attr("class", "axis")
      //     // I translate this element to its right position on the x axis
      //     .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
      //     // And I build the axis with the call function
      //     .each(function(d) { d3.select(this).call(d3.axisLeft().ticks(5).scale(y[d])); })
      //     // Add axis title
      //     .append("text")
      //     .style("text-anchor", "middle")
      //     .attr("y", -9)
      //     .text(function(d) { return d; })
      //     .style("fill", "black")
    }
  }
}
</script>

<style scoped>

</style>