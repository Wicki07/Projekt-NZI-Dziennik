$(document).ready(function() {
    $('.deleteChildOpenMenu').click(function(event) {
        $('#childDeleteMenu').toggle();
        $('#toDeleteHiddenChildID').attr('value',$(this).val())
        $('#displayChildName').text($(this).attr('childName'))
    });
    $('#closeView').click(function(event) {
        $('#childDeleteMenu').toggle();
    });
});
