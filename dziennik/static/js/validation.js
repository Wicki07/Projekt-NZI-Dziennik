function userValidation() {
    const input = document.getElementsByClassName("form-control");
    const error = document.getElementsByClassName("error");
    var validityState_object = input[0].validity;
    console.log(input)
    console.log(validityState_object.valueMissing)
    for(i=0; i < input.length; i++){
        let validityState_object = input[i].validity;
        console.log(validityState_object)
        switch (i) {
            case 0:
                if (validityState_object.valueMissing)
                {
                 input[i].setCustomValidity('');
                 input[i].reportValidity();
                 error[i].innerHTML = '<p>Nie podano imienia</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwe imie</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[0].innerHTML = ''
                  });
              break;
              case 1:
                if (validityState_object.valueMissing)
                {
                 input[i].setCustomValidity('');
                 input[i].reportValidity();
                 error[i].innerHTML = '<p>Nie podano nazwiska</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwe nazwisko</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[1].innerHTML = ''
                  });
              break;
              case 2:
                console.log(validityState_object.typeMismatch)
                if (validityState_object.valueMissing)
                {
                 input[i].setCustomValidity('');
                 input[i].reportValidity();
                 error[i].innerHTML = '<p>Nie podano maila</p>'
                }
                else if(validityState_object.typeMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podany mail nie jest prawidłowy</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podany mail jest nieprawidłowy</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[2].innerHTML = ''
                  });
              break;
              case 3:
                if (validityState_object.valueMissing)
                {
                 input[i].setCustomValidity('');
                 input[i].reportValidity();
                 error[i].innerHTML = '<p>Nie podano hasła</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podane hasło jest nieprawidłowe (minimum 8 znaków, 1 mała litera, 1 duża litera, 1 cyfra)</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[3].innerHTML = ''
                  });
              break;
              case 4:
                if (validityState_object.valueMissing)
                {
                 input[i].setCustomValidity('');
                 input[i].reportValidity();
                 error[i].innerHTML = '<p>Nie podano hasła ponownie</p>'
                }
                else if(input[i].value != input[i-1].value)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podane hasła się nie zgdzają</p>'
                }
                else{

                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[4].innerHTML = ''
                  });
              break;
              case 5:
                console.log(i)
                if (validityState_object.valueMissing)
                {
                 input[i].setCustomValidity('');
                 input[i].reportValidity();
                 error[i].innerHTML = '<p>Nie podano telefonu</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podany nr telefonu nie jest prawidłowy</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[5].innerHTML = ''
                  });
              break;
            default:
          }
    }
}
function instytutionValidation() {
    const input = document.getElementsByClassName("form-control");
    const error = document.getElementsByClassName("error");
    var validityState_object = input[0].validity;
    console.log(input)
    console.log(validityState_object.valueMissing)
    for(i=0; i < input.length; i++){
        let validityState_object = input[i].validity;
        console.log(validityState_object)
        switch (i) {
            case 0:
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano nazwy</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwą nazwę</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[0].innerHTML = ''
                    });
                break;
            case 1:
                console.log(validityState_object.typeMismatch)
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano maila</p>'
                }
                else if(validityState_object.typeMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podany mail nie jest prawidłowy</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podany mail jest nieprawidłowy</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[1].innerHTML = ''
                    });
                break;
            case 2:
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano hasła</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podane hasło jest nieprawidłowe (minimum 8 znaków, 1 mała litera, 1 duża litera, 1 cyfra)</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[2].innerHTML = ''
                    });
                break;
            case 3:
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano hasła ponownie</p>'
                }
                else if(input[i].value != input[i-1].value)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podane hasła się nie zgdzają</p>'
                }
                else{

                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[3].innerHTML = ''
                    });
                break;
            case 4:
                console.log(i)
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano telefonu</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podany nr telefonu nie jest prawidłowy</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[4].innerHTML = ''
                    });
                break;
            case 6:
                console.log(i)
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano kategorii</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podany kategoria jest nieprawidłowa</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[6].innerHTML = ''
                    });
                break;
            case 5:
                console.log(i)
                if (validityState_object.valid)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie wybrano kategorii</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[5].innerHTML = ''
                    });
                break;
            default:
            }
    }
}
function employeeValidation() {
    const input = document.getElementsByClassName("form-control");
    const error = document.getElementsByClassName("error");
    var validityState_object = input[0].validity;
    console.log(error)
    console.log(validityState_object.valueMissing)
    for(i=0; i < input.length; i++){
        let validityState_object = input[i].validity;
        console.log(validityState_object)
        switch (i) {
            case 0:
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano imienia</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwe imie</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[0].innerHTML = ''
                    });
                break;
            case 1:
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano nazwiska</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwe nazwisko</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[1].innerHTML = ''
                    });
                break;
            case 2:
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano specjalizacji</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwą specjalizacje</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[2].innerHTML = ''
                    });
                break;
            case 3:
                console.log(validityState_object.typeMismatch)
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano maila</p>'
                }
                else if(validityState_object.typeMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podany mail nie jest prawidłowy</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podany mail jest nieprawidłowy</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[3].innerHTML = ''
                    });
                break;
            case 6:
                console.log(i)
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[4].innerHTML = '<p>Nie podano telefonu</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[4].innerHTML = '<p>Podany nr telefonu nie jest prawidłowy</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[4].innerHTML = ''
                    });
                break;
            default:
            }
    }
}

