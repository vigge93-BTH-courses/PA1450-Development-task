$(function () {
    $('.intervallSelector').on('click', updateSelectors)
    updateSelectors()
})

function updateSelectors() {
    $('#timeSelector').children('div').each(function () {
        $(this).css('display', 'none')
    });
    if (this.id === "year") {
        $("#years").css("display", "initial")
    } else if (this.id === "month") {
        $("#months").css("display", "initial")
    } else if (this.id === "date") {
        $("#dates").css("display", "initial")
    }
}

function generate_graph() {
    attribute = $('input.attribute:checked', '#attributes').val();
    timeIntervallSelector = null
    timeArgument = null
    valid = false
    if (document.getElementById("year").checked) {
        valid = document.getElementById("yearValue").checkValidity()
        timeIntervallSelector = "year"
        timeArgument = [document.getElementById("yearValue").value]
    } else if (document.getElementById("month").checked) {
        valid = document.getElementById("monthValue").checkValidity()
        timeIntervallSelector = "month"
        timeArgument = [document.getElementById("monthValue").value]
    } else if (document.getElementById("date").checked) {
        valid = document.getElementById("dateStart").checkValidity() && document.getElementById("dateEnd").checkValidity()
        timeIntervallSelector = "intervall"
        timeArgument = [document.getElementById("dateStart").value, document.getElementById("dateEnd").value]
    }
    if (valid){
        parameterString = "?attribute=" + attribute + "&timeIntervallType=" + timeIntervallSelector + "&timeArgument=" + timeArgument
        window.location.assign('/' + parameterString)
    } else {
        alert("Dunce, invalid arguments!")
    }
}