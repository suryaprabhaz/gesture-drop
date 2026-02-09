/* Author: @SuryaPrabhas */
async function main() {
    const video = document.getElementById("video");
    const output = document.getElementById("output");
    const imgPreview = document.getElementById("image-preview");
    const historyList = document.getElementById("history-list");
    let lastHistoryFetch = 0;

    // Check camera permission
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        alert("⚠️ Please allow camera access to use gesture control.");
        return;
    }

    const model = await handpose.load();
    console.log("Handpose model loaded");

    // Throttling to prevent excessive requests
    let lastRequestTime = 0;
    const requestCooldown = 1000; // 1 second

    async function updateHistory() {
        const now = Date.now();
        if (now - lastHistoryFetch < 5000) return; // Fetch every 5s max

        try {
            const res = await fetch("/history");
            const data = await res.json();

            if (historyList) {
                historyList.innerHTML = data.history.map(item => `
                    <li class="history-item">
                        <span>${item.text}</span>
                        <span class="history-time">${item.time}</span>
                    </li>
                `).join('');
            }
            lastHistoryFetch = now;
        } catch (e) {
            console.error("Failed to fetch history", e);
        }
    }

    // Initial history fetch
    updateHistory();
    setInterval(updateHistory, 10000); // Auto-update history every 10s

    async function detect() {
        const predictions = await model.estimateHands(video);

        if (predictions.length > 0) {
            const hand = predictions[0];
            const landmarks = hand.landmarks;

            const [thumbTip, thumbIP, thumbMCP] = [landmarks[4], landmarks[3], landmarks[2]];
            const [indexTip, middleTip, ringTip, pinkyTip] = [
                landmarks[8], landmarks[12], landmarks[16], landmarks[20]
            ];
            const wrist = landmarks[0];

            // Gesture Logic
            const isThumbUp = thumbTip[1] < thumbIP[1] && thumbIP[1] < thumbMCP[1];

            // Check if other fingers are down (below wrist or curled)
            // Using a simple y-check relative to a lower joint (MCP) roughly
            const indexMCP = landmarks[5];
            const middleMCP = landmarks[9];
            const ringMCP = landmarks[13];
            const pinkyMCP = landmarks[17];

            const areFingersDown =
                indexTip[1] > indexMCP[1] &&
                middleTip[1] > middleMCP[1] &&
                ringTip[1] > ringMCP[1] &&
                pinkyTip[1] > pinkyMCP[1];

            const isOpenPalm =
                indexTip[1] < indexMCP[1] &&
                middleTip[1] < middleMCP[1] &&
                ringTip[1] < ringMCP[1] &&
                pinkyTip[1] < pinkyMCP[1];

            const now = Date.now();

            if (now - lastRequestTime > requestCooldown) {
                if (isThumbUp && areFingersDown) {
                    console.log("Gesture: Thumbs Up (Image Only)");
                    fetchData(true); // Image only
                    lastRequestTime = now;
                } else if (isOpenPalm) {
                    console.log("Gesture: Open Palm (Text + Image)");
                    fetchData(false); // Text + Image
                    lastRequestTime = now;
                }
            }
        }

        requestAnimationFrame(detect);
    }

    function fetchData(imageOnly) {
        output.classList.add("active");
        fetch("/get")
            .then(res => res.json())
            .then(data => {
                if (imageOnly) {
                    output.innerText = "🖼️ Showing Image Only";
                } else {
                    output.innerText = data.text || "Scanning...";
                }

                if (data.image) {
                    imgPreview.src = `/static/uploads/${data.image}`;
                    imgPreview.classList.add("show");
                } else {
                    imgPreview.classList.remove("show");
                }

                // Update history after a successful fetch action
                setTimeout(updateHistory, 1000);
            })
            .catch(err => {
                console.error("Error fetching data:", err);
                output.innerText = "Error connecting to server";
            });

        setTimeout(() => {
            output.classList.remove("active");
        }, 2000);
    }

    detect();
}

main();
