$(document).ready(function () {
    let nextBtn = document.querySelector("#nextBtn");
    let s_id = document.querySelector("#id").value;
    let s_name = document.querySelector("#name").value;
    let s_class = document.querySelector("#class").value;
    
    let idConatainer = document.querySelector("#idContainer");
    let nameConatainer = document.querySelector("#nameContainer");
    let classConatainer = document.querySelector("#classContainer");    
    console.log(idConatainer, nameConatainer, classConatainer);
    
    $(nextBtn).click(function() {
        console.log("function run");

        $.post("http://127.0.0.1:8000/vote/EOIugodNIvWJOOamwUqw", 
        { "id": s_id, "name": s_name, "class": s_class }, 
        function(data) {
            console.log(data);
            
            idConatainer.innerHTML = data.StudentID;
            nameConatainer.innerHTML = data.Name;
            classConatainer.innerHTML = data.Class;
        });
    });
});