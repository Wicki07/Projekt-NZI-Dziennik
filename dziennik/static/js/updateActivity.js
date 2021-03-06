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
    let activity = 0
    let nameTemp = ''
    $('.activity').click(function(event) {
        $('#view').toggle();
        activity = this.id
        let jsonData = $('#institutionActivitiesJSON').text()
        jsonData = JSON.parse(jsonData)
        let jsonDataChildren = $('#childrenActivitiesJSON').text()
        jsonDataChildren = JSON.parse(jsonDataChildren)
        $('#idActivityToUpdate').attr('value',activity)
        for (const [key, value] of Object.entries(jsonData)) {
            if(value.pk == activity){
                $('#id_name').attr('value',value.fields.name)
                nameTemp = value.fields.name
                $('#date').attr('value',value.fields.date)
                $('#start_time').attr('value',value.fields.start_time.replace(/:[^:]*$/,''))
                $('#end_time').attr('value',value.fields.end_time.replace(/:[^:]*$/,''))
                $('#periodicity').val(value.fields.periodicity)
                $('#employee').val(value.fields.employee_id)

            }
        }
          
    });
    
    $('#deleteActivityByInstitution').click(function(event) {
        $('#acticityMenu').toggle();
        $('#confirmActivityDeletion').toggle();
        $('#activityNameToDisplay').text(nameTemp)
        $('#inputActivityDeleteId').attr('value',activity)
    });
    $('#closeEdit').click(function(event) {
        $('#view').toggle();
    });
    $('#closeActivityDeletion').click(function(event) {
        $('#acticityMenu').toggle();
        $('#confirmActivityDeletion').toggle();
        $('#view').toggle();
    });
    $('#closeView').click(function(event) {
        $('#view').toggle();
    });
    $('#closeEditView').click(function(event) {
        $('#childEditMenu').toggle();
    });
    $('#closeDeleteView').click(function(event) {
        $('#childDeleteMenu').toggle();
    });
});
