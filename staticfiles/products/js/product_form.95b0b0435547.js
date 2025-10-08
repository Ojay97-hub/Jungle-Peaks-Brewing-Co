document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector("[data-image-input]");
    const previewImage = document.querySelector("[data-image-preview]");
    const placeholder = document.querySelector("[data-image-placeholder]");
    const filenameOutput = document.querySelector("[data-image-filename]");

    if (fileInput) {
        fileInput.addEventListener("change", () => {
            const file = fileInput.files[0];

            if (!file) {
                if (previewImage && !previewImage.dataset.hasOriginal) {
                    previewImage.hidden = true;
                    if (placeholder) {
                        placeholder.hidden = false;
                    }
                }
                if (filenameOutput) {
                    filenameOutput.textContent = "No image selected";
                }
                return;
            }

            if (filenameOutput) {
                filenameOutput.textContent = file.name;
            }

            if (!previewImage) {
                return;
            }

            const reader = new FileReader();
            reader.addEventListener("load", () => {
                previewImage.src = reader.result;
                previewImage.hidden = false;
                if (placeholder) {
                    placeholder.hidden = true;
                }
            });
            reader.readAsDataURL(file);
        });
    }
});
