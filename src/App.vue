<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >

      <v-spacer></v-spacer>

    </v-app-bar>

    <v-main>
      <KnowledgeGraph></KnowledgeGraph>
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
    //
  }),
};
</script>
