$(document).ready(function() {
    $('.activity').click(function(event) {
        $('#view').toggle();
        let activity = this.id
        let remind = $(this).attr("remind")
        if(remind=="true"){
            $('#changeRemindActivity').html('<i class="fas display-1 mb-3 fa-check-square"></i>')
            $('#changeRemindActivityDescription').html('Przypomienie włączone')
            $('#changeRemindActivity').val(1)
        }else{
            $('#changeRemindActivity').html('<i class="far display-1 mb-3 fa-check-square"></i>')
            $('#changeRemindActivityDescription').html('Przypomienie wyłączone')
            $('#changeRemindActivity').val(-1)
        }
        $('.inputActivityId').each(function(){
            $( this ).attr('value', activity)
        })
    });
    $('#closeView').click(function(event) {
        $('#view').toggle();
    });

    $('#goToActicitySendMessage').click(function(event) {
        $('#acticityMenu').toggle();
        $('#acticitySendMessage').toggle();
    });
    $('#backToActivityMenu').click(function(event) {
        $('#acticitySendMessage').toggle();
        $('#acticityMenu').toggle();
    });
    $('#goToViewActicitySendMessage').click(function(event) {
        if($('#messageToEmployee').val()){
            $('#acticitySendMessage').toggle();
            $('#viewActicitySendMessage').toggle();
            $('#viewMessageToEmployee').text($('#messageToEmployee').val())
            let temp = String($('#messageToEmployee').val())
            $('#hoverMessageToEmployee').attr('value', temp)
            $('#noMessageTyped').hide();
        }else{
            $('#noMessageTyped').show();
        }
    });
    $('#backToActicitySendMessage').click(function(event) {
        $('#viewActicitySendMessage').toggle();
        $('#acticitySendMessage').toggle();
    });
});
