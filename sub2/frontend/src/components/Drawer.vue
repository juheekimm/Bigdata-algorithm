<template>
  <v-navigation-drawer
    id="app-drawer"
    v-model="inputValue"
    app
    dark
    floating
    persistent
    mobile-break-point="1800"
    width="250"
  >
    <v-layout column justify-center style="align-items: center;">
      <v-img width="150" class="ma-5" src="../assets/logo.png">
      </v-img>
    </v-layout>
    <v-divider class="mx-4" />
    <v-layout column>
      <v-list rounded>
        <v-list-item
          v-for="(link, i) in links"
          :key="i"
          :to="link.to"
          active-class="blue lighten-1 white--text"
          class="v-list-item ma-3"
        >
          <v-list-item-action>
            <v-icon>{{ link.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-title v-text="link.text" />
        </v-list-item>
      </v-list>
    </v-layout>
  </v-navigation-drawer>
</template>

<script>
import { mapMutations, mapState } from "vuex";

export default {
  props: {
    opened: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    links: [
      {
        to: "/",
        icon: "mdi-home",
        text: "Home"
      },
      {
        to: "/search",
        icon: "mdi-card-search",
        text: "맛집 검색"
      },
      {
        to: "/nearbyStore",
        icon: "mdi-map",
        text: "근처 음식점"
      },
      {
        to: "/aboutus",
        icon: "mdi-human-greeting",
        text: "AboutUs"
      },
      
    ]
  }),
  computed: {
    ...mapState("app", ["drawer"]),
    inputValue: {
      get() {
        return this.drawer;
      },
      set(val) {
        this.setDrawer(val);
      }
    }
  },

  methods: {
    ...mapMutations("app", ["setDrawer"])
  }
};
</script>
