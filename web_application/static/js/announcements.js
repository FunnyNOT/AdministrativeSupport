function editAnnouncment(announcement_id, announcement_title, announcement_body, announcement_visible_to_students){
    
    $('#edit_announcement_id').val(announcement_id);
    $('#edit_announcement_title').val(announcement_title);
    $('#edit_announcement_body').val(announcement_body);
    if (announcement_visible_to_students == 'True'){ 
        $('#edit_announcement_visible_to_students').prop('checked', true);
    }
}

function deleteAnnouncement(announcement_id){
    $('#delete_announcement_id').val(announcement_id);
}