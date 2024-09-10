<template>
  <div class="container-fluid">
    <div class="header">
      <span class="logo-name">Neuro Vision</span>
    </div>
    <div class="content">
      <div class="text-container">
        <h1>Welcome to,</h1>
        <h2 class="dynamic-text">{{ dynamicTitle }}</h2>
      </div>
      <select v-model="selectedDocument" @change="navigateToForm" class="form-control select-document">
        <option value="none">Select Document Type</option>
        <option value="aadhar">Aadhar Card</option>
        <option value="pan">PAN Card</option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      selectedDocument: 'none',
      titles: ["Neuro Vision", "Verify Your Doc Easily"],
      currentTitleIndex: 0,
      dynamicTitle: '',
      isDeleting: false,
      typeSpeed: 150,
    };
  },
  mounted() {
    this.animateText();
  },
  methods: {
    navigateToForm() {
      if (this.selectedDocument === 'aadhar') {
        this.$router.push({ path: '/aadhar' });
      } else if (this.selectedDocument === 'pan') {
        this.$router.push({ path: '/pan' });
      }
    },
    animateText() {
      const targetTitle = this.titles[this.currentTitleIndex];
      let i = this.dynamicTitle.length;
      if (this.isDeleting) {
        // Backspace effect
        this.dynamicTitle = targetTitle.substring(0, i - 1);
        if (this.dynamicTitle === '') {
          this.isDeleting = false;
          this.currentTitleIndex = (this.currentTitleIndex + 1) % this.titles.length;
        }
      } else {
        // Typing effect
        this.dynamicTitle = targetTitle.substring(0, i + 1);
        if (this.dynamicTitle === targetTitle) {
          this.isDeleting = true;
        }
      }
      let timeout = this.isDeleting ? this.typeSpeed / 2 : this.typeSpeed;
      setTimeout(this.animateText, timeout);
    }
  },
};
</script>

<style scoped>
.container-fluid {
  height: 100vh;
  background: url('~@/assets/darkimage.jpg') no-repeat center center fixed;
  background-size: cover;
  color: white;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  align-items: center;
  padding: 20px 5%; /* Spacing from the edges */
}

.logo-name {
  font-size: 2rem;
  font-weight: bold;
}

.content {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 5%;
}

.text-container {
  text-align: left;
}

h1 {
  font-size: 3.5rem; /* Increased font size */
  margin: 0;
  font-weight: bold;
}

h2 {
  font-size: 2rem;
  position: relative;
  display: inline-block;
  margin: 0;
}

.dynamic-text::after {
  content: '|';
  position: absolute;
  right: 0;
  animation: blink 1s infinite;
}

@keyframes blink {
  50% {
    opacity: 0;
  }
}

.select-document {
  width: 40%; /* Adjust width */
  height: 60px; /* Increased height */
  font-size: 1.75rem; /* Increased font size */
  color: white;
  background-color: black;
  border: 2px solid white;
}
</style>
