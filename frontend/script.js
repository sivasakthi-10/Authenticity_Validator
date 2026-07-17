async function uploadFile() {

    const fileInput = document.getElementById("fileInput");

    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file.");
        return;
    }

    document.getElementById("loading").style.display = "block";
    document.getElementById("result").style.display = "none";

    const formData = new FormData();
    formData.append("file", file);

    try {

        const response = await fetch("http://127.0.0.1:5000/upload", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        document.getElementById("loading").style.display = "none";
        document.getElementById("result").style.display = "block";

        document.getElementById("filename").innerText = data.filename;

        document.getElementById("plagiarism").innerText = data.plagiarism_score;

        document.getElementById("ai").innerText = data.ai_generated_score;

        document.getElementById("originality").innerText = data.originality;

    }

    catch(error){

        console.log(error);

        alert("Server Error");

        document.getElementById("loading").style.display="none";

    }

}
