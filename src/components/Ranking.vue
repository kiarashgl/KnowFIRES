<template>
  <v-card class="pa-2">
    <h3>Compare Rankings</h3>
    <div id="ranking"></div>
  </v-card>
</template>

<script>
import * as d3 from 'd3'

var margin = {top: 30, right: 100, bottom: 10, left: 102},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;
export default {
  name: "Ranking",
  props: {
    rankings: Array,
    selectedNode: Object,
    retrievers: Array
  },
  data: function () {
    return {
      svg: undefined
    }
  },
  mounted() {
    this.svg = d3.select("#ranking")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");
  },
  watch: {
    selectedNode: function(newVal, oldVal) {
      if (newVal === null) {
        this.svg.selectAll(`path`).classed("dim", false)
      }
      else {
        this.svg.selectAll(`path.name-${newVal.id}`).classed("dim", false)
        this.svg.selectAll(`path:not(.name-${newVal.id})`).classed("dim", true)
      }
    },
    rankings: function (newVal, oldVal) {
      const topK = this.rankings[0].length

      d3.select("#ranking svg").remove()
      this.svg = d3.select("#ranking")
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");
// append the svg object to the body of the page
      // console.log(newVal);
      const y1 = d3.scaleBand()
          .domain(newVal[0].map(item => item[0]))
          .range([0, height])
          .padding(1)
      const y2 = d3.scaleBand()
          .domain(newVal[1].map(item => item[0]))
          .range([0, height])
          .padding(1)

      var chartData = {}
      newVal[0].forEach(item => {
        chartData[item[0]] = {color: "#2271B2", list: [0, 0]}
      })
      newVal[1].forEach(item => {
        chartData[item[0]] = {color: "#359B73", list: [0, 0]}
      })
      newVal.forEach((item, index) => {
        Object.entries(item).forEach((ii, jj) => {
          chartData[ii[1][0]].list[+index] = jj + 1
        })
      })

      Object.entries(chartData).forEach(d => {
        if (d[1].list[0] !== 0 && d[1].list[1] !== 0)
          d[1].color = "#F748A5"
      })


      const points = Object.entries(chartData).map(d => {
        const x1 = d[1].list[0] !== 0 ? 0 : 60
        const yy1 = d[1].list[0] !== 0 ? y1(d[0]) : y2(d[0])
        const x2 = d[1].list[1] !== 0 ? 80 : 20
        const yy2 = d[1].list[1] !== 0 ? y2(d[0]) : y1(d[0])
        return [{x: x1, y: yy1, c: d[1].color, id: d[0]},
          {x: x2, y: yy2 ,c: d[1].color, id: d[0]},
        ]
      })
      this.svg
          .selectAll("myPath")
          .data(points)
          .enter()
          .append("path")
          .attr("d", d3.line(d => d.x, d => d.y).curve(d3.curveBumpX))//.curve(d3.curveNatural()))
          .style("fill", "none" )
          .style("stroke", (d) => {
            return d[0].c
          })
          .style("stroke-width", "5")
          // .style("opacity", 0.5)
          .attr("class", d => {
            return `rank name-${d[0].id}`
          })

      const r1 = this.retrievers[0]
      const r2 = this.retrievers[1]
      this.svg
          // For each dimension of the dataset I add a 'g' element:
          .append("g")
          // I translate this element to its right position on the x axis
          .attr("transform",  "translate(" + 0 + ")")
          // And I build the axis with the call function
          .call(d3.axisLeft().scale(y1))
          // Add axis title
          .append("text")
          .style("text-anchor", "middle")
          .attr("y", -9)
          .attr("x", -10)

          .text(function(d) { return `Rank in ${r1}`; })
          .style("fill", "black")

      this.svg
          .append("g")
          .attr("transform",  "translate(" + 80 + ")")
          .call(d3.axisRight().scale(y2))
          .append("text")
          .style("text-anchor", "middle")
          .attr("y", -9)
          .attr("x", 10)
          .text(function(d) { return `Rank in ${r2}`; })
          .style("fill", "black")

          this.svg.selectAll(".tick text")
          .call(truncateLabel, y2.bandwidth())

    }
  }
}
function truncateLabel(text, width) {
  text.each(function() {
    var name = d3.select(this).text();
    if(name.length > 13){
      name = name.slice(0, 13) + "..."
    }
    d3.select(this).text(name)
  })
}
</script>

<style>
path.rank.dim {
  opacity: 0.2!important;
}
path {
  transition: all 0.5s ease;

}
</style>