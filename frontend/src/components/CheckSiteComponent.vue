<script>
export default {
  data() {
    return {
      url: '',
      serverError: null,
      result: null,
      message: null,
      loading: null,
      loaderIntervalId: 0,
      dots: '',
      validity: null,
    };
  },
  methods: {
    onSubmit() {
      this.loading = null;
      this.result = null;
      this.message = null;
      this.serverError = null;

      if (!this.$refs.form.checkValidity()) {
        if (!!this.validity) {
          this.validity = null;
          setTimeout(() => {
            this.validity = this.$refs.url.validity;
          }, 200);
        } else {
          this.validity = this.$refs.url.validity;
        }
        return;
      }
      this.onLoading();

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
          this.doneLoading();
        });
    },
    updateDots() {
      if (this.dots === '...') {
        this.dots = '';
      } else {
        this.dots += '.';
      }
    },
    onLoading() {
      this.loading = true;
      this.loaderIntervalId = setInterval(() => this.updateDots(), 500);
    },
    doneLoading() {
      this.dots = '...';
      this.loading = false;
      if (this.loaderIntervalId) {
        clearInterval(this.loaderIntervalId);
        this.loaderIntervalId = 0;
      }
    },
  },
};
</script>

<template>
  <div class="container max-w-screen-md mx-auto">
    <div class="my-4 text-center text-xl">
      <div id="urllabel">Enter a gemini:// URL to check if it's serving a Gemini site</div>
    </div>
    <form ref="form" @submit.prevent="onSubmit()" class="container mx-auto" novalidate>
      <div class="md:flex w-full px-8">
        <div class="md:basis-4/5 my-4 md:my-0">
          <input
            v-model="url"
            ref="url"
            name="url"
            type="url"
            required
            pattern="gemini://.*"
            placeholder="gemini://my-cool-site.party"
            class="w-full px-2 py-1 border-solid border-black invalid:[&:not(:placeholder-shown):not(:focus)]:border-orange-600 rounded"
            aria-labelledby="urllabel"
          />
        </div>
        <div>
          <button
            class="md:w-32 md:flex-none md:ml-4 bg-blue-500 hover:bg-blue-700 text-white font-bold px-2 py-1 rounded"
          >
            Check site
          </button>
        </div>
      </div>
      <div class="w-full px-8">
        <div class="my-4 md:my-0">
          <div v-if="!!validity" class="text-orange-600" aria-live="polite">
            <div v-if="validity.patternMismatch">
              Please enter a valid Gemini url, starting with gemini://
            </div>
            <div v-else-if="validity.valueMissing">Please enter a URL</div>
          </div>
          <div
            v-if="loading !== null"
            class="my-4 font-bold"
            aria-live="polite"
            aria-atomic="false"
          >
            <span aria-atomic="true">Checking</span><span ref="spinner">{{ dots }}</span
            ><span v-if="!loading">done!</span>
          </div>
          <div v-if="result !== null" class="my-4 text-pink-800" aria-live="polite">
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
      </div>
    </form>
  </div>
</template>
