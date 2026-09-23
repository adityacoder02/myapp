const form = document.querySelector("#study-form");
const textarea = document.querySelector("#prompt");
const dropdown = document.querySelector("#mode");
const status = document.querySelector("#status");
const output = document.querySelector("#output");

const submitButton = document.querySelector("#submit-btn");
const buttonText = document.querySelector("#button-text");

const copyButton = document.querySelector("#copy-btn");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  status.textContent = "";

  const inputPrompt = textarea.value.trim();
  const selectedMode = dropdown.value;

  if (inputPrompt === "") {
    status.textContent = "Please enter some study material first.";
    textarea.focus();
    return;
  }

  // Loading state
  submitButton.disabled = true;
  submitButton.classList.add("loading");
  buttonText.textContent = "Generating...";

  status.textContent = "AI is working on your response...";

  try {
    const response = await fetch("/generate", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        prompt: inputPrompt,
        mode: selectedMode,
      }),
    });

    const data = await response.json();

    if (!response.ok || data.error) {
      throw new Error(data.error || "Something went wrong.");
    }

    // Render Markdown
    output.innerHTML = marked.parse(data.response);

    status.textContent = "Response generated successfully!";
  } catch (error) {
    console.error(error);

    output.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">⚠️</div>
        <p>${error.message}</p>
      </div>
    `;

    status.textContent = "Unable to generate response.";
  } finally {
    submitButton.disabled = false;
    submitButton.classList.remove("loading");
    buttonText.textContent = "Ask AI";
  }
});

/* =========================
   COPY RESPONSE
========================= */

copyButton.addEventListener("click", async () => {
  const responseText = output.innerText.trim();

  if (!responseText) {
    status.textContent = "There is nothing to copy yet.";
    return;
  }

  try {
    await navigator.clipboard.writeText(responseText);

    copyButton.textContent = "Copied!";

    setTimeout(() => {
      copyButton.textContent = "Copy";
    }, 1500);
  } catch (error) {
    console.error(error);

    status.textContent = "Unable to copy the response.";
  }
});
