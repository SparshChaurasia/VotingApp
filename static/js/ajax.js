$(document).ready(function () {
    let nextBtn1 = document.querySelector("#nextBtn");
    let nextBtn2 = document.querySelector("#nextBtn2");
    
    let idConatainer = document.querySelector("#idContainer");
    let nameConatainer = document.querySelector("#nameContainer");
    let classConatainer = document.querySelector("#classContainer");    
    console.log(idConatainer, nameConatainer, classConatainer);
    
    $(nextBtn1).click(function() {
        let s_id = document.querySelector("#id").value;
        let s_name = document.querySelector("#name").value;
        let s_class = document.querySelector("#class").value;

        $.post("http://127.0.0.1:8000/vote/EOIugodNIvWJOOamwUqw", 
        { "id": s_id, "name": s_name, "class": s_class }, 
        function(data) {
            if (data.Status == 200) {
                idConatainer.innerHTML = data.StudentID;
                nameConatainer.innerHTML = data.Name;
                classConatainer.innerHTML = data.Class;

                nextBtn2.disabled = false;
            } else {
                idConatainer.innerHTML = "Not Found";
                nameConatainer.innerHTML = "Not Found";
                classConatainer.innerHTML = "Not Found";

                nextBtn2.disabled = true;
            }
        });
    });
});