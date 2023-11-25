function navigate(direction, currentQuestionIndex) {
  var currentQuestion = document.getElementById('question' + currentQuestionIndex); // Use currentQuestionIndex
  var radios = currentQuestion.getElementsByTagName('input');
          
  if (direction === 'next') {
      // Check if any radio button is selected
      var isSelected = Array.from(radios).some(radio => radio.checked);
      
      if (!isSelected) {
          alert('Please select an option to continue.');
          return; // Do not navigate to the next question
      }
  }

  var totalQuestions = document.getElementsByClassName('question').length;
  var newQuestionIndex = direction === 'next' ? currentQuestionIndex + 1 : currentQuestionIndex - 1;
  
  // Hide current question
  if (currentQuestionIndex > 0) {
      document.getElementById('question' + currentQuestionIndex).style.display = 'none';
  }
  
  // Show new question
  var newQuestion = document.getElementById('question' + newQuestionIndex);
  if (newQuestion) {
      newQuestion.style.display = 'block';
  } else {
      // Handle out of bounds navigation
      if (newQuestionIndex < 1) {
          newQuestionIndex = 1; // Loop back to first question if going back from first question
      } else if (newQuestionIndex > totalQuestions) {
          newQuestionIndex = totalQuestions; // Prevent going beyond the last question
      }
      document.getElementById('question' + newQuestionIndex).style.display = 'block';
  }
}


function startQuiz() {
    document.getElementById('home-screen').style.display = 'none';
    document.getElementById('question1').style.display = 'block';
}

function handleSubmit(event) {
  // Prevent the default form submission
  event.preventDefault();

  var form = document.getElementById('quiz-form');
  var answers = {};
  //var answerOptionCounts = []
  var countOption1 = 0;
  var countOption2 = 0;

  // Iterate over each question
  for (var i = 1; i <= form.elements.length; i++) {
    if(form.elements['question' + i]) {
      var radios = form.elements['question' + i];
      // Iterate over radio buttons within the question
      for (var j = 0; j < radios.length; j++) {
        if (radios[j].checked) {
          // If a radio button is checked, add the value to the answers object
          answers['question' + i] = radios[j].value;
          if (radios[j].value === "0") {
            countOption1++;
          } else if (radios[j].value === "1") {
            countOption2++;
          }
          break; // Stop looking through the rest once we've found the checked one
        }
      }
    }
  }

  // Determine the result based on counts
  var resultMessageText = "";
  if (countOption1 > countOption2) {
      resultMessageText = "You seem to be more of a visual learner!";
  } else if (countOption2 > countOption1) {
      resultMessageText = "You seem to be more of an auditory learner!";
  } else {
      resultMessageText = "You have a balanced learning style!";
  }

  // Show the results section
  var resultsSection = document.getElementById('results-section');
  resultsSection.style.display = 'block';

  // Set the result message text
  var resultMessageElement = document.getElementById('resultMessage');
  resultMessageElement.textContent = resultMessageText;

  // Scroll to the results section
  resultsSection.scrollIntoView();
}