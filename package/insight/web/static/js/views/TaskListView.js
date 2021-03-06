var app = app || {};

(function($) {
    'use strict';
    app.TaskListView = Backbone.View.extend({
        el: '#tasks-table-body',

        initialize: function() {
            this.collection = new app.TaskCollection();
            this.collection.fetch({ reset: true });

            this.render();
            this.listenTo(this.collection, 'reset', this.render);
            this.listenTo(this.collection, 'add', this.render);
            this.listenTo(this.collection, 'remove', this.render);
        },

        refresh: function() {
            this.collection.fetch({ reset: true });
        },

        // render library by rendering each book in its collection
        render: function() {
            this.$el.html('');
            this.collection.each(function(model) {
                this.$el.append(new app.TaskView({
                    model: model
                }).el);
            }, this);
            return this;
        }
    });
})(jQuery);