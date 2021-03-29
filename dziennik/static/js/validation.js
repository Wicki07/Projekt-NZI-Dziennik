function nameValidation() {
    const input = document.getElementsByName("name")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_name");
    if (validityState_object.valueMissing)
    {
     input[0].setCustomValidity('');
     input[0].reportValidity();
     error[0].innerHTML = '<p>Nie podano nazwy</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podano niewłaściwą nazwę</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
      });
}
function emailValidation() {
    const input = document.getElementsByName("email")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_email");
    if (validityState_object.valueMissing)
    {
     input[0].setCustomValidity('');
     input[0].reportValidity();
     error[0].innerHTML = '<p>Nie podano maila</p>'
    }
    else if(validityState_object.typeMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podany mail nie jest prawidłowy</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podany mail jest nieprawidłowy</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
      });
}
function password1Validation() {
    const input = document.getElementsByName("password1")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_password1");
    if (validityState_object.valueMissing)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie podano hasła</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podane hasło jest nieprawidłowe (minimum 8 znaków, 1 mała litera, 1 duża litera, 1 cyfra)</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
        });
}
function old_passwordValidation() {
    const input = document.getElementsByName("old_password")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_old_password");
    if (validityState_object.valueMissing)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie podano hasła</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podane hasło jest nieprawidłowe (minimum 8 znaków, 1 mała litera, 1 duża litera, 1 cyfra)</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
        });
}
function new_password1Validation() {
    const input = document.getElementsByName("new_password1")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_new_password1");
    if (validityState_object.valueMissing)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie podano hasła</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podane hasło jest nieprawidłowe (minimum 8 znaków, 1 mała litera, 1 duża litera, 1 cyfra)</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
        });
}
function password2Validation() {
    const input = document.getElementsByName("password2")
    const inputPreviousPass = document.getElementsByName("password1")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_password2");
    if (validityState_object.valueMissing)
    {
     input[0].setCustomValidity('');
     input[0].reportValidity();
     error[0].innerHTML = '<p>Nie podano hasła ponownie</p>'
    }
    else if(input[0].value != inputPreviousPass[0].value)
    {
        input[0].value = '';
        inputPreviousPass[0].value = '';
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podane hasła się nie zgdzają</p>'
    }
    else{

        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
      });
}
function new_password2Validation() {
    const input = document.getElementsByName("new_password2")
    const inputPreviousPass = document.getElementsByName("new_password1")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_new_password2");
    if (validityState_object.valueMissing)
    {
     input[0].setCustomValidity('');
     input[0].reportValidity();
     error[0].innerHTML = '<p>Nie podano hasła ponownie</p>'
    }
    else if(input[0].value != inputPreviousPass[0].value)
    {
        input[0].value = '';
        inputPreviousPass[0].value = '';
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podane hasła się nie zgdzają</p>'
    }
    else{

        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
      });
}
function phoneValidation() {
    const input = document.getElementsByName("phone")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_phone");
    if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podany nr telefonu nie jest prawidłowy</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
      });
}
function categoryValidation() {
    const input = document.getElementsByName("category")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_category");
    if (input[0].value == "Wybierz z listy...")
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie wybrano kategorii</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
        });
}
function proflieValidation() {
    const input = document.getElementsByName("profile")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_profile");
    if (validityState_object.valueMissing)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie podano profilu np. klub piłkarski, szkoła j. angielskiego</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podany profil jest nieprawidłowy</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
        });
}
function firstNameValidation() {
    const input = document.getElementsByName("first_name")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_first_name");
    if (validityState_object.valueMissing)
    {
     input[0].setCustomValidity('');
     input[0].reportValidity();
     error[0].innerHTML = '<p>Nie podano imienia</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podano niewłaściwe imie</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
      });
}
function ageValidation() {
    const input = document.getElementsByName("age")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_age");
    if (validityState_object.valueMissing)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie podano wieku</p>'
    }
    else if(!validityState_object.valid)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podano niewłaściwy wiek</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podano niewłaściwy wiek</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
        });
}
function lastNameValidation() {
    const input = document.getElementsByName("last_name")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_last_name");
    if (validityState_object.valueMissing)
    {
     input[0].setCustomValidity('');
     input[0].reportValidity();
     error[0].innerHTML = '<p>Nie podano nazwiska</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podano niewłaściwe nazwisko</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
      });
}
function specjalizationValidation() {
    const input = document.getElementsByName("specjalization")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_specjalization");
    if (validityState_object.valueMissing)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie podano specjalizacji</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podano niewłaściwą specjalizacje</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
        });
}
function dateValidation() {
    const input = document.getElementsByName("date")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_date");
    if (validityState_object.valueMissing)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie podano daty zajęć</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podana data jest nieprawidłowa</p>'
    }
    else if(Date.parse((input[0].value)) < Date.now())
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podana data jest nieprawidłowa</p>'
    }
}
function startTimeValidation() {
    const input = document.getElementsByName("start_time")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_start_time");
    if (validityState_object.valueMissing)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie podano godziny rozpoczęcia</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podano niewłaściwy format godziny</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
        });
}
function endTimeValidation() {
    const input = document.getElementsByName("end_time")
    const inputStartTime = document.getElementsByName("start_time")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_end_time");
    if (validityState_object.valueMissing)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie podano godziny zakończenia</p>'
    }
    else if(validityState_object.patternMismatch)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podano niewłaściwy format godziny</p>'
    }
    else if(input[0].value > inputStartTime[0].value)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Podano złą godzinę</p>'
    }
    else{

        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
        });
}
function periodicityValidation() {
    const input = document.getElementsByName("periodicity")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_periodicity");
    if (validityState_object.valid)
    {
        input[i].setCustomValidity('');
        input[i].reportValidity();
        error[i].innerHTML = '<p>Nie wybrano cykliczności</p>'
    }
    else
    {
        input[i].setCustomValidity('');
        input[i].reportValidity();
    }
    input[i].addEventListener('change', (event) => {
        error[4].innerHTML = ''
        });
}
function employeeValidation() {
    const input = document.getElementsByName("employee")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_employee");
    if (validityState_object.valid)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie wybrano prowadzącego</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
        });
}
function childrenValidation() {
    const input = document.getElementsByName("children")
    let validityState_object = input[0].validity;
    const error = document.getElementsByClassName("error_children");
    if (validityState_object.valid)
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
        error[0].innerHTML = '<p>Nie wybrano uczestników</p>'
    }
    else
    {
        input[0].setCustomValidity('');
        input[0].reportValidity();
    }
    input[0].addEventListener('change', (event) => {
        error[0].innerHTML = ''
        });
}
function validate(){
    const input = document.getElementsByClassName("form-control");
    for(i=0; i < input.length; i++){
        switch (input[i].name) {
            case "name":
                nameValidation()
                break;
            case "email":
                emailValidation()
                break;
            case "password1":
                password1Validation()
                break;
            case "password2":
                password2Validation()
                break;
            case "old_password":
                old_passwordValidation()
                break;
            case "new_password1":
                new_password1Validation()
                break;
            case "new_password2":
                new_password2Validation()
                break;
            case "phone":
                phoneValidation()
                break;
            case "category":
                categoryValidation()
                break;
            case "profile":
                proflieValidation()
                break;
            case "first_name":
                firstNameValidation()
                break;
            case "age":
                ageValidation()
                break;
            case "last_name":
                lastNameValidation()
                break;
            case "specjalization":
                specjalizationValidation()
                break;
            case "date":
                dateValidation()
                break;
            case "start_time":
                startTimeValidation()
                break;
            case "end_time":
                endTimeValidation()
                break;
            case "periodicity":
                periodicityValidation()
                break;
            case "employee":
                employeeValidation()
                break;
            case "children":
                childrenValidation()
                break;
            default:
                break;
        }
        console.log(input)
    }
}