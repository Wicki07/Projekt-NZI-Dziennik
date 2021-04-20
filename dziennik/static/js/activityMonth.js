$(document).ready(function() {
    $.getScript("/static/js/activity.js");
    $('.activityList').click(function(event) {
        $.getScript("/static/js/activity.js");
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
        $.getScript("/static/js/activity.js");
    });
});
