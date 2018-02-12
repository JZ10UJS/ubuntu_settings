odoo.define('button_notify.notify', function(require){
    var core = require('web.core');

    var ListView = require('web.ListView');

    ListView.List.include({
        init: function() {
            var self = this;

            this._super.apply(self, arguments);
            this.$current.undelegate('td button', 'click');
            this.$current.delegate('td button:not(.o_notify)', 'click', function (e) {
                e.stopPropagation();
                var $target = $(e.currentTarget),
                      field = $target.closest('td').data('field'),
                       $row = $target.closest('tr'),
                  record_id = self.row_id($row);

                if ($target.attr('disabled')) {
                    return;
                }
                $target.attr('disabled', 'disabled');

                // note: $.data converts data to number if it's composed only
                // of digits, nice when storing actual numbers, not nice when
                // storing strings composed only of digits. Force the action
                // name to be a string
                $(self).trigger('action', [field.toString(), record_id, function (id) {
                    $target.removeAttr('disabled');
                    return self.reload_record(self.records.get(id));
                }]);
            });
            this.$current.delegate('td button.o_notify', 'click', function (e) {
                e.stopPropagation();
                var $target = $(e.currentTarget),
                      field = $target.closest('td').data('field'),
                       $row = $target.closest('tr'),
                  record_id = self.row_id($row);

                if ($target.attr('disabled')) {
                    return;
                }
                $target.attr('disabled', 'disabled');
                $(self).trigger('action', [field.toString(), record_id, function (id) {
                    $target.removeAttr('disabled');
                    return self.reload_record(self.records.get(id)).then(function(){
                        self.view.do_notify('Success', 'Button Call Done');
                    });
                }]);
            });
        }
    })
});