$(document).ready(function() {
    $('*').click(function(event){
        var height;
        //if(document.documentElement.scrollHeight>=screen.height+(0.25*screen.height))height = screen.height+(0.25*screen.height)
        height = document.documentElement.scrollHeight;
        width = document.documentElement.scrollWidth;
        var popup = document.querySelectorAll(".popup-background")[0];
        popup.style.height = height+"px";
        //popup.style.width = width+"px"
        console.log('test')
    })
    $.getScript("/static/js/updateActivity.js");
    $('.activityList').click(function(event) {
        $.getScript("/static/js/updateActivity.js");
        $('#viewList').toggle();
        let htmlToInsert = ''

        var getActivitiesOfWeek = document.querySelectorAll(`span[weektofind="`+$(this).attr('week')+`"]`)
		var getActivitiesOfDay = getActivitiesOfWeek[$(this).attr('day')]

        getActivitiesOfWeek.forEach(day => {
            if($(day).attr('daytofind') == $(this).attr('day')){
                htmlToInsert += $(day).attr('hiddeninfo')
            }
        });
        $('.weekScheduleList').html(htmlToInsert)
    });
    $('#closeViewList').click(function(event) {
        $('#viewList').toggle();
        $.getScript("/static/js/updateActivity.js");
    });
});
