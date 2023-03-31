<template>
  <v-card v-if="entity">
    <v-card-text>
      <div>
        <a :href="'https://en.wikipedia.org/wiki/' + entity.id"><h1>
          {{entity.name}}
        </h1></a>
<!--        <a href="google.com">{{entity.name}}</a>-->
      </div>
      <div v-if="entity.metadata.type">
        Type:
        <v-chip class="ma-1" v-for="item in entity.metadata.type">{{item}}</v-chip>

      </div>
      <v-img v-if="hasImage" :src="entity.metadata.image"></v-img>
      <div v-if="entity.metadata.subject" id="subjects">
        Related subjects:
        <v-chip class="ma-1" v-for="item in entity.metadata.subject">{{item}}</v-chip>

      </div>
<!--      {{entity.metadata}}-->
    </v-card-text>
  </v-card>
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
  }
}
</script>

<style scoped>
.v-chip {
  border-radius: 12px!important;
  font-size: 12px!important;
  height: 24px!important;
}
</style>