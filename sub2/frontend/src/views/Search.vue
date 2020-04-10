<template>
  <v-container>
    <v-layout justify-center wrap mt-5>
      <v-flex md8 xs8>
        <autocomplete
          :search="search"
          placeholder="음식점을 찾아보세요"
          aria-label="Search for a country"
  >
    <template
      #default="{
        rootProps,
        inputProps,
        inputListeners,
        resultListProps,
        resultListListeners,
        results,
        resultProps
      }"
      
    >
      <div v-bind="rootProps">
        <custom-input
          v-bind="inputProps"
          v-on="inputListeners"
          :class="[
            'autocomplete-input',
            { 'autocomplete-input-no-results': noResults },
            { 'autocomplete-input-focused': focused }
          ]"
          @focus="handleFocus"
          @blur="handleBlur"
          @change="handleChange"
        ></custom-input>
        <ul
          v-if="noResults"
          class="autocomplete-result-list"
          style="position: absolute; z-index: 1; width: 100%; top: 100%;"
        >
          <li class="autocomplete-result">
            No results found
          </li>
        </ul>
        <v-container v-bind="resultListProps" v-on="resultListListeners" class="pa-0" style="
    background: #ffffff;">
          <v-hover
          v-slot:default="{ hover }"
        open-delay="50"
        v-for="(result, index) in results"
            :key="resultProps[index].id"
            v-bind="resultProps[index]">
            <v-card
            flat
            :color = "hover || findSeleted(resultProps[index])? '#cccccc' : 'white' "
            class="px-3"
          >
            <v-row>
              <v-col class="">
                {{result}}
              </v-col>
              <v-col justify-right class="text-right">
                임시
              </v-col>
            </v-row>   
          </v-card>
          </v-hover>

          
        </v-container>
      </div>
    </template>
  </autocomplete>
      </v-flex>
    </v-layout>
    <v-row>
      <v-col>
        
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Card from "@/components/Card";
import StoreListCard from "@/components/StoreListCard";
import Autocomplete from "@trevoreyre/autocomplete-vue";
import { mapState, mapActions } from "vuex";
import CustomInput from "@/components/CustomInput"
import http from "../http-common";
import axios from "axios";

const wikiUrl = 'https://en.wikipedia.org'
const params = 'action=query&list=search&format=json&origin=*'

export default {
  components: {
    Autocomplete,
    CustomInput },

  data: () => ({
    focused: false,
    value: '',
    results: [],
  }),
  computed: {
    noResults() {
      return this.value && this.results.length === 0;
    } },

  methods: {
    handleFocus() {
      console.log("handleFocus")
      this.focused = true;
    },

    handleBlur() {
      console.log("handleBlur")
      this.focused = false;
    },
    search(input) {
    let form = new FormData() 
    form.append('keyword', input)
      return new Promise(resolve => {
        if (input.length < 2) {
            return resolve([])
        }

        http
          .post("/api/review/SearchStoreforComplete/",form)
          .then(response => {
            // console.log(response.data)
            var list = []
            response.data.forEach(element => list.push(element.store_name))
            console.log(list)
            this.results = list
            return resolve(this.results)
          })
          .catch(err => {
            return resolve([])
          })

      })
      
    },
    findSeleted(str){
      console.log("findSeleted")
      return "aria-selected" in str
    },
    handleChange(input){
      console.log("handleChange"+" "+input.target.value)
    },
    
    
  }
}
</script>

<style scoped>
.autocomplete-input-no-results.autocomplete-input-focused {
  border: 3px solid green;
  /* border-bottom-color: transparent;
  border-radius: 8px 8px 0 0; */
}
.autocomplete-input-no-results:not(.autocomplete-input-focused) ~ .autocomplete-result-list {
  display: none;
}
input:focus { 
  outline: none;
  border: 5px solid green;
}

input {
  border: 5px solid gray;
  border-radius: 20px;
  padding:20px;
  width:100%
}

.v-card{
  margin : 0px
}
</style>
