<script>
export default {
  data() {
    return {
      url: '',
      checkedUrl: '',
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

      const serverErrorMsg =
        'Server Error: We could not check the validity of the Gemini site at this time. ' +
        "This does not necessary mean the site is down (we don't know either way).";

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
      this.validity = null;
      this.onLoading();

      this.checkedUrl = this.url.startsWith('gemini://') ? this.url : `gemini://${this.url}`;

      try {
        const requestUrl = `/api/v1/check`;
        fetch(requestUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: this.checkedUrl }),
        })
          .then((res) => {
            if (!res.ok) {
              this.serverError = true;
              this.result = false;
            }

            const contentType = res.headers.get('content-type');
            if (contentType && contentType.indexOf('application/json') !== -1) {
              return res.json();
            } else {
              return Promise.resolve({
                message: serverErrorMsg,
              });
            }
          })
          .then((data) => {
            if (data) {
              if (!this.serverError) {
                this.result = data.result;
              }
              this.message = data.message ? data.message : '';
            }
            this.doneLoading();
          });
      } catch (err) {
        this.serverError = true;
        this.result = false;
        this.message = serverErrorMsg;
      }
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
      if (this.loaderIntervalId) {
        clearInterval(this.loaderIntervalId);
        this.loaderIntervalId = 0;
      }
      this.dots = '...';
      this.loading = false;
    },
  },
  computed: {
    validatedUrl() {
      if (this.result === null) {
        return null;
      }
      return this.result ? this.url : null;
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
        <div class="flex flex-col md:basis-4/5 my-4 md:my-0">
          <input
            v-model="url"
            ref="url"
            name="url"
            required
            placeholder="gemini://my-cool-site.party"
            class="w-full px-2 py-1 border-solid border-black rounded"
            :class="{ 'border-orange-600': !!validity }"
            aria-labelledby="urllabel"
          />
          <div
            class="h-8 text-orange-600"
            :class="{ visible: !!validity, invisible: !validity }"
            aria-live="polite"
          >
            <div>Please enter a URL</div>
          </div>
        </div>
        <div>
          <button
            class="md:w-32 md:flex-none md:ml-4 bg-blue-500 disabled:bg-blue-300 hover:bg-blue-800 text-white font-bold px-2 py-1 rounded"
            :disabled="loading"
          >
            Check site
          </button>
        </div>
      </div>
      <div class="w-full px-8">
        <div class="my-2">
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
            <div v-if="result" class="text-green-800">
              Yes, it looks like {{ checkedUrl }} is online.
            </div>
            <div v-else class="ml-0">
              <div v-if="!serverError">
                No, {{ checkedUrl }} is not online.
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
