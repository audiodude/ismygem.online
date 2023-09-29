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
      if (!this.$refs.form.checkValidity()) {
        return;
      }
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
  <div class="w-full max-w-s">
    <div class="mt-4 mb-4 text-center text-xl">
      <div v-if="result">Yes, that is a Gemini site</div>
      <div v-else-if="result === null">
        Enter a gemini:// URL to check if it's serving a Gemini site
      </div>
      <div class="italic text-pink-500" v-else="!result">
        Sorry, that Gemini site is down, or isn't a Gemini site at all
      </div>
    </div>
    <form ref="form" @submit.prevent="onSubmit()" class="container mx-auto" novalidate>
      <div class="md:flex md:justify-center w-4/5 md:w-2/3 mx-auto">
        <div class="grow my-4 md:my-0 mr-8">
          <input
            v-model="url"
            name="url"
            type="url"
            required
            pattern="gemini://.*"
            placeholder="gemini://my-cool-site.party"
            class="w-full px-2 py-1 border-solid border-black invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 rounded"
          />
        </div>
        <div>
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold px-2 py-1 rounded"
            type="submit"
          >
            Check site
          </button>
        </div>
      </div>
    </form>
  </div>
</template>
