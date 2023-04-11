<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-app-bar-title>KnowFIRES</v-app-bar-title>
      <v-spacer></v-spacer>
        <v-text-field placeholder="Search" v-model="searchQuery" append-icon="mdi-magnify" hide-details dense
        @keyup.enter="search" @click:append="search"></v-text-field>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-main>
      <KnowledgeGraph ref="knowledgeGraph" :searchQuery="searchQuery"></KnowledgeGraph>
    </v-main>
  </v-app>
</template>

<script>
import KnowledgeGraph from "@/components/KnowledgeGraph.vue";

export default {
  name: 'App',

  components: {
    KnowledgeGraph,
  },

  data: () => ({
    searchQuery: ""
  }),
  methods: {
    search: function() {
      this.$refs.knowledgeGraph.search()
    }
  }
};
</script>
