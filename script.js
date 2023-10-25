function validateForm(form) {
    let isValid = true;
    const fields = form.querySelectorAll("[required]");

    fields.forEach((field) => {
        if (field.value.trim() === "") {
            field.classList.add("error"); // Add an error class
            isValid = false;
        } else {
            field.classList.remove("error"); // Remove the error class if the field is filled
        }
    });

    return isValid;
}

// Function to convert an image file to base64
function convertImageToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            resolve(reader.result);
        };
        reader.onerror = (error) => {
            reject(error);
        };
        reader.readAsDataURL(file);
    });
}

const manForm = document.getElementById("manForm");
manForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    if (validateForm(manForm)) {
        const formData = new FormData(manForm);
        const formDataObject = { gender: "man" };

        // Convert image files to base64 and add to formDataObject
        const photoInputs = manForm.querySelectorAll("input[type='file'][name='manPhotos']");
        for (let i = 0; i < photoInputs.length; i++) {
            const input = photoInputs[i];
            const files = input.files;

            for (let j = 0; j < files.length; j++) {
                const file = files[j];
                const base64 = await convertImageToBase64(file);
                formDataObject[`manPhoto${i + 1}`] = base64;
            }
        }

        formData.forEach((value, key) => {
            formDataObject[key] = value;
        });

        
        tg.sendData(JSON.stringify(formDataObject));
        tg.close();
        // Here, you can send the data to the server or perform any other required actions.
    }
});

const womanForm = document.getElementById("womanForm");
womanForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    if (validateForm(womanForm)) {
        const formData = new FormData(womanForm);
        const formDataObject = { gender: "woman" };

        // Convert image files to base64 and add to formDataObject
        const photoInputs = womanForm.querySelectorAll("input[type='file'][name='womanPhotos']");
        for (let i = 0; i < photoInputs.length; i++) {
            const input = photoInputs[i];
            const files = input.files;

            for (let j = 0; j < files.length; j++) {
                const file = files[j];
                const base64 = await convertImageToBase64(file);
                formDataObject[`womanPhoto${i + 1}`] = base64;
            }
        }

        formData.forEach((value, key) => {
            formDataObject[key] = value;
        });

        console.log(formDataObject);
        tg.sendData(JSON.stringify(formDataObject));
        tg.close();
        // Here, you can send the data to the server or perform any other required actions.
    }
});
