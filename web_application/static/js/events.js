function editEvent(event_id, event_title, event_descripiton, event_visible_to_students){
    
    $('#edit_event_id').val(event_id);
    $('#edit_event_title').val(event_title);
    $('#edit_event_description').val(event_descripiton);
    if (event_visible_to_students == 'True'){ 
        $('#edit_event_visible_to_students').prop('checked', true);
    }
    
}

function deleteEvent(event_id){
    $('#delete_event_id').val(event_id);
}