/**
 * Created by sladjan on 11.8.15..
 */
openerp.university_management=function(instance) {
    //var _t = instance.web._t,
    //_lt = instance.web._lt;
    //var QWeb = instance.web.qweb;
    //alert("asd");
    instance.web.ListView.Groups.include({
        get_selection: function () {
            res = this._super.apply(this, arguments);
            //console.log("asdadwawd");

            $elem = $('button#um_exam_apply_button');
            if(res['ids'].length == 0) $elem.hide();
            else $elem.show();

            //return res;
            return this._super.apply(this, arguments);
        },
    });

    instance.web.Sidebar = instance.web.Sidebar.extend({
        init: function (parent) {
            this._super(parent);
        },
        start: function(){
            this._super(this);
            var self = this;
            $('button#um_exam_apply_button').click(function(){
                var Exams = new instance.web.Model(self.getParent().dataset.model);
                console.log( self.getParent().get_selected_ids());
                Exams.call('sign_exam',[self.getParent().get_selected_ids(), self.getParent().get_selected_ids()]).done(function(results){
                    console.log("==MOJ==");
                    console.log(results);

                    var ActWindow = new instance.web.Model('ir.actions.act_window');
                    ActWindow.call('for_xml_id', ['university_management','action_um_exam']).done(function(result){

                        result['views'] = [[false, 'list'], [false, 'form']];
                        result['view_mode'] = 'list, form'

                        self.getParent().do_action(result).then(function(){

                        });

                    });
                });
            });
        },
    });
}