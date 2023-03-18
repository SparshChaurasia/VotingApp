formSteps = document.querySelectorAll(".form-step");    
let formStepCounter = 0;

function nextFormStep(){
    formSteps[formStepCounter].classList.remove("form-step-active");

    formStepCounter += 1
    formSteps[formStepCounter].classList.add("form-step-active")
}

function prevFormStep(){
    formSteps[formStepCounter].classList.remove("form-step-active");

    formStepCounter -= 1
    formSteps[formStepCounter].classList.add("form-step-active")
}