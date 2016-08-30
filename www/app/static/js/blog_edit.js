var vm = new Vue({
    el: '#blog',
    data: {
        action: '/api/manage/blogs',
        message: '',
        tags:[],
        blog: {
            name: '',
            tag: '',
            summary: '',
            content: ''
        }
    },
    ready: function () {
        if (location.pathname.split('/').pop() === 'edit') {
            var id = getUrlParams('id');
            this.action = this.action + '/' + id;
            getJSON('/api/manage/tags', function (err, data) {
                vm.tags = data.items;
            });
            getJSON('/api/manage/blogs/' + id, function (err, blog) {
                vm.blog = blog;
            });
            
        }
    },
    methods: {
        submit: function () {
            postJSON(this.action, this.blog, function (err, blog) {
                if (err) {
                    return showAlert(vm, err.message || err.data || err)
                }
                return location.assign(location.pathname.split('manage')[0] + 'blog/' + blog.id);
            });
        },

        clickitem: function (txt)
        {
            document.getElementById("tag").value = '"'+txt+'"';
        }

    }
});

