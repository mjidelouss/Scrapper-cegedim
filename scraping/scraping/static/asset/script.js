
function handleButtonClick(siren) {

    document.getElementById("simple-search").value = siren
     const checkboxes = document.querySelectorAll(".checkbox");
     const form = document.getElementById("myForm");
     checkboxes.forEach(checkbox => {
            checkbox.checked = true;
     });
      form.submit();
}

