<template>
  <div class="aadhar-page-container">
    <!-- Navbar -->
    <nav class="navbar navbar-dark">
      <a class="navbar-brand mx-auto text-white" href="#">NEURO VISION</a>
    </nav>

    <div class="aadhar-content">
      <!-- Left Side: Upload Document Section -->
      <div class="upload-section">
        <div class="card shadow-lg p-4 bg-body rounded text-light upload-card">
          <div class="card-body">
            <h3 class="section-title">Upload Aadhar Document</h3>
            <div class="upload-file-section">
              <input type="file" @change="handleFileUpload" accept=".pdf,.jpg,.jpeg,.png" class="form-control mb-3" />
              <p class="file-info text-muted">
                <i class="fas fa-upload"></i> Accepts PDF, JPG, JPEG, PNG
              </p>
              <button @click="uploadFile" class="btn btn-primary upload-btn" :disabled="!selectedFile">Upload</button>
            </div>

            <!-- Show Loading Spinner While Uploading -->
            <div v-if="loading" class="loading-spinner">
              <i class="fas fa-circle-notch fa-spin fa-2x"></i> Uploading...
            </div>

            <!-- Dotted Box for Extracted Details -->
            <div class="extracted-details mt-4 p-3 border rounded bg-dark text-light" v-if="!loading">
              <div class="dotted-box">
                <h3 class="extracted-heading">Extracted Details</h3> <!-- Center the heading -->
                <div class="extracted-content" v-if="docData">
                  <!-- Left Column -->
                  <div class="extracted-left">
                    <p><strong>Language detected:</strong> English</p>
                    <p><strong>Doc type:</strong> Aadhar</p>
                    <p><strong>Confidence:</strong> 0.96</p>
                    <p><strong>Image Dimensions:</strong> 480px (Height) x 600px (Width)</p>
                  </div>
                  <!-- Right Column -->
                  <div class="extracted-right">
                    <p><strong>Name:</strong> {{ docData.name }}</p>
                    <p><strong>DOB:</strong> {{ docData.dob }}</p>
                    <p><strong>Gender:</strong> {{ docData.gender }}</p>
                    <p><strong>Aadhar Number:</strong> {{ docData.aadharNumber }}</p>
                  </div>
                </div>
                <p v-else class="text-muted">No document uploaded yet.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Side: User Input Form -->
      <div class="form-section">
        <div class="input-container card shadow-lg p-4 bg-body rounded text-light">
          <form @submit.prevent="submitForm" class="form-group">
            <h4 class="section-title">Enter Your Details</h4>

            <div class="mb-5 input-wrapper">
              <label for="name" class="input-label">Name</label>
              <input type="text" id="name" class="input-box" v-model="name" @input="checkMatch('name')" placeholder="Enter your name" />
              <small v-if="status.name" :class="status.name === 'matched' ? 'text-success' : 'text-danger'">
                {{ status.name === 'matched' ? '✔ Matched' : '✖ Mismatch' }}
              </small>
            </div>

            <div class="mb-5 input-wrapper">
              <label for="dob" class="input-label">Date of Birth</label>
              <input type="date" id="dob" class="input-box" v-model="dob" @input="checkMatch('dob')" />
              <small v-if="status.dob" :class="status.dob === 'matched' ? 'text-success' : 'text-danger'">
                {{ status.dob === 'matched' ? '✔ Matched' : '✖ Mismatch' }}
              </small>
            </div>

            <!-- Gender Radio Buttons -->
            <div class="mb-5 input-wrapper">
              <label class="input-label">Gender</label>
              <br>
              <div class="radio-group">
                <div class="form-check">
                  <input type="radio" id="male" value="male" v-model="gender" @change="checkMatch('gender')" class="form-check-input" />
                  <label for="male" class="form-check-label">Male</label>
                </div>
                <div class="form-check">
                  <input type="radio" id="female" value="female" v-model="gender" @change="checkMatch('gender')" class="form-check-input" />
                  <label for="female" class="form-check-label">Female</label>
                </div>
                <div class="form-check">
                  <input type="radio" id="other" value="other" v-model="gender" @change="checkMatch('gender')" class="form-check-input" />
                  <label for="other" class="form-check-label">Other</label>
                </div>
              </div>
              <small v-if="status.gender" :class="status.gender === 'matched' ? 'text-success' : 'text-danger'">
                {{ status.gender === 'matched' ? '✔ Matched' : '✖ Mismatch' }}
              </small>
            </div>

            <div class="mb-5 input-wrapper">
              <label for="aadharNumber" class="input-label">Aadhar Number</label>
              <input type="text" id="aadharNumber" class="input-box" maxlength="12" v-model="aadharNumber" @input="validateAadhar; checkMatch('aadharNumber')" placeholder="Enter your Aadhar number" />
              <small v-if="status.aadharNumber" :class="status.aadharNumber === 'matched' ? 'text-success' : 'text-danger'">
                {{ status.aadharNumber === 'matched' ? '✔ Matched' : '✖ Mismatch' }}
              </small>
            </div>

            <button type="submit" class="btn btn-success submit-btn">Submit Form</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      name: '',
      dob: '',
      gender: '',
      aadharNumber: '',
      docData: null,
      status: {
        name: null,
        dob: null,
        gender: null,
        aadharNumber: null,
      },
      loading: false, // To control the loading spinner
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadFile() {
      // Start showing the loading spinner
      this.loading = true;

      const formData = new FormData();
      formData.append('document', this.selectedFile);

      fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          this.docData = data;
          this.checkAllMatches();
        })
        .catch((error) => console.error('Error uploading file:', error))
        .finally(() => {
          // Stop showing the loading spinner
          this.loading = false;
        });
    },
    checkAllMatches() {
      this.checkMatch('name');
      this.checkMatch('dob');
      this.checkMatch('gender');
      this.checkMatch('aadharNumber');
    },
    checkMatch(field) {
      if (!this.docData) return;
      switch (field) {
        case 'name':
          this.status.name = this.name.toLowerCase() === this.docData.name.toLowerCase() ? 'matched' : 'mismatch';
          break;
        case 'dob':
          this.status.dob = this.dob === this.docData.dob ? 'matched' : 'mismatch';
          break;
        case 'gender':
          this.status.gender = this.gender.toLowerCase() === this.docData.gender.toLowerCase() ? 'matched' : 'mismatch';
          break;
        case 'aadharNumber':
          this.status.aadharNumber = this.aadharNumber === this.docData.aadharNumber ? 'matched' : 'mismatch';
          break;
      }
    },
    validateAadhar() {
      if (this.aadharNumber.length > 12) {
        this.aadharNumber = this.aadharNumber.slice(0, 12);
      }
    },
    submitForm() {
      if (!this.isFormValid()) {
        alert('Please fill all the details correctly.');
      } else {
        this.$router.push({ path: '/FinalPage' });
      }
    },
    isFormValid() {
      return (
        this.status.name === 'matched' &&
        this.status.dob === 'matched' &&
        this.status.gender === 'matched' &&
        this.status.aadharNumber === 'matched' &&
        this.selectedFile
      );
    },
  },
};
</script>

