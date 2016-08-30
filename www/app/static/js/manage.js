var vm = new Vue({
    el: '#vm',
    data: {
        table: location.pathname.split('/').pop(),
        items: [],
        page: null,
        models: {
            'blogs': {'name': '标题', 'summary': '摘要'},
            'tags': {'name': '名称'},
        },
    },
    computed:{
        fields: function () {
            return this.models[this.table];
        }
    },
    ready: function () {
        this.getItemsByPage(getUrlParams('page'), getUrlParams('size'));
    },
    methods: {

        getItemsByPage: function  (page, size) {
            var self = this;
            getJSON('/api/manage/' + this.table, {
                page: page || '1',
                size: size || '10'
            }, function (err, data) {
                self.items = data.items;
                self.page = data.page;
            })
        },
        delete_item: function (item) {
            var self = this;
            if (confirm('确认要删除“' + (item.name || item.content) + '”？删除后不可恢复！')) {
                postJSON('/api/manage/' + this.table + '/' + item.id + '/delete', function (err, r) {
                    self.items.$remove(item);
                    if (self.items.length === 0 && self.page.index > 1) {
                        self.getItemsByPage(self.page.index - 1, self.page.limit);
                    }
                    else if (self.items.length < 10 && self.page.index < self.page.last) {
                        self.getItemsByPage(self.page.index, self.page.limit);
                    }
                });
            }
        },
        vaildPage: function(i) {
            return (i > 1) && (Math.abs(i - this.page.index) < 3);
        },
        gotoPage: function (page) {
            return this.getItemsByPage(page, this.page.limit);
        }
    }
});
