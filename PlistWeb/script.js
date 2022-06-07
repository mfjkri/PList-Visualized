formBody = document.getElementById("form-body");
progressbar = document.getElementById("progressbar");
formResult = document.getElementById("form-result");

questionTemplate = document.getElementById("step-template");
progressNodeTemplate = document.getElementById("progress-node-template");

const Questions = [];

function safelyParseJSON(json) {
  let parsed;
  try {
    parsed = JSON.parse(json);
  } catch (err) {}
  return parsed;
}

function createProgressNode(idx) {
  let newNode = progressNodeTemplate.cloneNode(true);
  newNode.setAttribute("id", "progress-node-" + idx);
  progressbar.appendChild(newNode);
}

function createQuestion(questionNumber, questionDesc, questionOptions) {
  let newQuestion = questionTemplate.cloneNode(true);
  newQuestion.setAttribute("id", "step" + questionNumber);

  let descDiv = newQuestion.querySelector(".question-desc");
  descDiv.innerHTML = questionDesc;

  let inputGroup = newQuestion.querySelector(".input-group");
  questionOptions.forEach((option, idx) => {
    let newLabel = document.createElement("label");
    newLabel.setAttribute("class", "form-control");
    newLabel.innerHTML =
      `<input type="radio" class="input-radio" name="q${questionNumber}" value="${idx}">` +
      option;
    inputGroup.appendChild(newLabel);
  });

  let btnsGroup = newQuestion.querySelector(".btns-group");
  if (questionNumber == 0) {
    btnsGroup.classList.remove("btns-group");

    let prevBtn = btnsGroup.querySelector(".btn-prev");
    prevBtn.remove();
  }

  if (questionNumber + 1 == Questions.length) {
    let nextBtn = btnsGroup.querySelector(".btn-next");
    nextBtn.remove();

    // <input type="submit" value="Submit" class="btn">
    let submitBtn = document.createElement("a");
    submitBtn.setAttribute("class", "btn btn-submit");
    submitBtn.innerHTML = "<b>Submit</b>";
    btnsGroup.appendChild(submitBtn);
  }

  createProgressNode(questionNumber);
  formBody.appendChild(newQuestion);
}

function disableFormSteps(formSteps) {
  formSteps.forEach((formStep) => {
    formStep.classList.contains("form-step-active") &&
      formStep.classList.remove("form-step-active");
  });
}

function updateFormSteps(formSteps, stateNumber) {
  disableFormSteps(formSteps);
  formSteps[stateNumber].classList.add("form-step-active");
}

function disableProgressBar() {
  progressbar.classList.remove("progressbar-active");
}

function enableProgressBar() {
  progressbar.classList.add("progressbar-active");
}

function updateProgressBar(progresSteps, stateNumber) {
  progresSteps.forEach((progressStep, idx) => {
    if (idx < stateNumber + 1) {
      progressStep.classList.add("progress-step-active");
    } else {
      progressStep.classList.remove("progress-step-active");
    }
  });

  const progressActive = document.querySelectorAll(".progress-step-active");
  progress.style.width =
    ((progressActive.length - 1) / (progresSteps.length - 1)) * 100 + "%";
}

function checkOptionFilled(actionBtn, stateNumber) {
  let isSelected = document.querySelector(
    `input[name="q${stateNumber}"]:checked`
  );
  if (isSelected) {
    return true;
  } else {
    actionBtn.parentElement.parentElement
      .querySelector(".error-msg")
      .classList.add("error-msg-active");
    return false;
  }
}

function download(filename, text) {
  var element = document.createElement("a");
  element.setAttribute(
    "href",
    "data:text/plain;charset=utf-8," + encodeURIComponent(text)
  );
  element.setAttribute("download", filename);

  element.style.display = "none";
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

function displayResult() {
  formResult.classList.add("form-result-active");
}

function generateForm() {
  /* ---------------------------------- Init ---------------------------------- */
  Questions.forEach(function (question, questionNumber) {
    createQuestion(questionNumber, question[0], question[1]);
  });
  questionTemplate.remove();
  progressNodeTemplate.remove();
  /* -------------------------------------------------------------------------- */

  const formSteps = document.querySelectorAll(".form-step");
  const progresSteps = document.querySelectorAll(".progress-step");

  const prevBtns = document.querySelectorAll(".btn-prev");
  const nextBtns = document.querySelectorAll(".btn-next");
  const radioBtns = document.querySelectorAll(".input-radio");

  const submitBtn = document.querySelector(".btn-submit");

  let stateNumber = 0;

  nextBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (checkOptionFilled(btn, stateNumber)) {
        stateNumber++;
        updateFormSteps(formSteps, stateNumber);
        updateProgressBar(progresSteps, stateNumber);
      }
    });
  });

  prevBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      stateNumber--;
      updateFormSteps(formSteps, stateNumber);
      updateProgressBar(progresSteps, stateNumber);
    });
  });

  radioBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const activeRadioBtns = btn.parentElement.parentElement.querySelectorAll(
        ".form-control-selected"
      );
      activeRadioBtns.forEach((activeBtn) => {
        activeBtn.classList.remove("form-control-selected");
      });

      btn.parentElement.classList.add("form-control-selected");

      const activeQuestionFrame = document.querySelector(".error-msg-active");
      if (activeQuestionFrame) {
        activeQuestionFrame.classList.remove("error-msg-active");
      }
    });
  });

  submitBtn.addEventListener("click", () => {
    results = "Participant Name|Webex Username\n";

    if (checkOptionFilled(submitBtn, stateNumber)) {
      selectedOptions = {};
      sortedOptions = [];

      Questions.forEach(function (question, questionNumber) {
        let isSelected = document.querySelector(
          `input[name="q${questionNumber}"]:checked`
        );
        let selectedOption = isSelected.getAttribute("value");

        participantName = Questions[questionNumber][0];
        selectedName = Questions[questionNumber][1][selectedOption];

        if (!(selectedName === "  ")) {
          results += `${participantName}|${selectedName}\n`;
        }
      });

      download("output.csv", results);

      // disableProgressBar();
      // disableFormSteps(formSteps);
    }
  });

  enableProgressBar();
  updateFormSteps(formSteps, stateNumber);
  updateProgressBar(progresSteps, stateNumber);
}

function main() {
  let attendeesFile = new XMLHttpRequest();
  let url = window.location.origin;

  attendeesFile.open("GET", `${url}/PlistWeb/attendees.json`, true);
  attendeesFile.send();

  attendeesFile.onreadystatechange = function () {
    if (attendeesFile.readyState == 4 && attendeesFile.status == 200) {
      const json = safelyParseJSON(attendeesFile.responseText);
      if (json) {
        for (const [key, value] of Object.entries(json)) {
          Questions.push([key, value]);
        }
      }
      generateForm(Questions);
    }
  };
}

main();
