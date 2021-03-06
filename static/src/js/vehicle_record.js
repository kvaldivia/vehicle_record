instance.web_kanban.KanbanRecord.include({
        kanban_getcolor: function (variable) {
            if (this.view.fields_view.model == 'project.task') {
                return (0 % this.view.number_of_color_schemes);
            } else {
                return this._super(variable);
            }
        },
        renderElement: function () {
            this._super();
            if (this.values.hex_value) {
                //Apply the color to the record, if there is one.
                this.$el.find('.oe_kanban_card').css("background-color", this.values.hex_value.value || 'white');
            }
        }
    });
