DOMquestion = document.getElementById("question")
DOMlistAnswers = document.getElementById("answers")

function createButton(textAnswer, idAnswer, answerIndex){
    divButton = document.createElement("div")
    divButton.className = "m-4"

    button = document.createElement("input")
    button.className = "btn-check"
    button.setAttribute("type", "radio")
    button.setAttribute("name", "vote")
    button.setAttribute("id", "option" + String(answerIndex))
    button.setAttribute("value", idAnswer)

    label = document.createElement("label")
    label.className = "btn vote-input"
    label.setAttribute("for", "option" + String(answerIndex))
    label.innerText = textAnswer

    DOMlistAnswers.appendChild(divButton)
    divButton.appendChild(button)
    divButton.appendChild(label)
}

var myModal = new bootstrap.Modal(document.getElementById('modal'), {})
myModal.show()

fetch("http://localhost:8000/api/sondages").then(response => {
    return response.json();
}).then(data => {
    DOMquestion.innerText = data[0].question
    for (i=0; i < data[0].questions.length; i++)
    {
        createButton(data[0].questions[i].text, data[0].questions[i].id, i)
    }
    div = document.createElement("div")
    div.style.height = "50px"
    DOMlistAnswers.appendChild(div)
})