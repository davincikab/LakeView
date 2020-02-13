function getParent(data, form_id,select_id) {
    $.ajax({
        url: '/citizen/search/',
        data: data,
        type: 'GET',
        success: function (response) {
            var res = JSON.parse(response);
            $(form_id).empty();
            //Populate the results 
            console.log(res);
            res.forEach(element => {
                $(form_id).append(
                    `<li class="list-group-item">${element.pk}</li>`
                );
            });

            parent_list = document.querySelectorAll(`${form_id} li`);
            parent_list.forEach(el => {
                $(el).on('click', function (e) {
                    console.log($(this).text());
                    $(select_id).val($(this).text());
                });
            });
        },
        error: function (e) {
            alert("Failed to submit the data try again");
        }
    });
}

function getStudent(data, student_id, select_id) {
    $.ajax({
        url: '/student/search/',
        data: data,
        type: 'GET',
        success: function (response) {
            var res = JSON.parse(response);
            $(student_id).empty();
            //Populate the results 
            console.log(res);
            res.forEach(element => {
                $(student_id).append(
                    `<li class="list-group-item">${element.pk} ${element.fields.admission_number} ${element.fields.school}</li>`
                );
            });

            student_list = document.querySelectorAll(`${student_id} li`);
            student_list.forEach(el => {
                $(el).on('click', function (e) {
                    console.log($(this).text());
                    var student_value = $(this).text().split(' ')[0]
                    $(select_id).val(student_value);
                });
            });

        },
        error: function (e) {
            alert("Failed to submit the data try again");
        }
    });
}