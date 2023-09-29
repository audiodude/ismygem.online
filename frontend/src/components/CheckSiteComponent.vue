<script>
export default {
  data() {
    return {
      url: '',
      result: null,
    };
  },
  methods: {
    onSubmit() {
      const url = `/api/v1/hello`;
      fetch(url)
        .then((res) => {
          if (res.ok) {
            return res.json();
          }
        })
        .then((data) => {
          this.result = data.result;
        });
    },
  },
};
</script>

<template>
  <form @submit.prevent="onSubmit()">
    <label for="url">Gemini URL</label>
    <div class="input-cont">
      <input
        v-model="url"
        name="url"
        type="url"
        required
        pattern="gemini://.*"
        placeholder="gemini://my-cool-site.party"
      />
    </div>
    <button type="submit">Check site</button>
  </form>
  <div v-if="result">Yes, that is a Gemini site</div>
  <div v-else-if="result === null">
    Enter a gemini:// URL to check if it's serving a Gemini site
  </div>
  <div v-else="!result">Sorry, that Gemini site is down, or isn't a Gemini site at all</div>
</template>

<style scoped>
input:not(:placeholder-shown):invalid {
  border: 2px dashed red;
}

input:valid {
  border: 2px solid black;
}
</style>