<style scoped>
/* Navbar */
.navbar {
  background-color: #2c2c2c;
  padding: 20px; /* Increased padding for larger navbar */
  font-size: 28px;
}

.navbar a.navbar-brand {
  color: white !important;
  text-decoration: none;
}

/* Content Layout */
.aadhar-content {
  display: flex;
  height: calc(100vh - 76px); /* Adjusted for navbar height */
  width: 100%;
  background-color: black;
  color: white;
}

/* Left Section (Upload) */
.upload-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 50px;
}

.upload-card {
  border: 1px solid white;
  width: 100%; /* Full-width on the left side */
  background-color: #000;
}

.upload-file-section {
  margin-bottom: 20px;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dotted-box {
  border: 2px dotted white;
  padding: 20px;
  margin-top: 20px;
  text-align: left; /* Align the text to the left */
}

.extracted-heading {
  text-align: center;
}

.extracted-content {
  display: flex;
  justify-content: space-between;
}

.extracted-left,
.extracted-right {
  flex: 1;
}

/* Right Section (Form) */
.form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 50px;
}

.input-container {
  width: 100%; /* Full-width on the right side */
}

.input-wrapper {
  position: relative;
  margin-bottom: 35px;
}

.input-label {
  position: absolute;
  top: -10px;
  left: 10px;
  background-color: black;
  padding: 0 5px;
  font-size: 14px;
}

.input-box {
  background-color: black;
  border: 2px solid white;
  color: white;
  padding: 8px;
  width: 100%;
  margin-top: 15px;
}

/* Radio Group */
.radio-group {
  display: flex;
  gap: 20px; /* Adjusted gap between radio buttons */
}

.form-check {
  display: flex;
  align-items: center;
}

/* Submit Button */
.submit-btn {
  background-color: #28a745 !important;
  width: 40%;
  padding: 12px 15px;
  margin-top: 20px;
}

/* Loading Spinner */
.loading-spinner {
  text-align: center;
  margin-top: 20px;
  color: white;
}

.text-success {
  color: #27ae60;
}

.text-danger {
  color: #e74c3c;
}
</style>
