$(document).ready(function() {
    /*
    $('#formset-wrapper').formset({
        addText: 'add family member',
        deleteText: 'remove',
        prefix: 'familymember_set'
    });
    */

    // click to add a label...
    $('#add-item').click(function(e) {
        e.preventDefault();

        // get the highest number in the set so far.
        var next_n = $('#label_table').find('tbody').find('tr').length;

        console.log(next_n);

        // make that new row. 
        var new_tr_string = "<tr><td><input id='id_labels-nnnn-id' type='hidden' name='labels-nnnn-id'><input id='id_labels-nnnn-project' type='hidden' name='labels-nnnn-project'><input id='id_labels-nnnn-name' type='text' name='labels-nnnn-name' maxlength='200'></td><td><input type='checkbox' name='labels-2-DELETE' id='id_labels-2-DELETE'></td></tr>";
        new_tr_string = new_tr_string.replace(/nnnn/g, String(next_n));
        $(new_tr_string).appendTo($('#label_table').find('tbody'));
    });
});
