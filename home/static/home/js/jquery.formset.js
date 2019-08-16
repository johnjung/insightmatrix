(function( $ ) {
    $.fn.formset = function(options) {
        let base = this;

        /** Init plugin */
        base.init = function() {
            base.options = $.extend({}, $.fn.formset.defaultOptions, options);
            base.idFormPrefix = 'id_' + base.options.prefix + '-';  // id_<prefix>_-
            base.template = document.getElementById(base.options.templateId).innerHTML;
            base.totalForms = base.getValueById(base.idFormPrefix + 'TOTAL_FORMS');
            base.maxForms = base.getValueById(base.idFormPrefix + 'MAX_NUM_FORMS');
            base.minForms = base.getValueById(base.idFormPrefix + 'MIN_NUM_FORMS');
            base.initialForms = base.getValueById(base.idFormPrefix + 'INITIAL_FORMS');
            base.itemsBase = base[0].querySelector('.' + base.options.itemsSelectorClass);
            base.addButton = document.getElementById(base.options.addButtonId);

            /* init listeners */
            base.on('click', '.' + base.options.deleteButtonClassname, base.deleteRow);
            document.getElementById(base.options.addButtonId).addEventListener("click", base.addRow);
        };

        /** get integer value given the element Id */
        base.getValueById = function(eltId) {
            return parseInt(document.getElementById(eltId).value);
        };

        /** Add a row based on the given template and sync form numbers */
        base.addRow = function(evt) {
            evt.preventDefault();
            if (!base.canAddRow()) { return; }

            let row = document.createElement(base.options.itemElementName);
            row.setAttribute('class', base.options.itemElementClass);
            row.setAttribute('id', 'id_' + base.options.prefix + '-' + base.totalForms);
            row.innerHTML = base.template.replace(/__prefix__/g, base.totalForms);
            base.itemsBase.appendChild(row);

            base.updateTotalForm();
        };

        /** Delete a row and sync form numbers */
        base.deleteRow = function(evt) {
            evt.preventDefault();
            let row = document.getElementById(this.getAttribute('data-row-id'));
            $(row).remove();

            // Resync id
            let els = base[0].querySelectorAll('.' + base.options.itemElementClass);

            for (let i = 0; i < els.length; i++) {
                let currentId = els[i].getAttribute('id');
                let newId = currentId.replace(/\d+$/, i);
                let re = new RegExp(base.options.prefix + '-\\d+', 'g');
                let replacement = base.options.prefix + '-' + i;
                els[i].setAttribute('id', newId);
                els[i].innerHTML = els[i].innerHTML.replace(re, replacement);
            }

            base.updateTotalForm();
        };

        /** Return true is the number of forms is less than the number of max forms, else false */
        base.canAddRow = function() {
            return base.totalForms < base.maxForms;
        };

        /** Update the number of total forms and enable/disable the add button if the limit is reached */
        base.updateTotalForm = function() {
            let total = base[0].querySelectorAll('.' + base.options.itemElementClass).length;
            document.getElementById(base.idFormPrefix + 'TOTAL_FORMS').value = total;
            base.totalForms = total;

            if (base.canAddRow()) {
                let re = new RegExp(base.options.addButtonDisableClass, 'g');
                base.addButton.className = base.addButton.className.replace(re, '').trim();
            } else {
                if (!base.addButton.className.match(new RegExp(base.options.addButtonDisableClass))) {
                    base.addButton.className += ' ' + base.options.addButtonDisableClass;
                }
            }
        };

        base.init();
    };

    /* Setup plugin defaults */
    $.fn.formset.defaultOptions = {
        templateId: 'item-tpl',
        prefix: 'form',
        addButtonId: 'add-item',
        addButtonDisableClass: 'disabled',
        deleteButtonClassname: 'delete-item',
        itemElementName: 'div',
        itemElementClass: 'item',
        itemsSelectorClass: 'items'
    };
}( jQuery ));
