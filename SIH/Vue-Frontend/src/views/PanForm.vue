<template>
  <div class="container-fluid">
    <!-- Navbar -->
    <nav class="navbar navbar-dark">
      <a class="navbar-brand mx-auto text-white" href="#">NEURO VISION</a>
    </nav>

    <div class="row aadhar-content">
      <!-- Left side: Upload Document Section -->
      <div class="col-md-6 upload-section d-flex align-items-center justify-content-center">
        <div class="card shadow-lg p-4 bg-body rounded text-light upload-card">
          <div class="card-body">
            <h3 class="section-title">Upload PAN Card Document</h3>
            <div class="upload-file-section">
              <input type="file" @change="handleFileUpload" accept=".pdf,.jpg,.jpeg,.png" class="form-control mb-3" />
              <p class="file-info text-muted">
                <i class="fas fa-upload"></i> Accepts PDF, JPG, JPEG, PNG
              </p>
              <button @click="uploadFile" class="btn btn-primary upload-btn" :disabled="!selectedFile">Upload</button>
            </div>

            <!-- Conditionally render the extracted details if docData is available -->
            <div class="extracted-details mt-4 p-3 border rounded bg-dark text-light" v-if="docData">
              <div class="dotted-box">
                <h5 class="extracted-heading">Extracted Details</h5>
                <div class="extracted-content">
                  <!-- Left Column -->
                  <div class="extracted-left">
                    <p><strong>Language detected:</strong> English</p>
                    <p><strong>Doc type:</strong> PAN Card</p>
                    <p><strong>Confidence:</strong> 0.96</p>
                    <p><strong>Image Dimensions:</strong> 480px (Height) x 600px (Width)</p>
                  </div>
                  <!-- Right Column -->
                  <div class="extracted-right">
                    <p><strong>Name:</strong> {{ docData.name }}</p>
                    <p><strong>Father's Name:</strong> {{ docData.fathersName }}</p>
                    <p><strong>DOB:</strong> {{ docData.dob }}</p>
                    <p><strong>PAN Number:</strong> {{ docData.panNumber }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Show a message if no document has been uploaded yet -->
            <p v-else class="text-muted">No document uploaded yet.</p>
          </div>
        </div>
      </div>

      <!-- Right side: User Input Form -->
      <div class="col-md-6 form-section d-flex align-items-center justify-content-center">
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
              <label for="fathersName" class="input-label">Father's Name</label>
              <input type="text" id="fathersName" class="input-box" v-model="fathersName" @input="checkMatch('fathersName')" placeholder="Enter your father's name" />
              <small v-if="status.fathersName" :class="status.fathersName === 'matched' ? 'text-success' : 'text-danger'">
                {{ status.fathersName === 'matched' ? '✔ Matched' : '✖ Mismatch' }}
              </small>
            </div>
            <div class="mb-5 input-wrapper">
              <label for="dob" class="input-label">Date of Birth</label>
              <input type="date" id="dob" class="input-box" v-model="dob" @input="checkMatch('dob')" />
              <small v-if="status.dob" :class="status.dob === 'matched' ? 'text-success' : 'text-danger'">
                {{ status.dob === 'matched' ? '✔ Matched' : '✖ Mismatch' }}
              </small>
            </div>
            <div class="mb-5 input-wrapper">
              <label for="panNumber" class="input-label">PAN Number</label>
              <input type="text" id="panNumber" class="input-box" maxlength="10" v-model="panNumber" @input="validatePan; checkMatch('panNumber')" placeholder="Enter your PAN number" />
              <small v-if="status.panNumber" :class="status.panNumber === 'matched' ? 'text-success' : 'text-danger'">
                {{ status.panNumber === 'matched' ? '✔ Matched' : '✖ Mismatch' }}
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
      fathersName: '',
      dob: '',
      panNumber: '',
      docData: null, // Initialize as null
      status: {
        name: null,
        fathersName: null,
        dob: null,
        panNumber: null,
      },
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadFile() {
      const formData = new FormData();
      formData.append('document', this.selectedFile);

      fetch('http://localhost:5000/panupload', {
        method: 'POST',
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          this.docData = data; // Assign received data
          console.log(this.docData);
          this.checkAllMatches();
        })
        .catch(error => console.error('Error uploading file:', error));
    },
    checkAllMatches() {
      this.checkMatch('name');
      this.checkMatch('fathersName');
      this.checkMatch('dob');
      this.checkMatch('panNumber');
    },
    checkMatch(field) {
      if (!this.docData) return;
      switch (field) {
        case 'name':
          this.status.name = this.name.toLowerCase() === this.docData.name.toLowerCase() ? 'matched' : 'mismatch';
          break;
        case 'fathersName':
          this.status.fathersName = this.fathersName.toLowerCase() === this.docData.fathersName.toLowerCase() ? 'matched' : 'mismatch';
          break;
        case 'dob':
          this.status.dob = this.dob === this.docData.dob ? 'matched' : 'mismatch';
          break;
        case 'panNumber':
          this.status.panNumber = this.panNumber === this.docData.panNumber ? 'matched' : 'mismatch';
          break;
      }
    },
    validatePan() {
      if (this.panNumber.length > 10) {
        this.panNumber = this.panNumber.slice(0, 10);
      }
    },
    submitForm() {
      this.$router.push({ path: '/FinalPage' }); // Navigate to Thank You page
    },
  },
};
</script>

<style scoped>
/* Navbar */
.navbar {
  background-color: #2c2c2c;
  padding: 20px;
  font-size: 28px;
}

.navbar a.navbar-brand {
  color: white !important;
  text-decoration: none;
}

/* Content Layout */
.aadhar-content {
  display: flex;
  height: calc(100vh - 76px);
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
  width: 100%;
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
  text-align: left;
}

.extracted-heading {
  text-align: center;
}

.extracted-content {
  display: flex;
  justify-content: space-between;
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
  width: 100%;
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

.submit-btn {
  background-color: #28a745 !important;
  width: 40%;
  padding: 12px 15px;
  margin-top: 20px;
}

.text-success {
  color: #27ae60;
}

.text-danger {
  color: #e74c3c;
}
</style>
