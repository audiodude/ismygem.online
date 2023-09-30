<script>
export default {
  data() {
    return {
      url: '',
      serverError: null,
      result: null,
      message: null,
    };
  },
  methods: {
    onSubmit() {
      if (!this.$refs.form.checkValidity()) {
        return;
      }
      const requestUrl = `/api/v1/check`;
      fetch(requestUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: this.url }),
      })
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            this.serverError = true;
            this.result = false;
            this.message =
              'Server Error: We could not check the validity of the Gemini site at this time';
          }
        })
        .then((data) => {
          this.result = data.result;
          this.message = data.message;
        });
    },
  },
};
</script>

<template>
  <div class="w-full max-w-s">
    <div class="mt-4 mb-4 text-center text-xl">
      <div>Enter a gemini:// URL to check if it's serving a Gemini site</div>
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
          <div v-if="result !== null" class="my-4 text-pink-800">
            <div v-if="result" class="text-green-800">Yes, that looks like a valid Gemini site</div>
            <div v-else class="ml-0">
              <div v-if="!serverError">
                No, there was an error connecting to the site
                <ul v-if="message" class="list-disc ml-12">
                  <li>{{ message }}</li>
                </ul>
              </div>
              <div v-else>
                {{ message }}
              </div>
            </div>
          </div>
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
