<template>
    <input
      :value="value"
      v-on="$listeners"
      />

</template>

<script>
export default {
    props: {
    value: {
      type: String,
      default: ''
    }
  },
}
</script>

<style scoped>
/* .autocomplete-input-no-results.autocomplete-input-focused {
  border-bottom-color: transparent;
  border-radius: 8px 8px 0 0;
}

.autocomplete-input-no-results:not(.autocomplete-input-focused) ~ .autocomplete-result-list {
  display: none;
} */


</style>