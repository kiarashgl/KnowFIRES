<template>
  <v-container class="pa-5" fluid>
    <v-row>
      <v-col cols="3">
        <v-card class="pa-3 mb-4">
          <h3>Retriever Selector</h3>
          <v-row>
            <v-col>
              <v-select density="compact" label="Retriever 1" v-model="selectedRetrievers[0]" :items="retrievers"></v-select>
            </v-col>
            <v-col>
              <v-select density="compact" label="Retriever 2" v-model="selectedRetrievers[1]" :items="retrievers"></v-select>
            </v-col>
          </v-row>
          <v-slider label="# Retrieved" class="mt-5" hide-details dense min="3" max="15" step="1" thumb-label="always" v-model="topK"></v-slider>
          <v-switch dense hide-details v-model="merged" label="Merged view"></v-switch>
          <v-switch dense hide-details @change="refreshGraphs" v-model="showNeighbors" label="Show neighbor links"></v-switch>
        </v-card>
        <Card :entity="selectedNode"></Card>
      </v-col>
      <v-col>
        <v-progress-circular indeterminate v-if="searchRunning"></v-progress-circular>
        <v-card class="pa-3" v-show="searchDone">
          <h3 class="mb-2">Knowledge Graph</h3>
          <svg id="legend"></svg>
          <div v-show="merged" id="mygraph"></div>
          <div v-show="!merged" id="mygraph1"></div>
          <div v-show="!merged" id="mygraph2"></div>
        </v-card>
      </v-col>
      <v-col cols="3">
          <Ranking v-show="searchDone" :retrievers="selectedRetrievers" :rankings="rankings" :selectedNode="selectedNode"></Ranking>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ForceGraph from 'force-graph';
