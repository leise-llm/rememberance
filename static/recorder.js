let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
    });
}

function stopRecording() {
    mediaRecorder.stop();
    mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunks, { type: "audio/wav" });
        const formData = new FormData();
        formData.append("audio", blob, "aufnahme.wav");

        fetch("/transcribe", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("result").innerText = "Erkannt: " + (data.text || data.error);
        });
    };
}
