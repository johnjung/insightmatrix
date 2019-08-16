$(document).ready(function() {
    $('#formset-wrapper').formset({
        addText: 'add family member',
        deleteText: 'remove',
        prefix: 'familymember_set'
    });
});
