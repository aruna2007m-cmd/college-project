const endpointMap = {
    qa: "/qa",
    explain: "/explain",
    quiz: "/quiz",
    summarize: "/summarize",
    learn: "/learn/recommendations",
    schedule: "/study/schedule"
};


// -----------------------------
// DOM Elements
// -----------------------------

const task = document.getElementById("task");
const scheduleFields = document.getElementById("scheduleFields");

const subjects = document.getElementById("subjects");
const studyHours = document.getElementById("studyHours");
const examDate = document.getElementById("examDate");
const importantTopics = document.getElementById("importantTopics");

const inputText = document.getElementById("inputText");
const submitBtn = document.getElementById("submitBtn");
const clearBtn = document.getElementById("clearBtn");

const resultCard = document.getElementById("resultCard");
const result = document.getElementById("result");
const status = document.getElementById("status");
const copyBtn = document.getElementById("copyBtn");


// -----------------------------
// Placeholders
// -----------------------------

const placeholders = {
    qa: "Example: Which is the largest ocean?",
    explain: "Example: Explain the Pythagoras theorem to a beginner.",
    quiz: "Paste a topic or educational passage here.",
    summarize: "Paste the educational passage you want to summarize.",
    learn: "Example: SQL",
    schedule: "Enter study schedule details below."
};


// -----------------------------
// Task Change
// -----------------------------

task.addEventListener("change", function () {

    inputText.placeholder = placeholders[task.value];

    if (task.value === "schedule") {
        scheduleFields.classList.remove("hidden");
    } else {
        scheduleFields.classList.add("hidden");
    }
});


// -----------------------------
// Clear
// -----------------------------

clearBtn.addEventListener("click", function () {

    inputText.value = "";

    subjects.value = "";
    studyHours.value = "";
    examDate.value = "";
    importantTopics.value = "";

    result.innerHTML = "";

    resultCard.classList.add("hidden");

    status.textContent = "Ready";
});


// -----------------------------
// HTML Escape
// -----------------------------

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// -----------------------------
// Copy Result
// -----------------------------

copyBtn.addEventListener("click", async function () {

    try {

        await navigator.clipboard.writeText(
            result.innerText
        );

        status.textContent = "Copied";

        setTimeout(function () {
            status.textContent = "Ready";
        }, 1200);

    } catch (error) {

        status.textContent = "Copy failed";
    }
});


// -----------------------------
// Render Quiz
// -----------------------------

function renderQuiz(data) {

    result.innerHTML = `
        <div id="quizContainer"></div>

        <button id="checkQuiz">
            Check Answers
        </button>
    `;

    const quizContainer =
        document.getElementById("quizContainer");


    data.questions.forEach(function (question, index) {

        let optionsHTML = "";

        question.options.forEach(
            function (option, optionIndex) {

                optionsHTML += `
                    <label class="quiz-option">

                        <input
                            type="radio"
                            name="q${index}"
                            value="${escapeHtml(option)}"
                        >

                        ${String.fromCharCode(65 + optionIndex)}.
                        ${escapeHtml(option)}

                    </label>
                `;
            }
        );


        quizContainer.insertAdjacentHTML(
            "beforeend",
            `
            <div class="quiz-question">

                <h3>
                    ${index + 1}.
                    ${escapeHtml(question.question)}
                </h3>

                ${optionsHTML}

                <div
                    class="feedback"
                    id="feedback${index}"
                ></div>

            </div>
            `
        );

    });


    document
        .getElementById("checkQuiz")
        .addEventListener(
            "click",
            checkQuizAnswers
        );


    function checkQuizAnswers() {

        let score = 0;

        data.questions.forEach(
            function (question, index) {

                const selected =
                    document.querySelector(
                        `input[name="q${index}"]:checked`
                    );

                const feedback =
                    document.getElementById(
                        `feedback${index}`
                    );


                if (!selected) {

                    feedback.textContent =
                        "Please choose an answer.";

                    return;
                }


                if (
                    selected.value ===
                    question.correct_answer
                ) {

                    score++;

                    feedback.textContent =
                        "Correct ✓";

                } else {

                    feedback.textContent =
                        "Incorrect. Correct answer: " +
                        question.correct_answer;
                }

            }
        );


        const oldScore =
            document.querySelector(".score");

        if (oldScore) {
            oldScore.remove();
        }


        quizContainer.insertAdjacentHTML(
            "afterbegin",
            `
            <div class="score">
                Score:
                ${score}/${data.questions.length}
            </div>
            `
        );
    }
}


// -----------------------------
// Submit Request
// -----------------------------

async function submitRequest() {

    const selectedTask = task.value;
    const text = inputText.value.trim();


    // -------------------------
    // Validate Input
    // -------------------------

    if (selectedTask === "schedule") {

        if (
            !subjects.value.trim() ||
            !studyHours.value.trim() ||
            !examDate.value ||
            !importantTopics.value.trim()
        ) {

            status.textContent =
                "Please fill all schedule fields.";

            return;
        }

    } else {

        if (!text) {

            status.textContent =
                "Enter some text first.";

            inputText.focus();

            return;
        }
    }


    submitBtn.disabled = true;

    status.textContent = "Thinking...";

    resultCard.classList.remove("hidden");

    result.innerHTML =
        "<p>Generating your result...</p>";


    // -------------------------
    // Request Body
    // -------------------------

    let body;


    if (selectedTask === "qa") {

        body = {
            question: text
        };

    } else if (selectedTask === "schedule") {

        body = {
            subjects: subjects.value.trim(),
            study_hours: studyHours.value.trim(),
            exam_date: examDate.value,
            important_topics: importantTopics.value.trim()
        };

    } else {

        body = {
            text: text
        };
    }


    // -------------------------
    // Send Request
    // -------------------------

    try {

        const response = await fetch(
            endpointMap[selectedTask],
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(body)
            }
        );


        const contentType =
            response.headers.get("content-type") || "";


        let data;


        if (contentType.includes("application/json")) {

            data = await response.json();

        } else {

            const message =
                await response.text();

            throw new Error(
                message || "Server returned an invalid response."
            );
        }


        // -------------------------
        // Server Error
        // -------------------------

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed."
            );
        }


        // -------------------------
        // Quiz
        // -------------------------

        if (selectedTask === "quiz") {

            renderQuiz(data);

        } else {

            let output;


            if (selectedTask === "qa") {

                output = data.answer;

            } else if (selectedTask === "explain") {

                output = data.explanation;

            } else if (selectedTask === "summarize") {

                output = data.summary;

            } else if (selectedTask === "learn") {

                output = data.learning_path;

            } else if (selectedTask === "schedule") {

                output = data.schedule;
            }


            result.innerHTML = `
                <div class="result-content">
                    ${escapeHtml(
                        output || "No result returned."
                    )}
                </div>
            `;
        }


        status.textContent = "Done";


    } catch (error) {

        result.innerHTML = `
            <div class="result-content">
                Error:
                ${escapeHtml(error.message)}
            </div>
        `;

        status.textContent = "Error";


    } finally {

        submitBtn.disabled = false;
    }
}


// -----------------------------
// Generate Button
// -----------------------------

submitBtn.addEventListener(
    "click",
    submitRequest
);