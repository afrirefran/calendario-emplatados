odoo.define('calendarioEmplatados.custom_area', function(require) {
    'use strict';

    var FormController = require('web.FormController');
    var rpc = require('web.rpc');

    var CustomFormController = FormController.include({
        start: function() {
            this._super.apply(this, arguments);

            if (this.modelName === 'calendario.emplatados') {
                this.initializeCustomArea();
            }
        },

        initializeCustomArea: function() {
            var $custom_area = $('<div id="custom_area"></div>');
            $('body').append($custom_area);

            $('#custom_area').append('<div id="datepicker"></div>');

            $("#datepicker").datepicker({
                beforeShowDay: this.highlightDates.bind(this),
                onSelect: this.onDateSelect.bind(this)
            });

            this.$custom_area = $custom_area;
            this.getHolidaysAndDaySet();
        },

        destroy: function() {
            if (this.$custom_area) {
                this.$custom_area.remove();
            }
            this._super.apply(this, arguments);
        },

        highlightDates: function(date) {
            var highlight = '';
            var dateString = $.datepicker.formatDate('yy-mm-dd', date);

            if (this.holidays && this.holidays.includes(dateString)) {
                highlight = 'holiday';
            } else if (this.selected_dates && this.selected_dates.includes(dateString)) {
                highlight = 'workday';
            }

            return [true, highlight];
        },

        onDateSelect: function(dateText, inst) {
            var self = this;
            var date = $(inst.input).datepicker('getDate');

            if (!date) {
                return;
            }

            var formattedDate = $.datepicker.formatDate('yy-mm-dd', date);
            var recordId = this.model.localData[this.handle].data.id;
            
            rpc.query({
                model: 'calendario.emplatados',
                method: 'save_selected_date',
                args: [recordId, formattedDate],
            }).then(function(result) {
                if (result.success) {
                    self.selected_dates.push(formattedDate);
                    $("#datepicker").datepicker("refresh");
                } else {
                    console.log("Error saving date: ", result.error);
                }
            }, function(error) {
                console.error("RPC error: ", error);
            });
        },

        getHolidaysAndDaySet: function() {
            var self = this;
            var recordId = this.model.localData[this.handle].data.id; // Obtener el ID del registro

            console.log("Fetching holidays and day set for record ID: ", recordId); // Añadir log para el ID del registro

            rpc.query({
                model: 'calendario.emplatados',
                method: 'get_holidays_and_day_set',
                args: [recordId],
            }).then(function(result) {
                console.log("Received result: ", result);
                self.holidays = result.holidays.map(function(d) {
                    return $.datepicker.formatDate('yy-mm-dd', new Date(d));
                });
                self.selected_dates = result.selected_dates ? result.selected_dates.map(function(d) {
                    return $.datepicker.formatDate('yy-mm-dd', new Date(d));
                }) : [];
                $("#datepicker").datepicker("refresh");
            });
        }
    });

    return CustomFormController;
});


















