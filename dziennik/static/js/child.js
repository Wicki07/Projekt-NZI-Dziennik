$(document).ready(function() {
    //usuwanie dziecka
    $('.deleteChildOpenMenu').click(function(event) {
        $('#childDeleteMenu').toggle();
        $('#toDeleteHiddenChildID').attr('value',$(this).val())
        $('#displayChildName').text($(this).attr('childName'))
    });
    $('#closeDelView').click(function(event) {
        $('#childDeleteMenu').toggle();
    });
    //edycja dziecka
    $('.editChildOpenMenu').click(function(event) {
        $('#childEditMenu').toggle();
        $('#toEditHiddenChildID').attr('value',$(this).val())
        $('#displayChildNameToEdit').text($(this).attr('childName'))
        $('#id_first_name').val($(this).attr('childName').split(' ')[0])
        $('#id_last_name').val($(this).attr('childName').split(' ')[1])
        $('#id_age').val($(this).attr('age'))
    });
    $('#closeEditView').click(function(event) {
        $('#childEditMenu').toggle();
    });
});
