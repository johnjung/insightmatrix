$(document).ready(function() {
    $('.formset_row').formset({
        addText: 'add family member',
        deleteText: 'remove',
        prefix: 'familymember_set'
    });
});
