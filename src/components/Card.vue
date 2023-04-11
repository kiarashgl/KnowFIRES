<template>
<div v-if="entity" :key="entity.id">
  <h3>Related Content</h3>
  <v-card >
    <v-img v-if="hasImage" :src="entity.metadata.image"></v-img>
    <v-card-title>
      <a :href="'https://en.wikipedia.org/wiki/' + entity.id">
        {{ entity.name }}
      </a>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-subtitle v-if="entity.metadata.type">
      Type:
      <v-chip class="ma-1" v-for="item in entity.metadata.type">{{ item }}</v-chip>
    </v-card-subtitle>
    <v-card-text>

      <div v-if="entity.metadata.subject" id="subjects">
        Related subjects:
        <v-chip class="my-1 mr-1" v-for="(item, i) in entity.metadata.subject" :key="i">{{ replaceUnderline(item) }}</v-chip>

      </div>
    </v-card-text>
  </v-card>
</div>

</template>

<script>
export default {
  name: "Card",
  props: {
    entity: {
      type: Object,
      required: false,
      default: null
    }
  },
  computed: {
    hasImage: function () {
      return this.entity.metadata.hasOwnProperty('image')
    }
  },
  methods: {
    replaceUnderline: function (text) {
      return text.replaceAll("_", " ")
    }
  }
}
</script>

<style scoped>
.v-chip {
  border-radius: 12px !important;
  font-size: 12px !important;
  height: 24px !important;
}

a {
  text-decoration: none;
}

.v-card__title {
  word-break: normal;
}

</style>