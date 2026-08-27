const API_BASE = "http://127.0.0.1:8000";

const fileInput = document.getElementById("csvFile");
const uploadArea = document.getElementById("uploadArea");
const analyzeBtn = document.getElementById("analyzeBtn");
const fileName = document.getElementById("fileName");

const statusMessage = document.getElementById("statusMessage");
const resultsSection = document.getElementById("resultsSection");

const totalFlows = document.getElementById("totalFlows");
const attackFlows = document.getElementById("attackFlows");
const benignFlows = document.getElementById("benignFlows");
const attackRate = document.getElementById("attackRate");

const attackTypes = document.getElementById("attackTypes");
const resultsTableBody = document.getElementById("resultsTableBody");


/* =========================================
   FILE SELECTION
========================================= */

fileInput.addEventListener("change", () => {

    if (!fileInput.files.length) {
        fileName.textContent = "No file selected";
        analyzeBtn.disabled = true;
        return;
    }

    const file = fileInput.files[0];

    if (!file.name.toLowerCase().endsWith(".csv")) {

        fileName.textContent = "Please select a CSV file";
        analyzeBtn.disabled = true;

        return;
    }

    fileName.textContent = file.name;
    analyzeBtn.disabled = false;
});


/* =========================================
   DRAG & DROP
========================================= */

uploadArea.addEventListener("dragover", (event) => {

    event.preventDefault();

    uploadArea.classList.add("dragging");
});


uploadArea.addEventListener("dragleave", () => {

    uploadArea.classList.remove("dragging");
});


uploadArea.addEventListener("drop", (event) => {

    event.preventDefault();

    uploadArea.classList.remove("dragging");

    const files = event.dataTransfer.files;

    if (!files.length) {
        return;
    }

    const file = files[0];

    if (!file.name.toLowerCase().endsWith(".csv")) {

        fileName.textContent = "Please select a CSV file";
        analyzeBtn.disabled = true;

        return;
    }

    fileInput.files = files;

    fileName.textContent = file.name;
    analyzeBtn.disabled = false;
});


/* =========================================
   ANALYZE CSV
========================================= */

analyzeBtn.addEventListener("click", async () => {

    if (!fileInput.files.length) {
        return;
    }

    const file = fileInput.files[0];

    const formData = new FormData();

    formData.append("file", file);


    analyzeBtn.disabled = true;

    statusMessage.textContent = "Analyzing network flows...";
    statusMessage.className = "status loading";


    try {

        const response = await fetch(
            `${API_BASE}/predict-csv`,
            {
                method: "POST",
                body: formData
            }
        );


        if (!response.ok) {

            let errorMessage = "Prediction failed.";

            try {

                const errorData = await response.json();

                if (errorData.detail) {
                    errorMessage = errorData.detail;
                }

            } catch (_) {}

            throw new Error(errorMessage);
        }


        const data = await response.json();


        displayResults(data);


        statusMessage.textContent =
            "Analysis completed successfully.";

        statusMessage.className = "status success";


    } catch (error) {

        console.error(error);

        statusMessage.textContent =
            "Error: " + error.message;

        statusMessage.className = "status error";


    } finally {

        analyzeBtn.disabled = false;
    }
});


/* =========================================
   DISPLAY RESULTS
========================================= */

function displayResults(data) {

    resultsSection.style.display = "block";


    totalFlows.textContent =
        formatNumber(data.total_flows);

    attackFlows.textContent =
        formatNumber(data.attacks);

    benignFlows.textContent =
        formatNumber(data.benign);

    attackRate.textContent =
        `${data.attack_rate}%`;


    displayAttackTypes(data.attack_types);

    displayResultsTable(data.results);


    resultsSection.scrollIntoView({
        behavior: "smooth"
    });
}


/* =========================================
   ATTACK TYPE DISTRIBUTION
========================================= */

function displayAttackTypes(types) {

    attackTypes.innerHTML = "";


    if (!types || Object.keys(types).length === 0) {

        attackTypes.innerHTML = `
            <div class="empty-state">
                No attacks detected
            </div>
        `;

        return;
    }


    const entries =
        Object.entries(types);


    entries.forEach(([type, count]) => {

        const item =
            document.createElement("div");

        item.className = "attack-type-item";


        const percentage =
            calculatePercentage(
                count,
                entries.reduce(
                    (sum, [, value]) =>
                        sum + value,
                    0
                )
            );


        item.innerHTML = `

            <div class="attack-type-header">

                <span class="attack-type-name">
                    ${escapeHtml(type)}
                </span>

                <span class="attack-type-count">
                    ${formatNumber(count)}
                </span>

            </div>


            <div class="progress-bar">

                <div
                    class="progress-fill"
                    style="width: ${percentage}%"
                ></div>

            </div>

        `;


        attackTypes.appendChild(item);

    });
}


/* =========================================
   RESULTS TABLE
========================================= */

function displayResultsTable(results) {

    resultsTableBody.innerHTML = "";


    if (!results || results.length === 0) {

        resultsTableBody.innerHTML = `
            <tr>
                <td colspan="5">
                    No prediction results available.
                </td>
            </tr>
        `;

        return;
    }


    results.forEach((result) => {

        const row =
            document.createElement("tr");


        const confidence =
            Number(result.confidence || 0) * 100;


        const statusClass =
            result.label === "ATTACK"
                ? "attack"
                : "benign";


        row.innerHTML = `

            <td>
                ${result.flow}
            </td>

            <td>
                <span class="status-badge ${statusClass}">
                    ${escapeHtml(result.label)}
                </span>
            </td>

            <td>
                ${escapeHtml(result.threat_type)}
            </td>

            <td>
                ${confidence.toFixed(2)}%
            </td>

            <td>
                ${escapeHtml(result.prediction)}
            </td>

        `;


        resultsTableBody.appendChild(row);

    });
}


/* =========================================
   UTILITIES
========================================= */

function formatNumber(number) {

    return Number(number).toLocaleString();
}


function calculatePercentage(value, total) {

    if (!total) {
        return 0;
    }

    return ((value / total) * 100).toFixed(1);
}


function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent =
        String(value);

    return div.innerHTML;
}