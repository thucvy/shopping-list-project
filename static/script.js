$(document).on('click', '.table__row-delete-button', function () {
    $("#confirmDeleteModal").attr("caller-id", $(this).attr("id"));
});

$(document).on('click', '#confirmDeleteButtonModal', function () {
    var caller = $("#confirmDeleteButtonModal").closest(".modal").attr("caller-id");
    window.location = $("#".concat(caller)).attr("href");
});


$(document).on('click', '.submitbar__link', function () {
    $("#deleteModal").attr("caller-id", $(this).attr("id"));
});

$(document).on('click', '#deleteButtonModal', function () {
    var caller = $("#deleteButtonModal").closest(".modal").attr("caller-id");
    window.location = $("#".concat(caller)).attr("href");
});