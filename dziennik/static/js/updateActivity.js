$(document).ready(function() {
    $('.activity').click(function(event) {
        $('#view').toggle();
        let activity = this.id
        let jsonData = $('#institutionActivitiesJSON').text()
        jsonData = JSON.parse(jsonData)
        let jsonDataChildren = $('#childrenActivitiesJSON').text()
        jsonDataChildren = JSON.parse(jsonDataChildren)
        $('#idActivityToUpdate').attr('value',activity)
        for (const [key, value] of Object.entries(jsonData)) {
            if(value.pk == activity){
                $('#id_name').attr('value',value.fields.name)
                $('#date').attr('value',value.fields.date)
                $('#start_time').attr('value',value.fields.start_time.replace(/:[^:]*$/,''))
                $('#end_time').attr('value',value.fields.end_time.replace(/:[^:]*$/,''))
                $('#periodicity').val(value.fields.periodicity)
                $('#employee').val(value.fields.employee_id)

            }
        }
          
    });
    $('#closeView').click(function(event) {
        $('#view').toggle();
    });
});