import axios from "axios";
import Card from "@/components/Card.vue";
import Ranking from "@/components/Ranking.vue";
import * as d3 from 'd3'
export default {
  name: "KnowledgeGraph",
  components: {Ranking, Card},
  props: {
    searchQuery: String
  },
  data: function () {
    return {
      merged: true,
      showNeighbors: false,
      topK: 10,
      retrievers: [
        "bm25",
        "bm25prf",
        "ql",
        "qlprf",
        "ColBERT",
        "SentenceBERT",
      ],
      selectedRetrievers: ["bm25", "ql"],

      graph: {
        graph1: {
          nodes: [],
          links: []
        },
        graph2: {
          nodes: [],
          links: []
        },
        graph3: {
          nodes: [],
          links: []
        },
      },
      responses: {
      },
      selectedNode: null,
      plot: {
        mygraph: ForceGraph(),
        mygraph1: ForceGraph(),
        mygraph2: ForceGraph(),
      },
      searchRunning: false,
      searchDone: false,
      rankings: [
        [], []
      ],
      commonIds: []
    }
  },
  // Create the graph structures
  mounted() {
    const ll = ['mygraph', 'mygraph1', 'mygraph2']
    for (const i in ll) {
      const gid = ll[i]
      this.plot[gid](document.getElementById(gid))
          .nodeId('id')
          .nodeAutoColorBy('retriever')
          .backgroundColor("white")
          .width("600")
          .height(gid === "mygraph" ? 600 : 300)
          .onNodeClick(node => {
            this.selectedNode = node
          })
          .onBackgroundClick(event => {this.selectedNode = null})
          .nodeCanvasObject((node, ctx, globalScale) => {
            var label = node.name;
            if ("metadata" in node && node.metadata) {
              if (node.metadata.hasOwnProperty('image'))
                label = label + " ℹ️"
            }
            const fontSize = node.score / 3;

            ctx.font = `${fontSize}px Sans-Serif`;
            const textWidth = ctx.measureText(label).width;
            const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding

            ctx.fillStyle = 'rgba(255, 255, 255, 0)';

            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = node.color;
            ctx.fillText(label, node.x, node.y);

            node.__bckgDimensions = bckgDimensions;
          })
          .nodePointerAreaPaint((node, color, ctx) => {
            ctx.fillStyle = color;
            const bckgDimensions = node.__bckgDimensions;
            bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
          })
          .linkDirectionalParticleWidth((item) => {
            return item.type === "main" ? 2 : 0
          })
          .linkDirectionalParticles(1)
          .linkDirectionalParticleSpeed(0.01)

          .linkCanvasObjectMode(() => 'after')
          .linkCanvasObject((link, ctx) => {
            const MAX_FONT_SIZE = 2;
            const LABEL_NODE_MARGIN = this.plot[gid].nodeRelSize() * 1.5;

            const start = link.source;
            const end = link.target;

            if (typeof start !== 'object' || typeof end !== 'object') return;

            const textPos = Object.assign(...['x', 'y'].map(c => ({
              [c]: start[c] + (end[c] - start[c]) / 2
            })));

            const relLink = {x: end.x - start.x, y: end.y - start.y};

            const maxTextLength = Math.sqrt(Math.pow(relLink.x, 2) + Math.pow(relLink.y, 2)) - LABEL_NODE_MARGIN * 2;

            let textAngle = Math.atan2(relLink.y, relLink.x);
            if (textAngle > Math.PI / 2) textAngle = -(Math.PI - textAngle);
            if (textAngle < -Math.PI / 2) textAngle = -(-Math.PI - textAngle);

            const label = link.p;
            ctx.font = '1px Sans-Serif';
            const fontSize = Math.min(MAX_FONT_SIZE, maxTextLength / ctx.measureText(label).width);
            ctx.font = `${fontSize}px Sans-Serif`;
            const textWidth = ctx.measureText(label).width;
            const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding

            ctx.save();
            ctx.translate(textPos.x, textPos.y);
            ctx.rotate(textAngle);

            ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            ctx.fillRect(-bckgDimensions[0] / 2, -bckgDimensions[1] / 2, ...bckgDimensions);

            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = 'darkgrey';
            ctx.fillText(label, 0, 0);
            ctx.restore();
          })
    }
  },
  methods: {
    // Maintain the node color based on appearance in retrieval results
    nodeColor: function(node) {
      if (this.commonIds.includes(node.id))
        return "#F748A5";
      else return (node.retriever === this.selectedRetrievers[0] ? "#2271B2"
          : (node.retriever === this.selectedRetrievers[1] ? "#359B73"
              : ((node.retriever === "Both" ? "#F748A5"
                  : (node.retriever === "query" ? "black" : "#bbb8b8")))))
    },
    // Get sorted order of retrieved entities
    generateRankings: function(res, retriever) {
      return Object.entries(res.retrieved_results).map((item, value) => [+item[1].rank, item]).sort((a, b) => {
        return a[0] - b[0]
      }).map(item => item[1])
    },
    // Send GET request to backend and fetch responses
    search: async function () {
      this.searchDone = false
      this.searchRunning = true

      this.selectedNode = null
      this.commonIds = []
      for (var [index, retriever] of this.selectedRetrievers.entries()) {
        const res = await axios.get(`http://129.97.186.146:5000/search/${retriever}`,
            {params: {query: this.searchQuery, k: this.topK}})
        const data = res.data
        this.responses[retriever] = data
      }
      this.refreshGraphs()
      var legend = d3.select("#legend").attr("width", 600)
          .attr("height", 50)
      legend.selectAll("*").remove()
      legend.append("circle").attr("cx",10).attr("cy",10).attr("r", 6).style("fill", "#2271B2")
      legend.append("circle").attr("cx",210).attr("cy",10).attr("r", 6).style("fill", "#359B73")
      legend.append("circle").attr("cx",410).attr("cy",10).attr("r", 6).style("fill", "#F748A5")
      legend.append("text").attr("x", 20).attr("y", 10).text(`Retrieved by ${this.selectedRetrievers[0]}`).style("font-size", "15px").attr("alignment-baseline","middle")
      legend.append("text").attr("x", 220).attr("y", 10).text(`Retrieved by ${this.selectedRetrievers[1]}`).style("font-size", "15px").attr("alignment-baseline","middle")
      legend.append("text").attr("x", 420).attr("y", 10).text("Retrieved by Both").style("font-size", "15px").attr("alignment-baseline","middle")

      this.searchRunning = false
      this.searchDone = true
    },
    // Regenerate graphs based on new responses
    refreshGraphs: function() {
      for (var [index, retriever] of this.selectedRetrievers.entries()) {
        const data = this.responses[retriever]
        this.rankings[index].length = 0
        this.rankings[index].push(...this.generateRankings(data, index))
      }
      this.generateGraph(this.selectedRetrievers.entries(), this.graph.graph1)
      this.generateGraph(this.selectedRetrievers.slice(0, 1).entries(), this.graph.graph2)
      this.generateGraph(this.selectedRetrievers.slice(1, 2).entries(), this.graph.graph3)
    },
    // Generate graph nodes and links
    generateGraph: function(retrievers, graph) {
      var ids = {}

      graph.nodes = []
      graph.links = []
      // this.rankings = [[], []]
      graph.nodes.push({id: "query", retriever: "query", name: this.searchQuery, score: 12})

      for (var [index, retriever] of retrievers) {
        const data = this.responses[retriever]
        Object.entries(data.retrieved_results).forEach((item, value) => {
          const entryData = item[1]
          const metadata = entryData.metadata
          if (!(item[0] in ids)) {
            graph.nodes.push({
              id: item[0],
              retriever: retriever,
              rank: entryData.rank,
              name: entryData.name,
              score: entryData.score,
              metadata: entryData.meta_data,
              links: entryData.links
            })
            graph.links.push(
                {
                  source: "query",
                  target: item[0],
                  type: "main",
                  p: ""
                }
            )
            ids[item[0]] = graph.nodes.length - 1
          } else {
            graph.nodes[ids[item[0]]].retriever = "Both"
            this.commonIds.push(item[0])
            graph.nodes[ids[item[0]]].score += entryData.score * .8
            graph.nodes[ids[item[0]]].score *= 0.6
          }
          graph.nodes.forEach(node => node.color = this.nodeColor(node))
          if (this.showNeighbors)
            if ("links" in entryData)
              entryData.links.forEach(linkItem => {
                const predicate = linkItem["p"]
                const link = linkItem["v"]
                if (!(link in ids)) {
                  graph.nodes.push({
                    id: link,
                    retriever: "link",
                    rank: 0,
                    name: link,
                    score: entryData.score * .8,
                  })
                  ids[link] = graph.nodes.length - 1
                }
                graph.links.push(
                    {
                      source: item[0],
                      target: link,
                      type: "link",
                      p: predicate
                    })
              })
          })
        this.plot['mygraph'].graphData(this.graph.graph1)
        this.plot['mygraph1'].graphData(this.graph.graph2)
        this.plot['mygraph2'].graphData(this.graph.graph3)
      }
    }
  }
}
</script>

<style scoped>

</style>