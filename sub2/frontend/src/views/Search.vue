<template>
  <v-container>
    <v-layout justify-center wrap mt-5>
      <v-flex md8 xs8>
        <autocomplete
          :search="search"
          placeholder="음식점을 찾아보세요"
          aria-label="Search for a country"
          @submit="onSubmit"
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
              <v-container
                v-bind="resultListProps"
                v-on="resultListListeners"
                class="pa-0"
                style="
    background: #ffffff;"
              >
                <v-hover
                  v-slot:default="{ hover }"
                  open-delay="50"
                  v-for="(result, index) in results"
                  :key="resultProps[index].id"
                  v-bind="resultProps[index]"
                >
                  <v-card
                    flat
                    :color="
                      hover || findSeleted(resultProps[index])
                        ? '#cccccc'
                        : 'white'
                    "
                    class="px-3"
                  >
                    <v-row>
                      <v-col class="">
                        {{ result }}
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
    <v-layout justify-center wrap mt-5>
      <v-flex md8 xs12
        >s
        <v-layout justify-end md12>
          <v-btn text @click.stop="filterDialog = true">filter</v-btn>
          <v-dialog v-model="filterDialog" max-width="300">
            <v-card>
              <v-card-title>
                <span class="headline">Filter</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" class="pb-0">
                      정렬순
                      <v-radio-group v-model="orderStandard" column>
                        <v-radio label="이름순" value="name"></v-radio>
                        <v-radio label="리뷰순" value="review"></v-radio>
                        <v-radio label="평점순" value="score"></v-radio>
                      </v-radio-group>
                    </v-col>
                  </v-row>
                  <v-layout justify-end>
                    <v-btn color="primary">적용하기</v-btn>
                  </v-layout>
                </v-container>
              </v-card-text>
            </v-card>
          </v-dialog>
        </v-layout>
        <v-layout justify-center>
          <v-card> </v-card>
          put list
        </v-layout>
      </v-flex>
      <v-flex md4 class="d-none d-md-block">
        <v-col>
          map
        </v-col>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Card from '@/components/Card'
import StoreListCard from '@/components/StoreListCard'
import Autocomplete from '@trevoreyre/autocomplete-vue'
import { mapState, mapActions } from 'vuex'
import CustomInput from '@/components/CustomInput'
import http from '../http-common'
import axios from 'axios'

export default {
  components: {
    Autocomplete,
    CustomInput
  },

  data: () => ({
    focused: false,
    value: '',
    results: [],
    keyword: '',
    filterDialog: false,
    orderStandard: 'name'
  }),
  computed: {
    noResults() {
      return this.value && this.results.length === 0
    }
  },

  methods: {
    handleFocus() {
      console.log('handleFocus')
      this.focused = true
    },

    handleBlur() {
      console.log('handleBlur')
      this.focused = false
    },
    search(input) {
      let form = new FormData()
      form.append('keyword', input)
      this.keyword = input
      return new Promise(resolve => {
        if (input.length < 2) {
          return resolve([])
        }

        http
          .post('/api/review/SearchStoreforComplete/', form)
          .then(response => {
            // console.log(response.data)
            var list = []
            response.data.forEach(element => list.push(element.store_name))
            console.log(list)
            resolve(list)
          })
          .catch(err => {
            resolve([])
          })
      })
    },
    findSeleted(str) {
      console.log('findSeleted')
      return 'aria-selected' in str
    },
    handleChange(input) {
      console.log('handleChange' + ' ' + input.target.value)
    },
    onSubmit(result) {
      // if(result != undefined && result.length > this.keyword.length){
      //   alert(result)
      // }else{
      //   alert(this.keyword)
      // }
    }
  }
}
</script>

<style scoped>
.autocomplete-input-no-results.autocomplete-input-focused {
  border: 3px solid green;
  /* border-bottom-color: transparent;
  border-radius: 8px 8px 0 0; */
}
.autocomplete-input-no-results:not(.autocomplete-input-focused)
  ~ .autocomplete-result-list {
  display: none;
}
input:focus {
  outline: none;
  border: 5px solid green;
}

input {
  border: 5px solid gray;
  border-radius: 20px;
  padding: 20px;
  width: 100%;
}

.v-card {
  margin: 0px;
}
</style>
