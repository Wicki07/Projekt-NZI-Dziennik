$(document).ready(function() {
    $('*').click(function(event){
        var height;
        //if(document.documentElement.scrollHeight>=screen.height+(0.25*screen.height))height = screen.height+(0.25*screen.height)
        height = document.documentElement.scrollHeight
        width = document.documentElement.scrollWidth
        var popup = document.querySelectorAll(".popup-background")[1]
        popup.style.height = height+"px"
        //popup.style.width = width+"px"
        console.log('test')
    })
    $('.activity').click(function(event) {
        $('#view').toggle();
        let activity = this.id
        let remind = $(this).attr("remind")
        $('#goToActicityCheckAttendance').attr('activityid', activity)
        if(remind=="true"){
            $('#changeRemindActivity').html('<i style="font-size:6rem;" class="fas display-1 mb-3 fa-check-square rem6point9"></i>')
            $('#changeRemindActivityDescription').html('Przypomienie włączone')
            $('#changeRemindActivity').val(1)
        }else{
            $('#changeRemindActivity').html('<i style="font-size:6rem;"  class="far display-1 mb-3 fa-check-square"></i>')
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
    $('#backToActivityMenuFromAttendanceList').click(function(event) {
        $('#acticityCheckAttendance').toggle();
        $('#acticityMenu').toggle();
    });
    $('#goToActicityCheckAttendance').click(function(event) {
        if($(document.querySelectorAll(`span[id="`+$(this).attr('activityid')+`"]`)[1]).attr('attendencelist') != undefined){
            $('#attendenceListDisplay').html($(document.querySelectorAll(`span[id="`+$(this).attr('activityid')+`"]`)[1]).attr('attendencelist')) 
        }else{
            $('#attendenceListDisplay').html($(document.querySelectorAll(`span[id="`+$(this).attr('activityid')+`"]`)[0]).attr('attendencelist')) 
        }
        $('#acticityMenu').toggle();
        $('#acticityCheckAttendance').toggle();
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

    $(document).on("change",'input[type=checkbox]',function(){
        var target = $(document.querySelectorAll("."+$(this).attr('id'))[0])
        if($(this).is(':checked'))
        {
            target[0].checked=false
        }
        else
        {
            target[0].checked=true
        }
    });
});
