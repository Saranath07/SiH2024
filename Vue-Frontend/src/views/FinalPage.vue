<template>
  <div class="aadhar-content d-flex flex-column align-items-center justify-content-center">
    <h1>Thank You!</h1>
    <p>Your document has been verified successfully.</p>
    <button @click="redirectToLandingPage" class="btn btn-primary mt-3">Do you want to verify another document?</button>
  </div>
</template>

<script>
export default {
  methods: {
    redirectToLandingPage() {
      this.$router.push({ path: '/' }); // Redirect to landing page
    },
  },
};
</script>

<style scoped>
.aadhar-content {
  height: 100vh;
  width: 100%;
  background-color: black; /* Solid black background */
  background-image: url('~@/assets/darkimage.jpg'); /* Background image from assets */
  background-size: cover; /* Cover the entire space */
  background-repeat: no-repeat; /* No repetition */
  background-position: center; /* Center the background image */
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  color: white; /* Light text for readability */
}

h1, p {
  font-size: 2em; /* Increase the font size for better visibility */
}

.btn-primary {
  background-color: #007bff; /* Bootstrap primary color */
  border-color: #007bff; /* Matching border */
  font-size: 1.25em; /* Slightly larger buttons */
}
</style>
