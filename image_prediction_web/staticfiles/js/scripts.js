// File: predictor/static/js/scripts.js
document.addEventListener('DOMContentLoaded', function () {
    // Elements
    const imageInput = document.getElementById('image-input');
    const clearButton = document.getElementById('clear-button');
    const preview = document.getElementById('preview');
    const predictionResults = document.getElementById('prediction-results');

    // Hide preview if prediction results are already displayed (after form submit)
    if (preview && predictionResults) {
        preview.style.display = 'none';
    }

    // Event: Preview selected image
    imageInput.addEventListener('change', function (event) {
        const reader = new FileReader();
        const file = event.target.files[0];

        if (file) {
            reader.onload = function () {
                preview.src = reader.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }

        // Hide previous prediction result
        if (predictionResults) {
            predictionResults.style.display = 'none';
        }
    });

    // Event: Clear form
    clearButton.addEventListener('click', function () {
        imageInput.value = '';

        if (preview) {
            preview.src = '';
            preview.style.display = 'none';
        }

        if (predictionResults) {
            predictionResults.style.display = 'none';
        }
    });
});