function activityValidation() {
    const input = document.getElementsByClassName("form-control");
    const error = document.getElementsByClassName("error");
    var validityState_object = input[0].validity;
    console.log(input)
    console.log(validityState_object.valueMissing)
    for(i=0; i < input.length; i++){
        let validityState_object = input[i].validity;
        console.log(validityState_object)
        switch (i) {
            case 0:
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano nazwy</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwą nazwę</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[0].innerHTML = ''
                    });
                break;
            case 1:
                console.log(validityState_object.typeMismatch)
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano daty zajęć</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podana data jest nieprawidłowa</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[1].innerHTML = ''
                    });
                break;
            case 2:
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano godziny rozpoczęcia</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwy format godziny</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[2].innerHTML = ''
                    });
                break;
            case 3:
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano godziny zakończenia</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwy format godziny</p>'
                }
                else if(input[i].value > input[i-1].value)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano złą godzinę</p>'
                }
                else{

                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[3].innerHTML = ''
                    });
                break;
            case 4:
                console.log(i)
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
                break;
            case 5:
                console.log(i)
                if (validityState_object.valid)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie wybrano prowadzącego</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[5].innerHTML = ''
                    });
                break;
            case 6:
                console.log(i)
                if (validityState_object.valid)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie wybrano uczestników</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[6].innerHTML = ''
                    });
                break;
            default:
            }
    }
}
function childValidation() {
    const input = document.getElementsByClassName("form-control");
    const error = document.getElementsByClassName("error");
    var validityState_object = input[0].validity;
    console.log(input)
    console.log(validityState_object.valueMissing)
    for(i=0; i < input.length; i++){
        let validityState_object = input[i].validity;
        console.log(validityState_object)
        switch (i) {
            case 0:
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano imienia</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwe imię</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[0].innerHTML = ''
                    });
                break;
            case 1:
                console.log(validityState_object.typeMismatch)
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano nazwiska</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Poadne niewłaściwe nazwisko</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[1].innerHTML = ''
                    });
                break;
            case 2:
                if (validityState_object.valueMissing)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Nie podano wieku</p>'
                }
                else if(!validityState_object.valid)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwy wiek</p>'
                }
                else if(validityState_object.patternMismatch)
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                    error[i].innerHTML = '<p>Podano niewłaściwy wiek</p>'
                }
                else
                {
                    input[i].setCustomValidity('');
                    input[i].reportValidity();
                }
                input[i].addEventListener('change', (event) => {
                    error[2].innerHTML = ''
                    });
                break;
            default:
            }
    }
}