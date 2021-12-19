DOMquestion = document.getElementById("question")
DOMlistAnswers = document.getElementById("answers")
list_buttons = []
list_labels = []

function createButton(textAnswer, idAnswer, answerIndex){
    divButton = document.createElement("div")
    divButton.className = "m-4"

    button = document.createElement("input")
    button.className = "btn-check"
    button.setAttribute("type", "radio")
    button.setAttribute("name", "vote") 
    button.setAttribute("id", "option" + String(answerIndex))
    button.setAttribute("value", idAnswer)
    list_buttons.push(button)
    button.addEventListener("click", toggleButton)


    label = document.createElement("label")
    label.className = "btn vote-input shadow-none"
    label.setAttribute("for", "option" + String(answerIndex))
    label.innerText = textAnswer
    list_labels.push(label)

    DOMlistAnswers.appendChild(divButton)
    divButton.appendChild(button)
    divButton.appendChild(label)
}

data = JSON.parse(data)
if (data.length == 0)
{   
    document.getElementById("my-card").hidden = true
    document.getElementById("no-survey").hidden = false
}
else
{
    document.getElementById("no-survey").hidden = true
    document.getElementById("my-card").hidden = false
    DOMquestion.innerText = data[0].question
    for (i=0; i < data[0].questions.length; i++)
    {
        createButton(data[0].questions[i].text, data[0].questions[i].id, i)
    }
    div = document.createElement("div")
    div.style.height = "50px"
    DOMlistAnswers.appendChild(div)
}


function trySubmit(){
    var myModal = new bootstrap.Modal(document.getElementById('modal'), {})
    myModal.show()
}

function toggleButton()
{
    for (i=0; i<list_buttons.length; i++)
    {
        if (list_buttons[i].checked == true)
        {
            list_labels[i].style.background = "#FF83044D"

        }
        else
        {
            list_labels[i].style.background = "white"
        }
    }
}