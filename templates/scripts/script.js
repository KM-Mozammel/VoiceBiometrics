async function upload() {
      const file1 = document.getElementById('file1').files[0];
      const file2 = document.getElementById('file2').files[0];
      const errorDiv = document.getElementById('error');
      const resultDiv = document.getElementById('result');
      errorDiv.textContent = "";
      resultDiv.textContent = "";

      if (!file1 || !file2) {
        errorDiv.textContent = "⚠️ Please select both audio files!";
        return;
      }

      try {
        const formData = new FormData();
        formData.append("file1", file1);
        formData.append("file2", file2);

        const response = await fetch("http://192.168.0.192:5000/compare", {
          method: "POST",
          body: formData
        });

        const result = await response.json();

        if (!response.ok || result.error) {
          errorDiv.textContent = "❌ Error: " + (result.error || response.statusText);
        } else {
          resultDiv.textContent = JSON.stringify(result, null, 2);
        }
      } catch (err) {
        errorDiv.textContent = "❌ Network Error: " + err.message;
      }
    }